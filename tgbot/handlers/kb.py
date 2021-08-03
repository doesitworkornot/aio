from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_print = InlineKeyboardButton('I want to print some stuff',
                                        callback_data='print')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_print)
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_print)
inline_kb_full.add(InlineKeyboardButton('Id like to know smth about my account',
                                        callback_data='info'))


inline_btn_user_confirm = InlineKeyboardButton('Yes, im sure', callback_data = 'user_add_confirm')
inline_kb_user_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_user_confirm)
inline_kb_user_full.add(InlineKeyboardButton('No, just a miss click', callback_data='user_add_decline'))


inline_btn_del_confirm = InlineKeyboardButton('Yes, im sure', callback_data = 'user_del_confirm')
inline_kb_del_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_del_confirm)
inline_kb_del_full.add(InlineKeyboardButton('No, just a miss click', callback_data='user_del_decline'))
