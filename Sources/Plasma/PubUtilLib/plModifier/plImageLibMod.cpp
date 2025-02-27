/*==LICENSE==*

CyanWorlds.com Engine - MMOG client, server and tools
Copyright (C) 2011  Cyan Worlds, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Additional permissions under GNU GPL version 3 section 7

If you modify this Program, or any covered work, by linking or
combining it with any of RAD Game Tools Bink SDK, Autodesk 3ds Max SDK,
NVIDIA PhysX SDK, Microsoft DirectX SDK, OpenSSL library, Independent
JPEG Group JPEG library, Microsoft Windows Media SDK, or Apple QuickTime SDK
(or a modified version of those libraries),
containing parts covered by the terms of the Bink SDK EULA, 3ds Max EULA,
PhysX SDK EULA, DirectX SDK EULA, OpenSSL and SSLeay licenses, IJG
JPEG Library README, Windows Media SDK EULA, or QuickTime SDK EULA, the
licensors of this Program grant you additional
permission to convey the resulting work. Corresponding Source for a
non-source form of such a combination shall include the source code for
the parts of OpenSSL and IJG JPEG Library used as well as that of the covered
work.

You can contact Cyan Worlds, Inc. by email legal@cyan.com
 or by snail mail at:
      Cyan Worlds, Inc.
      14617 N Newport Hwy
      Mead, WA   99021

*==LICENSE==*/

#include "plImageLibMod.h"

#include "plGImage/plBitmap.h"
#include "pnMessage/plRefMsg.h"

#include "hsTimer.h"
#include "hsStream.h"
#include "hsResMgr.h"


bool plImageLibMod::MsgReceive(plMessage* msg)
{
    plGenRefMsg *refMsg = plGenRefMsg::ConvertNoRef( msg );
    if (refMsg != nullptr)
    {
        if( refMsg->GetContext() & ( plRefMsg::kOnCreate | plRefMsg::kOnRequest | plRefMsg::kOnReplace ) )
        {
            if ((hsSsize_t)fImages.size() <= refMsg->fWhich)
                fImages.resize(refMsg->fWhich + 1);

            fImages[ refMsg->fWhich ] = plBitmap::ConvertNoRef( refMsg->GetRef() );
        }
        else if( refMsg->GetContext() & ( plRefMsg::kOnRemove | plRefMsg::kOnDestroy ) )
        {
            fImages[refMsg->fWhich] = nullptr;
        }
        return true;
    }

    return plSingleModifier::MsgReceive(msg);
}
    
void plImageLibMod::Read(hsStream* stream, hsResMgr* mgr)
{
    plSingleModifier::Read(stream, mgr);

    uint32_t count = stream->ReadLE32();
    fImages.assign(count, nullptr);
    for (uint32_t i = 0; i < count; i++)
        mgr->ReadKeyNotifyMe( stream, new plGenRefMsg( GetKey(), plRefMsg::kOnCreate, i, kRefImage ), plRefFlags::kActiveRef );
}

void plImageLibMod::Write(hsStream* stream, hsResMgr* mgr)
{
    plSingleModifier::Write(stream, mgr);

    stream->WriteLE32((uint32_t)fImages.size());
    for (plBitmap* image : fImages)
        mgr->WriteKey(stream, image->GetKey());
}

plBitmap* plImageLibMod::GetImage(const ST::string& imageName) const
{
    auto findIt = std::find_if(fImages.begin(), fImages.end(), [&imageName](plBitmap* x) { return x->GetKeyName() == imageName; });
    if (findIt != fImages.end())
        return *findIt;
    return nullptr;
}

std::vector<ST::string> plImageLibMod::GetImageNames() const
{
    std::vector<ST::string> names;
    names.reserve(fImages.size());

    for (const auto& image : fImages) {
        if (image)
            names.emplace_back(image->GetKeyName());
    }
    return names;
}
