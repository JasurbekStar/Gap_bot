import asyncio
import logging
import sys
import os
import edge_tts
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API")
dp = Dispatcher()
user = {}

def ta2(m):
    return [m[i:i + 2] for i in range(0, len(m), 2)]

async def ovoz(matn, filename="output.mp3", voice="uz-UZ-MadinaNeural"):
    max_len = 300
    chunks = [matn[i:i + max_len] for i in range(0, len(matn), max_len)]
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_name = f"chunk_{i}_{filename}"
        tts = edge_tts.Communicate(chunk, voice)
        await tts.save(temp_name)
        temp_files.append(temp_name)

    with open(filename, "wb") as out_f:
        for t in temp_files:
            with open(t, "rb") as f:
                out_f.write(f.read())
            os.remove(t)
    return filename

menu = {
    "👨‍🦰 Sardor 🇺🇿": "uz-UZ-SardorNeural",
    "👩 Madina 🇺🇿": "uz-UZ-MadinaNeural",
    "👨‍🦱 Ahmet 🇹🇷": "tr-TR-AhmetNeural",
    "👩 Emel 🇹🇷": "tr-TR-EmelNeural",
    "👨‍🦰 Dmitry 🇷🇺": "ru-RU-DmitryNeural",
    "👩 Svetlana 🇷🇺": "ru-RU-SvetlanaNeural",
    "👩‍🦰 Dariya 🇷🇺": "ru-RU-DariyaNeural",
    "🤖 Neural 🇺🇸": "en-US-GuyNeural",
    "👨 Andrew 🇺🇸": "en-US-AndrewNeural",
    "👨 Brian 🇺🇸": "en-US-BrianNeural",
    "👨 Eric 🇺🇸": "en-US-EricNeural",
    "👨 Roger 🇺🇸": "en-US-RogerNeural",
    "👨 Steffan 🇺🇸": "en-US-SteffanNeural",
    "👨 Christopher 🇺🇸": "en-US-ChristopherNeural",
    "👩 Ava 🇺🇸": "en-US-AvaNeural",
    "👩 Emma 🇺🇸": "en-US-EmmaNeural",
    "👩 Jenny 🇺🇸": "en-US-JennyNeural",
    "👩 Michelle 🇺🇸": "en-US-MichelleNeural",
    "👩 Aria 🇺🇸": "en-US-AriaNeural",
    "👩 Ana 🇺🇸": "en-US-AnaNeural",
    "👨 Ryan 🇬🇧": "en-GB-RyanNeural",
    "👩 Sonia 🇬🇧": "en-GB-SoniaNeural",
    "👨 Brian 🇬🇧": "en-GB-BrianNeural",
    "👨‍🦱 Hamed 🇸🇦": "ar-SA-HamedNeural",
    "👩‍🦱 Zariyah 🇸🇦": "ar-SA-ZariyahNeural"
}

buttons = [KeyboardButton(text=key) for key in menu.keys()]
Menu = ReplyKeyboardMarkup(keyboard=ta2(buttons), resize_keyboard=True)

async def defoult(bot: Bot):
    command = [
        BotCommand(command='start', description='Boshlash uchun..'),
        BotCommand(command='help', description='Yordam kerakmi?'),
        BotCommand(command='about', description='Biz haqimizda!')
    ]
    await bot.set_my_commands(command)

@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!", reply_markup=Menu)

@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\nSizga qanday yordam kerak\nMurojat uchun @itlive_09")

@dp.message(Command('about'))
async def command_about_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\nGapiradigan bot\nMatin➡️Ovoz")

@dp.message(F.text.in_(menu))
async def choose_voice(message: Message):
    T = message.text
    voice_name = menu[T]
    user[message.from_user.id] = voice_name
    if "👨" in T or "🤖" in T:
        gender_emoji = "🧔 Erkak"
    elif "👩" in T:
        gender_emoji = "👩 Ayol"
    else:
        gender_emoji = "👤 Foydalanuvchi"
    await message.answer(f"✅ {gender_emoji} ovoz tanlandi ({T})\nEndi matn yuboring.")

@dp.message()
async def message_handler(message: Message):
    filename = None
    try:
        if message.from_user.id not in user:
            await message.answer("⚠️ Avval ovoz tanlang: /start")
            return
        text = message.text.strip()
        if not text:
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
        if filename and os.path.exists(filename):
            os.remove(filename)

async def main() -> None:
    bot = Bot(token=API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await defoult(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
