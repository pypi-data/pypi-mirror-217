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

import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

mongo = MongoClient(MONGO_URI)
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo['AYIIN']
mdb = mongo_client.AYIIN
