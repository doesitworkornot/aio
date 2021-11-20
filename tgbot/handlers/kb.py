from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_print = InlineKeyboardButton('Я хочу что то напечатать.',
                                        callback_data='print')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_print)
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_print)
inline_kb_full.add(InlineKeyboardButton('Хочу узнать, что с моим аккаунтом.',
                                        callback_data='info'))


inline_btn_user_confirm = InlineKeyboardButton('Да, я уверен.', callback_data = 'user_add_confirm')
inline_kb_user_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_user_confirm)
inline_kb_user_full.add(InlineKeyboardButton('Нет, просто случайность.', callback_data='user_add_decline'))


inline_btn_del_confirm = InlineKeyboardButton('Так точно', callback_data = 'user_del_confirm')
inline_kb_del_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_del_confirm)
inline_kb_del_full.add(InlineKeyboardButton('Никак нет!', callback_data='user_del_decline'))


inline_btn_print_confirm = InlineKeyboardButton('Подтверждаю.', callback_data = 'print_confirm')
inline_kb_print_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_print_confirm)
inline_kb_print_full.add(InlineKeyboardButton('Все пошло не по плану, прошу отложить печать.', callback_data='print_decline'))
