from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from tgbot.config import load_config

import logging
import urllib


allowedfiles = ['jpg','png', 'pdf', 'tiff', 'cdr', 'psd', 'ai', 'bmp', 'gif', 'odf', 'odt', 'doc', 'docx', 'jpeg']


async def download(state, m):
    data = await state.get_data()
    file_id = data.get('file_id')
    copies = data.get('copies')
    file_extension = data.get('file_extension')

    file = await m.bot.get_file(file_id)
    file_path = file.file_path
    file_dest = f'/home/botuser/aiobot/docs/{m.message.chat.id}{file_id}.{file_extension}'
    token = 'SOME RANDOM SYMBOLS'
    link = f'https://api.telegram.org/file/bot{token}/{file_path}'
    urllib.request.urlretrieve(link, file_dest)
