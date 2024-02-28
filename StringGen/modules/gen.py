import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from StringGen import Anony
from StringGen.utils import retry_key


async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"- تــيرمــكس"
    elif old_pyro:
        ty = f"- بــايروجــرامــ¹"
    else:
        ty = f"- بــايروجــرامــ²"

    await message.reply_text(f"☜ <b>جــاري اســتــخــراج جــلــســة</b> {ty}<b>بــواســطــة</b> @QYTHON")

    try:
        api_id = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="☜ <b>ارســل الــايبــي ايدي الــخــاص بــك لــلــرجــوع ارســل</b> /menu",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» ☜ <b>لــقــد نــفــذت مــدة اســتــخــراج الــجــلــســة </b>\n\n <b>يرجــى اعــادة بــدء الــاســتــخــراج مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    if await cancelled(api_id):
        return

    try:
        api_id = int(api_id.text)
    except ValueError:
        return await Anony.send_message(
            user_id,
            "☜ <b>الــايبــي ايدي الــذي ارســلــتــه غــير صــالــح</b> \n\n <b>يرجــي اعــادة اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    try:
        api_hash = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="☜ <b>ارســل الــان الــايبــي هاش الــخــاص بــك</b>",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "☜ <b>لــقــد نــفــذت مــدة اســتــخــراج الــجــلــســة </b>\n\n <b>يرجــى اعــادة بــدء الــاســتــخــراج مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    if await cancelled(api_hash):
        return

    api_hash = api_hash.text

    if len(api_hash) < 30:
        return await Anony.send_message(
            user_id,
            "☜ <b>الــايبــي هاش الــذي ارســلــتــه غــير صــالــح</b> \n\n <b>يرجــي اعــادة اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    try:
        phone_number = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="☜ <b>ارســل رقــم هاتــفــك مــع رمــز الــدولــة</b> \n\n <b>مــثــال</b>📱: +201253128651",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "☜ <b>لــقــد نــفــذت مــدة اســتــخــراج الــجــلــســة </b>\n\n <b>يرجــى اعــادة بــدء الــاســتــخــراج مــرة أخــرى</b>.",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await Anony.send_message(user_id, "<b>☜ جــاري ارســال الــكود الــي حــســابــك ...</b> ")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="Anony", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await Anony.send_message(
            user_id,
            f"☜ <b>فــشــل ارســال رمــز تــســجــيل الــدخــول يرجــي الــانــتــظــار لــمــدة</b> {f.value or f.x} <b>ثــانــية و اعــادة الــمــحــاولــة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await Anony.send_message(
            user_id,
            "<b>☜الــايبــي ايدي او الــايبــي هاش غــير صــالــحــان</b> \n\n <b>يرجــى اعــادة بــدأ اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await Anony.send_message(
            user_id,
            "☜ <b>رقــم الــهاتــف الــذي ارســلــتــه غــير صــالــح </b>\n\n <b>يرجــي اعــادة اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    try:
        otp = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"☜ <a href='https://telegra.ph/file/07ada278df6c6c11efb49.jpg'>ارســل كود الــتــحــقــق كمــا بــالــصــورة</a> \n\n مــثــل هكذا : 7 5 9 5 3 ✅ \n\n ولــيس هكذا : 35957 ❌ \n\n بــين كل رقــم فــراغ (مــســافــة)",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "☜ <b>لــقــد نــفــذت مــدة اســتــخــراج الــجــلــســة </b>\n\n <b>يرجــى اعــادة بــدء الــاســتــخــراج مــرة أخــرى</b>",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await Anony.send_message(
            user_id,
            "☜ <b>رمــز الــتــحــقــق الــذي ارســلــتــه غــير صــحــيح</b> \n\n <b>اعــد اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await Anony.send_message(
            user_id,
            "☜ <b>رمــز الــتــحــقــق الــذي ارســلــتــه مــنــتــهي الــصــلــاحــية</b> \n\n <b>اعــد اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await Anony.ask(
                identifier=(message.chat.id, user_id, None),
                text="☜ <b>ادخــل كلــمــة ســر الــتــحــقــق بــخــطــوتــين</b>",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return Anony.send_message(
                user_id,
                "☜ <b>لــقــد نــفــذت مــدة اســتــخــراج الــجــلــســة </b>\n\n <b>يرجــى اعــادة بــدء الــاســتــخــراج مــرة أخــرى</b>",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await Anony.send_message(
                user_id,
                "☜ <b>كلــمــة ســر الــتــحــقــق بــخــطــوتــين الــتــي ارســلــتــها غــير صــحــيحــة</b> \n\n <b>يرجــى اعــادة اســتــخــراج الــجــلــســة مــرة أخــرى</b>",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await Anony.send_message(user_id, f"ᴇʀʀᴏʀ : <code>{str(ex)}</code>")

    try:
        txt = "✓ تــم اســتــخــراج كود جــلــســة {0} بــنــجــاح \n\n <code>{1}</code> \n\n بــواســطــة⤈\n\n𝙱𝙾𝚃:- @session4bot \n\n 𝙲𝙷:- @QYTHON \n\n 𝙳𝙴𝚅:- @HO888 "
        if telethon:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html",
            )
            await client(JoinChannelRequest("@QYTHON"))
        else:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                disable_web_page_preview=True,
            )
            await client.join_chat("QYTHON")
    except KeyError:
        pass
    try:
        await client.disconnect()
        await Anony.send_message(
            chat_id=user_id,
            text=f"✓ تــم بــنــجــاح اســتــخــراج كود {ty} الــخــاص بــك \n تــحــقــق مــنــه فــي الــرســائل الــمــحــفــوظــة \n بــواســطــة <a href={SUPPORT_CHAT}>𝑞𝑦𝑡ℎ𝑜𝑛</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="• الــرســائل الــمــحــفــوظــة",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "☜ <b>تــم الــغــاء عــمــلــية الــاســتــخــراج بــنــجــاح</b>", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "☜ <b>تــمــت اعــادة تــشــغــيل الــبــوت بــنــجــاح</b>", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "☜ <b>تــم الــغــاء عــمــلــية الــاســتــخــراج بــنــجــاح</b>", reply_markup=retry_key
        )
        return True
    else:
        return False
