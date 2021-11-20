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


class User_printer(StatesGroup):
    copies = State()
    file = State()
    confirm = State()



'''########################################
                Handlers
########################################'''


async def user_start(m: Message):
    await m.reply('Добрый день, многоуважаемый пользователь, Выберете, что вам нужно или для списка команд и дополнительной информации наберите - /help', reply_markup=kb.inline_kb_full)


async def help_me(m: Message):
    await m.reply('Приветствую, этот телеграм бот умеет печатать файлы на школьном принтере, для начала необходимо зарегестрироваться у секретаря, а позже можно печатать файлы самому, поддерживаются почти все удобные для печати расширения, такие как PDF, DOCX, ODT и тд, для печати необходимо набрать команду /start, а далее следовать инструкциям бота, если что то пошло не так, то отменить все можно командой /cancel')



async def cancel(m: Message, state: FSMContext):
    await state.finish()
    await m.reply('Состояние аннулировано, можно начинать сначала')


async def print_q(m: Message):
    log.info('starting print f() by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='Сколько копий файла вы хотите напечатать?? Желательно, чтобы это было натуральное число меньше 40', chat_id=m.message.chat.id)
    await User_printer.copies.set()


async def copies(m: Message, state: FSMContext):
    copies = m.text
    if copies.isdigit():
        if int(copies)>=1 and int(copies)<=40:
            await  state.update_data(copies=copies)
            await m.bot.send_message(text=f'Отлично, следующий шаг - отправка файла на печать, важно отправлять именно как файл, а не фотография.', chat_id=m.chat.id)
            await User_printer.file.set()
        else:
            await m.bot.send_message(text='Слишком много, такими темпами можно разориться на колере', chat_id=m.chat.id)
    else:
        await m.bot.send_message(text='Отличная попытка, но попробуйте числа. Пример: 1, 4, 13. И все получится', chat_id=m.chat.id)


async def not_file(m: Message):
    await m.bot.send_message(text='На этом этапе необходимо отправить файл, обязательно как файл, фотографии как файл, файл и файл (файл)', chat_id=m.chat.id)


async def file(m: Message, state: FSMContext):
    file_name = m.document.file_name.split('.')
    file_extension = str(file_name[-1]).lower()
    if file_extension not in fp.allowedfiles:
        await m.bot.send_message(text='Неподдерживаемый формат, попробуйте сконвертировать в пригодный вид, PDF - лучший друг принтера', chat_id=m.chat.id)
    else:
        if m.document.file_size >= 20971520:
            await m.bot.send_message(text='Файл слишком большой, телеграм запрещает ботам скачивать такие большие файлы :(', chat_id=m.chat.id)
        else:
            await m.bot.send_message(text='Отлично, вы точно уверены, что хотите напечатать этот файл?', reply_markup=kb.inline_kb_print_full, chat_id=m.chat.id)
            file_id = m.document.file_id
            await state.update_data(file_extension=file_extension)
            await state.update_data(file_id=file_id)
            await User_printer.confirm.set()


async def print_confirm(m: Message, state: FSMContext):
    await m.bot.send_message(text='Восхитительно, файл обрабатывается....', chat_id=m.message.chat.id)
    print_status = await fp.download(state, m)
    if print_status == 0:
        await m.bot.send_message(text='Успешно отправлен на печать', chat_id=m.message.chat.id)
    else:
        await m.bot.send_message(text='Что то пошло не так и не ваша вина в том, обратитесь к администратору', chat_id=m.message.chat.id)
    await state.finish()


async def print_decline(m: Message, state: FSMContext):
    await m.bot.send_message(text='Успешно отменено', chat_id=m.message.chat.id)
    await state.finish()


async def info(m: Message):
    await m.bot.send_message(text='Как пожелаете', chat_id = m.message.chat.id)
    await User_states.info.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.USER)
    dp.register_message_handler(help_me, commands=['help'], state='*',
                                role=UserRole.USER)
    dp.register_callback_query_handler(print_q, text=['print'],
                                       role=UserRole.USER)
    dp.register_callback_query_handler(print_decline, text=['print_decline'], state = User_printer.confirm, role=UserRole.USER)
    dp.register_callback_query_handler(print_confirm, text=['print_confirm'], state = User_printer.confirm, role=UserRole.USER)
    dp.register_message_handler(copies, state=User_printer.copies,
                                role=UserRole.USER)
    dp.register_message_handler(file, content_types=['document'],
                                state=User_printer.file, role=UserRole.USER)
    dp.register_message_handler(not_file, state=User_printer.file,
                                role=UserRole.USER)
    dp.register_callback_query_handler(info, text=['info'],
                                       role=UserRole.USER)
    dp.register_message_handler(user_start, state='*',
                                commands=['start'], role=UserRole.USER)
