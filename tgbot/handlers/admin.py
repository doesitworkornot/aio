from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole
import tgbot.handlers.kb as kb


import logging


log = logging.getLogger(__name__)



'''########################################
                States
########################################'''

class Admin_printer(StatesGroup):
    pages = State()
    confirm = State()


class Admin_adding_user(StatesGroup):
    user_id = State()
    user_name = State()
    user_role = State()
    confirm = State()



'''########################################
                Handlers
########################################'''

async def cancel(m: Message, state: FSMContext):
    log.info('canceled state %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await state.finish()
    await m.reply('Just removed your state. Now you are clean')


async def print_q(m: Message):
    log.info('starting print f() by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='How much copies you want to print?.', chat_id = m.message.chat.id)
    await Admin_printer.pages.set()


async def info(m: Message):
    log.info('getting info by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='You gonna recieve ur data.', chat_id = m.message.chat.id)


async def add_user(m: Message, state: FSMContext):
    log.info('adding user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('Resend to me message from new user. So i could recieve new user id. Or just send me new id.')
    await Admin_adding_user.user_id.set()


async def del_user(m: Message):
    log.info('deleting user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('U gonna delete user')


async def admin_start(m: Message):
    await m.reply('Hello, dear admin! What do you want? If u dont know so lets just start with /help', reply_markup=kb.inline_kb_full)


async def help_me(m: Message):
    await m.bot.send_message(text='Short explanation.\n \n That bot is about printing files on school printer. \n Command list: \n \n /help - now you are here \n /cancel - aborting any acton \n /state - is showing to you current state in ur chat \n /start - starting dialog \n /add - adding new user \n /del - deleting user', chat_id = m.chat.id)


async def show_current_state(m: Message, state: FSMContext):
    log.info('showing state to %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    currentState = await state.get_state()
    await m.answer(f"Current state is: {currentState}")



'''########################################
                Main Handler
########################################'''

def register_admin(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.ADMIN)
    dp.register_message_handler(show_current_state, commands=['state'],
                                state='*', role=UserRole.ADMIN)
    dp.register_message_handler(help_me, commands=['help'], state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(add_user, commands=['add'], state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(del_user, commands=['del'], state=None,
                                role=UserRole.ADMIN)
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.ADMIN)
    dp.register_message_handler(admin_start, state=None,
                                commands=['start'], role=UserRole.ADMIN)
