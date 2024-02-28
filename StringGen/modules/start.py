from pyrogram import filters
from pyrogram.types import Message

from StringGen import Anony
from StringGen.utils import add_served_user, keyboard


@Anony.on_message(filters.command("start") & filters.private & filters.incoming)
async def f_start(_, message: Message):
    await message.reply_text(
        text=f"👋 : <b>مــرحــبــا عــزيزي</b> {message.from_user.first_name} \n\n فــي {Anony.mention} \n\n - <b>لــلــبــدأ اضــغــط « - بــدء اســتــخــراج الــجــلــســة • »</b>\n\n <b>الــمــطــور :-</b> <a href='https://t.me/HO888'>〝 𝒂𝒎𝒈𝒆𝒅 𝒔𝒉𝒐𝒌𝒓𝒂𝒍𝒍𝒂𝒉 〞</a>",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await add_served_user(message.from_user.id)
