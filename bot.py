import asyncio
import time
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from functions import *

TOKEN = '5950027811:AAEC9Yv3a5ZiFIBQT8i6ADu8dlezLb1pDL8'

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📅 Новости за дату")
    btn2 = types.KeyboardButton("🗓 Новости за промежуток времени")
    btn3 = types.KeyboardButton("📣 Новости по категориям за промежуток времени")
    btn4 = types.KeyboardButton("🤓 Топ комментаторов за промежуток времени")
    btn5 = types.KeyboardButton("🔝 Топ новостей за промежуток времени")
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)
    await bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
async def message_reply(message):
    format = '%d-%m-%Y'
    if message.text == "📅 Новости за дату":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        await bot.send_message(message.chat.id, "Введите дату в формате \n \'дд-мм-гггг\'", reply_markup=keyboard)
    elif message.text == "🗓 Новости за промежуток времени":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        await bot.send_message(message.chat.id, "Введите две даты через пробел в формате \n \'дд-мм-гггг дд-мм-гггг\'",
                               reply_markup=keyboard)
    elif message.text == "📣 Новости по категориям за промежуток времени":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        await bot.send_message(message.chat.id,
                               "Введите категорию (Политика, Общество, Наука, Экономика) и две даты через пробел в формате \n \'Категория дд-мм-гггг дд-мм-гггг\'",
                               reply_markup=keyboard)
    elif message.text == "🤓 Топ комментаторов за промежуток времени":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        await bot.send_message(message.chat.id,
                               "Введите слово \'Комментаторы\' и две даты через пробел в формате \n \'Комментаторы дд-мм-гггг дд-мм-гггг\'",
                               reply_markup=keyboard)
    elif message.text == "🔝 Топ новостей за промежуток времени":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        await bot.send_message(message.chat.id,
                               "Введите слово \'Топ\' и две даты через пробел в формате \n \'Топ дд-мм-гггг дд-мм-гггг\'",
                               reply_markup=keyboard)
    elif message.text == "Меню":
        await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        keyboard.add(btn1)
        text = ''
        try:
            dates = message.text.split(' ')

            ans = []
            if len(dates) == 2:
                if dt.datetime.strptime(dates[0], format) + dt.timedelta(days=30) < dt.datetime.strptime(dates[1],
                                                                                                         format):
                    await bot.send_message(message.chat.id, "Выберите промежуток поменьше", reply_markup=keyboard,
                                           parse_mode='Markdown')
                    return
                ans = await get_agg_news(dates[0], dates[1])

            elif len(dates) == 1:
                ans = await get_agg_news(dates[0], dates[0])
            elif len(dates) == 3:
                if (dt.datetime.strptime(dates[1], format) + dt.timedelta(days=30)) < dt.datetime.strptime(dates[2],
                                                                                                           format):
                    await bot.send_message(message.chat.id, "Выберите промежуток поменьше", reply_markup=keyboard,
                                           parse_mode='Markdown')
                    return
                if dates[0] == 'Комментаторы':
                    text = await get_top_commentators(dates[1], dates[2])
                    await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')
                    return
                elif dates[0] == 'Топ':
                    ans = await get_agg_news(dates[1], dates[2])
                    ans = sorted(ans, key=lambda x: -int(x[2].split(' ')[1]))[:5]
                else:
                    ans = await get_sections(dates[0], dates[1], dates[2])
            counter = 0
            if len(ans) == 0:
                await bot.send_message(message.chat.id, "Новости за этот промежуток отсутсвуют", reply_markup=keyboard,
                                       parse_mode='Markdown')
                return
            for (name, ref, rating, comments) in ans:
                text += '*Название новости*: {} \n *Ссылка*: {} \n'.format(name, ref)
                counter += 1
                if counter % 10 == 0:
                    await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')
                    text = ''
            if counter % 10 > 0:
                await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')
        except:
            await bot.send_message(message.chat.id, "Я не понимаю запроса, попробуйте ещё", reply_markup=keyboard)


async def main():
    await asyncio.gather(bot.infinity_polling(timeout=120))


# Run
if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception:
            time.sleep(3)
