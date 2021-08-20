from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
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


class Admin_del_user(StatesGroup):
    user_id = State()
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
    await m.bot.send_message(text='How much copies you want to print?.', chat_id=m.message.chat.id)
    await Admin_printer.pages.set()


async def info(m: Message):
    log.info('getting info by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='You gonna recieve ur data.', chat_id=m.message.chat.id)


async def add_user(m: Message, state: FSMContext):
    log.info('adding user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('Resend to me message from new user. So i could recieve new user id. Or just send me new id.')
    await Admin_adding_user.user_id.set()


async def new_user_id(m: Message, state: FSMContext):
    if m.forward_from != None:
        new_id = m.forward_from.id
        await  state.update_data(new_id=new_id)
        await m.bot.send_message(text=f'You gonna add user wit id: {new_id}. Send me user name', chat_id=m.chat.id)
        await Admin_adding_user.user_name.set()
    elif m.text.isdigit():
        new_id = m.text
        if int(new_id) <= 2000000000 and int(new_id) >=1:
            await  state.update_data(new_id=new_id)
            await m.bot.send_message(text=f'You gonna add user wit id: {new_id}. Send me user name', chat_id=m.chat.id)
            await Admin_adding_user.user_name.set()
        else:
            await m.bot.send_message(text='You failed. Try again. This number is way too big or could be negative', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='You failed. Try again. Or new user could set private forwarded message in settings, so ask him to send you his id', chat_id=m.chat.id)


async def new_user_name(m: Message, state: FSMContext):
    new_name = m.text
    await state.update_data(new_name=new_name)
    await m.bot.send_message(text='Its pretty isnt it? Next step is new users status. Rate it 1 or 2, where 1 is common user and 2 is powerfull admin', chat_id=m.chat.id)
    await Admin_adding_user.user_role.set()


async def new_user_role(m: Message, state: FSMContext):
    new_role = m.text
    if new_role.isdigit():
        new_role = int(new_role)
        if new_role == 1 or new_role == 2:
            await state.update_data(new_role=new_role)
            await m.reply('Ok. Thats great, but are you sure?',reply_markup=kb.inline_kb_user_full)
            await Admin_adding_user.confirm.set()
        else:
            await m.bot.send_message(text='Nice try. But only 1 and 2 allowed', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='Ohhh. seems great. But not realy', chat_id=m.chat.id)


async def new_user_confirm(m: Message, state: FSMContext, repo: Repo):
    data = await state.get_data()
    log.info(data)
    new_id = data.get('new_id')
    new_name = data.get('new_name')
    new_role = data.get('new_role')
    await m.bot.send_message(text=f'Ok, {new_name} with id: {new_id} and role: {new_role} will be added', chat_id=m.message.chat.id)
    await repo.add_user(**data)
    await state.finish()


async def new_user_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Allright, operation aborted.', chat_id=m.message.chat.id)
    await state.finish()


async def del_user(m: Message, state: FSMContext):
    log.info('deleting user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('Send me local id from database')
    await Admin_del_user.user_id.set()


async def del_user_id(m: Message, state: FSMContext):
    user_id = m.text
    if user_id.isdigit():
        await state.update_data(user_id=user_id)
        await m.reply('Ok. Thats great, but are you sure?',reply_markup=kb.inline_kb_del_full)
        await Admin_del_user.confirm.set()


async def del_user_confirm(m: Message, state: FSMContext, repo: Repo):
    data = await state.get_data()
    log.info(data)
    user_id = data.get('user_id')
    await m.bot.send_message(text='Good night, sweet prince', chat_id=m.message.chat.id)
    await repo.del_user(user_id)
    await state.finish()



async def del_user_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Allright, operation aborted.', chat_id = m.message.chat.id)
    await state.finish()


async def show_user(m: Message, repo: Repo):
    userlist = await repo.list_users()
    await m.answer(f'User List: {userlist}')


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
    ### Absolute Annihilation
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.ADMIN)
    ### Current State
    dp.register_message_handler(show_current_state, commands=['state'],
                                state='*', role=UserRole.ADMIN)

    ### State None Commands
    dp.register_message_handler(help_me, commands=['help'], state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(add_user, commands=['add'], state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(del_user, commands=['del'], state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(admin_start, commands=['start'],state=None,
                                role=UserRole.ADMIN)
    dp.register_message_handler(show_user, commands=['users'], state=None,
                                role=UserRole.ADMIN)

    ### Adding And Deleting User Handlers
    dp.register_message_handler(new_user_id, state=Admin_adding_user.user_id,
                                role=UserRole.ADMIN)
    dp.register_message_handler(new_user_name,
                                state=Admin_adding_user.user_name,
                                role=UserRole.ADMIN)
    dp.register_message_handler(new_user_role,
                                state=Admin_adding_user.user_role,
                                role=UserRole.ADMIN)
    dp.register_message_handler(del_user_id,
                                state=Admin_del_user.user_id,
                                role=UserRole.ADMIN)

    ### Callbacks
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(new_user_confirm, text=['user_add_confirm'], state = Admin_adding_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(new_user_decline, text=['user_add_decline'], state = Admin_adding_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(del_user_confirm, text=['user_del_confirm'], state = Admin_del_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(del_user_decline, text=['user_del_decline'], state = Admin_del_user.confirm, role=UserRole.ADMIN)
