import telebot
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from app.const import USER_STEP
from app.models import TgUser, Barber, NearBarber
from app.services import enter_phone_number, enter_address, choice_section, enter_name, \
    show_barber, confirm, start_mess, print_barber

bot = telebot.TeleBot(token='1172780082:AAG-ywdQ9Om-Byg-ULPohKosjCgzOKTItK0')


# @sartaroshxonabot

# telegram click connect token
# 398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065

# 567316052:AAHaOLbcFq_I3kNkM4Qwc6QJczZJcgYD7VI
# @nontechbot

class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    start_mess(message, bot)


@bot.message_handler(content_types=['location'])
def read_location(message):
    enter_address(message, bot)


@bot.message_handler(content_types=['contact'])
def read_contact(message):
    enter_phone_number(message, bot)


@bot.message_handler(regexp='◀️ Bosh menyu qaytish')
def back_menu(message):
    user = TgUser.objects.filter(user_id=message.from_user.id).get()
    user.step = USER_STEP['CHOICE']
    user.save()
    start_message(message)


@bot.message_handler(regexp='♻️Yangilash')
def back_menu(message):
    user = TgUser.objects.get(user_id=message.from_user.id)
    Barber.objects.filter(user=user).delete()
    start_message(message)


@bot.message_handler(content_types=['text'])
def text_message(message):
    switcher = {
        USER_STEP['DEFAULT']: start_mess,
        USER_STEP['CHOICE']: choice_section,
        USER_STEP['ENTER_NAME']: enter_name,
        USER_STEP['ENTER_PHONE_NUMBER']: enter_phone_number,
        USER_STEP['ENTER_ADDRESS']: enter_address,
        USER_STEP['CONFIRM']: confirm,
        USER_STEP['SHOW_BARBERS']: show_barber,
    }
    print(TgUser.objects.filter(user_id=message.from_user.id).last().step)
    func = switcher.get(TgUser.objects.filter(user_id=message.from_user.id).last().step, lambda: start_message(message))
    func(message, bot)


@bot.callback_query_handler(func=lambda c: True)
def inline_handler(message):
    current_user = TgUser.objects.get(user_id=message.from_user.id)
    near_barbers = NearBarber.objects.filter(user=current_user).order_by('length')

    user_id = int(message.data.split('/')[0])
    near_barber_id = int(message.data.split('/')[1])
    user = TgUser.objects.filter(user_id=user_id).first()

    if message.data.endswith('contact'):
        text = 'Aloqa uchun\n' + str(user.number)
        if user.username:
            text += " [" + str(user.username) + "](tg://user?id=" + str(
                user.user_id) + ")"
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
        bot.send_message(message.from_user.id, text, parse_mode='Markdown', reply_markup=reply_keyboard)
    elif message.data.endswith('oldingisi'):
        bot.delete_message(message.from_user.id, message.message.message_id)
        print_barber(message, bot, near_barber_id)
    elif message.data.endswith('keyingisi'):
        bot.delete_message(message.from_user.id, message.message.message_id)
        print_barber(message, bot, near_barber_id)
    else:
        pass

# for i in range(1, len(data), 2):
#     product_name = re.search(r'✏ (.*)\d', data[i - 1][0]['text']).group(1)[:-2]
#     cart_qs = ""
#     if cart_qs:
#         if message.data == product_name + ' product_del':
#             cart_qs.delete()
#         elif message.data == product_name + ' product_minus':
#             cart_qs.qty -= 1
#             cart_qs.save()
#         elif message.data == product_name + ' product_plus':
#             cart_qs.qty += 1
#             cart_qs.save()
