from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.questions import QUESTIONS
from src.keyboards import inline, play_again_keyboard
# Импортируем функции работы с БД
from db.questions import add_question, get_all_questions, delete_question

router = Router()

class Quiz(StatesGroup):
    waiting_answer = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я твой первый бот.\n\n"
        "Доступные админ-команды для управления вопросами:\n"
        "/add [вопрос] [ответ] — добавить вопрос\n"
        "/list — показать список всех вопросов\n"
        "/del [ID] — удалить вопрос", 
        reply_markup=inline
    )

# 1. Вывод списка вопросов из БД
@router.message(Command("list"))
async def cmd_list(message: Message):
    questions = get_all_questions()
    if not questions:
        await message.answer("В базе данных пока нет вопросов. Добавь через /add!")
        return

    response_lines = ["📋 **Список вопросов в базе данных:**\n"]
    for q in questions:
        # q[0] - id, q[1] - текст вопроса, q[2] - правильный ответ
        response_lines.append(f"{q[0]}. Вопрос: {q[1]} | Ответ: {q[2]}")
    
    # Объединяем строки в одно сообщение, как советовали в ДЗ
    await message.answer("\n".join(response_lines), parse_mode="Markdown")

# 2. Добавление вопроса в БД
@router.message(Command("add"))
async def cmd_add(message: Message):
    # Убираем саму команду /add из текста
    args = message.text.replace("/add", "").strip()
    
    # Нам нужно разделить текст и ответ. Договоримся, что юзер вводит их через пробел или в кавычках.
    # Простой парсинг: ищем текст внутри или делим по пробелу между вопросом и ответом.
    # Для ДЗ разделим по последнему пробелу или через разделитель. Сделаем разделение через пробел:
    parts = args.split()
    if len(parts) < 2:
        await message.answer("⚠️ Ошибка! Напишите команду в формате:\n`/add Тема_вопроса Ответ`\nПример: `/add Столица_Италии рим`")
        return

    # Ответ — последнее слово, всё остальное — текст вопроса
    answer = parts[-1]
    text = " ".join(parts[:-1]).replace("_", " ") # Заменяем подчеркивания на пробелы для красоты, если использовались

    add_question(text, answer)
    await message.answer(f"✅ Вопрос успешно добавлен!\n**Вопрос:** {text}\n**Ответ:** {answer}", parse_mode="Markdown")

# 3. Удаление вопроса из БД по ID
@router.message(Command("del"))
async def cmd_del(message: Message):
    args = message.text.replace("/del", "").strip()
    if not args.isdigit():
        await message.answer("⚠️ Укажите числовой ID вопроса. Пример: `/del 5`")
        return

    question_id = int(args)
    delete_question(question_id)
    await message.answer(f"🗑️ Вопрос с ID {question_id} был удален (если он существовал).")


# --- Логика Викторины (из прошлого ДЗ) ---
@router.message(Command('game'))
async def cmd_game(message: Message):
    await message.answer("Выбери один из пунктов меню:", reply_markup=inline)

@router.callback_query(F.data == 'quiz_start')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем игру!!! 🔥', show_alert=True)
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)
    await callback.message.answer(f"Вопрос 1: {QUESTIONS[0]['q']}")

@router.message(Quiz.waiting_answer)  
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data['index']
    score = data['score']

    if message.text.lower().strip() == QUESTIONS[index]['a']:
        score += 1
        await message.answer("Правильно! 🎉 +1")
    else:
        await message.answer(f"Неправильно. ❌ Правильный ответ: {QUESTIONS[index]['a']}")
    
    index += 1

    if index >= len(QUESTIONS):
        await message.answer(
            f"🏆 **Конец викторины!**\nВаш итоговый счет: {score} из {len(QUESTIONS)}.",
            parse_mode="Markdown",
            reply_markup=play_again_keyboard
        )
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {QUESTIONS[index]['q']}")
