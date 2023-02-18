import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils import executor
from config import TOKEN
from transformers import pipeline

import torch
from transformers import BertForQuestionAnswering, BertTokenizer, pipeline

# инициализируем токенизатор и модель BERT для поиска ответов на вопросы
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# инициализируем логирование
logging.basicConfig(level=logging.INFO)

# инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
#dp = Dispatcher(bot)
#bot = Bot(token=os.environ['5566139697:AAHmjMaNbmiNiwzaqAvhFTEtt1vPamH8L9k'])
dp = Dispatcher(bot, storage=MemoryStorage())


# обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await message.answer("Привет! Я готов отвечать на твои вопросы. Напиши мне что-нибудь, и я постараюсь помочь.")


# обработчик текстовых сообщений
@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message, state: FSMContext):
    question = message.text  # получаем вопрос от пользователя
    answer = find_answer(question)  # ищем ответ на вопрос в пуле
    await message.answer(answer, parse_mode=ParseMode.HTML)


# функция для поиска ответа на вопрос в пуле
def find_answer(question):
    nlp = pipeline("question-answering")
    result = nlp({
        "question": question,
        "context": "Если вы стали победителем Всероссийского конкурса молодежных инициатив среди физических лиц (вышел приказ и в разделе «Мои заявки» сменился статус заявки), то в грантовом модуле ФГАИС Молодёжь России вам стал доступен раздел для заключения соглашения. Для того чтобы начать процесс заключения соглашения, необходимо пройти в обозначенный выше раздел и нажать «Начать заключение договора».1 шаг — это изменение проекта. После изменения проекта необходимо сохранить изменения ( проект сохраниться только тогда, когда в проекте будет корректная сумма) 2 шаг — это внесение информации о вас. После заполнения всех полей, необходимо сохранить данные и отправить на проверку.После проверки вам будет либо согласованы вкладки, либо придут комментарии от куратора по тем изменениям, которые необходимо внести.После согласования вкладки Проект и вкладки Данные, начнется процесс регистрации проекта соглашения в ГИИС «Электронный бюджет», после окончания данного процесса у вас сменится статус и станет доступно подписание.Обращаем внимание, что подписание будет доступно только с верифицированного аккаунта. Последовательность подписания: Проект — Данные — Приложения(все) — Соглашение По техническим вопросам обращаться на почту"
    })
    #print(result)
    # преобразуем вопрос в векторное представление
    #input_ids = tokenizer.encode(question, return_tensors='pt')
    # используем модель BERT для поиска ответа на вопрос в пуле
    #start_scores, end_scores = model(input_ids)
    #start_index = torch.argmax(start_scores)
    #end_index = torch.argmax(end_scores)
    #answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][start_index:end_index+1]))
    return result


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
'''
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await  bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)
'''