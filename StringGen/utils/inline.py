from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="- بــدء اســتــخــراج الــجــلــســة •", callback_data="gensession")],
        [
            InlineKeyboardButton(text="- كايثــون •", url=SUPPORT_CHAT),
            InlineKeyboardButton(
                text="- الــمــطــور •", url="https://t.me/HO888"
            ),
        ],
    ]
)

gen_key = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="- بــايروجــرامــ¹", callback_data="pyrogram1"),
            InlineKeyboardButton(text="- بــايروجــرامــ²", callback_data="pyrogram"),
        ],
        [InlineKeyboardButton(text="- تــيرمــكس", callback_data="telethon")],
    ]
)

retry_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="اعــد الــمــحــاولــة", callback_data="gensession")]]
)
