import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

from models import Problem, Topic
from utils import get_problems, get_random_problems

import os
from dotenv import load_dotenv

# load .env.dev file
load_dotenv(".env.dev")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance and get token from BotFather
bot = Bot(token=os.getenv("API_TOKEN"))

# Create a dispatcher instance
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Define states
class SearchForm(StatesGroup):
    difficulty = State()
    topic = State()

# Define command handlers
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the task search bot! Use /search to find tasks.")

@dp.message_handler(commands=['search'])
async def start_search(message: types.Message):
    await SearchForm.difficulty.set()
    await message.reply("Enter the difficulty (e.g. 800):")

@dp.message_handler(state=SearchForm.difficulty)
async def set_difficulty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['difficulty'] = message.text
    await SearchForm.next()
    await message.reply("Enter the topic:")

@dp.message_handler(state=SearchForm.topic)
async def set_topic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['topic'] = str(message.text).lower()

    # Query the database for tasks
    difficulty = data['difficulty']
    topic = data['topic']
    tasks = get_random_problems(topic=topic, difficulty=difficulty, limit=10)

    # If no tasks were found
    if not tasks:
        await message.reply("No tasks found. Try a different search.")

    # Send the list of tasks
    for task in tasks:
        task_text = f"<b>{task.name} ({task.number})</b>\n\n" \
                    f"Difficulty: {task.difficulty}\n" \
                    f"Topics: {[topic.name for topic in task.topics]}\n" \
                    f"Solutions: {task.solved_count}\n" \
                    f"Url: {task.url}\n"
        await message.reply(task_text, parse_mode=ParseMode.HTML)

    # Reset the state
    await state.finish()

# Define callback query handlers
@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    help_text = "Use /search to find tasks."
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, help_text)


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    