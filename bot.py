import telebot
from telebot import types

import random
import requests
import json
import string

import threading
from datetime import datetime, timedelta
import time

from SimpleQIWI import *
import sqlite3

import others

bot = telebot.TeleBot(others.bot_token)
admin_user_id = others.admin_user_id
channel_id = others.channel_id

in_comment = []
threads = list()

# Главная клавиатура
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile = types.KeyboardButton('💁🏻‍♀️ Мой профиль')
catalog = types.KeyboardButton('🚀 Каталог')
ref = types.KeyboardButton('♻️ Вопрос - Ответ')
support = types.KeyboardButton('Поддержка')
about = types.KeyboardButton('💠 Отзывы')
referal = types.KeyboardButton('🎭 Реф. система')
bonus = types.KeyboardButton('🎉 Бонус')
markup.add(profile, catalog)
markup.add(ref, about)
markup.add(referal, bonus)
# Главная клавиатура

# Каталог
product = types.ReplyKeyboardMarkup(resize_keyboard=True)
hqd = types.KeyboardButton('🍇 Товары HQD')
juul = types.KeyboardButton('🍭 Товары Juul')
back = types.KeyboardButton('Назад')
product.add(hqd, juul)
product.add(back)
# Каталог

# Вкусы
tastes = types.ReplyKeyboardMarkup(resize_keyboard=True)
tastes_1 = types.KeyboardButton('Клубника')
tastes_2 = types.KeyboardButton('Черника')
tastes_3 = types.KeyboardButton('Вишня')
tastes_4 = types.KeyboardButton('Банан')
tastes_5 = types.KeyboardButton('Арбуз')
tastes_6 = types.KeyboardButton('Персик')
tastes_7 = types.KeyboardButton('Виноград')
tastes_8 = types.KeyboardButton('Яблоко')
tastes_9 = types.KeyboardButton('Дыня')
tastes_10 = types.KeyboardButton('Ананас')
tastes_11 = types.KeyboardButton('Корица')
tastes_12 = types.KeyboardButton('Жвачка')
tastes_13 = types.KeyboardButton('Кола')
tastes_14 = types.KeyboardButton('Орех')
tastes_15 = types.KeyboardButton('Мята')
tastes_16 = types.KeyboardButton('Табак')
tastes.add(tastes_1, tastes_2, tastes_3)
tastes.add(tastes_4, tastes_5, tastes_6)
tastes.add(tastes_7, tastes_8, tastes_9)
tastes.add(tastes_10, tastes_11, tastes_12)
tastes.add(tastes_13, tastes_14, tastes_15)
tastes.add(tastes_16)


tastes_juul = types.ReplyKeyboardMarkup(resize_keyboard=True)
tastes_17 = types.KeyboardButton('Манго')
tastes_18 = types.KeyboardButton('Мята')
tastes_19 = types.KeyboardButton('Табак')
tastes_20 = types.KeyboardButton('Табак Вирджиния')
tastes_21 = types.KeyboardButton('Фруктовый микс')
tastes_juul.add(tastes_17, tastes_18)
tastes_juul.add(tastes_19, tastes_20)
tastes_juul.add(tastes_21)
# Вкусы

# Этап заказа 0 - товар 1 - вкус 2 - город 3 - количество HQD
user_dict = {}
class User:
    def __init__(self, city):
        self.city = city

        keys = ['name', 'taste', 'country', 
                'amount']
        
        for key in keys:
            self.key = None

def enterAmount(message):
	try:
		chat_id = message.chat.id
		chat_message = int(message.text)

		user = user_dict[chat_id]
		user.amount = message.text
		
		inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
		inline = types.InlineKeyboardButton(text="Купить", callback_data='BUY')
		inline_keyboard.add(inline)
		if (user.id == '0'):
			bot.send_message(chat_id, "💁🏻‍♀️ Заказ *готов*!", parse_mode="Markdown", reply_markup=markup)
			Price = others.get_price_from_name(user.name)
			Price = Price * int(user.amount)
			bot.send_message(chat_id, f"*Товар:* {user.name}" +
				f"\n*Вкус:* {user.taste}\n*Цена:* {others.get_price_from_name(user.name)} ₽\n*Количество:* {user.amount}\n*К оплате:* {Price}\n"
				+ f"*Доставка в:* город {user.country}\n\nℹ️ После покупки данного товара с *Вами свяжется менеджер*", parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (user.id == '1'):
			name = user.name.split(" ")
			Price = others.get_price_from_name(name[1])
			Price = Price * int(user.amount)
			bot.send_message(chat_id, "💁🏻‍♀️ Заказ *готов*!", parse_mode="Markdown", reply_markup=markup)
			bot.send_message(chat_id, f"*Товар:* картридж {name[0]}\n*Упаковка:* {name[1]} шт.\n*Цена:* {others.get_price_from_name(user.name)} ₽\n"
				+ f"*Количество:* {user.amount}\n*К оплате:* {Price}\n*Доставка в:* город {user.country}\n\nℹ️ После покупки данного товара с *Вами свяжется менеджер*",
				parse_mode="Markdown", reply_markup=inline_keyboard)
		else:
			bot.send_message(chat_id, "😟 Заказ не был *найден*.", parse_mode="Markdown")
	except:
		pass

def enterCountry(message):
	try:
		chat_id = message.chat.id
		chat_message = message.text

		tastes = types.ReplyKeyboardRemove(selective=False)

		user = user_dict[chat_id]
		user.country = message.text

		msg = bot.send_message(chat_id, "💁🏻‍♀️ Введите *количество* которое хотите приобрести", parse_mode="Markdown", reply_markup=tastes)
		bot.register_next_step_handler(msg, enterAmount)
	except:
		pass

def enterTastes(message):
	try:
		chat_id = message.chat.id
		chat_message = message.text

		tastes = types.ReplyKeyboardRemove(selective=False)

		user = user_dict[chat_id]
		user.taste = message.text

		msg = bot.send_message(chat_id, "💁🏻‍♀️ Напишите Ваш *город*", parse_mode="Markdown", reply_markup=tastes)
		bot.register_next_step_handler(msg, enterCountry)
	except:
		pass

def enterCount(message):
	chat_id = message.chat.id
	count = message.text

	user = user_dict[chat_id]

	tastes = types.ReplyKeyboardRemove(selective=False)

	if (count == '2'):
		user.name += ' 2'
		msg = bot.send_message(chat_id, "💁🏻‍♀️ Напишите Ваш *город*", parse_mode="Markdown", reply_markup=tastes)
		bot.register_next_step_handler(msg, enterCountry)
	elif (count == '4'):
		user.name += ' 4'
		msg = bot.send_message(chat_id, "💁🏻‍♀️ Напишите Ваш *город*", parse_mode="Markdown", reply_markup=tastes)
		bot.register_next_step_handler(msg, enterCountry)
	else:
		bot.send_message(chat_id, "😟 Данной упаковки *нет в наличии*", parse_mode="Markdown")
# Этап заказа

# Этап заказа 0 - товар 1 - вкус 2 - город 3 - количество Juul
def enterTastesJuul(message):
	try:
		chat_id = message.chat.id
		chat_message = message.text

		tastes = types.ReplyKeyboardRemove(selective=False)

		user = user_dict[chat_id]
		user.taste = message.text

		msg = bot.send_message(chat_id, "💁🏻‍♀️ Напишите Ваш *город*", parse_mode="Markdown", reply_markup=tastes)
		bot.register_next_step_handler(msg, enterCountry)
	except:
		pass
# Этап заказа 0 - товар 1 - вкус 2 - город 3 - количество Juul

# Показ реферала
def getReferal(message):
	referal = message.text
	chat_id = message.chat.id
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (referal,)).fetchall()
			for row in result:
				if (row[3] != 0):
					bot.send_message(chat_id, f"💁🏻‍♀️ Реферал пользователя {referal} является *ID: {row[3]}*", parse_mode="Markdown")
					break
				else:
					bot.send_message(chat_id, "😟 Реферал *не найден*", parse_mode="Markdown")
	except:
		pass
# Показ реферала

# Пополние
def session_cp(chat_id):
	try:
		end = datetime.now() + timedelta(minutes = 30)
		api_start = True

		while (api_start == True):

			if (datetime.now() >= end):
				api_start = False
				bot.send_message(chat_id, "💁🏻‍♀️ Время на пополнение баланса *истекло.* Повторите попытку позже.", parse_mode="Markdown")
				others.user_delete_bill(chat_id)
	except:
		pass

def create_session_cp(chat_id):
	try:
		x = threading.Thread(target = session_cp, args=(chat_id,))
		x.start()
	except:
		pass

def notification(user_id, payment):
	try:
		worker = others.found_worker(user_id)
		username = ''

		if (worker != 0) and (worker != admin_user_id):
			bot.send_message(worker, f"💞 Успешное *пополнение*\nПоздравляю!\n\n🚀 *Пользователь:* {user_id} ([@{others.name_from_id(user_id)}])\n💸 *Сумма:* {payment} ₽", parse_mode="Markdown")
			username = f'{worker} (@[{others.name_from_id(worker)}])'
		elif (worker == 0):
			username = 'не найден'
			
		bot.send_message(admin_user_id, f"💞 Успешное *пополнение*\nПоздравляю!\n\n🚀 *Пользователь:* {user_id} ([@{others.name_from_id(user_id)}])\n💸 *Сумма:* {payment} ₽\n"
			+ f"👨‍💻 *Воркер:* {username}", parse_mode="Markdown")
		bot.send_message(channel_id, f"💞 Успешное *пополнение*\nПоздравляю!\n\n🚀 *Пользователь:* {user_id} ([@{others.name_from_id(user_id)}])\n💸 *Сумма:* {payment} ₽\n"
			+ f"👨‍💻 *Воркер:* {username}", parse_mode="Markdown")
	except:
		pass

def session(chat_id):
	try:
		api = QApi(token=others.token, phone=others.phone)
		price = 1

		code = f'{bill_create(5)}_{random.randint(0, 999999999)}'
		if (code in in_comment):
			code += f'{random.randint(0, 999)}'
		else:
			in_comment.append(code)

		others.create_bill_id(chat_id, code)
		comment = api.bill(price, code)

		inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
		inline = types.InlineKeyboardButton(text="Перейти к оплате", url=f'https://qiwi.com/payment/form/99?extra[%27account%27]=+{others.phone}&amountInteger=1&amountFraction=0&currency=643&extra[%27comment%27]={others.user_bill_id(chat_id)}&blocked[0]=account&blocked[1]=comment')
		inline_keyboard.add(inline)
		bot.send_message(chat_id, f"💁🏻‍♀️ Пополнение *баланса* QIWI\n\nЛицевой счёт: `{others.phone}`\nПримечание: `{comment}`\nМинимальный перевод: *{price}* ₽\n\nℹ️ Вы можете воспользоваться ссылкой для быстрого пополнения кошелька", parse_mode="Markdown", reply_markup=inline_keyboard)
		api.start() 

		api_start = True
		end = datetime.now() + timedelta(minutes = 5)
		while (api_start == True):
			if (datetime.now() >= end):
				api_start = False
				bot.send_message(chat_id, "💁🏻‍♀️ Время на пополнение баланса истекло. Повторите попытку позже.")
				others.user_delete_bill(chat_id)
				api.stop()

			if api.check(comment):
				json_data = api.payments['data']
				payment = ''
				for x in json_data:
					if (x['comment']) == comment:
						payment = x['sum']['amount']
						bot.send_message(chat_id, f"💁🏻‍♀️ Пополнение баланса *завершено*\n\nПополнение счета на сумму *{payment}* ₽ успешно завершено.", parse_mode="Markdown")
						others.user_update_balance(chat_id, int(payment))
						
						notification(chat_id, payment)

						others.user_delete_bill(chat_id)
						api.stop()
						api_start = False
						break
	except:
		pass

def create_session(chat_id):
	if (others.user_exists_bill(chat_id) == False):
		x = threading.Thread(target=session, args=(chat_id,))
		x.start()
	else:
		bot.send_message(chat_id, "💁🏻‍♀️ У вас есть *активная* сессия. Для создания новой, Вы должны завершить предыдущую сессию.", parse_mode="Markdown")

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

def bill_create(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def enterDeposit(message):
	try:
		price = message.text
		chat_id = message.chat.id
		if (is_digit(price) == True):

			if (int(price) >= 200):
				request = requests.get(f'https://api.crystalpay.ru/api.php?s={others.secret}&n={others.login}&o=generate&amount={price}')
				js = request.json()

				url = js['url']
				code = js['id']

				others.create_bill_id(chat_id, code)
				create_session_cp(chat_id)

				inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
				inline_1 = types.InlineKeyboardButton(text="Перейти к оплате", url=f'{url}')
				inline_2 = types.InlineKeyboardButton(text="Проверить", callback_data=f'CHECK-{code}')
				inline_keyboard.add(inline_1, inline_2)
				bot.send_message(chat_id, f"ℹ️ После *оплаты* нажмите кнопку «Проверить»", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			else:
				bot.send_message(chat_id, "💁🏻‍♀️ Пополнение баланса через этот метод начинается от *200 рублей*", parse_mode="Markdown")
		else:
			bot.send_message(chat_id, "💁🏻‍♀️ Ошибка: укажите *сумму* пополнения", parse_mode="Markdown")
	except:
		pass
# Пополние платежной системой

def user_invite_code(message):
	try:
		code = message.text
		chat_id = message.chat.id
		if (is_digit(code) == True):
			if (others.user_exists(code) == True):
				others.user_update_referal(chat_id, code)
				bot.send_message(chat_id, "💁🏻‍♀️ Здорово! Вы получили бонус в размере *50* рублей!", parse_mode="Markdown")
				bot.send_message(code, f"❤️ /{chat_id} использовал твой *код-приглашение*", parse_mode="Markdown")
			else:
				bot.send_message(chat_id, "💁🏻‍♀️ Код-приглашение *не найден*", parse_mode="Markdown")
		else:
			bot.send_message(chat_id, "💁🏻‍♀️ Код-приглашение *не найден*", parse_mode="Markdown")
	except:
		pass

@bot.message_handler(commands=['start'])  
def start_command(message):
	chat_id = message.chat.id
	command = message.text
	user_name = message.from_user.username

	if (not others.user_exists(chat_id)):
		if 'ref' in command:
			command = command.split('ref')
			others.user_add_ref(chat_id, user_name, command[1])
			bot.send_message(command[1], f"❤️ /{chat_id} зарегистрировался используя Вашу *реф. ссылку*", parse_mode="Markdown")
		else:
			others.user_add(chat_id, user_name)

	bot.send_message(chat_id, f"💁🏻‍♀️ Привет, *{message.from_user.first_name}*!\n\nРады тебя видеть в нашем магазине!"
		+ " У нас очень хороший выбор товара, каждый найдет для себя что-то своё! Мы будем рады *Вашим* покупкам!\n\n🦄 Если не появились вспомогательные кнопки, введите /start",
		parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	chat_message = message.text
	chat_id = message.chat.id

	if (chat_message == "💁🏻‍♀️ Мой профиль"):
		inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
		inline = types.InlineKeyboardButton(text="Пополнить баланс", callback_data='DEPOSIT')
		inline_keyboard.add(inline)
		bot.send_message(chat_id, f"💁🏻‍♀️ *Твой* профиль\n\n🚀 Telegram ID: *{chat_id}*\n💵 Баланс: {others.user_balance(chat_id)} ₽" +
			f"\n\n💸 *Количество покупок:* 0\n🤝 *Приглашено*: {others.user_count_ref(chat_id)} пользователей\n💰 *Заработано:* 0 ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
	elif (chat_message == "♻️ Вопрос - Ответ"):
		inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
		inline = types.InlineKeyboardButton(text="Менеджер", url=f'https://t.me/{others.manager}')
		inline_keyboard.add(inline)
		text = str("💁🏻‍♀️ *Ответы* на часто задаваемые вопросы\n\nQ: *Вы продаете если нет 18 лет?*\nA: *Мы не требуем никаких документов для подтверждения Вашего возраста*" + 
			f"\n\nQ: *Как я получу свой HQD?*\nA: *В большинство городах работают курьеры, которые и доставят Вам максимально быстро и куда угодно*" +
			f"\n\nQ: *Что делать если моего города нет в списке?*\nA: *Напишите менеджеру, он решит Вашу проблему*" +
			f"\n\nQ: *Как оплатить товар?*\nA: *Мы принимаем только на QIWI Кошелек. Вам нужно будет просто пополнить баланс и посмотреть наш Каталог товаров*" +
			f"\n\nQ: *Оригинал или подделка?*\nA: *В нашем магазине исключительно представлен оригинальный продукт*" +
			f"\n\nℹ️ Если у Вас остались какие-то вопросы пишите менеджеру. Мы попробуем решить Вашу проблему.")
		
		bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=inline_keyboard)
	elif (chat_message == "💠 Отзывы"):
		bot.send_message(chat_id, f"💁🏻‍♀️ *Отзывы* о нас\n\nПосмотреть отзывы Вы можете в нашей группе: [{others.group}]",
			parse_mode="Markdown")
	elif (chat_message == "🚀 Каталог"):
		bot.send_message(chat_id, "💁🏻‍♀️ Выберите *категорию* которую хотите приобрести", parse_mode="Markdown",
			reply_markup=product)
	elif (chat_message == "🍭 Товары Juul"):
		product_juul = types.ReplyKeyboardMarkup(resize_keyboard=True)
		product_1 = types.KeyboardButton('POD-системы JUUL')
		product_2 = types.KeyboardButton('Картриджи JUUL')
		back = types.KeyboardButton('Назад')
		product_juul.add(product_1, product_2)
		product_juul.add(back)
		bot.send_message(chat_id, "💁🏻‍♀️ Выберите категорию товара *Juul*", parse_mode="Markdown", reply_markup=product_juul)
	elif (chat_message == "POD-системы JUUL"):
		product_pod = types.ReplyKeyboardMarkup(resize_keyboard=True)
		product_1 = types.KeyboardButton('Juul Promo Kit')
		product_2 = types.KeyboardButton('Juul Starter Kit')
		product_3 = types.KeyboardButton('Juul Device Kit')
		back = types.KeyboardButton('Назад')
		product_pod.add(product_1, product_2)
		product_pod.add(product_3, back)

		bot.send_message(chat_id, "💁🏻‍♀️ Ниже предоставлены *POD-системы* Juul", parse_mode="Markdown", 
			reply_markup=product_pod)
	elif (chat_message == "Картриджи JUUL"):
		product_catridge = types.ReplyKeyboardMarkup(resize_keyboard=True)
		product_1 = types.KeyboardButton('Манго x2 / x4')
		product_2 = types.KeyboardButton('Фруктовый микс x2 / x4')
		product_3 = types.KeyboardButton('Ваниль x2 / x4')
		product_4 = types.KeyboardButton('Табак x2 / x4')
		product_5 = types.KeyboardButton('Мята x2 / x4')
		product_6 = types.KeyboardButton('Табак Вирджиния x2 / x4')
		back = types.KeyboardButton('Назад')
		product_catridge.add(product_1, product_2)
		product_catridge.add(product_3, product_4)
		product_catridge.add(product_5, product_6)
		product_catridge.add(back)

		bot.send_message(chat_id, "💁🏻‍♀️ Ниже предоставлены *сменные картриджи* Juul", parse_mode="Markdown",
			reply_markup=product_catridge)
	elif (chat_message == "🍇 Товары HQD"):
		product_hqd = types.ReplyKeyboardMarkup(resize_keyboard=True)
		product_1 = types.KeyboardButton('HQD Cuvie')
		product_2 = types.KeyboardButton('HQD Stark')
		product_3 = types.KeyboardButton('HQD V2')
		product_4 = types.KeyboardButton('HQD Cuvie Plus')
		product_5 = types.KeyboardButton('HQD Maxim')
		product_6 = types.KeyboardButton('HQD Ultra Stick')
		back = types.KeyboardButton('Назад')
		product_hqd.add(product_1, product_2)
		product_hqd.add(product_3, product_4)
		product_hqd.add(product_5, product_6)
		product_hqd.add(back)
		bot.send_message(chat_id, "💁🏻‍♀️ Выберите нужный Вам *HQD*", parse_mode="Markdown", reply_markup=product_hqd)
	elif (chat_message == "Назад"):
		bot.send_message(chat_id, "💁🏻‍♀️ Вы вернулись в *главное* меню", parse_mode="Markdown",
			reply_markup=markup)
	elif ('HQD' in chat_message):
		try:
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			episodes = chat_message.split(" ")
			if (episodes[1] == "Cuvie"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Cuvie')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 300 - 400\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (episodes[1] == "Stark"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Stark')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 300\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (episodes[1] == "V2"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='V2')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 200 - 300\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (episodes[1] == "Cuvie Plus"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='CuviePlus')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 500 - 600\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (episodes[1] == "Ultra"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Ultra')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 500\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (episodes[1] == "Maxim"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Maxim')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n"
					+ f"*Корпус:* Пластиковый\n*Испаритель:* Одноразовый\n*Затяжек:* 400\n*Никотин:* 50 МГ (солевой)\n*Стоимость:* {others.get_price_from_name(chat_message)}", parse_mode="Markdown", reply_markup=inline_keyboard)
			else:
				bot.send_message(chat_id, "😟 Товар *не найден*", parse_mode="Markdown")
		except:
			pass
	elif ('Juul' in chat_message):
		try:
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			episodes = chat_message.split(" ")

			if (episodes[1] == "Promo"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Promo')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n*Артикул:* 202190\n*Бренд:* JUUL Labs\n*Цвет:* Графит\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			elif (episodes[1] == "Starter"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Starter')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n*Артикул:* 212591\n*Бренд:* JUUL Labs\n*Цвет:* Графит\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			elif (episodes[1] == "Device"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Device')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Информация о *{chat_message}*\n\n*Артикул:* 105593\n*Бренд:* JUUL Labs\n*Цвет:* Графит\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
		except:
			pass
	elif ('x2 / x4' in chat_message):
		try:
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			episodes = chat_message.split(" ")

			if (episodes[0] == "Манго"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Mango')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			if (episodes[0] == "Фруктовый"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Mix')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			if (episodes[0] == "Ваниль"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Vanilla')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			if (episodes[0] == "Табак"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Tobacco')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			if (episodes[0] == "Мята"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Mint')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
			if (episodes[2] == "Вирджиния"):
				inline = types.InlineKeyboardButton(text="Заказать", callback_data='Virginia')
				inline_keyboard.add(inline)
				bot.send_message(chat_id, f"💁🏻‍♀️ Сменный картридж *{episodes[0]} {episodes[1]}*\n\n*Крепкость:* 5%\n*Бренд:* JUUL Labs\n*Упаковка:* 2 или 4 пода\n*Стоимость:* {others.get_price_from_name(chat_message)} ₽", parse_mode="Markdown",
					reply_markup=inline_keyboard)
		except:
			pass
	elif (chat_message == "🎭 Реф. система"):
		inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
		inline = types.InlineKeyboardButton(text="Статистика моих рефералов", callback_data='REFERAL')
		inline_keyboard.add(inline)
		bot.send_message(chat_id, "💁🏻‍♀️ *Реферальная* система\n\nПриглашайте новых пользователей и получайте пассивный доход от успешных операций ваших рефералов!"
			+ f"\n\nИспользуйте уникальную реферальную ссылку для приглашения пользователей. Для достижения высоких результатов, внимательно подходите к поиску целевой аудитории: *привлекайте только тех, кто будет покупать наши услуги.*\n\n[https://t.me/{others.bot_name}?start=ref{chat_id}]", parse_mode="Markdown",
			reply_markup=inline_keyboard)
	elif (chat_message == "Реферал") and (chat_id == admin_user_id):
		msg = bot.send_message(chat_id, "💁🏻‍♀️ Впишите User Id")
		bot.register_next_step_handler(msg, getReferal)
	elif (chat_message == "🎉 Бонус"):
		worker = others.found_worker(chat_id)
		if (worker != 0):
			bot.send_message(chat_id, "💁🏻‍♀️ Вы уже получили бонус в размере *50* ₽", parse_mode="Markdown")
		else:
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Ввести код-приглашение", callback_data=f'SEND_CODE')
			inline_keyboard.add(inline)
			bot.send_message(chat_id, "💁🏻‍♀️ Чтобы получить бонус в размере *50* ₽ нужно ввести *код-приглашение* друга", parse_mode="Markdown", reply_markup=inline_keyboard)
	elif ('/' in chat_message):
		user_id = chat_message.split("/")
		user_id = user_id[1]

		if (others.found_worker(user_id) == chat_id):
			name = others.name_from_id(user_id)
			if ('_' in name):
				name = name.replace('_', '\\_')

			bot.send_message(chat_id, f"Информация о пользователе *{user_id}*\n\n*Пользователь:* @{name}\n"
				+ f"*Баланс:* {others.user_balance(user_id)} ₽", parse_mode="Markdown")
	else:
		bot.send_message(chat_id, "💁🏻‍♀️ *Неизвестная* команда", parse_mode="Markdown", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	chat_id = call.message.chat.id
	try:
		if (call.data) == "Cuvie":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD Cuvie'
			
			user.id = '0'

			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD Cuvie*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)
		elif (call.data) == "Stark":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD Stark'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD Stark*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)
		elif (call.data) == "V2":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD V2'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD V2*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)
		elif (call.data) == "CuviePlus":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD Cuvie Plus'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD Cuvie Plus*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)
		elif (call.data) == "Ultra":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD Ultra Stick'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD Ultra Stick*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)		
		elif (call.data) == "Maxim":
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'HQD Maxim'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *HQD Maxim*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes)
			bot.register_next_step_handler(msg, enterTastes)
		elif (call.data == "Promo"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Juul Promo Kit'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *Juul Promo Kit*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes_juul)
			bot.register_next_step_handler(msg, enterTastesJuul)
		elif (call.data == "Device"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Juul Device Kit'
			user.id = '0'

			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *Juul Device Kit*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes_juul)
			bot.register_next_step_handler(msg, enterTastesJuul)
		elif (call.data == "Starter"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Juul Starter Kit'
			user.id = '0'
			
			msg = bot.send_message(chat_id, "💁🏻‍♀️ Этап покупки *Juul Starter Kit*\n\nВыберите *вкус*", parse_mode="Markdown", reply_markup=tastes_juul)
			bot.register_next_step_handler(msg, enterTastesJuul)	
		elif (call.data) == "CANCEL":
			bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
		elif (call.data == "DEPOSIT"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline_1 = types.InlineKeyboardButton(text="Прямой перевод QIWI 0%", callback_data='QIWI')
			inline_2 = types.InlineKeyboardButton(text="Crystal Pay (Card, Yandex, Qiwi) 2%", callback_data='CARD')
			inline_keyboard.add(inline_1, inline_2)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💁🏻‍♀️ Пополнение *баланса*\n\nВыберите желаемый метод пополнения", parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (call.data) == "QIWI":
			try:
				create_session(chat_id)
			except:
				pass
		elif (call.data) == "CARD":
			if (others.user_exists_bill(chat_id) == False):
				msg = bot.send_message(chat_id, f"💁🏻‍♀️ Введите *сумму пополнения* баланса. Минимальное пополнение — *200 рублей*", parse_mode="Markdown")
				bot.register_next_step_handler(msg, enterDeposit)		
			else:
				bot.send_message(chat_id, "💁🏻‍♀️ У вас есть *активная* сессия. Для создания новой, Вы должны завершить предыдущую сессию.", parse_mode="Markdown")
		elif (call.data) == "BUY":
			chat_message = call.message.text
			chat_message = chat_message.split("\n")
			price_split = chat_message[4].split(":")
			price = int(price_split[1])
			others.user_un_balance(chat_id, price)
			if (others.user_un_balance(chat_id, price) == True):
				bot.send_message(chat_id, "💁🏻‍♀️ Товар *успешно* куплен. Ваша заявка в очереди, с Вами свяжется спец-менеджер.", parse_mode="Markdown")
			else:
				bot.send_message(chat_id, "💁🏻‍♀️ Ошибка покупки: *недостаточно* средств на балансе.", parse_mode="Markdown")
		elif (call.data) == "REFERAL":
			if (others.user_count_ref(chat_id) > 0):
				ref_ = ''
				for referal in others.user_referals(chat_id):
					ref_ += f"{referal}\n"
				
				bot.send_message(chat_id, f"💁🏻‍♀️ *Ваши* рефералы\n\nКоличество приглашенных: *{others.user_count_ref(chat_id)}*\nЗаработано: *0* ₽\n\nДля достижения высоких результатов, внимательно подходите к поиску целевой аудитории: *привлекайте только тех, кто будет покупать наши услуги.*\n\n*Telegram ID:*`\n{ref_}`",
						parse_mode="Markdown")
			else:
				bot.send_message(chat_id, "💁🏻‍♀️ У вас нет *рефералов*\n\nИспользуйте свою реферальную ссылку для привлечения новых пользователей и зарабатывайте на этом!", parse_mode="Markdown")		
		elif ("CHECK-" in call.data):
			code = call.data
			code = code.split("-")
			code = code[1]
			
			request = requests.get(f'https://api.crystalpay.ru/api.php?s={others.secret}&n={others.login}&o=checkpay&i={code}')
			js = request.json()

			if (js['state'] == "payed"):
				payment = int(js['amount'])

				bot.send_message(chat_id, f"💁🏻‍♀️ Пополнение баланса *завершено*\n\nПополнение счета на сумму *{payment}* ₽ успешно завершено.", parse_mode="Markdown")
				others.user_update_balance(chat_id, int(payment))

				notification(chat_id, payment)

				others.user_delete_bill(chat_id)
				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
			else:
				bot.send_message(chat_id, "😟 Платеж *не был найден.* Повторите попытку снова или свяжитесь с поддержкой", parse_mode="Markdown")				
		elif (call.data == "Mango"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Манго'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "Mix"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Микс'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "Vanilla"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Ваниль'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "Mint"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Мята'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "Tobacco"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Табак'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "Virginia"):
			inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
			inline = types.InlineKeyboardButton(text="Отменить покупку", callback_data='CANCEL')
			inline_keyboard.add(inline)

			user_dict[chat_id] = User(chat_id)
			user = user_dict[chat_id]
			user.name = 'Вирджиния'
			user.id = '1'
			
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Этап покупки картридж *{user.name}*\n\nВыберите упаковку _(2 или 4)_", parse_mode="Markdown")
			bot.register_next_step_handler(msg, enterCount)	
		elif (call.data == "SEND_CODE"):
			msg = bot.send_message(chat_id, f"💁🏻‍♀️ Бонус *50* ₽\n\nВведите *код-приглашение*", parse_mode="Markdown")
			bot.register_next_step_handler(msg, user_invite_code)	
	except:
		pass
	



bot.polling(none_stop = True, interval = 0)	