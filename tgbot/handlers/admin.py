from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Message, ParseMode
#import aiogram.utils.markdown as md

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

from .dialog import DialogBaseTemplate


class AddUserDialog(StatesGroup):
    get_forwarded_message = State()
    status = State()
    submit = State()


class DelUserDialog(StatesGroup):
    db_id = State()
    submit = State()


class AddUserProc(DialogBaseTemplate):
    """/adduser unique dialog instructions"""

    def __init__(self, fsm, fsm_group, rules={} ):
        super().__init__(self, fsm, fsm_group )
        self.fsm = fsm
        self.fsm_group = fsm_group
        self.rules = {
            'get_forwarded_message': {
                'question': (
                    'Для добавления пользователя в базу перешлите мне'
                        ' сообщение от него. Если в нем не будет'
                        ' поля "forward_from" - напишите telegram user_id',
                    'Перешлите мне сообщение с полем "forward_from"'
                        ' или напишите telegram user_id!',),
                'test': self.get_forwarded_message_test,
                'calc': self.get_forwarded_message_calc,
                'after_answer': self.default_after_answer_proc,
            },
            'status': {
                'question': ('Укажите статус пользователя (от 1 до 5)', ),
                'test': self.status_test,
                'after_answer': self.default_after_answer_proc,
            },
            'submit': {
                'question': ('Подтвердите введенные данные:', ),
                'keyboard': self.KEYBOARD_APPROVE,
                'test': self.has_approve_answer,
                'after_question': self.submit_after_question_proc,
                'after_answer': self.submit_after_answer_proc,
            },
        } | rules

    def get_forwarded_message_test(self, message):
        if self.has_forward_from(message) == 0:
            return 0
        return self.is_int(message, from_=1, to_=2000000000)

    def status_test(self, message):
        return self.is_int(message, from_=1, to_=5)

    def get_forwarded_message_calc(self, message):
        if self.has_forward_from(message) == 0:
            user = message.forward_from
            return {
                'telegram_id': user.id,
                'name': user.username if user.username else ''}
        return {'telegram_id': message.text, 'name': ''}

    def submit_after_question_proc(self, data):
        return (
            f"Telegram user_id: {data.get('telegram_id', '')}\n"
            f"Username: {data.get('name', '')}\n"
            f"Статус: {data.get('status', '')}\n")

    async def submit_after_answer_proc(self, m, state, repo, **notused):
        data = await state.get_data()
        if data.get('submit', '') == 'Подтверждаю':
            await repo.add_user(**data)
            mes_text = 'Пользователь добавлен в базу'
        else:
            mes_text = 'Пользователь НЕ добавлен в базу'
        await m.answer(mes_text, reply_markup=self.KEYBOARD_REMOVE)

    async def default_after_answer_proc(self, m, answer_data,  **notused):
        await m.answer(f"Ok. {answer_data}")


class DelUserProc(DialogBaseTemplate):
    """/deluser unique dialog instructions"""

    def __init__(self, fsm, fsm_group, rules={} ):
        super().__init__(self, fsm, fsm_group )
        self.fsm = fsm
        self.fsm_group = fsm_group
        self.rules = {
            'db_id': {
                'question': ('Для удаления пользователя из базы напишите мне его id', ),
                'test': self.is_int,
            },
            'submit': {
                'question': ('Подтвердите удаление пользователя', ),
                'keyboard': self.KEYBOARD_APPROVE,
                'test': self.has_approve_answer,
                'after_question': self.submit_after_question_proc,
                'after_answer': self.submit_after_answer_proc,
            },
        } | rules

    def submit_after_question_proc(self, data):
        return (f"id пользователя: {data.get('db_id', '')}")

    async def submit_after_answer_proc(self, m, state, repo, **notused):
        data = await state.get_data()
        if data.get('submit', '') == 'Подтверждаю':
            await repo.del_user(data['db_id'])
            mes_text = 'Пользователь удален'
        else:
            mes_text = 'Пользователь НЕ удален'

        await m.answer(mes_text, reply_markup=self.KEYBOARD_REMOVE)


# Место, за которое стыдно... но я пока ничего красивее не придумал
dialogs = {
    'AddUserDialog': AddUserProc(AddUserDialog, 'AddUserDialog'),
    'DelUserDialog': DelUserProc(DelUserDialog, 'DelUserDialog'),
}


async def adduser_start(m: Message, state: FSMContext):
    dialog = dialogs['AddUserDialog']
    await dialog.next_step()
    await first_question(m, state, dialog)


async def deluser_start(m: Message, state: FSMContext):
    dialog = dialogs['DelUserDialog']
    await dialog.next_step()
    await first_question(m, state, dialog)


async def first_question(m, state, dialog):
    current_step = await state.get_state()
    if current_step:
        dialog.set_state(current_step)
        await m.answer(dialog.question_text(), reply_markup=dialog.keyboard())


async def do_dialog(m: Message, state: FSMContext, repo: Repo):
    current_step = await state.get_state()
    dialog = dialogs[current_step.split(':')[0]]
    dialog.process_current_step(current_step, m)

    if not dialog.ready_to_next_step():
        await m.reply(dialog.question_text())
        return

    answer_data = dialog.get_answer_result()
    await state.update_data(**answer_data)

    if dialog.has_after_answer_proc():
        await dialog.after_answer_proc(m=m,
            state=state, repo=repo, answer_data=answer_data)

    await dialog.next_step()

    current_step = await state.get_state()
    if not current_step:
        return

    await first_question(m, state, dialog)
    if dialog.has_after_question_proc():
        data = await state.get_data()
        await m.answer(dialog.after_question_proc(data))


async def any_message(m: Message):
    user = m.from_user
    await m.answer(f"Привет, админ! {user.first_name} {user.last_name}! (@{user.username}, id: {user.id})")
    await m.answer(
        '/adduser - добавить пользователя в БД\n'
        '/showuser - посмотреть список пользователей\n'
        '/deluser - удалить пользователя из БД\n'
        '/state - текущее состояние диалога от FSM\n'
        'cancel - прервать текущую процедуру (диалог)'
    )


async def showuser(m: Message, repo: Repo):
    userlist = await repo.list_users()
    await m.answer(f"Список пользователей: {userlist}")


async def show_current_state(m: Message, state: FSMContext):
    currentState = await state.get_state()
    await m.answer(f"Cостояние текущего процесса: {currentState}")


async def do_cancel(m: Message, state: FSMContext):
    await state.finish()
    await m.answer('Текущий процесс прерван...Удачи!',
                           reply_markup=DialogBaseTemplate.KEYBOARD_REMOVE)


async def nope(a):
    pass


def register_admin(dp: Dispatcher):
    dp.register_message_handler(any_message, commands=['start', 'help'], is_admin=True)
    dp.register_message_handler(adduser_start, commands=['adduser'], is_admin=True)
    dp.register_message_handler(deluser_start, commands=['deluser'], is_admin=True)
    dp.register_message_handler(showuser, commands=['showuser'], is_admin=True)
    dp.register_message_handler(show_current_state, commands=['state'], state='*', is_admin=True)
    dp.register_message_handler(nope, text=['cancel','A','А'], state=None, is_admin=True)
    dp.register_message_handler(do_cancel, text=['cancel','A','А'], state='*', is_admin=True)
    dp.register_message_handler(any_message, state=None, is_admin=True)
    dp.register_message_handler(do_dialog, state='*',is_admin=True)
