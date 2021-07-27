from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole
import tgbot.handlers.kb as kb


class User_states(StatesGroup):
    print = State()
    info = State()


async def user_start(m: Message):
    await m.reply('Hello, dear user! What do you want? Something usuall? Or want to get some mental support via /help', reply_markup=kb.inline_kb_full)


async def help_me(m: Message):
    await m.bot.send_message(text='Hello, User. This bot is about printing files on school printer \n Default commands: \n /start - starting main dialog \n /help - now you are here \n /cancel - nullification of your dialog state', chat_id = m.message.chat.id)



async def cancel(m: Message, state: FSMContext):
    await state.finish()
    await m.reply('Just removed your state. Now you are clean')


async def print_q(m: Message):
    await m.bot.send_message(text='You gonna print smth.', chat_id = m.message.chat.id)
    await User_states.print.set()


async def info(m: Message):
    await m.bot.send_message(text='You gonna recieve ur data.', chat_id = m.message.chat.id)
    await User_states.info.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.USER)
    dp.register_message_handler(help_me, commands=['help'], state='*',
                                role=UserRole.USER)
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.USER)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.USER)
    dp.register_message_handler(user_start, state='*',
                                commands=['start'], role=UserRole.USER)
