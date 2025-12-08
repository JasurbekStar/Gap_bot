import asyncio
import logging
import os
import sys
import edge_tts

from aiogram import Bot, Dispatcher, Router, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand, FSInputFile

API = "8492831992:AAGO4Z3FYGER39ppw6-VRRny8ztxSAVwEEo"


dp = Dispatcher()
router = Router()
dp.include_router(router)

async def default(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="about", description="About the bot"),
    ]
    await bot.set_my_commands(commands=commands)


async def ovoz(matn, filename="output.mp3", voice="uz-UZ-MadinaNeural"):
    max_len = 300
    chunks = [matn[i:i + max_len] for i in range(0, len(matn), max_len)]
    tts = edge_tts.Communicate("", voice)
    temp_files = []
    for i, chunk in enumerate(chunks):
        temp_name = f"chunk_{i}.mp3"
        tts = edge_tts.Communicate(chunk, voice)
        await tts.save(temp_name)
        temp_files.append(temp_name)

    with open(filename, "wb") as out_f:
        for t in temp_files:
            with open(t, "rb") as f:
                out_f.write(f.read())
            os.remove(t)

    return filename


@dp.message(Command(commands=["help"]))
async def help_cmd(message: Message):
    await message.answer(
        "📖 Men siz yozgan matnni o‘zbek tilida ovozga aylantirib beraman.\n\n"
        "👉 /start - Boshlash va ovoz tanlash\n"
        "👉 /help - Yordam\n\n"
        "Yordam uchun: @itlive_09"
    )


@dp.message(Command(commands=["about"]))
async def about(message: Message):
    await message.answer(
        "🤖 Ushbu bot `edge_tts` yordamida turli tillarda ovoz hosil qiladi.\n\n"
        "Muallif: @itlive_09\n"
        "Til va ovozlarni tanlang, matn yuboring va tayyor audioni oling 🎧"
    )


user = {}

menu = [
    "👨‍🦰 Sardor 🇺🇿",
    "👩 Madina 🇺🇿",
    "👨‍🦱 Ahmet 🇹🇷",
    "👩 Emel 🇹🇷",
    "👨‍🦰 Dmitry 🇷🇺",
    "👩 Svetlana 🇷🇺",
    "👩‍🦰 Dariya 🇷🇺",
    "🤖 Neural 🇺🇸",
    "👩 Jenny 🇺🇸",
    "👨 Ryan 🇺🇸",
    "👩 Sonia 🇺🇸",
    "👩 Emma 🇬🇧",
    "👨 Brian 🇬🇧",
    "👨‍🦱 Hamed 🇸🇦",
    "👩‍🦱 Zariyah 🇸🇦"
]

Menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=menu[0]), KeyboardButton(text=menu[1])],
        [KeyboardButton(text=menu[2]), KeyboardButton(text=menu[3])],
        [KeyboardButton(text=menu[4]), KeyboardButton(text=menu[5]), KeyboardButton(text=menu[6])],
        [KeyboardButton(text=menu[7]), KeyboardButton(text=menu[8])],
        [KeyboardButton(text=menu[9]), KeyboardButton(text=menu[10])],
        [KeyboardButton(text=menu[11]), KeyboardButton(text=menu[12])],
        [KeyboardButton(text=menu[13]), KeyboardButton(text=menu[14])]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer(
        f"Assalomu alaykum,  {html.bold(message.from_user.full_name)}!\n"
        "Men siz yozgan matnni ovozga aylantiraman.\n"
        "👉 Iltimos, ovoz turini tanlang:",
        reply_markup=Menu
    )

mapping = {
    menu[0]: "uz-UZ-SardorNeural",
    menu[1]: "uz-UZ-MadinaNeural",
    menu[2]: "tr-TR-AhmetNeural",
    menu[3]: "tr-TR-EmelNeural",
    menu[4]: "ru-RU-DmitryNeural",
    menu[5]: "ru-RU-SvetlanaNeural",
    menu[6]: "ru-RU-DariyaNeural",
    menu[7]: "en-US-GuyNeural",
    menu[8]: "en-US-JennyNeural",
    menu[9]: "en-US-RyanNeural",
    menu[10]: "en-US-SoniaNeural",
    menu[11]: "en-GB-EmmaNeural",
    menu[12]: "en-GB-BrianNeural",
    menu[13]: "ar-SA-HamedNeural",
    menu[14]: "ar-SA-ZariyahNeural"
}

voice_gender = {
    menu[0]: "🧔 Erkak ovoz tanlandi (Sardor 🇺🇿)",
    menu[1]: "👩 Ayol ovoz tanlandi (Madina 🇺🇿)",
    menu[2]: "🧔 Erkak ovoz tanlandi (Ahmet 🇹🇷)",
    menu[3]: "👩 Ayol ovoz tanlandi (Emel 🇹🇷)",
    menu[4]: "🧔 Erkak ovoz tanlandi (Dmitry 🇷🇺)",
    menu[5]: "👩 Ayol ovoz tanlandi (Svetlana 🇷🇺)",
    menu[6]: "👩 Ayol ovoz tanlandi (Dariya 🇷🇺)",
    menu[7]: "🧔 Erkak ovoz tanlandi (Neural 🇺🇸)",
    menu[8]: "👩 Ayol ovoz tanlandi (Jenny 🇺🇸)",
    menu[9]: "🧔 Erkak ovoz tanlandi (Ryan 🇺🇸)",
    menu[10]: "👩 Ayol ovoz tanlandi (Sonia 🇺🇸)",
    menu[11]: "👩 Ayol ovoz tanlandi (Emma 🇬🇧)",
    menu[12]: "🧔 Erkak ovoz tanlandi (Brian 🇬🇧)",
    menu[13]: "🧔 Erkak ovoz tanlandi (Hamed 🇸🇦)",
    menu[14]: "👩 Ayol ovoz tanlandi (Zariyah 🇸🇦)"
}


@dp.message(F.text.in_(menu))
async def choose_voice(message: Message):
    T = message.text
    voice = mapping.get(T)
    if voice:
        user[message.from_user.id] = voice
        gender_text = voice_gender.get(T, "🔊 Ovoz tanlandi!")
        await message.answer(f"✅ {gender_text}\nEndi matn yuboring.")

@dp.message()
async def message_handler(message: Message):
    try:
        if message.from_user.id not in user:
            await message.answer("⚠️ Avval ovoz tanlang: /start")
            return

        text = message.text.strip()
        if not text:
            await message.answer("⚠️ Bo‘sh matn yuborib bo‘lmaydi.")
            return

        voice = user[message.from_user.id]
        filename = f"audio_{message.chat.id}_{message.message_id}.mp3"

        await ovoz(text, filename, voice)
        audio = FSInputFile(filename)
        await message.answer_voice(audio, caption="🔊 Tayyor! ✅")

    except Exception as e:
        logging.error(f"❌ Xatolik: {e}")
        await message.answer("❌ Xatolik yuz berdi, qayta urinib ko‘ring.")
    finally:
        if os.path.exists(filename):
            os.remove(filename)


async def main():
    logging.info("✅ Bot ishga tushmoqda...")
    bot = Bot(token=API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await default(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

