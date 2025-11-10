import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import (
    init_db, get_new_applications, get_applications, get_application_detail,
    get_latest_application_id, toggle_application_status
)
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# Получаем список админских ID из переменных окружения
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
if not ADMIN_IDS_STR:
    raise ValueError("ADMIN_IDS не найден в .env файле")

# Преобразуем строку в список целых чисел
ADMIN_IDS = [int(admin_id.strip()) for admin_id in ADMIN_IDS_STR.split(",") if admin_id.strip()]

if not ADMIN_IDS:
    raise ValueError("ADMIN_IDS должен содержать хотя бы один ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_checked_id = None

def format_date(dt_str):
    # Создаем timezone для GMT+4
    gmt4 = timezone(timedelta(hours=4))
    
    # Парсим дату из строки
    dt = datetime.fromisoformat(dt_str)
    
    # Если дата не имеет timezone, считаем её UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Конвертируем в GMT+4
    dt_gmt4 = dt.astimezone(gmt4)
    
    # Форматируем дату и время
    return dt_gmt4.strftime("%d.%m.%Y %H:%M")

def format_application(app):
    app_id, phone, comment, created_at, status = app
    text = f"Новая заявка от {format_date(created_at)}\n\n"
    text += f"Телефон: `{phone}`\n"
    if comment:
        text += f"\nКомментарий: {comment}"
    text += f"\nСтатус: {status}"
    return text

# --- Проверка прав администратора ---
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# --- Фоновая задача для новых заявок ---
async def check_new_applications():
    global last_checked_id
    if last_checked_id is None:
        last_checked_id = get_latest_application_id() or 0

    while True:
        try:
            new_apps = get_new_applications(last_checked_id)
            for app in new_apps:
                text = format_application(app)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="Закрыть заявку" if app[4]=="Новая" else "Открыть заявку",
                        callback_data=f"toggle_{app[0]}_0"
                    )]
                ])
                # Отправляем уведомление всем администраторам
                for admin_id in ADMIN_IDS:
                    await bot.send_message(chat_id=admin_id, text=text, reply_markup=keyboard, parse_mode="Markdown")
                last_checked_id = max(last_checked_id, app[0])
        except Exception as e:
            print(f"Ошибка при проверке новых заявок: {e}")
        await asyncio.sleep(10)

# --- Список заявок ---
@dp.message(Command(commands=["applications"]))
async def applications_list(message: types.Message, offset: int = 0, limit: int = 5):
    # Проверяем, что пользователь является администратором
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
    
    apps = get_applications(offset=offset, limit=limit)
    if not apps:
        await message.answer("Заявок пока нет.")
        return

    buttons = [
        [InlineKeyboardButton(
            text=f"{format_date(created_at)} - {phone} ({status})",
            callback_data=f"view_{app_id}_{offset}"
        )] for app_id, phone, created_at, status in reversed(apps)
    ]
    if len(apps) == limit:
        buttons.append([InlineKeyboardButton(text="Следующие", callback_data=f"next_{offset + limit}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Список заявок:", reply_markup=keyboard)

# --- Callback для деталей и управления ---
@dp.callback_query()
async def applications_callback_handler(callback: types.CallbackQuery):
    # Проверяем, что пользователь является администратором
    if not is_admin(callback.from_user.id):
        await callback.answer("У вас нет прав для выполнения этого действия.", show_alert=True)
        return
    
    data = callback.data

    if data.startswith("view_"):
        _, app_id, offset = data.split("_")
        app_id = int(app_id)
        offset = int(offset)
        app = get_application_detail(app_id)
        if app:
            text = format_application(app)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Закрыть заявку" if app[4]=="Новая" else "Открыть заявку",
                    callback_data=f"toggle_{app_id}_{offset}"
                )],
                [InlineKeyboardButton(text="Назад", callback_data=f"back_{offset}")]
            ])
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

    elif data.startswith("next_") or data.startswith("back_"):
        offset = int(data.split("_")[1])
        apps = get_applications(offset=offset, limit=5)
        buttons = [
            [InlineKeyboardButton(
                text=f"{format_date(created_at)} - {phone} ({status})",
                callback_data=f"view_{app_id}_{offset}"
            )] for app_id, phone, created_at, status in reversed(apps)
        ]
        if len(apps) == 5:
            buttons.append([InlineKeyboardButton(text="Следующие", callback_data=f"next_{offset + 5}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text("Список заявок:", reply_markup=keyboard)

    elif data.startswith("toggle_"):
        _, app_id, offset = data.split("_")
        app_id = int(app_id)
        offset = int(offset)
        new_status = toggle_application_status(app_id)
        app = get_application_detail(app_id)
        if app:
            text = format_application(app)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Закрыть заявку" if new_status=="Новая" else "Открыть заявку",
                    callback_data=f"toggle_{app_id}_{offset}"
                )],
                [InlineKeyboardButton(text="Назад", callback_data=f"back_{offset}")]
            ])
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

# --- Основной запуск ---
async def main():
    # Инициализируем базу данных
    init_db()
    asyncio.create_task(check_new_applications())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
