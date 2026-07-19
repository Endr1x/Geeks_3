from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню бота
inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать викторину 🚀", callback_data="quiz_start")],
    [InlineKeyboardButton(text="Мой счет 📊", callback_data="my_score")],
    [InlineKeyboardButton(text="Наш сайт 🌐", url="https://geeks.kg")]
])

keyboard_main = inline

# Клавиатура после окончания игры
play_again_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сыграть снова 🔄", callback_data="quiz_start")]
])
