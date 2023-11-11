file(GLOB_RECURSE GameScripts "${CMAKE_CURRENT_SOURCE_DIR}/Python/*.py")
file(GLOB_RECURSE GameSDL "${CMAKE_CURRENT_SOURCE_DIR}/SDL/*.sdl")
file(GLOB_RECURSE GameData "${CMAKE_CURRENT_SOURCE_DIR}/dat/*.age" "${CMAKE_CURRENT_SOURCE_DIR}/dat/*.fni")

source_group(TREE "${CMAKE_CURRENT_SOURCE_DIR}/Python/" PREFIX "Python" FILES ${GameScripts})
source_group("SDL" FILES ${GameSDL})
source_group("Ages" FILES ${GameData})

add_custom_target(Scripts
                  SOURCES ${GameScripts} ${GameSDL} ${GameData}
)

install(
    DIRECTORY "Config/"
    DESTINATION client
    FILES_MATCHING PATTERN "*.ini"
)
install(
    FILES
        ${Plasma_SOURCE_DIR}/COPYING.txt
        ${Plasma_SOURCE_DIR}/CREDITS.txt
        ${Plasma_SOURCE_DIR}/LICENSE.txt
    DESTINATION client/license
)
install(
    FILES "NAGUS/COPYING.txt"
    DESTINATION client/license
    RENAME COPYING-NAGUS.txt
)
install(
    DIRECTORY "Python/"
    DESTINATION client/python
    FILES_MATCHING PATTERN "*.py"
)
install(
    DIRECTORY "NAGUS/src/"
    DESTINATION client/python
    FILES_MATCHING PATTERN "*.py"
)
install(
    DIRECTORY "SDL/"
    DESTINATION client/SDL
    FILES_MATCHING PATTERN "*.sdl"
)
install(
    DIRECTORY "dat/"
    DESTINATION client/dat
    FILES_MATCHING PATTERN "*.age" PATTERN "*.fni"
)

file(TO_CMAKE_PATH "${Python3_STDARCH}" Scripts_SYSTEM_PATH)
install(
    DIRECTORY "${Scripts_SYSTEM_PATH}/"
    DESTINATION client/python/system

    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "lib-dynload/*"
    PATTERN "*.pyc" EXCLUDE

    # These Python stdlib modules should be EXCLUDED from the copy due to either practical or
    # security concerns. NOTE: When adding a new PATTERN, be sure to "quote" the directory or file
    # name, otherwise you will break the install command in a silent, yet disastrous way.
    PATTERN "__pycache__" EXCLUDE
    PATTERN "ctypes" EXCLUDE
    PATTERN "curses" EXCLUDE
    PATTERN "distutils" EXCLUDE
    PATTERN "dist-packages" EXCLUDE
    PATTERN "email" EXCLUDE
    PATTERN "ensurepip" EXCLUDE
    PATTERN "http" EXCLUDE
    # contains a module-level SystemExit
    PATTERN "idlelib" EXCLUDE
    PATTERN "lib2to3" EXCLUDE
    PATTERN "msilib" EXCLUDE
    # Windows turd
    PATTERN "site-packages" EXCLUDE
    PATTERN "test" EXCLUDE
    PATTERN "tkinter" EXCLUDE
    PATTERN "turtledemo" EXCLUDE
    PATTERN "unittest" EXCLUDE
    PATTERN "urllib" EXCLUDE
    PATTERN "venv" EXCLUDE
    PATTERN "wsgiref" EXCLUDE

    # Annoying browser popup turd.
    PATTERN "antigravity.py" EXCLUDE
    PATTERN "asynchat.py" EXCLUDE
    PATTERN "asyncore.py" EXCLUDE
)
install(
    DIRECTORY "${Scripts_SYSTEM_PATH}/../DLLs/"
    DESTINATION client/python/system/lib-dynload

    FILES_MATCHING
    PATTERN "_asyncio.pyd"
    PATTERN "_overlapped.pyd"
    PATTERN "_socket.pyd"
    PATTERN "_sqlite3.pyd"
    PATTERN "_uuid.pyd"
    PATTERN "select.pyd"
)
install(
    DIRECTORY "${Scripts_SYSTEM_PATH}/../../../debug/bin/"
    DESTINATION client/python/system/lib-dynload

    FILES_MATCHING
    PATTERN "_asyncio_d.pyd"
    PATTERN "_overlapped_d.pyd"
    PATTERN "_socket_d.pyd"
    PATTERN "_sqlite3_d.pyd"
    PATTERN "_uuid_d.pyd"
    PATTERN "select_d.pyd"
)
