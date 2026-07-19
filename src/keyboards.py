from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_tasks_keyboard(tasks) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for idx, task in enumerate(tasks, 1):
        task_id, title, is_done = task
        if not is_done:
            builder.button(
                text=f"Выполнить №{idx}", 
                callback_data=f"done_{task_id}"
            )
    builder.adjust(2)
    return builder.as_markup()
