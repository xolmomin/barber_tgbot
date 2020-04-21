from django.db.models import F
from math import sqrt

from .const import USER_STEP
from .models import TgUser, Barber, NearBarber
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def choice_section(message, bot):  # 1
    user = TgUser.objects.get(user_id=message.from_user.id)

    if message.text == 'Men Mijozman':
        user.check = False
        user.step = USER_STEP['SHOW_BARBERS']  # 7
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.add(KeyboardButton('Manzilni yuborish', request_location=True))
        reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
        bot.send_message(message.from_user.id, 'Manzilingizni yuboring', reply_markup=reply_keyboard)
    elif message.text == 'Men Sartaroshman':
        user.check = True
        if Barber.objects.filter(user=user).exists():
            reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_keyboard.add(KeyboardButton('◀️ qaytish'), KeyboardButton('♻️Yangilash'))

            bot.send_message(message.from_user.id, 'Siz sartaroshlar ro\'yhatida borsiz '
                                                   '\nMa\'lumotlaringizni yangilish uchun "yangilash" tugmasini bosing',
                             reply_markup=reply_keyboard)
        else:
            user.step = USER_STEP['ENTER_ADDRESS']  # 2
            reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_keyboard.add(KeyboardButton('Manzilni yuborish', request_location=True))
            reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
            bot.send_message(message.from_user.id, 'Manzilingizni yuboring', reply_markup=reply_keyboard)
    user.save()


def enter_address(message, bot):  # 3
    user = TgUser.objects.get(user_id=message.from_user.id)
    if message.location:
        user.longitude = str(message.location.longitude)
        user.latitude = str(message.location.latitude)
        # user.step = USER_STEP['ENTER_NAME']
        # user.save()

        if user.check:
            user.step = USER_STEP['ENTER_NAME']
        else:
            user.step = USER_STEP['SHOW_BARBERS']
            NearBarber.objects.filter(user=user).delete()
            barbers = Barber.objects.all()
            for barber in barbers:
                le = sqrt((float(user.latitude) - float(barber.user.latitude)) ** 2 + (
                        float(user.longitude) - float(barber.user.longitude)) ** 2)
                near_barber = NearBarber(user=user, barber=barber, length=le)
                near_barber.save()
        user.save()

        if user.step == USER_STEP['SHOW_BARBERS']:  # 7
            show_barber(message, bot)
        elif user.step == USER_STEP['ENTER_NAME']:  # 2
            reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
            bot.send_message(message.from_user.id, 'Ismingizni yuboring', reply_markup=reply_keyboard)
    else:
        user.step = USER_STEP['ENTER_ADDRESS']  # 3
        user.save()
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.add(KeyboardButton('Manzilni yuborish', request_location=True))
        reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
        bot.send_message(message.from_user.id, 'Manzilni to\'g\'ri yuboring', reply_markup=reply_keyboard)


def enter_name(message, bot):  # 2
    user = TgUser.objects.get(user_id=message.from_user.id)
    user.first_name = message.text
    user.step = USER_STEP['ENTER_PHONE_NUMBER']  # 4
    user.save()

    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(KeyboardButton('📞 Raqamni ulashish', request_contact=True))
    reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'))
    bot.send_message(message.from_user.id,
                     'O\'z raqamingizni xalqaro formatda yuboring (998xxxxxxxxx)'
                     ' yoki "📞 Raqamni ulashish " tugmasini bosing',
                     reply_markup=reply_keyboard)


def show_barber(message, bot):  # 7
    current_user = TgUser.objects.get(user_id=message.from_user.id)
    near_barbers = NearBarber.objects.filter(user=current_user).order_by('length')
    kon = 0
    for i in near_barbers:
        i.sort_by_leng = kon
        kon += 1
        i.save()
    if near_barbers:
        print_barber(message, bot, 0)
    else:
        bot.send_message(message.from_user.id, 'Hozircha Sartaroshlar yo\'q')


def print_barber(message, bot, k):
    current_user = TgUser.objects.get(user_id=message.from_user.id)
    prev = NearBarber.objects.filter(sort_by_leng=k - 1, user=current_user).first()
    next = NearBarber.objects.filter(sort_by_leng=k + 1, user=current_user).first()
    current = NearBarber.objects.filter(sort_by_leng=k, user=current_user).first()
    text = f'Yaqin {k + 1}-sartarosh\n'
    if current.barber.user:
        text += current.barber.user.first_name

    inline_keyboard_markup = InlineKeyboardMarkup(2)
    inline_keyboard_markup.row(
        InlineKeyboardButton('Bog\'lanish',
                             callback_data=str(current.barber.user) + '/' + str(
                                 current.sort_by_leng) + '/show contact'))
    if prev:
        inline_keyboard_markup.row(
            InlineKeyboardButton('⬅ oldingi', callback_data=str(current.barber.user) + '/' + str(k - 1) + '/oldingisi'))

    if next:
        inline_keyboard_markup.row(
            InlineKeyboardButton('keyingi ➡', callback_data=str(current.barber.user) + '/' + str(k + 1) + '/keyingisi'))

    # kid' if age < 18 else 'adult'

    bot.send_message(message.from_user.id, text, parse_mode='Markdown', reply_markup=inline_keyboard_markup)


def enter_phone_number(message, bot):  # 4
    if message.contact:
        phone_num = message.contact.phone_number
    else:
        phone_num = message.text
    if phone_num.isdigit() and len(phone_num) == 12:
        TgUser.objects.filter(user_id=message.from_user.id).update(number=int(phone_num))
        user = TgUser.objects.filter(user_id=message.from_user.id).get()
        user.step = USER_STEP['CHOICE']  # 1
        user.save()
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.row(KeyboardButton('◀️ Bosh menyu qaytish'))
        Barber.objects.get_or_create(user=user)
        bot.send_message(message.from_user.id, 'Siz sartaroshlar ro\'yhatiga qo\'shildingiz\n'
                                               'Rahmat \n'
                                               'Endi mijozlar sizga o\'zlari murojaat qilishadi',
                         reply_markup=reply_keyboard)

    else:
        bot.send_message(message.from_user.id, 'Nomeringizni to\'g\'ri kiriting')


def confirm(message, bot):  # 6
    user = TgUser.objects.filter(user_id=message.from_user.id).get()
    user.step = USER_STEP['CONFIRM']  # 6
    user.save()
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(KeyboardButton('◀️ Bosh menyu qaytish'), KeyboardButton('♻️Yangilash'))

    bot.send_message(message.from_user.id, 'Siz sartaroshlar ro\'yhatida borsiz '
                                           '\n ma\'lumotlaringizni yangilish uchun "yangilash" tugmasini bosing',
                     reply_markup=reply_keyboard)


def start_mess(message, bot):
    if TgUser.objects.filter(user_id=message.from_user.id).exists():
        TgUser.objects.filter(user_id=message.from_user.id).update(step=1, username=message.from_user.username)
    else:
        TgUser.objects.create(user_id=message.from_user.id, step=1, username=message.from_user.username)

    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    reply_keyboard.row(KeyboardButton('Men Mijozman'), KeyboardButton('Men Sartaroshman'))
    bot.send_message(message.from_user.id, 'Bo\'limni tanlang', reply_markup=reply_keyboard)
