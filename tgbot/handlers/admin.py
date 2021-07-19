from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup


from tgbot.models.role import UserRole


class Admin_states(StatesGroup):
    first = State()
    second = State()


async def admin_start(m: Message):
    await m.reply('Hello, dear admin! Want to know ur state?')
    await Admin_states.first.set()


async def cancel(m: Message, state: FSMContext):
    await state.finish()
    await m.reply('Just removed your state. Now you are clean')


async def state_one(m: Message):
    await m.reply('Anyway. You are on first position.')
    await Admin_states.second.set()


async def show_current_state(m: Message, state: FSMContext):
    currentState = await state.get_state()
    await m.answer(f"Current state is: {currentState}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*',
                                role=UserRole.ADMIN)
    dp.register_message_handler(state_one, state=Admin_states.first)
    dp.register_message_handler(show_current_state, commands=['state'],
                                state='*', role=UserRole.ADMIN)
    dp.register_message_handler(admin_start, state='*',
                                commands=['start'], role=UserRole.ADMIN)
