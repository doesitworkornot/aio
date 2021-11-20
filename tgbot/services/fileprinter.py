from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from tgbot.config import load_config

import logging
import urllib
import subprocess

log = logging.getLogger(__name__)

allowedfiles = ['jpg','png', 'pdf', 'tiff', 'cdr', 'psd', 'ai', 'bmp', 'gif', 'odf', 'odt', 'doc', 'docx', 'jpeg']


async def download(state, m):
    data = await state.get_data()
    file_id = data.get('file_id')
    copies = data.get('copies')
    file_extension = data.get('file_extension')
    log.info(f'Get default info...')
    file = await m.bot.get_file(file_id)
    file_path = file.file_path
    token = 'YOUR BOT TOKEN'
    link = f'https://api.telegram.org/file/bot{token}/{file_path}'
    file_name = f'{m.message.chat.id}{file_id}.{file_extension}'
    log.info(f'File name - {file_name}')
    if file_extension == 'pdf':
        file_dest = f'/home/botuser/aiobot/pdfs/{file_name}'
        urllib.request.urlretrieve(link, file_dest)
        log.info('Requested urllib')
    else:
        file_dest = f'/home/botuser/aiobot/docs/{file_name}'
        urllib.request.urlretrieve(link, file_dest)
        log.info('Requested urllib')
        await convert(file_dest)
    file_dest = f'/home/botuser/aiobot/pdfs/{m.message.chat.id}{file_id}.pdf'
    if int(copies) > 1:
        cmd = ['lp', '-n', copies, file_dest]
    else:
        cmd = ['lp', file_dest]
    traceback = subprocess.run(cmd)
    if traceback.returncode == 0:
        return 0




async def convert(file_dest):
    cmd = ['lowriter', '--convert-to', 'pdf', '--outdir', '/home/botuser/aiobot/pdfs', file_dest]
    traceback = subprocess.run(cmd, check=True)
    return traceback.returncode
