import config
import logging
import asyncio
from datetime import datetime
import time


from aiogram import Bot, Dispatcher, executor, types
from parser_app import parser_one, parser_three, parser_two
from sqlighter import SQLighter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

db = SQLighter('db.db')


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    me = await bot.get_me()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if (not db.subscriber_exists(message.from_user.id)):
        buttons = ['Подписаться на рассылку', 'Получить актуальные цены']
    else:
        buttons = ['Отписаться от рассылки', 'Получить актуальные цены']
    keyboard.add(*buttons)
    await message.answer(f'Здравствуйте, <b>{message.from_user.first_name}!</b> Я <b>{me.username}.</b>\n\nВы можете подписаться на <u>ежедневную рассылку цен</u> \nили запросить <u>актуальные цены</u> в любой момент:', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Подписаться на рассылку')
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscribtion(message.from_user.id, True)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Отписаться от рассылки', 'Получить актуальные цены']
    keyboard.add(*buttons)

    await message.answer('Вы успешно подписались на рассылку цен!\nРассылка происходит каждый день в 9, 15 и 18 часов.', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Получить актуальные цены')
async def check_price(message: types.Message):
    try:
        res_one = parser_one()
        await message.answer(f'<u><b>Юг-Мет:</b></u>\n\n{res_one[0]} $\n{res_one[1]} $')
    except Exception:
        await message.answer(f'<u><b>Юг-Мет:</b></u>\n\nНе удалось получить данные, попробуйте позже.')
    try:
        res_two = parser_two()
        await message.answer(f'<u><b>ФЕРРАТЕК:</b></u>\n\n{res_two[0]} \n{res_two[1]} ')
    except Exception:
        await message.answer(f'<u><b>ФЕРРАТЕК:</b></u>\n\nНе удалось получить данные, попробуйте позже.')
    try:
        res_three = parser_three()
        await message.answer(f'<u><b>РусЛом61:</b></u>\n\n{res_three[0]}\n{res_three[1]}\n{res_three[2]}')
    except Exception:
        await message.answer(f'<u><b>РусЛом61:</b></u>\n\nНе удалось получить данные, попробуйте позже.')


@dp.message_handler(lambda message: message.text == 'Отписаться на рассылки')
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы итак не подписаны')
    else:
        db.delete_subscribtion(message.from_user.id)
        await message.answer('Вы отписались от рассылки\nВсего хорошего!', reply_markup=types.ReplyKeyboardRemove())


async def scheduled(wait_for):
    while True:

        if time.strftime('%X') == '09:00:00' or time.strftime('%X') == '15:00:00' or time.strftime('%X') == '18:00:00':

            subscribers = db.get_subscribers()

            for sub in subscribers:
                try:
                    try:
                        res_one = parser_one()
                        await bot.send_message(sub[1], f'<u><b>Юг-Мет:</b></u>\n\n{res_one[0]} $\n{res_one[1]} $')
                    except Exception as e:
                        await bot.send_message(sub[1], f'<u><b>Юг-Мет:</b></u>\n\nНе удалось получить данные, попробуйте позже.')
                except Exception:
                    print('Block bot')

            try:
                res_two = parser_two()
                for sub in subscribers:
                    try:
                        await bot.send_message(sub[1], f'<u><b>ФЕРРАТЕК:</b></u>\n\n{res_two[0]} \n{res_two[1]} ')
                    except Exception:
                        print('Bot block')
            except Exception:
                await bot.send_message(sub[1], f'<u><b>ФЕРРАТЕК:</b></u>\n\nНе удалось получить данные, попробуйте позже.')

            try:
                res_three = parser_three()
                for sub in subscribers:
                    try:
                        await bot.send_message(sub[1], f'<u><b>РусЛом61:</b></u>\n\n{res_three[0]}\n{res_three[1]}\n{res_three[2]}')
                    except Exception:
                        print('Bot block')
            except Exception:
                await bot.send_message(sub[1], f'<u><b>РусЛом61:</b></u>\n\nНе удалось получить данные, попробуйте позже.')

        else:
            await asyncio.sleep(wait_for)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
