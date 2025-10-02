import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, Router,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand, FSInputFile
from audio import ovoz

API = "8492831992:AAGJ22wSYHBMadwK7nXpqPsdJ6Zauemkhxs"
dp = Dispatcher()

router=Router()

dp.include_router(router)
async def default(bot:Bot):
    commands=[
        BotCommand(command="start",description="Start the bot"),
        BotCommand(command="help",description="Get help"),
        BotCommand(command="about",description="About the bot"),
    ]
    await bot.set_my_commands(commands=commands)

@dp.message(Command(commands="help"))
async def help_cmd(message: Message):
    await message.answer(
        "📖 Men siz yozgan matnni o‘zbek tilida ovozga aylantirib beraman.\n\n"
        "👉 /start - Boshlash va ovoz tanlash\n"
        "👉 /help - Yordam\n\n"
        "Yordam uchun: @itlive_09")

@dp.message(Command(commands="about"))
async def help_cmd(message: Message):
    await message.answer(
        "📖 Men siz yozgan matnni o‘zbek tilida ovozga aylantirib beraman.\n\n"
        "👉 /start - Boshlash va ovoz tanlash\n"
        "👉 /help - Yordam\n\n"
        "Yordam uchun: @itlive_09")

user={}
menu=["👨 Erkak ovoz  🇺🇿", "👩 Ayol ovoz  🇺🇿","Ahmet 🇹🇷","EmelNeural 🇹🇷","Dmitry 🇷🇺","Svetlana 🇷🇺","Dariya 🇷🇺","Neural 🇺🇸","Jenny 🇺🇸","Ryan 🇺🇸","Sonia 🇺🇸"]
Menu=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=menu[0]),KeyboardButton(text=menu[1])],
    [KeyboardButton(text=menu[2]),KeyboardButton(text=menu[3])],
    [KeyboardButton(text=menu[4]),KeyboardButton(text=menu[5]),KeyboardButton(text=menu[6])],
    [KeyboardButton(text=menu[7]),KeyboardButton(text=menu[8])],
    [KeyboardButton(text=menu[9]),KeyboardButton(text=menu[10])]
],resize_keyboard=True,one_time_keyboard=True)


@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer(f"""Assalomu allekum, {message.from_user.full_name}!
Matn yuboring, men uni o‘zbek tilida ovoz qilib beraman.
👉 Iltimos, ovoz turini tanlang:
""",reply_markup=Menu)

@dp.message(F.text.in_(menu))
async def choose_voice(message: Message):
    T = message.text
    if T in menu:
        if T==menu[0]:
            user[message.from_user.id] = "uz-UZ-SardorNeural"
            await message.answer("✅ Erkak ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[1]:
            user[message.from_user.id] = "uz-UZ-MadinaNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[2]:
            user[message.from_user.id] = "tr-TR-AhmetNeural"
            await message.answer("✅ Erkak ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[3]:
            user[message.from_user.id] = "tr-TR-EmelNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[4]:
            user[message.from_user.id] = "ru-RU-DmitryNeural"
            await message.answer("✅ Erkak ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[5]:
            user[message.from_user.id] = "ru-RU-SvetlanaNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[6]:
            user[message.from_user.id] = "ru-RU-DariyaNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[7]:
            user[message.from_user.id] = "en-US-GuyNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[8]:
            user[message.from_user.id] = "en-US-JennyNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[9]:
            user[message.from_user.id] = "en-GB-RyanNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")
        elif T==menu[10]:
            user[message.from_user.id] = "en-GB-SoniaNeural"
            await message.answer("✅ Ayol ovoz tanlandi! Endi matn yuboring.")



@dp.message()
async def message_handler(message: Message):
    try:
        if message.from_user.id not in user:
           await message.answer("⚠️ Avval ovoz tanlang: /start")
           return
        voice = user[message.from_user.id]
        text = message.text.strip()

        if not text:
            await message.answer("⚠️ Bo‘sh matn yuborib bo‘lmaydi.")
            return
        filename = f"audio_{message.chat.id}_{message.message_id}.mp3"

        await ovoz(text, filename, voice)

        audio = FSInputFile(filename)
        await message.answer_voice(audio, caption="🔊 Mana Tayor ✔")
    except Exception as e:
            logging.error(f"Xatolik: {e}")
            await message.answer("❌ Xatolik yuz berdi, qaytadan urinib ko‘ring.")
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                logging.warning(f"⚠️ Faylni o‘chirishda muammo: {e}")


async def main():
    logging.info("✅ Bot ishga tushyapti...")
    bot = Bot(token=API,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await default(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)
    asyncio.run(main())
