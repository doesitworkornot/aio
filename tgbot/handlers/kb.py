from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_print = InlineKeyboardButton('I want to print some stuff',
                                        callback_data='print')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_print)
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_print)
inline_kb_full.add(InlineKeyboardButton('Id like to know smth about my account',
                                        callback_data='info'))
