VLAD, [20.10.2025 11:37]
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import asyncio
import subprocess
import sys
import os
TOKEN = os.getenv("8285721437:AAEU7LArZhK_U9UWbbCL4eMGR59DP6cFFNY")

ADMIN_ID = 7816829354  # 👈 Теперь админ получает уведомления корректно

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ====== Словарь товаров ======
products_info = {
    "❄️ A–PVP ❄️": {
        "description": """💎 A–PVP 💎
0.5г — 9.60 $ ≈ 384 грн
1г   — 13.20 $ ≈ 528 грн
2г   — 27.60 $ ≈ 1104 грн
3г   — 28.80 $ ≈ 1152 грн
5г   — 43.20 $ ≈ 1728 грн""",
        "image": r"C:\Users\artem\OneDrive\Desktop\POWER CANDY SHOP\a_pvp.png"
    },
    "❄️ МЕТАДОН ❄️": {
        "description": """💎 МЕТАДОН 💎
0.25г — 10.90 $ ≈ 436 грн
0.5г  — 18.00 $ ≈ 720 грн
1г    — 33.60 $ ≈ 1344 грн
2г    — 57.13 $ ≈ 2285 грн
5г    — 72.00 $ ≈ 2880 грн""",
        "image": r"C:\Users\artem\OneDrive\Desktop\POWER CANDY SHOP\metadon.png"
    },
    "❄️ МЕФЕДРОН ❄️": {
        "description": """💎 МЕФЕДРОН 💎
0.5г — 12.00 $ ≈ 480 грн
1г   — 17.52 $ ≈ 701 грн
2г   — 27.80 $ ≈ 1112 грн
5г   — 51.60 $ ≈ 2064 грн""",
        "image": r"C:\Users\artem\OneDrive\Desktop\POWER CANDY SHOP\photo_2025-10-13_23-22-18.jpg"
    }
}

# ====== Состояния ======
# user_state[user_id] = {'level': 'start'|'products'|'country'|'city'|'district'|'payment'|'confirm', 'product':..., 'country':..., 'city':..., 'district':...}
user_state = {}

# ====== Кнопки ======
btn_back = KeyboardButton("⬅️ Назад")
back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)

# Кнопки товаров
products_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for product in products_info.keys():
    products_keyboard.add(KeyboardButton(product))

# Кнопки оплаты
payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(KeyboardButton("🪙 Оплата крипто"), KeyboardButton("💳 Оплата картой"))
payment_keyboard.add(btn_back)

# Кнопка подтверждения и далее
confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_keyboard.add(KeyboardButton("✅ Подтвердить"))
confirm_keyboard.add(btn_back)

next_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
next_keyboard.add(KeyboardButton("➡️ Далее"))

# ====== Города и районы (расширенные) ======
cities = {
    "Украина": ["Киев", "Львов", "Одесса", "Харьков", "Днепр", "Запорожье", "Херсон", "Чернигов", "Полтава", "Винница"],
    "Беларусь": ["Минск", "Гомель", "Могилёв", "Брест", "Витебск", "Гродно", "Бобруйск", "Мозырь", "Орша", "Пинск"],
    "Россия": ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург", "Нижний Новгород", "Самара", "Челябинск", "Ростов-на-Дону", "Уфа"]
}

VLAD, [20.10.2025 11:37]
districts = {
    "Киев": ["Оболонский", "Подол", "Шевченковский", "Печерский", "Дарницкий", "Святошинский", "Деснянский", "Голосеевский"],
    "Львов": ["Галицкий", "Франковский", "Шевченковский", "Сыховский", "Зализнычный", "Лычаковский"],
    "Одесса": ["Приморский", "Суворовский", "Киевский", "Малиновский", "Черноморский", "Слободской"],
    "Харьков": ["Холодногорский", "Основянский", "Киевский", "Слободской", "Индустриальный", "Коминтерновский"],
    "Днепр": ["Амур-Нижнеднепровский", "Жовтневый", "Индустриальный", "Самарский", "Чечеловский"],
    "Минск": ["Центральный", "Советский", "Партизанский", "Фрунзенский", "Октябрьский", "Ленинский", "Первомайский"],
    "Москва": ["Арбат", "Хамовники", "Тверской", "Пресненский", "Сокольники", "Замоскворечье", "Лефортово", "Басманный", "Таганский"],
    "Санкт-Петербург": ["Центральный", "Василеостровский", "Адмиралтейский", "Петроградский", "Калининский", "Красногвардейский", "Московский"],
    "Казань": ["Вахитовский", "Приволжский", "Кировский", "Московский", "Советский"],
    "Новосибирск": ["Центральный", "Калининский", "Октябрьский", "Ленинский", "Кировский"],
    "Екатеринбург": ["Калининский", "Железнодорожный", "Чкаловский", "Верх-Исетский", "Кировский"],
    "Нижний Новгород": ["Нижегородский", "Советский", "Московский", "Приокский", "Сормовский"],
    "Самара": ["Кировский", "Самарский", "Железнодорожный", "Советский", "Приволжский"],
    "Челябинск": ["Центральный", "Ленинский", "Тракторозаводский", "Калининский", "Советский"],
    "Ростов-на-Дону": ["Ворошиловский", "Пролетарский", "Кировский", "Советский", "Октябрьский"],
    "Уфа": ["Калининский", "Ленинский", "Орджоникидзевский", "Советский", "Дёмский"]
}

# ====== Сообщения оплаты ======
crypto_message = """🪙 ОПЛАТА КРИПТОВАЛЮТОЙ 🪙
USDT
TRMLKjSPauqfY9QFQgEHMH42xucSWTkRPA
BTC
1EhHLZCWmWUvutj9ZzuaWdxC2BmUm3g64Q"""

card_message = """💳 ОПЛАТА КАРТОЙ 💳
4149499091509693"""

# ====== Отправщики клавиатур (помогают при бек-навигейшн) ======
def send_start_keyboard(chat_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📦 АССОРТИМЕНТ 📦")
    return kb

def send_products_keyboard(chat):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for p in products_info.keys():
        kb.add(KeyboardButton(p))
    kb.add(btn_back)
    return kb

def send_countries_keyboard(country_list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for country in country_list:
        kb.add(KeyboardButton(country))
    kb.add(btn_back)
    return kb

def send_cities_keyboard(country):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in cities[country]:
        kb.add(KeyboardButton(f"🌃 {city} 🌃"))
    kb.add(btn_back)
    return kb

def send_districts_keyboard(city_name):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for d in districts.get(city_name, []):
        kb.add(KeyboardButton(f"🌃 {d} 🌃"))
    kb.add(btn_back)
    return kb

# ---------- Хендлеры ----------

# ====== Старт ======
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_state[message.from_user.id] = {'level': 'start'}
    welcome = "🎉🎉 Добро пожаловать! 🎉🎉\nВыберите товар:"
    await message.answer(welcome, reply_markup=send_products_keyboard(message.chat))

VLAD, [20.10.2025 11:37]
# ====== Выбор товара ======
@dp.message_handler(lambda message: message.text in products_info.keys())
async def choose_product(message: types.Message):
    uid = message.from_user.id
    user_state.setdefault(uid, {})['product'] = message.text
    user_state[uid]['level'] = 'products'  # сейчас на уровне выбора страны после показа товара
    product = products_info[message.text]
    try:
        with open(product["image"], "rb") as img:
            await message.answer_photo(img, caption=product["description"])
    except Exception:
        # если картинка не найдена — просто отправим текст
        await message.answer(product["description"])
    # отправляем список стран
    countries_keyboard = send_countries_keyboard(list(cities.keys()))
    user_state[uid]['level'] = 'country'
    await message.answer("Выберите страну:", reply_markup=countries_keyboard)

# ====== Выбор страны ======
@dp.message_handler(lambda message: message.text in cities.keys())
async def choose_country(message: types.Message):
    uid = message.from_user.id
    user_state.setdefault(uid, {})['country'] = message.text
    user_state[uid]['level'] = 'city'
    city_kb = send_cities_keyboard(message.text)
    await message.answer("Выберите город: 🌃", reply_markup=city_kb)

# ====== Выбор города ======
@dp.message_handler(lambda message: any(city in message.text for city_list in cities.values() for city in city_list))
async def choose_city(message: types.Message):
    uid = message.from_user.id
    city_name = message.text.replace("🌃 ", "").replace(" 🌃", "")
    user_state.setdefault(uid, {})['city'] = city_name
    # если есть районы — показываем, иначе переходим к оплате
    if city_name in districts:
        user_state[uid]['level'] = 'district'
        district_kb = send_districts_keyboard(city_name)
        await message.answer("Выберите район: 🌃", reply_markup=district_kb)
    else:
        user_state[uid]['level'] = 'payment'
        await message.answer("Этап оплаты:", reply_markup=payment_keyboard)

# ====== Выбор района ======
@dp.message_handler(lambda message: any(district in message.text for district_list in districts.values() for district in district_list))
async def choose_district(message: types.Message):
    uid = message.from_user.id
    district_name = message.text.replace("🌃 ", "").replace(" 🌃", "")
    user_state.setdefault(uid, {})['district'] = district_name
    user_state[uid]['level'] = 'payment'
    await message.answer("Этап оплаты:", reply_markup=payment_keyboard)

# ====== Оплата ======
@dp.message_handler(lambda message: message.text in ["🪙 Оплата крипто", "💳 Оплата картой"])
async def choose_payment(message: types.Message):
    uid = message.from_user.id
    if message.text == "🪙 Оплата крипто":
        await message.answer(crypto_message)
    else:
        await message.answer(card_message)
    user_state.setdefault(uid, {})['level'] = 'confirm'
    await message.answer("После оплаты нажмите ✅ Подтвердить", reply_markup=confirm_keyboard)

# ====== Подтверждение оплаты ======
@dp.message_handler(lambda message: message.text == "✅ Подтвердить")
async def confirm_payment(message: types.Message):
    uid = message.from_user.id
    user_state.setdefault(uid, {})['level'] = 'final'
    await message.answer("📸 Перешлите скрин оплаты администратору.", reply_markup=next_keyboard)
    data = user_state.get(uid, {})
    msg = (
        f"💰 Новый заказ!\n"
        f"Товар: {data.get('product')}\n"
        f"Страна: {data.get('country')}\n"
        f"Город: {data.get('city')}\n"
        f"Район: {data.get('district')}\n"
        f"Пользователь: @{message.from_user.username or 'Без ника'}"
    )
    # шлём админу
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=msg)
    except Exception as e:
        # логирование ошибки отправки админу
        print("Ошибка отправки админу:", e)

# ====== Завершение ======
@dp.message_handler(lambda message: message.text == "➡️ Далее")
async def final_message(message: types.Message):
    await message.answer("🎉 Спасибо за покупку в нашем магазине! 💫 Возвращайтесь снова! 🎁")

VLAD, [20.10.2025 11:37]
# ====== Назад (один уровень) ======
@dp.message_handler(lambda message: message.text == "⬅️ Назад")
async def go_back(message: types.Message):
    uid = message.from_user.id
    state = user_state.get(uid, {'level': 'start'})
    level = state.get('level', 'start')

    # карта предыдущих уровней (один шаг назад)
    prev_map = {
        'products': 'start',       # если были на products (после /start) — возвращаемся к старту
        'country': 'products',     # после показа товара -> country => назад к товарам
        'city': 'country',
        'district': 'city',
        'payment': 'district' if state.get('city') in districts else 'city',
        'confirm': 'payment',
        'final': 'start',
        'start': 'start'
    }
    prev = prev_map.get(level, 'start')
    user_state.setdefault(uid, {})['level'] = prev

    # отправляем соответствующую клавиатуру/сообщение для предыдущего уровня
    if prev == 'start':
        await start_handler(message)
    elif prev == 'products':
        kb = send_products_keyboard(message.chat)
        await message.answer("📦 АССОРТИМЕНТ:", reply_markup=kb)
    elif prev == 'country':
        countries_keyboard = send_countries_keyboard(list(cities.keys()))
        await message.answer("Выберите страну:", reply_markup=countries_keyboard)
    elif prev == 'city':
        country = state.get('country')
        if country and country in cities:
            kb = send_cities_keyboard(country)
            await message.answer("Выберите город: 🌃", reply_markup=kb)
        else:
            # fallback — показать страны
            countries_keyboard = send_countries_keyboard(list(cities.keys()))
            user_state[uid]['level'] = 'country'
            await message.answer("Выберите страну:", reply_markup=countries_keyboard)
    elif prev == 'district':
        city_name = state.get('city')
        if city_name:
            kb = send_districts_keyboard(city_name)
            await message.answer("Выберите район: 🌃", reply_markup=kb)
        else:
            # fallback to cities
            country = state.get('country')
            if country:
                kb = send_cities_keyboard(country)
                user_state[uid]['level'] = 'city'
                await message.answer("Выберите город: 🌃", reply_markup=kb)
            else:
                await start_handler(message)
    elif prev == 'payment':
        await message.answer("Этап оплаты:", reply_markup=payment_keyboard)
    else:
        await start_handler(message)

# ====== Автоматический фон (detach) + немедленный старт ======
def spawn_detached():
    """Попытаться перезапустить себя в фоновом (detached) режиме — осторожно: избегаем множества копий."""
    # если уже запущен как "run_bot" — ничего не делаем
    if "run_bot" in sys.argv:
        return False

    # создаём небольшой lock-файл чтобы не спавнить несколько раз подряд
    lock_path = os.path.join(os.path.dirname(file), "bot_background.lock")
    try:
        # если lock существует, возможно уже есть фон. не спавним.
        if os.path.exists(lock_path):
            return False
        # создаём lock
        with open(lock_path, "w") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

VLAD, [20.10.2025 11:37]
try:
        if os.name == 'nt':
            # Windows: используем CREATE_NEW_PROCESS_GROUP и DETACHED_PROCESS
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen([sys.executable, file, "run_bot"],
                             stdout=open("bot.log", "a"),
                             stderr=open("bot_error.log", "a"),
                             creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS)
        else:
            # POSIX: используем setsid для отделения
            subprocess.Popen([sys.executable, file, "run_bot"],
                             stdout=open("bot.log", "a"),
                             stderr=open("bot_error.log", "a"),
                             preexec_fn=os.setsid)
        return True
    except Exception as e:
        print("Не удалось спавнить detached процесс:", e)
        return False

if name == "main":
    # Попытка запустить детачед-процесс (если он ещё не создан).
    spawned = spawn_detached()
    if spawned:
        print("🔁 Создан detached (фоновой) процесс. Продолжаю локальный запуск (чтобы была немедленная реакция).")
    else:
        print("ℹ️ Detached-процесс не создан (возможно уже запущен). Запускаю обычный экземпляр.")

    # Немедленный запуск (локальный): это гарантирует, что бот сразу отвечает в текущем терминале.
    print("✅ Бот запущен (локально). Если был создан фоновой процесс — он продолжит работу после закрытия терминала.")
    executor.start_polling(dp, skip_updates=True)