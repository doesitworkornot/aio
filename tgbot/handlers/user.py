import logging
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

log = logging.getLogger(__name__)

async def user_start(m: Message, repo: Repo):
    log.info('/start by %s(username) %s(first_name) id%s' %
        (m.from_user.username, m.from_user.first_name, m.from_user.id))
    await m.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], role=[UserRole.USER])
