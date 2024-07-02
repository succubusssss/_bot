import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from json import load
from modules.data_comp import data_comp
import modules.messages as msg
from modules.parser_excel import parser_excel

# Токен бота можно получить с помощью https://t.me/BotFather
bot_token = getenv("BOT_TOKEN")

# Все обработчики должны быть подключены к Router (или Dispatcher)
dp = Dispatcher()


# Загрузка файла json
def get_json(output_file):
    try:
        with open(output_file, "r", encoding="utf8") as file:
            return load(file)
    except:
        return parser_excel("./data/specialties.xlsx", "./data/spec.json")


json_data = get_json("./data/spec.json")


@dp.message(Command("start", "help", "data_update"))
async def command_start_handler(message: Message) -> None:
    """
    Этот обработчик получает сообщения с `/start` command
    """
    # Большинство объектов event имеют псевдонимы для методов API, которые могут быть вызваны в контексте событий
    # Например, если вы хотите ответить на входящее сообщение, вы можете использовать псевдоним "message.answer(...)"
    # и целевой чат будет передан в :ref:`aiogram.methods.send_message.SendMessage`
    # метод автоматически или вызвать метод API напрямую через
    # Экземпляр бота: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"{msg.answer(message.text)}")


@dp.message()
@dp.edited_message()
async def echo_handler(message: types.Message) -> None:
    """
    Обработчик переадресует полученное сообщение обратно отправителю

    По умолчанию обработчик сообщений будет обрабатывать все типы сообщений (например, текст, фотографию, наклейку и т.д.).
    """

    string = message.text
    input_text = data_comp(string, json_data)
    output_text = msg.answer(input_text)

    try:
        await message.answer(f"{output_text}", 
        parse_mode=ParseMode.HTML)
    except TypeError:
        # Но не все типы поддерживаются для копирования, поэтому нужно разобраться с этим
        await message.answer("Что-то пошло не так")


async def main() -> None:
    # Инициализируйте экземпляр бота режимом синтаксического анализа по умолчанию, который будет передаваться всем вызовам API
    # bot = Bot(TOKEN)
    bot = Bot(bot_token)
    # И диспетчеризация событий запуска
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
