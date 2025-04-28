
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import token, api_key

TOKEN = token

WEATHER_API_KEY = api_key
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Я бот для получения прогноза погоды. Используйте команду /weather <город>, чтобы узнать погоду.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''Доступные команды:
        /start - начать работу
        /help - список команд
        /weather <город> - узнать погоду в городе'''
        )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text('Пожалуйста, укажите название города. Например: /weather Москва')
        return

    city = ' '.join(context.args)
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
        }

    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        message = (
            f'Погода в {city}:\n'
            f'{weather_desc}\n'
            f'Температура: {temp}°C\n'
            f'Влажность: {humidity}%\n'
            f'Скорость ветра: {wind_speed} м/с'
            )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text('Не удалось получить данные о погоде. Проверьте название города.')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('weather', weather))

    print('Бот запущен...')
    app.run_polling()

if __name__ == '__main__':
    main()
