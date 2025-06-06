# /*==LICENSE==*
#
# CyanWorlds.com Engine - MMOG client, server and tools
# Copyright (C) 2011  Cyan Worlds, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Additional permissions under GNU GPL version 3 section 7
#
# If you modify this Program, or any covered work, by linking or
# combining it with any of RAD Game Tools Bink SDK, Autodesk 3ds Max SDK,
# NVIDIA PhysX SDK, Microsoft DirectX SDK, OpenSSL library, Independent
# JPEG Group JPEG library, Microsoft Windows Media SDK, or Apple QuickTime SDK
# (or a modified version of those libraries),
# containing parts covered by the terms of the Bink SDK EULA, 3ds Max EULA,
# PhysX SDK EULA, DirectX SDK EULA, OpenSSL and SSLeay licenses, IJG
# JPEG Library README, Windows Media SDK EULA, or QuickTime SDK EULA, the
# licensors of this Program grant you additional
# permission to convey the resulting work. Corresponding Source for a
# non-source form of such a combination shall include the source code for
# the parts of OpenSSL and IJG JPEG Library used as well as that of the covered
# work.
#
# You can contact Cyan Worlds, Inc. by email legal@cyan.com
#  or by snail mail at:
#       Cyan Worlds, Inc.
#       14617 N Newport Hwy
#       Mead, WA   99021
#
# *==LICENSE==*/

from Plasma import *
from PlasmaConstants import *
import PlasmaControlKeys
from PlasmaTypes import *
from PlasmaKITypes import *
import time

import grtzMarkerGames
import xMarkerGameUtils

# define the attributes that will be entered in max
MarkerGameDlg = ptAttribGUIDialog(1, "The MarkerGame GUI")
MGAnim = ptAttribAnimation(2, "Turn on/off entire animation")
MGMachineOnResp = ptAttribResponder(3, "Turn On responder")
MGMachineOffResp = ptAttribResponder(4, "Turn Off responder")
aScope1Act = ptAttribNamedActivator(5, "CGZ Scope1 Python", netForce=True)
aScope2Act = ptAttribNamedActivator(6, "CGZ Scope2 Python", netForce=True)
aScope3Act = ptAttribNamedActivator(7, "CGZ Scope3 Python", netForce=True)
aScope4Act = ptAttribNamedActivator(8, "CGZ Scope4 Python", netForce=True)

# TagIDs for the GUI
kRGMarkerGameSelect = 500
kMarkerGameFieldStart = 200
kMarkerGameFieldEnd = 340
kMarkerGameNumFieldOffset = 0
kMarkerGameNameFieldOffset = 1

# Game Score Sctuff
kGameScore = "GreatZeroCalibration_{:02d}"
kScoreType = PtGameScoreTypes.kFixed

# Timer CBs
kTimerUpdateActiveCB = 0
kTimerUpdateSecs = 1.0

# This should be a ptAttribSceneobject
kTelescopes = {"GZMachineScope01", "GZMachineScope02", "GZMachineScope03", "GZMachineScope04"}

class grtzMarkerScopeGUI(ptModifier):
    def __init__(self):
        ptModifier.__init__(self)
        self.id = 213
        self.version = 3

        self._lookingAtGUI = False

    def __del__(self):
        PtUnloadDialog("MarkerGameGUI")

    def OnBackdoorMsg(self, target, param):
        target = target.lower()
        if target.startswith("cgzm"):
            try:
                mission = int(target[-2:])
            except:
                return
            self._UpdateScore(mission, int(param))

        elif target == "cgztime":
            try:
                time = int(param)
            except:
                PtDebugPrint("grtzMarkerScopeGUI.OnBackdoorMsg():\tcgztime wants an integer")
            else:
                time =  xMarkerGameUtils.GetCurrentTime() - time
                PtDebugPrint("grtzMarkerScopeGUI.OnBackdoorMsg():\tUpdating CGZ Start Time to {}".format(time))
                xMarkerGameUtils.SetCGZMTimes(
                    xMarkerGameUtils.GetCurrentGZM(),
                    xMarkerGameUtils.CGZMTimes(start_time=time)
                )

        elif target == "gps":
            value = True if param in {"enable", "1", "true", "on"} else False
            self._GrantGPS(value)

    def _CheckForGPSCalibration(self):
        for i, score in enumerate(self._scores):
            if not isinstance(score, ptGameScore):
                if score == -1:
                    PtDebugPrint("grtzMarkerScopeGUI._CheckForGPSCalibration():\tMGS #{} is still loading. No GPS.".format(i), level=kDebugDumpLevel)
                    return
                else:
                    PtDebugPrint("grtzMarkerScopeGUI._CheckForGPSCalibration():\tMGS #{} has no score. No GPS.".format(i), level=kWarningLevel)
                    return
            if score.getPoints() == 0:
                PtDebugPrint("grtzMarkerScopeGUI._CheckForGPSCalibration():\tMGS #{} has a score of zero. No GPS.".format(i), level=kWarningLevel)
                return
        self._GrantGPS()

    def OnControlKeyEvent(self, controlKey, activeFlag):
        if controlKey in (PlasmaControlKeys.kKeyExitMode, PlasmaControlKeys.kKeyMoveBackward,
                          PlasmaControlKeys.kKeyRotateLeft, PlasmaControlKeys.kKeyRotateRight):
            self._PopTelescope()

    def OnFirstUpdate(self):
        PtLoadDialog("MarkerGameGUI", self.key)

    def OnGameScoreMsg(self, msg):
        if isinstance(msg, ptGameScoreListMsg):
            try:
                mission = int(msg.getName()[-2:])
            except:
                PtDebugPrint("grtzMarkerScopeGUI.OnGameScoreMsg():\tTITS! '{}' didn't match.".format(score.getName()))
                return

            legacyScore = xMarkerGameUtils.GetLegacyCGZMScore(mission)
            try:
                scores = msg.getScores()
            except:
                self._scores[mission] = 0
                # If we have a score in the legacy chronicle, then force the ScoreSrv value
                # to what the chronicle says. That way, we can be consistent and do leaderboards.
                if legacyScore > 0:
                    self._UpdateScore(mission, legacyScore)
            else:
                # Pick the lowest score in the list to use.
                scores = sorted(scores, key=lambda x: x.getPoints())
                score = scores[0]
                self._scores[mission] = score

                # All the other scores are garbage.
                for i in scores[1:]:
                    i.remove()

                # The legacy chronicle seems to have a better score value than ScoreSrv, so adopt
                # it per the comment above. If this happens, don't update the GUI with the stale
                # value from ScoreSrv - wait for the authorative update.
                if legacyScore > 0 and legacyScore < score.getPoints():
                    self._UpdateScore(mission, legacyScore)
                elif self._lookingAtGUI:
                    self._UpdateGUI(mission)

        elif isinstance(msg, ptGameScoreUpdateMsg):
            score = msg.getScore()
            try:
                mission = int(score.getName()[-2:])
            except:
                PtDebugPrint("grtzMarkerScopeGUI.OnGameScoreMsg():\tTITS! '{}' didn't match.".format(score.getName()))
                return

            points = score.getPoints()
            self._scores[mission] = score
            PtDebugPrint("grtzMarkerScopeGUI.OnGameScoreMsg():\tUpdated CGZ #{} = {}".format(mission, points))

            if self._lookingAtGUI:
                self._UpdateGUI(mission=mission, score=points, star=True)

        # We did something with a score... Maybe we have GPS nao?
        if -1 not in self._scores:
            self._CheckForGPSCalibration()

    def _GrantGPS(self, enable=True):
        PtDebugPrint("grtzMarkerScopeGUI._GrantGPS():\tYou have GPS...", level=kWarningLevel)

        vault = ptVault()
        psnlSDL = vault.getPsnlAgeSDL()
        if psnlSDL:
            GPSVar = psnlSDL.findVar("GPSEnabled")
            if GPSVar.getBool() != enable:
                GPSVar.setBool(enable)
                vault.updatePsnlAgeSDL(psnlSDL)
                act = "Enabled" if enable else "Disabled"
                PtDebugPrint("grtzMarkerScopeGUI._GrantGPS():\t{} GPS!".format(act), level=kWarningLevel)

    def OnGUINotify(self, id, control, event):
        if id != MarkerGameDlg.id:
            return

        if event == kDialogLoaded:
            MGAnim.animation.skipToTime(1.5)
        elif event == kShowHide:
            self._lookingAtGUI = control.isEnabled()
            if control.isEnabled():
                self._ShowGUI()
        elif event == kValueChanged and self._lookingAtGUI:
            rgid = control.getTagID()
            if rgid == kRGMarkerGameSelect:
                gameSelector = MarkerGameDlg.dialog.getControlModFromTag(kRGMarkerGameSelect)
                mission = gameSelector.getValue()
                if mission == -1:
                    self._StopCGZM(win=False)
                elif mission != xMarkerGameUtils.GetCurrentCGZM():
                    self._PlayCGZM(mission)

    def OnNotify(self, state, id, events):
        PtDebugPrint("grtzMarkerScopeGUI:OnNotify():\tstate=%f id=%d events=" % (state, id), events, level=kDebugDumpLevel)

        if id in self._scopes:
            if PtDetermineKIMarkerLevel() < kKIMarkerNormalLevel:
                MarkerGameDlg.dialog.hide()
            else:
                MGMachineOffResp.run(self.key, netPropagate=False)
        elif id == MGMachineOnResp.id:
            PtEnableControlKeyEvents(self.key)
        elif id == MGMachineOffResp.id:
            MarkerGameDlg.dialog.hide()
            PtDisableControlKeyEvents(self.key)

    def OnServerInitComplete(self):
        numGames = len(grtzMarkerGames.mgs)
        self._scores = [-1] * numGames
        for i in range(numGames):
            ptGameScore.findPlayerScores(kGameScore.format(i), self.key)
        self._scopes = (aScope1Act.id, aScope2Act.id, aScope3Act.id, aScope4Act.id)

    def OnTimer(self, id):
        if id == kTimerUpdateActiveCB:
            if self._lookingAtGUI:
                mission = xMarkerGameUtils.GetCurrentCGZM()
                if mission != -1:
                    self._UpdateGUI(mission)
                    PtAtTimeCallback(self.key, kTimerUpdateSecs, kTimerUpdateActiveCB)

    def _PlayCGZM(self, mission):
        PtDebugPrint("grtzMarkerScopeGUI._PlayCGZM():\tStarting CGZM #{}".format(mission), level=kWarningLevel)
        if self._lookingAtGUI:
            self._UpdateGUI(mission, score=0, star=True)
            PtAtTimeCallback(self.key, kTimerUpdateSecs, kTimerUpdateActiveCB)
        PtSendKIMessageInt(kMGStartCGZGame, mission)

    def _PopTelescope(self):
        """Tells the telescope script we're done"""
        notify = ptNotify(self.key)
        notify.clearReceivers()
        for i in kTelescopes:
            try: 
                obj = PtFindSceneobject(i, PtGetAgeName())
                pythonScripts = obj.getPythonMods()
                for script in pythonScripts:
                    notify.addReceiver(script)
            except:
                PtDebugPrint("grtzMarkerScopeGUI._PopTelescope():\tCould not send quit message to '{}'".format(i))
        notify.netPropagate(False)
        notify.setActivate(1.0)
        notify.send()

    def _ShowGUI(self):
        MGMachineOnResp.run(self.key, netPropagate=False)
        gameSelector = MarkerGameDlg.dialog.getControlModFromTag(kRGMarkerGameSelect)
        if PtDetermineKIMarkerLevel() < kKIMarkerNormalLevel:
            PtDebugPrint("grtzMarkerScopeGUI._ShowGUI():\tKI Level not high enough, disabling GUI controls", level=kWarningLevel)
            gameSelector.setValue(-1)
            gameSelector.disable()
        else:
            self._UpdateGUI()
            mission = xMarkerGameUtils.GetCurrentCGZM()
            gameSelector.setValue(mission)
            if mission != -1:
                if xMarkerGameUtils.IsCGZMComplete():
                    PtDebugPrint("grtzMarkerScopeGUI._ShowGUI():\tCGZM #{}: complete!".format(mission), level=kWarningLevel)
                    self._StopCGZM(win=True)
                else:
                    PtDebugPrint("grtzMarkerScopeGUI._ShowGUI():\tCGZM #{}: still playing...".format(mission), level=kWarningLevel)
                    PtAtTimeCallback(self.key, kTimerUpdateSecs, kTimerUpdateActiveCB)

    def _StopCGZM(self, win):
        mission = xMarkerGameUtils.GetCurrentCGZM()
        if win:
            score = self._scores[mission]
            timeRange = xMarkerGameUtils.GetCGZMTimes(mission)
            currentTime = xMarkerGameUtils.GetCurrentTime()
            time = currentTime - timeRange.start_time
            isBestTime = time < timeRange.best_time
            timeRange.best_time = min(timeRange.best_time, time) if timeRange.best_time else time
            PtDebugPrint(f"grtzMarkerScopeGUI._StopCGZM():\t{timeRange=!s}, {currentTime=}, {score.getPoints()=} {time=}", level=kWarningLevel)

            # Update the score. Be aware that we may not actually have the GameScore at all...
            self._UpdateScore(mission, timeRange.best_time)
            xMarkerGameUtils.SetCGZMTimes(mission, timeRange, legacyOnly=True)
            self._UpdateGUI(mission, quitting=False, score=time, star=isBestTime)

        # Tear down game brain
        PtSendKIMessageInt(kMGStopCGZGame, -1)

        # Update UI
        gameSelector = MarkerGameDlg.dialog.getControlModFromTag(kRGMarkerGameSelect)
        gameSelector.setValue(-1)

    def _UpdateGUI(self, mission=-1, quitting=False, score=None, star=None):
        # If mission is -1, this is a total update
        if mission == -1:
            for i in range(len(grtzMarkerGames.mgs)):
                self._UpdateGUI(i)
            return

        # Update this marker mission
        if score is None:
            prevScore = self._scores[mission]
            prev = prevScore.getPoints() if isinstance(prevScore, ptGameScore) else prevScore
            if quitting:
                span = prev
            else:
                if xMarkerGameUtils.GetCurrentCGZM() == mission:
                    timeRange = xMarkerGameUtils.GetCGZMTimes(mission)
                    span = xMarkerGameUtils.GetCurrentTime() - timeRange.start_time
                else:
                    span = prev
                if star is None and span < prev:
                    star = True
        else:
            span = score

        # Generate the message
        if score is None and span == 0:
            if span == -1:
                msg = PtGetLocalizedString("KI.MarkerGame.pendingActionLoading")
            else:
                msg = "--:--:--"
        else:
            st = time.gmtime(span)
            if st.tm_yday > 1:
                # days, hours, minutes, seconds -- you really suck at this
                # if you go over a year, you really suck
                msg = "{:02d}:{:02d}:{:02d}:{:02d}".format(st.tm_yday, st.tm_hour, st.tm_min, st.tm_sec)
            else:
                # hours, minutes, seconds
                msg = "{:02d}:{:02d}:{:02d}".format(st.tm_hour, st.tm_min, st.tm_sec)

        if star:
            msg = "** {}".format(msg)

        # Now do the deed
        fieldID = (mission * 10) + kMarkerGameFieldStart
        numTB = MarkerGameDlg.dialog.getControlModFromTag(fieldID + kMarkerGameNumFieldOffset)
        numTB.setString(str(len(grtzMarkerGames.mgs[mission])))
        timeTB = MarkerGameDlg.dialog.getControlModFromTag(fieldID + kMarkerGameNameFieldOffset)
        timeTB.setString(msg)

    def _UpdateScore(self, mission: int, points: int) -> None:
        if isinstance(self._scores[mission], ptGameScore):
            self._scores[mission].remove()
            self._scores[mission] = -1
        ptGameScore.createPlayerScore(kGameScore.format(mission), kScoreType, points, self.key)
