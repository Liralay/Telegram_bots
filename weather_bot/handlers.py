from main import bot, dp
from config import adminID, WEATHER_ТOKEN
from client_keyboard import kb_client
from states import is_city_name_given

from aiogram.types import Message
from aiogram.dispatcher import FSMContext


import logging 
import time
import requests
import json


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


async def send_to_admin(dp):
    await bot.send_message(chat_id = adminID, text = "Bot launched") 


@dp.message_handler(commands=["start"], state="*")
async def start_message(message: Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await is_city_name_given.programm_started.set()
    #do not use f-string on logging
    logger.info('User %s, %s, wrote at %s', message.from_user.id,message.from_user.full_name,time.asctime())
    await message.answer (f"Привет, {user_full_name}! \nЯ помогу узнать текущий прогноз погоды в любом городе планеты", reply_markup=kb_client)
    logger.info("start_message function is done working")


@dp.message_handler(commands=["help"], state="*")
async def get_help(message: Message):
    await message.answer("Доступные команды:\n\
/help - все команды бота\n\
/change_city - изменить текущий город\n\
/my_city - узнать текущий город\n\
/get_weather - узнать погоду в указанном городе")
    logger.info("get_help function is done working")


@dp.message_handler(commands=["change_city"], state="*")
async def change_city(message: Message, state: FSMContext):
    await is_city_name_given.getting_city_name.set()
    logger.info("state changed to " +  await state.get_state())
    await message.answer("Введите полное название города\nНапример: Москва")
    logger.info("change_city function is done working")


@dp.message_handler(state=is_city_name_given.getting_city_name)
async def user_city_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["city_name"] = message.text
    await message.answer(f'Ваш город установлен на {data["city_name"]}')
    await is_city_name_given.city_name_given.set()
    logger.info("user_city_name function is done working")


@dp.message_handler(commands=["my_city"], state="*")
async def tell_city_name (message: Message, state: FSMContext):
    data = await state.get_data()
    city_name = data.get("city_name")
    if city_name != None:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_ТOKEN}&lang=ru&units=metric")
        data_r = r.json()
        city = data_r["name"]
        await message.answer (f"Ваш город: {city}")
    else:
        await message.answer ("Я еще не знаю ваш город. \nНапишите /change_city для того, чтобы установить город")
    logger.info("tell_city_name function is done working")


@dp.message_handler(commands=["get_weather"], state="*")
async def get_weather (message: Message, state: FSMContext):
    if await state.get_state() == "is_city_name_given:city_name_given":
        logger.info(f"state is {await state.get_state()}")
        data = await state.get_data()
        city_name = str(data.get("city_name"))
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_ТOKEN}&lang=ru&units=metric")
        data_r = r.json()
        city = data_r["name"]
        condition = data_r["weather"][0]["description"]
        temp = data_r["main"]["temp"]
        await message.answer(f"Сейчас в городе {city} {condition}, {int(temp)}°C")
    else:
        await message.answer ("Я еще не знаю ваш город. \nНапишите /change_city для того, чтобы установить город")
    logger.info("get_weather function is done working")

