from pyrogram.types import InlineKeyboardButton

async def start_cmd(Legend):
    x = await Legend.get_me()
    START_OP = [
        [
            InlineKeyboardButton(
                text="🥀 Developer 🥀", url=f"https://t.me/Tashribots2342"
            ),
            InlineKeyboardButton(
                text="✨ Support ✨", url=f"https://t.me/TeamTashri"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🧸 Add me in your group 🧸",
                url=f"https://t.me/{x.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❄️ Repo ❄️", url=f"https://github.com/Tashri2342/BOTSPAM"
            ),
            InlineKeyboardButton(
                text="☁️ Updates ☁️", url=f"https://t.me/Tashribots2342"
            ),
        ],
    ]
    return START_OP
