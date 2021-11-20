from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole


import logging


log = logging.getLogger(__name__)


async def needed(m: Message):
    log.info('Another outsider trying to use me. He could be find by:  %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.bot.send_message(text='Для использования бота и печати файлов на принтере необходимо зарегистрироваться у администратора.', chat_id = m.chat.id)


def register_nobody(dp: Dispatcher):
    dp.register_message_handler(needed, state='*',
                                role=UserRole.NOBODY)
