Нужно создать в корне файл .env с содержимым:
BOT_TOKEN = ВАШ_ТОКЕН

Указать свои почту, либо телеграмм в переменной admin в файле /modules/messages.py

Создать виртуальное окружение командой:
python -m venv env

Активировать виртуальное окружение командой:
env\Scripts\activate

Установить зависимости:
python -m pip install -r requirements.txt

Запустить бота командой:
python bot.py