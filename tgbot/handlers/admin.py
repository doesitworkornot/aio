from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole
import tgbot.handlers.kb as kb


class Admin_states(StatesGroup):
    print = State()
    info = State()


async def cancel(m: Message, state: FSMContext):
    await state.finish()
    await m.reply('Just removed your state. Now you are clean')


async def print_q(m: Message):
    await m.bot.send_message(text='You gonna print smth.', chat_id = m.message.chat.id)
    await Admin_states.print.set()


async def info(m: Message):
    await m.bot.send_message(text='You gonna recieve ur data.', chat_id = m.message.chat.id)
    await Admin_states.info.set()


async def add_user(m: Message):
    await m.reply('U gonna add new user')


async def del_user(m: Message):
    await m.reply('U gonna delete user')


async def admin_start(m: Message):
    await m.reply('Hello, dear admin! What do you want? If u dont know so lets just start with /help', reply_markup=kb.inline_kb_full)


async def help_me(m: Message):
    await m.bot.send_message(text='Short explanation.\n \n That bot is about printing files on school printer. \n Command list: /help - now you are here \n /cancel - aborting any acton \n /state - is showing to you current state in ur chat \n /start - starting dialog', chat_id = m.message.chat.id)


async def show_current_state(m: Message, state: FSMContext):
    currentState = await state.get_state()
    await m.answer(f"Current state is: {currentState}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.ADMIN)
    dp.register_message_handler(help_me, commands=['help'], state='*',
                                role=UserRole.ADMIN)
    dp.register_message_handler(add_user, commands=['add'], state='*',
                                role=UserRole.ADMIN)
    dp.register_message_handler(del_user, commands=['del'], state='*',
                                role=UserRole.ADMIN)
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.ADMIN)
    dp.register_message_handler(show_current_state, commands=['state'],
                                state='*', role=UserRole.ADMIN)
    dp.register_message_handler(admin_start, state='*',
                                commands=['start'], role=UserRole.ADMIN)
