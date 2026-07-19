from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.questions import QUESTIONS
from src.keyboards import inline, play_again_keyboard

router = Router()

class Quiz(StatesGroup):
    waiting_answer = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я твой первый бот.", 
        reply_markup=inline
    )

@router.message(Command('game'))
async def cmd_game(message: Message):
    await message.answer("Выбери один из пунктов меню:", reply_markup=inline)

# Хэндлер кнопки "Мой счет" (пока заглушка)
@router.callback_query(F.data == 'my_score')
async def show_score(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("📊 Функция просмотра статистики из БД будет настроена позже!")

# Старт викторины
@router.callback_query(F.data == 'quiz_start')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем игру!!! 🔥', show_alert=True)
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)
    await callback.message.answer(f"Вопрос 1: {QUESTIONS[0]['q']}")

# Обработка ответов пользователя внутри FSM
@router.message(Quiz.waiting_answer)  
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data['index']
    score = data['score']

    # Проверяем ответ
    if message.text.lower().strip() == QUESTIONS[index]['a']:
        score += 1
        await message.answer("Правильно! 🎉 +1")
    else:
        await message.answer(f"Неправильно. ❌ Правильный ответ: {QUESTIONS[index]['a']}")
    
    index += 1

    # Проверяем, закончились ли вопросы
    if index >= len(QUESTIONS):
        await message.answer(
            f"🏆 **Конец викторины!**\nВаш итоговый счет: {score} из {len(QUESTIONS)}.",
            parse_mode="Markdown",
            reply_markup=play_again_keyboard  # Предлагаем сыграть снова
        )
        await state.clear()  # Очищаем состояние в самом конце
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {QUESTIONS[index]['q']}")
