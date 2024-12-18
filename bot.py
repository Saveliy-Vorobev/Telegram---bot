import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа 
from aiogram.filters.command import Command   # обрабатываем команды /start

# Инициализация объектов
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)                        # Создаем объект бота
dp = Dispatcher()                             # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Задаем словарь для транслитерации
translate_dict = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh',
    'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
    'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
    'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ы': 'Y', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    'Ь': '', 'Ъ': 'IE', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
    'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e',
    'ю': 'yu', 'я': 'ya', 'ь': '', 'ъ': 'IE'
}

# Функция для транслитерации
def transliterate(text):
    return ''.join(translate_dict.get(char, char) for char in text)

# Функция для проверки формата введенного сообщения
def is_valid_fio(text):
    if len(text.split()) != 3:
        return False
    for word in text.split():
        if not word.isalpha() or not word[0].isupper() or not word[1:].islower():
            return False
    return True


# Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}! Я крутой бот! Отправь мне ФИО на кириллице, и я переведу его на латиницу.'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)
    
# Обработка/Хэндлер сообщений с ФИО
@dp.message()
async def transliteration(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text 
    if is_valid_fio(text):
        transliterated_text = transliterate(text)
        logging.info(f'{user_name} ({user_id}): {text} -> {transliterated_text}')
        await message.answer(text=transliterated_text)
    else:
        logging.warning(f'{user_name} ({user_id}) отправил некорректное сообщение: {text}')
        await message.answer(text='Йоу! Ты отправил сообщение не в корректном формате, отправьте ФИО в формате "Фамилия Имя Отчество" на кириллице. Например: Иванов Иван Иванович.')


# Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)