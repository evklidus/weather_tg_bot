from aiogram.utils.executor import start_polling
from aiogram import Bot, Dispatcher, types
from aiohttp import ClientSession

API_TOKEN = "6324497192:AAHOKHg2j_6b_N5toAJAqEuYby1qUfDmosk"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Узнать погоду в Краснодаре"]
    keyboard.add(*buttons)
    await bot.send_message(
        message.chat.id,
        "Привет, "
        + message.from_user.first_name
        + "! Чтобы узнать погоду, нажми на кнопку ниже.",
        reply_markup=keyboard,
    )


@dp.message_handler()
async def echo_message(msg: types.Message):
    if msg.text == "Узнать погоду в Краснодаре":
        async with ClientSession() as session:
            async with session.get(
                "http://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": 45.035470,
                    "longitude": 38.975313,
                    "current_weather": "true",
                },
            ) as resp:
                weather_data = await resp.json()
                await bot.send_message(
                    msg.from_user.id,
                    f"Сейчас в Краснодаре {weather_data['current_weather']['temperature']} °C",
                )


start_polling(dp)


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
