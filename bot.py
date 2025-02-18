import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа 
from aiogram.filters.command import Command   # обрабатываем команды /start, /help и другие

from dotenv import load_dotenv        # Для загрузки переменных из .env


# 2. Инициализация объектов
load_dotenv() # загружаем переменные из файла .env, в котором у нас содержится токен бота
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)                        # Создаем объект бота
dp = Dispatcher()                             # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"), 
        logging.StreamHandler()
    ]
)

logging.info("Бот запущен и логирование настроено.")


# 3. Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}! Ты запустил бота по транслитирации ФИО из кириллицы в латиницу! Отправь мне ФИО на кириллице!'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)


# 4 Задаем словарь для траслитирации, а также функцию для проверки введенного сообщения и дальнейшей транслитирации
translate_dict = {
    'А': 'A',  'Б': 'B',  'В': 'V',  'Г': 'G',  'Д': 'D',  'Е': 'E',  'Ё': 'E',
    'Ж': 'ZH', 'З': 'Z',  'И': 'I',  'Й': 'I',  'К': 'K',  'Л': 'L',  'М': 'M',
    'Н': 'N',  'О': 'O',  'П': 'P',  'Р': 'R',  'С': 'S',  'Т': 'T',  'У': 'U',
    'Ф': 'F',  'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'Sh', 'Щ': 'SHCH', 'Ъ': '',
    'Ы': 'Y',  'Ь': '',   'Э': 'E',  'Ю': 'Iu', 'Я': 'IA'
}
def is_valid_fio(text):
    return all('А' <= char.upper() <= 'Я' or char in ('Ё', 'ё', ' ') for char in text)

def transliterate(text: str) -> str:
    return ''.join(translate_dict.get(char.upper(), char) for char in text)


# 4. Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text 
    logging.info(f'Получено сообщение от {user_name} {user_id}: {text}')

    if not is_valid_fio(text):
        await message.answer("Dude!! Введи ФИО только русскими буквами.")
        return

    transliterated_text = transliterate(text)
    logging.info(f'Результат транслитерации: {transliterated_text}') 
    await message.answer(f"Твое имя латиницей: {transliterated_text}")



# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)