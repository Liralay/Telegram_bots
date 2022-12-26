from main import bot, dp

from aiogram.types import Message
from config import adminID

async def send_to_admin(dp):
    await bot.send_message(chat_id = adminID, text = "Bot launched") 

@dp.message_handler(commands=["start"])
async def start_message(message: Message):
    await message.answer("Привет. Этот бот поможет тебе найти картинки по твоему запросу \n Напиши любое слово и он найдет подходящую картинку")

@dp.message_handler()
async def echo(message: Message):
    user_query = message.text         #имеется запрос
    blok_list = user_query.split()                        #разбиваем слова по пробелам
    url_query = '%20'.join(blok_list)                     #разделяем их через %20
    text = f"https://yandex.ru/images/search?text={url_query}&lr=213"
    await message.answer(text=text)
