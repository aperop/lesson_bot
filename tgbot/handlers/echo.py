from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

echo_router = Router()


@echo_router.message(F.text)
async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Содержание сообщения:",
        message.text
    ]

    await message.answer('\n'.join(text))


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))

