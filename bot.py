water_data = {
    "Река Москва": {
        "level": "Высокий 🔴",
        "text": "❌ Купание не рекомендуется",
        "map": "https://yandex.ru/maps/?text=Река+Москва"
    },
    "Река Яуза": {
        "level": "Высокий 🔴",
        "text": "❌ Сильное антропогенное загрязнение",
        "map": "https://yandex.ru/maps/?text=Река+Яуза"
    },
    "Река Ока": {
        "level": "Средний 🟡",
        "text": "⚠️ Ограниченно безопасно",
        "map": "https://yandex.ru/maps/?text=Река+Ока"
    },
    "Река Дон": {
        "level": "Средний 🟡",
        "text": "⚠️ Загрязнение в верхнем течении",
        "map": "https://yandex.ru/maps/?text=Река+Дон"
    },
    "Озеро Селигер": {
        "level": "Низкий 🟢",
        "text": "✅ Относительно чистое озеро",
        "map": "https://yandex.ru/maps/?text=Озеро+Селигер"
    },
    "Озеро Сенеж": {
        "level": "Низкий 🟢",
        "text": "✅ В пределах нормы",
        "map": "https://yandex.ru/maps/?text=Озеро+Сенеж"
    }
}
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

water_data = {
    "Река Ока": {
        "level": "Высокий",
        "text": "❌ Купание не рекомендуется",
        "map": "https://yandex.ru/maps/?text=Река+Ока"
    },
    "Река Москва": {
        "level": "Средний",
        "text": "⚠️ Ограниченно безопасно",
        "map": "https://yandex.ru/maps/?text=Река+Москва"
    },
    "Озеро Сенеж": {
        "level": "Низкий",
        "text": "✅ Вода относительно чистая",
        "map": "https://yandex.ru/maps/?text=Озеро+Сенеж"
    }
}

last_water = {}

def water_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=name)] for name in water_data],
        resize_keyboard=True
    )

def action_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🗺️ Показать карту")],
            [types.KeyboardButton(text="⬅️ Назад к выбору водоёма")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🌍 Мониторинг загрязнения водоёмов ЦФО\n\n"
        "Выберите водоём:",
        reply_markup=water_keyboard()
    )

@dp.message(lambda msg: msg.text in water_data)
async def show_info(message: types.Message):
    name = message.text
    last_water[message.from_user.id] = name
    data = water_data[name]

    await message.answer(
        f"📍 {name}\n\n"
        f"💧 Уровень загрязнения: {data['level']}\n"
        f"{data['text']}",
        reply_markup=action_keyboard()
    )

@dp.message(lambda msg: msg.text == "🗺️ Показать карту")
async def show_map(message: types.Message):
    user_id = message.from_user.id
    if user_id in last_water:
        name = last_water[user_id]
        await message.answer(
            f"🗺️ Карта водоёма «{name}»:\n{water_data[name]['map']}"
        )
    else:
        await message.answer("Сначала выберите водоём.")

@dp.message(lambda msg: msg.text == "⬅️ Назад к выбору водоёма")
async def back(message: types.Message):
    await message.answer(
        "Выберите водоём:",
        reply_markup=water_keyboard()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
