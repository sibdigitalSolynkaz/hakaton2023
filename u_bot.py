from difflib import SequenceMatcher

from config import TOKEN
import json
import datetime
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Чтение файла с ответами
with open("answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

# Создание бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот. Спроси меня что-нибудь!")


# Обработчик всех остальных сообщений
@dp.message_handler()
async def answer_question(message: types.Message):
    # Извлечение всех вопросов и ответов из JSON-файла
    all_questions = list(answers.keys())
    all_answers = list(answers.values())

    # Поиск наиболее подходящего вопроса
    best_question = None
    best_answer = None
    best_similarity = 0
    for i in range(len(all_questions)):
        similarity = similar(message.text.lower(), all_questions[i].lower())
        if similarity > best_similarity:
            best_similarity = similarity
            best_question = all_questions[i]
            best_answer = all_answers[i]

    # Если наиболее подходящий вопрос найден, отправляем соответствующий ответ
    if best_question is not None and best_similarity > 0.6:
        # Замена переменной {дата} на текущую дату
        answer = best_answer.replace("{дата}", datetime.date.today().strftime("%d.%m.%Y"))
        await message.answer(answer)
    else:
        await message.answer("Переформулируйте вопрос, пожалуйста.")


# Функция для вычисления коэффициента сходства двух строк
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Запуск бота
if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
