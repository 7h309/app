import os
import random
import string
from flask import Flask, request
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(زيرو)
TOKEN = os.environ.get(8681664117:AAHOmLod5sozxgYJVv_iBifGEgR1QsdnWAo)
CHANNEL_USERNAME = os.environ.get(Z_7za)
bot = TeleBot(8681664117:AAHOmLod5sozxgYJVv_iBifGEgR1QsdnWAo)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    return "", 403

def unit_check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def unit_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("سوني")
    btn2 = KeyboardButton("ثلاثيات")
    btn3 = KeyboardButton("انستا")
    btn4 = KeyboardButton("سناب")
    btn5 = KeyboardButton("تيك توك")
    btn6 = KeyboardButton("الكل")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def unit_subscribe_keyboard():
    markup = InlineKeyboardMarkup()
    link = f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
    markup.add(InlineKeyboardButton("اشترك في القناة", url=link))
    markup.add(InlineKeyboardButton("تحقق من الاشتراك", callback_data="check_sub"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def unit_check_callback(call):
    if unit_check_subscription(call.from_user.id):
        bot.edit_message_text("تم التحقق. مرحباً بك.", call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "اختر أمرك:", reply_markup=unit_main_keyboard())
    else:
        bot.answer_callback_query(call.id, "لم تشترك بعد. اشترك ثم اضغط تحقق.", show_alert=True)

@bot.message_handler(commands=["start"])
def unit_start(message):
    if unit_check_subscription(message.from_user.id):
        bot.reply_to(message, "مرحباً بك. استخدم الأزرار:", reply_markup=unit_main_keyboard())
    else:
        link = f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
        bot.reply_to(message,
            f"يرجى الاشتراك في القناة أولاً:\n{link}\n\nبعد الاشتراك اضغط 'تحقق من الاشتراك'",
            reply_markup=unit_subscribe_keyboard())

def unit_sony_gen():
    results = []
    bases = ["abc", "xyz", "qwe", "asd", "zxc", "rty", "fgh", "vbn"]
    for base in bases[:3]:
        results.append(f"{base}@sony.com")
        results.append(f"{base}{random.randint(10,99)}@sony.com")
        results.append(f"{base}{random.choice(['x','z','v'])}@sony.com")
    return list(set(results))[:4]

def unit_three_gen():
    results = []
    chars = string.ascii_lowercase
    for _ in range(4):
        r = "".join(random.choices(chars, k=3))
        results.append(r)
        results.append(r + random.choice(["x","z","v","1","2"]))
    return list(set(results))[:4]

def unit_insta_gen():
    results = []
    for _ in range(4):
        name = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(4,7)))
        results.append(f"instagram.com/{name}")
    return results

def unit_snap_gen():
    results = []
    for _ in range(4):
        name = "".join(random.choices(string.ascii_lowercase, k=random.randint(4,8)))
        results.append(f"snapchat.com/add/{name}")
    return results

def unit_tiktok_gen():
    results = []
    for _ in range(4):
        name = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3,7)))
        results.append(f"tiktok.com/@{name}")
    return results

@bot.message_handler(func=lambda m: m.text in ["سوني", "ثلاثيات", "انستا", "سناب", "تيك توك", "الكل"])
def unit_handle_buttons(message):
    if not unit_check_subscription(message.from_user.id):
        link = f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
        bot.reply_to(message,
            f"أنت غير مشترك في القناة. اشترك أولاً:\n{link}",
            reply_markup=unit_subscribe_keyboard())
        return

    if message.text == "سوني":
        bot.reply_to(message, "\n".join(unit_sony_gen()))
    elif message.text == "ثلاثيات":
        bot.reply_to(message, "يوزرات شبه ثلاثية:\n" + "\n".join(unit_three_gen()))
    elif message.text == "انستا":
        bot.reply_to(message, "\n".join(unit_insta_gen()))
    elif message.text == "سناب":
        bot.reply_to(message, "\n".join(unit_snap_gen()))
    elif message.text == "تيك توك":
        bot.reply_to(message, "\n".join(unit_tiktok_gen()))
    elif message.text == "الكل":
        msg = "سوني:\n" + "\n".join(unit_sony_gen()) + "\n\n"
        msg += "ثلاثيات:\n" + "\n".join(unit_three_gen()) + "\n\n"
        msg += "انستا:\n" + "\n".join(unit_insta_gen()) + "\n\n"
        msg += "سناب:\n" + "\n".join(unit_snap_gen()) + "\n\n"
        msg += "تيك توك:\n" + "\n".join(unit_tiktok_gen())
        bot.reply_to(message, msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))