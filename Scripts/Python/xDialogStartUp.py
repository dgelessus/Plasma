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
"""
Module: xDialogStartUp
Age: Global
Date: March 2006
Author: Derek Odell
Start Up dialog logic
"""

from Plasma import *
from PlasmaTypes import *
from PlasmaConstants import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from xStartPathHelpers import *
import PlasmaControlKeys

import re
import webbrowser

# define the attributes that will be entered in max
GUIDiag4a   = ptAttribGUIDialog(1, "GUI Dialog 4a")
GUIDiag4b   = ptAttribGUIDialog(2, "GUI Dialog 4b")
GUIDiag4c   = ptAttribGUIDialog(3, "GUI Dialog 4c")
GUIDiag4d   = ptAttribGUIDialog(4, "GUI Dialog 4d")
GUIDiag5    = ptAttribGUIDialog(5, "GUI Dialog 5")
GUIDiag6    = ptAttribGUIDialog(6, "GUI Dialog 6")

resp4aPlayer01  = ptAttribResponder(7, "resp: 4A Player01", ["in", "out"])
resp4aPlayer02  = ptAttribResponder(8, "resp: 4A Player02", ["in", "out"])
resp4aPlayer03  = ptAttribResponder(9, "resp: 4A Player03", ["in", "out"])
resp4aPlayer04  = ptAttribResponder(10, "resp: 4A Player04", ["in", "out"])
resp4aPlayer05  = ptAttribResponder(11, "resp: 4A Player05", ["in", "out"])
resp4aPlayer06  = ptAttribResponder(12, "resp: 4A Player06", ["in", "out"])

resp4bPlayer01  = ptAttribResponder(13, "resp: 4B Player01", ["in", "out"])
resp4bPlayer02  = ptAttribResponder(14, "resp: 4B Player02", ["in", "out"])
resp4bPlayer03  = ptAttribResponder(15, "resp: 4B Player03", ["in", "out"])
resp4bPlayer04  = ptAttribResponder(16, "resp: 4B Player04", ["in", "out"])
resp4bPlayer05  = ptAttribResponder(17, "resp: 4B Player05", ["in", "out"])
resp4bPlayer06  = ptAttribResponder(18, "resp: 4B Player06", ["in", "out"])

respLink        = ptAttribResponder(19, "resp: Link", ["ACA", "Personal"])

mapPlayer01     = ptAttribDynamicMap(20, "map: Player01")
mapPlayer02     = ptAttribDynamicMap(21, "map: Player02")
mapPlayer03     = ptAttribDynamicMap(22, "map: Player03")
mapPlayer04     = ptAttribDynamicMap(23, "map: Player04")
mapPlayer05     = ptAttribDynamicMap(24, "map: Player05")
mapPlayer06     = ptAttribDynamicMap(25, "map: Player06")

GUIDiag6a       = ptAttribGUIDialog(26, "GUI Dialog 6a")
respLinkOutSND  = ptAttribResponder(27, "resp: Link Out SND")

#====================================
# GUI Dialog globals

#----Dialog 4a ## Text MUST Be +10 From HotSpot ##
k4aVisitID          = 100
k4aQuitID           = 101
k4aDeleteID         = 102
k4aPlayer01         = 103
k4aPlayerTxt01      = 113
k4aPlayer02         = 104
k4aPlayerTxt02      = 114
k4aPlayer03         = 105
k4aPlayerTxt03      = 115
k4aPlayer04         = 106
k4aPlayerTxt04      = 116
k4aPlayer05         = 107
k4aPlayerTxt05      = 117
k4aPlayer06         = 108
k4aPlayerTxt06      = 118

#----Dialog 4b ## Text MUST Be +10 From HotSpot ##
k4bExploreID        = 200
k4bQuitID           = 201
k4bDeleteID         = 202
k4bPlayer01         = 203
k4bPlayerTxt01      = 213
k4bPlayer02         = 204
k4bPlayerTxt02      = 214
k4bPlayer03         = 205
k4bPlayerTxt03      = 215
k4bPlayer04         = 206
k4bPlayerTxt04      = 216
k4bPlayer05         = 207
k4bPlayerTxt05      = 217
k4bPlayer06         = 208
k4bPlayerTxt06      = 218

#----Dialog 4c
k4cYesID            = 300
k4cNoID             = 301
k4cStaticID         = 302

#----Dialog 4d
k4dYesID            = 400
k4dTextID           = 401

#----Dialog 5
k5PayID             = 500
k5VisitID           = 501
k5BackID            = 502
k5LinkID            = 503

#----Dialog 6
k6QuitID            = 600
k6BackID            = 601
k6PlayID            = 602
k6PayingID          = 603
k6NameID            = 604
k6InviteID          = 605
k6MaleID            = 606
k6FemaleID          = 607
k6PlayTxtID         = 608
k6CleftID           = 609
k6ReltoID           = 610
k6CleftHelpID       = 611
k6ReltoHelpID       = 612

#====================================
# Globals
gPlayerList         = None
gSelectedSlot       = 0
gClickedWrongSlot   = 0
gBlueColor          = ptColor(0.414, 0.449, 0.617, 1.0)
gTanColor           = ptColor(0.500, 0.449, 0.375, 1.0)
gExp_HotSpot        = [k4bPlayer01,k4bPlayer02,k4bPlayer03,k4bPlayer04,k4bPlayer05,k4bPlayer06]
gVis_HotSpot        = [k4aPlayer01,k4aPlayer02,k4aPlayer03,k4aPlayer04,k4aPlayer05,k4aPlayer06]
gExp_TxtBox         = [k4bPlayerTxt01,k4bPlayerTxt02,k4bPlayerTxt03,k4bPlayerTxt04,k4bPlayerTxt05,k4bPlayerTxt06]
gVis_TxtBox         = [k4aPlayerTxt01,k4aPlayerTxt02,k4aPlayerTxt03,k4aPlayerTxt04,k4aPlayerTxt05,k4aPlayerTxt06]
gExp_HiLite         = [resp4bPlayer01,resp4bPlayer02,resp4bPlayer03,resp4bPlayer04,resp4bPlayer05,resp4bPlayer06]
gVis_HiLite         = [resp4aPlayer01,resp4aPlayer02,resp4aPlayer03,resp4aPlayer04,resp4aPlayer05,resp4aPlayer06]
gMinusExplorer      = 203
gMinusVisitor       = 103
gPlayerStart        = "relto"

WebLaunchCmd = None

#====================================

class xDialogStartUp(ptResponder):
    ###########################
    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5340
        self.version = 3
        self.ageLink = None
        PtDebugPrint("xDialogStartUp: init  version = %d" % self.version)

    ###########################
    def OnServerInitComplete(self):
        global gExp_HotSpot
        global gExp_TxtBox
        global gExp_HiLite
        global WebLaunchCmd

        self.InitPlayerList(GUIDiag4b, gExp_HotSpot, gExp_TxtBox, gExp_HiLite)

        GUIDiag6.dialog.getControlModFromTag(k6NameID).setStringSize(63)
        GUIDiag6.dialog.getControlModFromTag(k6InviteID).setStringSize(63)

        WebLaunchCmd = webbrowser.open_new

    ###########################
    def BeginAgeUnLoad(self,avatar):
        if GUIDiag4a.dialog.isEnabled():
            PtHideDialog("GUIDialog04a")
        if GUIDiag4b.dialog.isEnabled():
            PtHideDialog("GUIDialog04b")
        if GUIDiag4c.dialog.isEnabled():
            PtHideDialog("GUIDialog04c")
        if GUIDiag4d.dialog.isEnabled():
            PtHideDialog("GUIDialog04d")
        if GUIDiag5.dialog.isEnabled():
            PtHideDialog("GUIDialog05")
        if GUIDiag6.dialog.isEnabled():
            PtHideDialog("GUIDialog06")
        if GUIDiag6a.dialog.isEnabled():
            PtHideDialog("GUIDialog06a")

    ###########################
    def OnGUINotify(self,id,control,event):
        global gSelectedSlot
        global gPlayerList
        global gExp_HotSpot
        global gMinusExplorer
        global gMinusVisitor
        global gClickedWrongSlot
        global gPlayerStart

        #PtDebugPrint("xDialogStartUp: GUI Notify id=%d, event=%d control=" % (id,event),control)
        if control:
            tagID = control.getTagID()

        #################################
        ##     Visitor Player List     ##
        #################################
        if id == GUIDiag4a.id:
            if event == kAction or event == kValueChanged:
                if  tagID == k4aVisitID: ## Visit Uru ##
                    PtHideDialog("GUIDialog04a")
                    PtShowDialog("GUIDialog05")

                elif  tagID == k4aQuitID: ## Quit ##
                    PtLocalizedYesNoDialog(None, "KI.Messages.LeaveGame", dialogType=PtConfirmationType.ConfirmQuit)

                elif  tagID == k4aPlayer01: ## Click Event ##
                    if gPlayerList[0]:
                        self.SelectSlot(GUIDiag4a, tagID)
                    else:
                        PtHideDialog("GUIDialog04a")
                        PtShowDialog("GUIDialog06")

                elif  tagID == k4aPlayer02 or tagID == k4aPlayer03 or k4aPlayer04 or k4aPlayer05 or k4aPlayer06: ## Shortcut Skip to Create Visitor ##
                    gClickedWrongSlot = 1
                    PtHideDialog("GUIDialog04a")
                    PtShowDialog("GUIDialog05")

            elif event == kInterestingEvent:
                self.ToggleColor(GUIDiag4a, tagID, on=control.isInteresting())

        #################################
        ##    Explorer Player List     ##
        #################################
        elif id == GUIDiag4b.id:
            if event == kAction or event == kValueChanged:
                if  tagID == k4bExploreID: ## Explore Uru ##
                    if gSelectedSlot and gPlayerList[gSelectedSlot-gMinusExplorer]:
                        PtShowDialog("GUIDialog06a")
                        PtDebugPrint("Player selected.")

                        # start setting active player (we'll link out when this operation completes)
                        playerID = gPlayerList[gSelectedSlot-gMinusExplorer][1]
                        PtDebugPrint("Setting active player.")
                        PtSetActivePlayer(playerID)

                    ## Or Else?? ##

                elif  tagID == k4bQuitID: ## Quit ##
                    PtLocalizedYesNoDialog(None, "KI.Messages.LeaveGame", dialogType=PtConfirmationType.ConfirmQuit)

                elif  tagID == k4bDeleteID: ## Delete Explorer ##
                    if gSelectedSlot and gPlayerList[gSelectedSlot-gMinusExplorer]:
                        deleteString = "Would you like to delete the EXPLORER " + str(gPlayerList[gSelectedSlot-gMinusExplorer][0]) + "?"
                        GUIDiag4c.dialog.getControlModFromTag(k4cStaticID).setString(deleteString)
                        self.PlayerListNotify(GUIDiag4b, gExp_HotSpot, 0)
                        PtShowDialog("GUIDialog04c")
                    ## Or Else?? ##

                elif  (tagID == k4bPlayer02 or tagID == k4bPlayer03 or tagID == k4bPlayer04 or tagID == k4bPlayer05 or tagID == k4bPlayer06) and not (tagID == gSelectedSlot):
                    if gPlayerList[tagID-gMinusExplorer]:
                        self.SelectSlot(GUIDiag4b, tagID)
                    else:
                        PtHideDialog("GUIDialog04b")
                        PtShowDialog("GUIDialog06")

            elif event == kInterestingEvent: ## RollOver Event ##
                self.ToggleColor(GUIDiag4b, tagID, on=control.isInteresting())

            elif event == kSpecialAction:
                if tagID in gExp_HotSpot or tagID in gVis_HotSpot:
                    if gSelectedSlot and gPlayerList[gSelectedSlot-gMinusExplorer]:
                        PtShowDialog("GUIDialog06a")
                        PtDebugPrint("Player selected.")

                        # start setting active player (we'll link out when this operation completes)
                        playerID = gPlayerList[gSelectedSlot-gMinusExplorer][1]
                        PtDebugPrint("Setting active player.")
                        PtSetActivePlayer(playerID)

            elif event == kShowHide:
                self.SyncColorsToSelection(GUIDiag4b, gExp_HotSpot, gExp_TxtBox, gExp_HiLite)

        #################################
        ##        Delete Player        ##
        #################################
        elif id == GUIDiag4c.id:
            if event == kAction or event == kValueChanged:
                if  tagID == k4cYesID and gPlayerList[gSelectedSlot-gMinusExplorer]: ## Confirm Delete ##
                    playerID = 0
                    playerID = gPlayerList[gSelectedSlot-gMinusExplorer][1]
                    PtDeletePlayer(playerID)

                elif  tagID == k4cNoID: ## Cancel Delete ##
                    PtHideDialog("GUIDialog04c")
                    self.PlayerListNotify(GUIDiag4b, gExp_HotSpot, 1)

        #################################
        ##    Display Error Message    ##
        #################################
        elif id == GUIDiag4d.id:
            if event == kAction or event == kValueChanged:
                if tagID == k4dYesID: ## OK/Continue from Error ##
                    self.PlayerListNotify(GUIDiag4b, gExp_HotSpot, 1)
                    PtHideDialog("GUIDialog04d")
                    GUIDiag6.dialog.getControlModFromTag(k6PlayID).enable()

        #################################
        ##        Create Player        ##
        #################################
        elif id == GUIDiag6.id:
            if event == kAction or event == kValueChanged:
                if  tagID == k6QuitID: ## Quit ##
                    PtLocalizedYesNoDialog(None, "KI.Messages.LeaveGame", dialogType=PtConfirmationType.ConfirmQuit)

                elif  tagID == k6BackID: ## Back To Player Select ##
                    PtHideDialog("GUIDialog06")
                    PtShowDialog("GUIDialog04b")
                    # if no explorers, unselect all slots so any of them can be clicked again
                    if not gPlayerList or not gPlayerList[1]:
                        self.SelectSlot(GUIDiag4b, k4bPlayer01)

                elif  tagID == k6PlayID: ## Play ##
                    playerName = GUIDiag6.dialog.getControlModFromTag(k6NameID).getString()
                    playerGender = ""
                    playerStart = ""

                    if GUIDiag6.dialog.getControlModFromTag(k6MaleID).isChecked():
                        playerGender = "male"
                    if GUIDiag6.dialog.getControlModFromTag(k6FemaleID).isChecked():
                        playerGender = "female"
                    if GUIDiag6.dialog.getControlModFromTag(k6CleftID).isChecked():
                        playerStart = "cleft"
                    if GUIDiag6.dialog.getControlModFromTag(k6ReltoID).isChecked():
                        playerStart = "relto"

                    if playerName == "" or playerName.isspace():
                        errorString = PtGetLocalizedString("GUI.Dialog04d.ErrorName")
                        GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                        PtShowDialog("GUIDialog04d")
                    elif playerGender == "":
                        errorString = PtGetLocalizedString("GUI.Dialog04d.ErrorGender")
                        GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                        PtShowDialog("GUIDialog04d")
                    elif playerStart == "":
                        errorString = PtGetLocalizedString("GUI.Dialog04d.ErrorPath")
                        GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                        PtShowDialog("GUIDialog04d")
                    else:
                        fixedPlayerName = playerName.strip()
                        (fixedPlayerName, whitespacefixedcount) = re.subn(r"\s{2,}|[\t\n\r\f\v]", " ", fixedPlayerName)

                        (fixedPlayerName, RogueCount,) = re.subn('[\x00-\x1f]', '', fixedPlayerName)
                        if RogueCount > 0 or whitespacefixedcount > 0:
                            if RogueCount > 0:
                                errorString = PtGetLocalizedString("GUI.Dialog04d.InvalidCharacters")
                            else:
                                errorString = PtGetLocalizedString("GUI.Dialog04d.IncorrectFormatting")
                            GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                            PtShowDialog("GUIDialog04d")

                            GUIDiag6.dialog.getControlModFromTag(k6NameID).setString(fixedPlayerName)
                        else:
                            PtDebugPrint("Creating Player")
                            PtShowDialog("GUIDialog06a")
                            GUIDiag6.dialog.getControlModFromTag(k6PlayID).disable()
                            gPlayerStart = playerStart
                            PtCreatePlayer(fixedPlayerName, playerGender, "")  #                                                  <---

                elif  tagID == k6MaleID: ## Gender Male ##
                    GUIDiag6.dialog.getControlModFromTag(k6FemaleID).setChecked(False)

                elif  tagID == k6FemaleID: ## Gender Female ##
                    GUIDiag6.dialog.getControlModFromTag(k6MaleID).setChecked(False)

                elif  tagID == k6CleftID: ## Start Cleft ##
                    GUIDiag6.dialog.getControlModFromTag(k6ReltoID).setChecked(False)

                elif  tagID == k6ReltoID: ## Start Relto ##
                    GUIDiag6.dialog.getControlModFromTag(k6CleftID).setChecked(False)

                elif tagID == k6CleftHelpID: ## Cleft Help Button ##
                    errorString = PtGetLocalizedString("GUI.Dialog04d.CleftHelp")
                    GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                    PtShowDialog("GUIDialog04d")

                elif tagID == k6ReltoHelpID: ## Relto Help Button ##
                    errorString = PtGetLocalizedString("GUI.Dialog04d.ReltoHelp")
                    GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                    PtShowDialog("GUIDialog04d")

    ###########################
    def OnAccountUpdate(self, opType, result, playerInt):
        global gExp_HotSpot
        global gExp_TxtBox
        global gVis_TxtBox
        global gExp_HiLite
        global gPlayerList
        global gPlayerStart

        if result != 0:
            PtDebugPrint("OnAccountUpdate type %u failed: %u" % (opType, result))
            PtHideDialog("GUIDialog06a")

            if result == 12:
                errorString = PtGetLocalizedString("GUI.Dialog04d.NameAlreadyExists")
                GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                PtShowDialog("GUIDialog04d")
            elif result == 28:
                errorString = PtGetLocalizedString("GUI.Dialog04d.IllegalName")
                GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                PtShowDialog("GUIDialog04d")
            else:
                errorString = PtGetLocalizedString("GUI.Dialog04d.NetworkError")
                GUIDiag4d.dialog.getControlModFromTag(k4dTextID).setString(errorString)
                PtShowDialog("GUIDialog04d")
            return

        if playerInt == 0:
            return

        if opType == PtAccountUpdateType.kActivePlayer:
            PtDebugPrint("Active player set.")

            pythonBox = PtFindSceneobject("OptionsDialog", "GUI")
            pmlist = pythonBox.getPythonMods()
            for pm in pmlist:
                notify = ptNotify(self.key)
                notify.clearReceivers()
                notify.addReceiver(pm)
                notify.setActivate(1.0)
                notify.send()

            # setup the link to player's Relto
            self.ageLink = ptAgeLinkStruct()
            ageInfo = ptAgeInfoStruct()

            start = ptVault().findChronicleEntry("StartPathChosen")
            if start is not None:
                gPlayerStart = start.getValue()
            if StartInACA():
                ageInfo.setAgeFilename("AvatarCustomization")
            elif StartInCleft():
                ageInfo.setAgeFilename("Cleft")
            elif StartInRelto():
                ageInfo.setAgeFilename("Personal")
            SelectPath(gPlayerStart)

            self.ageLink.setAgeInfo(ageInfo)
            self.ageLink.setLinkingRules(PtLinkingRules.kOwnedBook)

            PtDebugPrint("Linking to %s" % (self.ageLink.getAgeInfo().getAgeFilename()))
            respLinkOutSND.run(self.key)
            ptNetLinkingMgr().linkToAge(self.ageLink)
            self.ageLink = None

        elif opType == PtAccountUpdateType.kCreatePlayer:
            PtDebugPrint("Player created.")

            # setup the link to ACA
            self.ageLink = ptAgeLinkStruct()
            ageInfo = ptAgeInfoStruct()
            ageInfo.setAgeFilename("AvatarCustomization")
            self.ageLink.setAgeInfo(ageInfo)
            self.ageLink.setLinkingRules(PtLinkingRules.kBasicLink)


            # start setting active player (we'll link out once this operation completes)
            PtDebugPrint("Setting active player.")
            PtSetActivePlayer(playerInt)

        elif opType == PtAccountUpdateType.kDeletePlayer:
            self.InitPlayerList(GUIDiag4b, gExp_HotSpot, gExp_TxtBox, gExp_HiLite)
            # unselect all slots so any of them can be clicked again
            self.SelectSlot(GUIDiag4b, k4bPlayer01)

            PtHideDialog("GUIDialog04c")

        else:
            PtDebugPrint("AccountUpdate - Unknown: optype = %d, result = %d, playerInt = %d" % (opType, result, playerInt))

    ###########################
    def ToggleColor(self, dlgObj, tagID, *, on: bool):
        global gTanColor
        global gBlueColor
        global gExp_HotSpot
        global gExp_HiLite

        currentColor = dlgObj.dialog.getControlModFromTag(tagID+10).getForeColor()

        idx = gExp_HotSpot.index(tagID)
        respToRun = gExp_HiLite[idx]

        if currentColor == gBlueColor and not on:
            PtDebugPrint(f"xDialogStartUp: toggle {tagID=} off")
            dlgObj.dialog.getControlModFromTag(tagID+10).setForeColor(gTanColor)
            respToRun.run(self.key,state="out")
        elif currentColor == gTanColor and on:
            PtDebugPrint(f"xDialogStartUp: toggle {tagID=} on")
            dlgObj.dialog.getControlModFromTag(tagID+10).setForeColor(gBlueColor)
            respToRun.run(self.key,state="in")

    ###########################
    def SelectSlot(self,dlgObj,tagID):
        global gSelectedSlot

        if tagID and tagID != gSelectedSlot: ## If there's a currently selected slot, return it to normal ##
            PtDebugPrint("xDialogStartUp.SelectSlot: tagID = %d   gSelectedSlot = %d" % (tagID, gSelectedSlot))
            if gSelectedSlot:
                self.ToggleColor(dlgObj, gSelectedSlot, on=False)
                dlgObj.dialog.getControlModFromTag(gSelectedSlot).setNotifyOnInteresting(True)
                PtDebugPrint("xDialogStartUp.SelectSlot: Setting old slot to Interesting")

            gSelectedSlot = tagID
            dlgObj.dialog.getControlModFromTag(gSelectedSlot).setNotifyOnInteresting(False)
            PtDebugPrint("xDialogStartUp.SelectSlot: Setting gSelectedSlot to new val and removing Interesting")

    ###########################
    def SyncColorsToSelection(self, dlgObj, listHotSpot, listTxtBox, listHiLite):
        for hotspot, txtbox, resp in zip(listHotSpot, listTxtBox, listHiLite):
            ctrl = dlgObj.dialog.getControlModFromTag(txtbox)
            if gSelectedSlot != hotspot and ctrl.getForeColor() == gBlueColor:
                ctrl.setForeColor(gTanColor)
                resp.run(self.key, state="out")
            elif gSelectedSlot == hotspot and ctrl.getForeColor() != gBlueColor:
                ctrl.setForeColor(gBlueColor)
                resp.run(self.key, state="in")
            if not gSelectedSlot != hotspot:
                ctrl.unFocus()

    ###########################
    def InitPlayerList(self,dlgObj,listHotSpot,listTxtBox,listHiLite):
        global gTanColor
        global gPlayerList

        gPlayerList = PtGetAccountPlayerList()
        ExplorerList = gPlayerList[1:]
        ExplorerList.sort(key=lambda x: x[1])
        if len(ExplorerList) > 1:
            del gPlayerList[1:]
            for Explorer in ExplorerList:
                gPlayerList.append(Explorer)

        PtDebugPrint("xDialogStartUp.InitPlayerList Enter: gPlayerList = %s" % (str(gPlayerList)))

        for tagID in listTxtBox: ## Setup The Slot Colors And Default Titles ##
            createExplorer = PtGetLocalizedString("GUI.Dialog04b.CreateExplorer")
            textbox = dlgObj.dialog.getControlModFromTag(tagID)
            textbox.setString(createExplorer)
            textbox.setForeColor(gTanColor)
        for respToRun in listHiLite:
            respToRun.run(self.key,state="out")

        self.PlayerListNotify(dlgObj, listHotSpot, 1)

        basePath = PtGetUserPath() + "\\Avatars\\"

        TextMaps = [mapPlayer01,mapPlayer02,mapPlayer03,mapPlayer04,mapPlayer05,mapPlayer06]
        for Tex in TextMaps:
            Tex.textmap.clearToColor(ptColor(0, 0, 0, 0))
            Tex.textmap.flush()

        for idx in range(1, len(gPlayerList[1:]) + 1): ## Setup The Explorer Slots ##
            player = gPlayerList[idx]
            dlgObj.dialog.getControlModFromTag(listTxtBox[idx]).setString(player[0])
            try:
                filename = basePath + str(player[1]) + ".jpg"
                PtDebugPrint("xDialogStartUp: Trying to load \"" + filename + "\"")
                theImage = PtLoadJPEGFromDisk(filename, 0, 0)
                TextMaps[idx].textmap.drawImage(0, 0, theImage, 0)
                TextMaps[idx].textmap.flush()
            except:
                PtDebugPrint("xDialogStartUp: Load failed. This avatar probably doesn't have a snapshot")

        try:
            gPlayerList[0]
        except IndexError:
            self.SelectSlot(dlgObj, k4bPlayer01)
        else:
            self.ToggleColor(dlgObj, listHotSpot[1], on=True)
            self.SelectSlot(dlgObj, listHotSpot[1])

        while len(gPlayerList) < 6:   ## Now That Slots Are Initialized, Fill Out The List ##
            gPlayerList.append(None)  ##    So We Don't Have Out Of Bounds Errors Later    ##
        PtDebugPrint("xDialogStartUp.InitPlayerList Exit: gPlayerList = %s" % (str(gPlayerList)))

    ###########################
    def PlayerListNotify(self,dlgObj,listHotSpot,toggle):
        global gSelectedSlot

        for tagID in listHotSpot:
            PtDebugPrint("xDialogStartUp.PlayerListNotify: setting tagID (%d) to Interesting = %d" % (tagID, toggle))
            dlgObj.dialog.getControlModFromTag(tagID).setNotifyOnInteresting(toggle)

        if toggle and gSelectedSlot:
            PtDebugPrint("xDialogStartUp.PlayerListNotify: setting gSelectedSlot (%d) to not Interesting" % (gSelectedSlot))
            dlgObj.dialog.getControlModFromTag(gSelectedSlot).setNotifyOnInteresting(False)

        # Everyone is an explorer, so disable the button for visiting.
        dlgObj.dialog.getControlModFromTag(listHotSpot[0]).disable()
