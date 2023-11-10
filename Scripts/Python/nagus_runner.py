import asyncio
import logging.config
import os
import threading
import typing

import nagus.__main__
import nagus.configuration

from Plasma import PtDebugPrint


loop: typing.Optional[asyncio.AbstractEventLoop] = None
server_task: typing.Optional[asyncio.Task[typing.Any]] = None
server_is_running_sema = threading.Semaphore()


class PtDebugPrintLoggingHandler(logging.Handler):
    def emit(self, record):
        try:
            PtDebugPrint(self.formatter.format(record))
        except Exception:
            self.handleError(record)


def load_config(config_file):
    config = nagus.configuration.Configuration()

    try:
        config.set_options_from_ini_file(config_file)
    except FileNotFoundError:
        PtDebugPrint(f"[WARNING] nagus_runner: Couldn't find server config file {config_file}")
    except nagus.configuration.ConfigError as exc:
        PtDebugPrint(f"[ERROR] nagus_runner: In config file {config_file}: {exc}")

    config.set_defaults()
    return config


async def async_nagus_wrapper(config):
    global loop
    global server_task
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(nagus.__main__.async_main(config))
    await server_task


def start_nagus():
    config = load_config(nagus.__main__.DEFAULT_CONFIG_FILE_NAME)

    logging.basicConfig(
        format="[%(levelname)s] %(name)s: %(message)s",
        handlers=[PtDebugPrintLoggingHandler()],
    )
    logging.config.dictConfig(config.logging_config)

    logger = logging.getLogger(__name__)

    def _run_nagus():
        global server_task

        try:
            try:
                os.mkdir("sav")
            except FileExistsError:
                pass

            with server_is_running_sema:
                try:
                    asyncio.run(async_nagus_wrapper(config))
                except asyncio.CancelledError:
                    logger.info("Server task cancelled - shutting down NAGUS...")
                finally:
                    server_task = None
        except BaseException:
            logger.error("Unhandled exception in NAGUS server event loop thread", exc_info=True)

    threading.Thread(target=_run_nagus, name="NAGUS server event loop").start()


def stop_nagus():
    if loop is not None and not loop.is_closed():
        @loop.call_soon_threadsafe
        def _stop_nagus():
            if server_task is not None:
                server_task.cancel()

    # Wait for the server thread to finish
    with server_is_running_sema:
        pass
