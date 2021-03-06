from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
import tgbot.handlers.kb as kb
import tgbot.services.fileprinter as fp


import logging


log = logging.getLogger(__name__)



'''########################################
                States
########################################'''

class Admin_printer(StatesGroup):
    copies = State()
    file = State()
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
    await m.reply('Можно начинать жизнь с нового листа')


async def print_q(m: Message):
    log.info('starting print f() by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='Сколько копий необходимо напечатать??', chat_id=m.message.chat.id)
    await Admin_printer.copies.set()


async def copies(m: Message, state: FSMContext):
    copies = m.text
    if copies.isdigit():
        if int(copies)>=1 and int(copies)<=40:
            await  state.update_data(copies=copies)
            await m.bot.send_message(text=f'Прелестно, далее требуется отправить файл.', chat_id=m.chat.id)
            await Admin_printer.file.set()
        else:
            await m.bot.send_message(text='Это слишком много, даже для многоуважаемого админа.', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='Отличная попытка!!!! Но если использовать цифры и числа, целые, а не флоаты и без знака -, то все должно получиться, желаю успехов!!', chat_id=m.chat.id)


async def not_file(m: Message):
    await m.bot.send_message(text='На этом этапе необходимо отправить файл, как файл, а не как фото, на компьютере надо отправить без сжатия', chat_id=m.chat.id)


async def file(m: Message, state: FSMContext):
    file_name = m.document.file_name.split('.')
    file_extension = str(file_name[-1]).lower()
    if file_extension not in fp.allowedfiles:
        await m.bot.send_message(text='Неподдерживаемый формат', chat_id=m.chat.id)
    else:
        if m.document.file_size >= 20971520:
            await m.bot.send_message(text='БОЛЬШООООООЙ. Телеграм такое не любит', chat_id=m.chat.id)
        else:
            await m.bot.send_message(text='Поздравляю с последним этапом! Вы уверены?', reply_markup=kb.inline_kb_print_full, chat_id=m.chat.id)
            file_id = m.document.file_id
            await state.update_data(file_extension=file_extension)
            await state.update_data(file_id=file_id)
            await Admin_printer.confirm.set()


async def print_confirm(m: Message, state: FSMContext):
    await m.bot.send_message(text='Добро, отправляю на обработку...', chat_id=m.message.chat.id)
    print_status = await fp.download(state, m)
    if print_status == 0:
        await m.bot.send_message(text='Файл отправлен принтеру на печать и все хорошо', chat_id=m.message.chat.id)
    else:
        await m.bot.send_message(text='Что то пошло не так, требуется починка от высшего мастера', chat_id=m.message.chat.id)
    await state.finish()


async def print_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Отменено', chat_id=m.message.chat.id)
    await state.finish()



async def info(m: Message):
    log.info('getting info by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='Вы получите данные, как появится возможность :)', chat_id=m.message.chat.id)


async def add_user(m: Message, state: FSMContext):
    log.info('adding user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('Перешлите сообщение от пользователя, которого необходимо добавить или просто отправьте телеграм id')
    await Admin_adding_user.user_id.set()


async def new_user_id(m: Message, state: FSMContext):
    if m.forward_from != None:
        new_id = m.forward_from.id
        await  state.update_data(new_id=new_id)
        await m.bot.send_message(text=f'Вы добавляете пользователя с id: {new_id}. Напишите, какими символами он будет записан в базу данных', chat_id=m.chat.id)
        await Admin_adding_user.user_name.set()
    elif m.text.isdigit():
        new_id = m.text
        if int(new_id) <= 2000000000 and int(new_id) >=1:
            await  state.update_data(new_id=new_id)
            await m.bot.send_message(text=f'Вы добавляете пользователя с id: {new_id}. Напишите, какими символами он будет записан в базу данных', chat_id=m.chat.id)
            await Admin_adding_user.user_name.set()
        else:
            await m.bot.send_message(text='Слишком большое число, можно попробовать второй раз', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='Неудача, скорей всего пользователь установил в настройках приватности сокрытие id, так что придется просить его отправить вам id', chat_id=m.chat.id)


async def new_user_name(m: Message, state: FSMContext):
    new_name = m.text
    await state.update_data(new_name=new_name)
    await m.bot.send_message(text='Очень красиво... Теперь введите его назначение. 1 - обычный человек, 2 - могучий администратор', chat_id=m.chat.id)
    await Admin_adding_user.user_role.set()


async def new_user_role(m: Message, state: FSMContext):
    new_role = m.text
    if new_role.isdigit():
        new_role = int(new_role)
        if new_role == 1 or new_role == 2:
            await state.update_data(new_role=new_role)
            await m.reply('Отлично, но вы уверены?',reply_markup=kb.inline_kb_user_full)
            await Admin_adding_user.confirm.set()
        else:
            await m.bot.send_message(text='Бесподобно, но можно ответить только 1 или 2', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='Очень оригинально, но если отправить простую цифру, то все получится, я верю, на выбор дается 1 или 2.', chat_id=m.chat.id)


async def new_user_confirm(m: Message, state: FSMContext, repo: Repo):
    data = await state.get_data()
    log.info(data)
    new_id = data.get('new_id')
    new_name = data.get('new_name')
    new_role = data.get('new_role')
    await m.bot.send_message(text=f'Дивно, {new_name} с id: {new_id} и ролью: {new_role} будет добавлен.', chat_id=m.message.chat.id)
    await repo.add_user(**data)
    await state.finish()


async def new_user_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Как пожелаете.', chat_id=m.message.chat.id)
    await state.finish()


async def del_user(m: Message, state: FSMContext):
    log.info('deleting user by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply('Отправьте id из базы данных. /users в помощь')
    await Admin_del_user.user_id.set()


async def del_user_id(m: Message, state: FSMContext):
    user_id = m.text
    if user_id.isdigit():
        await state.update_data(user_id=user_id)
        await m.reply('Любопытно, но вы уверены?',reply_markup=kb.inline_kb_del_full)
        await Admin_del_user.confirm.set()


async def del_user_confirm(m: Message, state: FSMContext, repo: Repo):
    data = await state.get_data()
    log.info(data)
    user_id = data.get('user_id')
    await m.bot.send_message(text='Good night, sweet prince', chat_id=m.message.chat.id)
    await repo.del_user(user_id)
    await state.finish()



async def del_user_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Почти получилось.', chat_id = m.message.chat.id)
    await state.finish()


async def show_user(m: Message, repo: Repo):
    userlist = await repo.list_users()
    await m.answer(f'Список пользователей: {userlist}')


async def admin_start(m: Message):
    await m.reply('Добрый вечер, многоуважаемый администратор, печать, информация или помощь? за последним - /help', reply_markup=kb.inline_kb_full)


async def help_me(m: Message):
    await m.bot.send_message(text='Короткое объяснение.\n \n Этот бот умеет печатать файлы на принтере. \n Список команд: \n \n /help - ультимативный гид \n /cancel - отмена любого состояния \n /users - показывает список пользователей, их права и локальный id \n /state - показывает текущее состояние процесса бота \n /start - начало стартогого диалога и печати \n /add - добавление нового пользователя \n /del - удаление пользователя', chat_id = m.chat.id)


async def show_current_state(m: Message, state: FSMContext):
    log.info('showing state to %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    currentState = await state.get_state()
    await m.answer(f"Текущее состояние: {currentState}")



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

    ### Printer Main dialog
    dp.register_message_handler(copies, state=Admin_printer.copies,
                                role=UserRole.ADMIN)
    dp.register_message_handler(not_file, state=Admin_printer.file,
                                role=UserRole.ADMIN)
    dp.register_message_handler(file, content_types=['document'],
                                state=Admin_printer.file, role=UserRole.ADMIN)

    ### Callbacks
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(new_user_confirm, text=['user_add_confirm'], state = Admin_adding_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(new_user_decline, text=['user_add_decline'], state = Admin_adding_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(del_user_confirm, text=['user_del_confirm'], state = Admin_del_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(del_user_decline, text=['user_del_decline'], state = Admin_del_user.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(print_decline, text=['print_decline'], state = Admin_printer.confirm, role=UserRole.ADMIN)
    dp.register_callback_query_handler(print_confirm, text=['print_confirm'], state = Admin_printer.confirm, role=UserRole.ADMIN)
