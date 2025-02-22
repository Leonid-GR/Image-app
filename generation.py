import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import token
from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def send_generate_button(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Сгенерировать случайное изображение", callback_data="generate_image"))
    keyboard = builder.as_markup()

    await message.reply("Нажмите кнопку, чтобы сгенерировать случайное изображение:", reply_markup=keyboard)


@dp.callback_query(lambda callback_query: callback_query.data == "generate_image")
async def generate_random_picture(callback_query: types.CallbackQuery):
    prompt = "случайный красивый пейзаж"
    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=image_url)
    await callback_query.answer()

@dp.callback_query(lambda callback_query: callback_query.data == "generate_image")
async def generate_picture(callback_query: types.CallbackQuery):
    prompt = "случайный красивый пейзаж"
    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=image_url)
    await callback_query.answer()

