class DialogBaseTemplate:
    """Base dialog template."""

    KEYBOARD_REMOVE = '{"remove_keyboard": true}'
    KEYBOARD_APPROVE = ('{"keyboard": [["Подтверждаю", "Отменить"]],'
                                        ' "resize_keyboard": true, "selective": true}')
    INCORRECT_ANSWER_DEFAULT_PHRASE = 'Ошибка. Повторите ввод.'


    def __init__(self, fsm, fsm_group, rules={} ):
        self.fsm = fsm
        self.fsm_group = fsm_group
        self.rules = rules
        self.state_name = ''
        self.answer_status = 0
        self.answer_value = {}

    def set_state(self, state):
        """
        Getting the current state of the FSM.
        Loading instance variables according to the current state.
        """

        if not state.startswith(self.fsm_group):
            # 'Не в тот диалог обращаетесь'
            # тут я не знаю какое исключение делать и кто его будет ловить
            raise Exception('StateGroupError')
        self.state_name = state[len(self.fsm_group)+1:]
        self.state_data = self.rules.get(self.state_name, {})
        self.answer_status = 0
        self.answer_value = {}

    def get_state(self):
        return self.state_name

    def answer_test(self, message):
        """Checking the validity of the answer. 0 means valid answer"""

        self.answer_status = self.state_data.get('test', lambda *x: 0)(message)

    def answer_result(self, message):
        """Calculating and saving the answer result"""

        self.answer_value = self.state_data.get('calc',
            lambda mes: {self.state_name: mes.text}
        )(message)

    def get_answer_result(self):
        return self.answer_value

    def process_current_step(self, state, message):
        self.set_state(state)
        self.answer_test(message)
        if self.answer_status == 0:
            self.answer_result(message)


    def has_forward_from(self, message):
        #return int(not bool(message.forward_from))
        if message.forward_from:
            return 0
        else:
            return 1

    def is_int(self, m, from_=0, to_=0):
        try:
            value = int(m.text)
        except ValueError:
            return 1  # Not int
        if (value >= from_ and value <= to_) or from_ == to_:
            return 0
        else:
            return 2  # Not in range

    def has_approve_answer(self, message):
        if message.text in ('Подтверждаю', 'Отменить'):
            return 0
        else:
            return 1

    def question_text(self):
        questions = self.state_data.get('question', [])
        q_numb = len(questions)
        if q_numb == 0:
            return self.INCORRECT_ANSWER_DEFAULT_PHRASE
        if q_numb <= self.answer_status:
            return f"{self.INCORRECT_ANSWER_DEFAULT_PHRASE}\n{questions[0]}"
        return questions[self.answer_status]

    def keyboard(self):
        return self.state_data.get('keyboard', self.KEYBOARD_REMOVE)

    async def next_step(self):
        await self.fsm.next()

    def ready_to_next_step(self):
        return self.answer_status == 0

    def has_after_question_proc(self):
        return 'after_question' in self.state_data

    def after_question_proc(self, data):
        return self.state_data.get('after_question', lambda *x: '')(data)

    def has_after_answer_proc(self):
        return 'after_answer' in self.state_data

    def after_answer_proc(self, **data):
        return self.state_data.get('after_answer', lambda *x: '')(**data)
