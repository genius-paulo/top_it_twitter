#!/usr/bin/python3.6
# encoding: utf-8

import tweepy
import time
import telebot
import re 
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from wand.image import Image as ImageW
from wand.drawing import Drawing
from wand.font import Font as FontW
#import vk
#import json
#from telethon.sync import TelegramClient, events
#import socks

#Twitter API доступы
consumer_key = 
consumer_secret = 
access_key = 
access_secret = 

# Доступы для Telegram
bot = telebot.TeleBot("")
token = ""
url = "https://api.telegram.org/bot"
channel_id = ""
url += token
method = url + "/sendMessage"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

userIDArr = ["nocchka", "nat_davydova", "BasicAppleGuy", "tproger", "hromoi_edinorog", "naera_meir", "bunopus", "aarexer", "_bravit", "vie_fastueuse", "iammemeloper", "iamdevloper", "darkgaro", "jaredpalmer", "avdeev_alexey", "computerfact", "el_platono", "sparenica"]

# Определяем нужные нам даты
startDate = datetime.now() - timedelta(days=1)
endDate = datetime.now()

# Пишем, какие даты мы берём
print("Меня интересуют твиты с " + str(startDate) + " и до " + str(endDate) + "\n")

#Объявляем массив для ID/лайков
likesIDArr = []

# Пробегаемся по всем пользователям из списка
for userID in userIDArr:
	# Получаем все твиты пользователя без реплаев и ретвитов
	tweets = api.user_timeline(screen_name = userID, include_rts = False, exclude_replies=True, tweet_mode = 'extended')

	# Пременная, чтобы считать количество подходящих твитов
	goodTweetsUser = 0

	#Заполняем  массив с ID твита и кол-вом лайков
	for info in tweets:
		status = api.get_status(info.id, include_entities = True, tweet_mode = "extended")
		if info.created_at > startDate and info.created_at < endDate and 'media' in status.entities:
			if  'video_info' not in status.extended_entities["media"][0]:
				likesIDArr.append([info.favorite_count, info.id])
				# Увеличиваем счётчик «хороших» твитов
				goodTweetsUser = goodTweetsUser + 1
		elif info.created_at > startDate and info.created_at < endDate and 'media' not in status.entities:
			likesIDArr.append([info.favorite_count, info.id])
			# Увеличиваем счётчик «хороших» твитов
			goodTweetsUser = goodTweetsUser + 1

	if len(likesIDArr) != 0:
		# Отчитываемся, сколько твитов у пользователя
		print("У " + userID + " " + str(goodTweetsUser) + " подходящих твитов")
	else:
		print("У " + userID + " нет подходящих твитов")


# Добавляем конкретный твит для проверки
"""
testID = '1550442492323045376'
testTweet = api.get_status(testID, include_entities = True, tweet_mode = "extended")
likesIDArr.append([testTweet.favorite_count, testTweet.id])
print("\nДобавляю тестовый твит " + testID)
"""

print("\nВсего " + str(len(likesIDArr)) + " твитов без видео, опубликованных с ", str(startDate) + " по " + str(endDate) + "\n")

print("\nОтправляю твиты:")

# Проверяем список на пустоту, только тогда двигаемся дальше
if len(likesIDArr) != 0:
	# Сортируем массив по убыванию лайков
	likesIDArr.sort(key = lambda x: x[0], reverse=True)
	print("Сортирую твиты")
	# Сколько максимально твитов нам нужно?
	topTweetsCount = 10
	# Проверяем, есть ли столько вообще. Если нет — публикуем сколько есть.
	if len(likesIDArr) < 10:
		topTweetsCount = len(likesIDArr)

	print("Нам нужно максимум 10 твит, а у нас есть ", topTweetsCount)

	# Выбираем и отправляем topTweetsCount твитов
	try:
		bot.send_message(chat_id=channel_id, text="Начинаю цикл подготовки постов")
		for i in range(topTweetsCount):
			# Присваиваем ID i-того твита из числа topTweetsCount
			id = likesIDArr[i][1]
			# Получаем всю информацию по твиту
			status = api.get_status(id, include_entities = True, tweet_mode = "extended")
			print("Твит ", id, " пользователя ", status.author.screen_name)
			full_text = re.sub(r'https://t.co/\w{10}', '', status.full_text)
			response = requests.get(status.author.profile_image_url)
			file = open("/home/GeniusPaulo/avatar.png", "wb")
			file.write(response.content)
			file.close()
			font = ImageFont.truetype("/home/GeniusPaulo/Roboto-Regular.ttf", size=48)

			print("Присваиваю ник автора")
			nickNameText = "@" + status.author.screen_name
			print(nickNameText)
			print("Ждём 1 секунду")
			time.sleep(1)

			print("Рисую подложку под ником") # Здесь почему-то иногда вылазит ошибка corrupted size vs. prev_size и python3.6: malloc.c:3839: _int_malloc: Assertion `chunk_main_arena (bck->bk)' failed.
			nickNameTextWidth = font.getsize(nickNameText)[0]
			print("Длину текста замерить удалось")
			print("Сейчас длина ника равна " + str(nickNameTextWidth))
			x2 = nickNameTextWidth + 200
			print("Ждём 1 секунду")
			time.sleep(1)
			print("А длина подложки ", x2)

			# Только здесь открываем изображение, мало ли, именно это влияет на ошибку
			image = Image.open('/home/GeniusPaulo/background.jpg')
			draw = ImageDraw.Draw(image)

			print("Рисую прямоугольник")
			draw.rectangle((0, 50, x2, 150), fill=('#00acee'))
			time.sleep(1)
			print("Рисую текст")
			draw.text((150, 70), nickNameText, font=font, fill='white')
			time.sleep(1)
			print("Сохраняю пикчу")
			image.save('/home/GeniusPaulo/pictureWithTweet.jpg')

			print("Обрезаю аватар")
			# Создаём маску для обрезки аватара по кругу
			size = (80, 80)
			mask = Image.new('L', size, 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0) + size, fill=255)
			# Обрезаем аватарку по кругу
			avatar = Image.open('/home/GeniusPaulo/avatar.png')
			avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
			avatar.putalpha(mask)
			avatar.save('/home/GeniusPaulo/avatarCircle.png')

			print("Накладываю аватар на общую пикчу")
			# Накладываем аватар на общее изображение и сохраняем
			avatar = Image.open('/home/GeniusPaulo/avatarCircle.png')
			image.paste(avatar, (50, 60), avatar)
			image.save('/home/GeniusPaulo/pictureWithTweet.jpg')
			# Возвращаем значение draw
			draw = ImageDraw.Draw(image)

			print("Накладываю вотермарку на общую пикчу")
			# Накладываем вотермарку
			nameText = "t.me/topittwit"
			# Рисуем подложку под ником
			draw.rectangle((750, 0, 1080, 50), fill=('#333333'))
			draw.text((780, -5), nameText, font=font, fill='white')

			# Если твит не пустой и есть пикча
			if len(full_text) != 0 and 'media' in status.entities:
				print('Здесь есть текст и пикча')

				# С помощью  wand  вмещаем текст в прямоугольник
				with ImageW(width=980, height=200, pseudo='xc:white') as canvas:
					left, top, width, height = 0, 0, 980, 200
					with Drawing() as context:
						context.fill_color = 'white'
						context.rectangle(left=left, top=top, width=width, height=height)
						font = FontW('/home/GeniusPaulo/Roboto-Regular.ttf')
						context(canvas)
						canvas.caption(full_text, left=left, top=top, width=width, height=height, font=font, gravity='north_west')
					canvas.save(filename='/home/GeniusPaulo/text.png')
				# И вставляем его на нашу пикчу
				textPicture = Image.open('/home/GeniusPaulo/text.png')
				image.paste(textPicture, (50, 200))

				# Рисуем подложку под пикчей
				draw.rectangle((0, 425, 1080, 1080), fill=('#F8F9F9'))

				# Скачиваем и сохраняем изображение
				response = requests.get(status.entities["media"][0]["media_url_https"])
				file = open("/home/GeniusPaulo/postPicture.png", "wb")
				file.write(response.content)
				file.close()
				postPicture = Image.open('/home/GeniusPaulo/postPicture.png')
				# Масштабируем пикчу на оставшееся пространство
				# Определяем высоту пикчи
				originalHeight = postPicture.size[1]
				# Задаём высоту оставшегося пространства — 40% поста
				freeSpaceHeight = 655
				# Определяем процент уменьшения
				percentScale = (freeSpaceHeight)/(originalHeight)
				# Если пикча больше пространства, уменьшаем её
				if percentScale < 1:
					width = int(postPicture.size[0] * percentScale)
					height = int(postPicture.size[1] * percentScale)
					newsize = (width, height)
					# Изменяем размер
					postPicture = postPicture.resize(newsize)
				# 1080 - freeSpaceHeight = начало вставки картинки
				# Вставляем сюда пикчу
				image.paste(postPicture, (540 - postPicture.size[0]//2, 425))

			# Также если нет текста, но есть пикча
			elif len(full_text) == 0 and ('media' in status.entities):
				print('Здесь есть только пикча')

				# Рисуем подложку под пикчей
				draw.rectangle((0, 400, 1080, 1080), fill=('#F8F9F9'))

				# Скачиваем и сохраняем изображение
				response = requests.get(status.entities["media"][0]["media_url_https"])
				file = open("/home/GeniusPaulo/postPicture.png", "wb")
				file.write(response.content)
				file.close()
				postPicture = Image.open('/home/GeniusPaulo/postPicture.png')
				# Масштабируем пикчу на оставшееся пространство
				# Определяем высоту пикчи
				originalHeight = postPicture.size[1]
				# Задаём высоту оставшегося пространства
				freeSpaceHeight = 880
				# Определяем процент уменьшения
				percentScale = (freeSpaceHeight)/(originalHeight)
				# Если пикча больше пространства, уменьшаем её
				if percentScale < 1:
					width = int(postPicture.size[0] * percentScale)
					height = int(postPicture.size[1] * percentScale)
					newsize = (width, height)
					# Изменяем размер
					postPicture = postPicture.resize(newsize)
				# 1080 - freeSpaceHeight = начало вставки картинки
				# Вставляем сюда пикчу
				image.paste(postPicture, (540 - postPicture.size[0]//2, 200))

			# Также если есть текст, но нет пикчи
			elif len(full_text) != 0 and 'media' not in status.entities:
				print('Здесь есть только текст')
				# С помощью  wand  вмещаем текст в прямоугольник
				with ImageW(width=980, height=880, pseudo='xc:white') as canvas:
					left, top, width, height = 0, 0, 980, 880
					with Drawing() as context:
						context.fill_color = 'white'
						context.rectangle(left=left, top=top, width=width, height=height)
						font = FontW('/home/GeniusPaulo/Roboto-Regular.ttf')
						context(canvas)
						canvas.caption(full_text, left=left, top=top, width=width, height=height, font=font, gravity='north_west')
					canvas.save(filename='/home/GeniusPaulo/text.png')
				# И вставляем его на нашу пикчу
				textPicture = Image.open('/home/GeniusPaulo/text.png')
				image.paste(textPicture, (50, 200))

			# Рисуем красивые линеечки
			draw.line((50, 180, image.size[0], 180), fill=('#333333'), width=2)

			draw.line((0, 0, 1080, 0), fill=('#333333'), width=1)
			draw.line((1079, 0, 1079, 1079), fill=('#333333'), width=1)
			draw.line((0, 1079, 1079, 1079), fill=('#333333'), width=1)
			draw.line((0, 0, 0, 1080), fill=('#333333'), width=1)

			# Сохраняем изображение
			image.save('/home/GeniusPaulo/pictureWithTweet.jpg')

			#Пробуем отправлять сообщение Telegram
			try:
				photo = open('/home/GeniusPaulo/pictureWithTweet.jpg', 'rb')
				bot.send_photo(channel_id, photo)
				bot.send_message(chat_id=channel_id, text="Пост Telegram успешно отправлен.")
			except Exception as error:
				errorText = "Пост Telegram не отправлен. Код ошибки:\n" + str(error)
				bot.send_message(chat_id=channel_id, text=errorText)

			"""
			#Пробуем отправлять сообщение VK
			try:
				photo = open('/home/GeniusPaulo/pictureWithTweet.jpg', 'rb')
				session = vk.Session(
					access_token='ee5f2b90ba9381dfa3b7ec128660b4e8eea489734c110317df41cf13547ec1ea02483b36a1ab526a3be17') # вместо 123abc свой токен
				vk_api = vk.API(session, v='5.85')
				groupID = '213409819'

				upload_url = vk_api.photos.getWallUploadServer(group_id=groupID)['upload_url']

				request = requests.post(upload_url, files={'photo': photo})
				params = {'server': request.json()['server'],
						  'photo': request.json()['photo'],
						  'hash': request.json()['hash'],
						  'group_id': groupID}


				data = vk_api.photos.saveWallPhoto(**params)

				photo_id = data [0]['id']

				params = {'attachments': 'photo'+ str(data [0]['owner_id']) + '_'+ str(photo_id),
						  'owner_id': '-' + groupID,
						  'from_group': '1'}
				vk_api.wall.post(**params)
				bot.send_message(chat_id=channel_id, text="Пост ВК успешно отправлен.")
			except Exception as error:
				errorText = "Пост в ВК не отправлен. Код ошибки:\n" + str(error)
				bot.send_message(chat_id=channel_id, text=errorText)

			print("Пробую подождать 3600 секунд или 1 час")

			try:
				bot.send_message(chat_id=channel_id, text="Пробую подождать 3600 секунд или 1 час")
				time.sleep(5)
			except Exception as error:
				errorText = "Дождаться не удалось. Код ошибки:\n" + str(error)
				bot.send_message(chat_id=channel_id, text=errorText)
		    """

	except Exception as error:
		errorText = "Что-то пошло не так. Код ошибки:\n" + str(error)
		bot.send_message(chat_id=channel_id, text=errorText)
