#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS, adminlist
from strings import get_string
from VIPMUSIC import app
from VIPMUSIC.core.call import VIP
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.plugins import extra_plugins_enabled
from VIPMUSIC.utils.database import (
    delete_filter,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
    set_loop,
)


@app.on_message(
    filters.command(["stop", "end", "cstop", "cend"]) & filters.group & ~BANNED_USERS
)
async def stop_music(cli, message: Message):
    if await is_maintenance() is False:
        if message.from_user.id not in SUDOERS:
            return await message.reply_text(
                "Bot is under maintenance. Please wait for some time..."
            )
    if not len(message.command) < 2:
        if extra_plugins_enabled:
            if not message.command[0][0] == "c" and not message.command[0][0] == "e":
                filter = " ".join(message.command[1:])
                deleted = await delete_filter(message.chat.id, filter)
                if deleted:
                    return await message.reply_text(f"**ᴅᴇʟᴇᴛᴇᴅ ғɪʟᴛᴇʀ {filter}.**")
                else:
                    return await message.reply_text("**ɴᴏ sᴜᴄʜ ғɪʟᴛᴇʀ.**")

    if await is_commanddelete_on(message.chat.id):
        try:
            await message.delete()
        except:
            pass
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    if message.sender_chat:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="How to Fix this? ",
                        callback_data="AnonymousAdmin",
                    ),
                ]
            ]
        )
        return await message.reply_text(_["general_4"], reply_markup=upl)

    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except:
            return await message.reply_text(_["cplay_4"])
    else:
        chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        if message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_18"])
            else:
                if message.from_user.id not in admins:
                    return await message.reply_text(_["admin_19"])
    await VIP.st_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(_["admin_9"].format(message.from_user.mention))


import random

from pyrogram import filters
from pyrogram.types import Message

from VIPMUSIC import app
from VIPMUSIC.utils.database import get_assistant

photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]


@app.on_message(filters.left_chat_member, group=-15)
async def on_left_chat_member(_, message: Message):
    try:
        chat_id = message.chat.id
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == userbot.id:
            remove_by = (
                message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
            )
            chat_id = message.chat.id
            left = f"✫ <b><u>#𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁_𝗕𝗮𝗻𝗻𝗲𝗱</u></b> ✫\n\n𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ : {title}\n\n𝐂ʜᴀᴛ 𝐈ᴅ : {chat_id}\n\n𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ : {remove_by}\n\n**𝐔sᴇʀɴᴀᴍᴇ:-**  @{userbot.username}\n\n**𝐈ᴅ:-** {userbot.id}"
            keyboard=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"✨𝐔𝐧𝐛𝐚𝐧 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭✨",
                                    callback_data=f"unban_userbot",
                                )
                            ]
                        ]
                    ),
            )
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
            await app.send_photo(
                message.chat.id,
                photo=random.choice(photo),
                caption=left,
                reply_markup=keyboard,
            )

    except Exception as e:
        return
