# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import fipper

from ._core import mdb


asstdb = mdb.assistant


class Assistant:
    async def set_assistant(self: "fipper.Client", api_id, api_hash, session_string):
        user = await asstdb.find_one({"user_id": self.me.id})
        if user:
            await asstdb.update_one(
                {"user_id": self.me.id},
                {
                    "$set": {
                        "api_id": api_id,
                        "api_hash": api_hash,
                        "session_string": session_string,
                    }
                },
            )
        else:
            await asstdb.insert_one(
                {
                    "user_id": self.me.id,
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
            )


    async def del_assistant(self: "fipper.Client"):
        return await asstdb.delete_one({"user_id": self.me.id})


    async def get_assistant(self: "fipper.Client"):
        data = []
        ubot = await asstdb.find_one({"user_id": self.me.id})
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
        return data
