from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_ID, CHANNEL_LINK, CARD_INFO
from database import init_db, add_user, get_user
from keep_alive import keep_alive

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

init_db()
keep_alive()

def approve_keyboard(user_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}"))
    return kb

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📥 Obuna olish", callback_data="subscribe"),
        InlineKeyboardButton("📄 Obuna holatim", callback_data="status")
    )
    await message.answer(f"Assalomu alaykum!\n\n{CARD_INFO}\n💰 1 oylik narx: 20 000 so‘m", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "subscribe")
async def subscribe_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("To‘lovni amalga oshiring va chekni rasm sifatida yuboring.")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == "status")
async def status_handler(callback_query: types.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if user:
        start, end = user
        await callback_query.message.answer(f"📆 Obuna muddati:\nBoshlanish: {start}\nTugash: {end}")
    else:
        await callback_query.message.answer("❌ Siz hali obuna bo‘lmagansiz.")
    await callback_query.answer()

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_handler(message: types.Message):
    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"💳 Yangi to‘lov cheki\nIsmi: {message.from_user.full_name}\nID: {message.from_user.id}",
        reply_markup=approve_keyboard(message.from_user.id)
    )
    await message.reply("✅ Chekingiz qabul qilindi. Admin tekshiradi.")

@dp.callback_query_handler(lambda c: c.data.startswith("approve_"))
async def approve_callback(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    add_user(user_id, callback_query.from_user.full_name)
    await bot.send_message(user_id, f"✅ Obunangiz tasdiqlandi.\n🔗 Kanal: {CHANNEL_LINK}")
    await callback_query.answer("Foydalanuvchi tasdiqlandi.")

if __name__ == "__main__":
    executor.start_polling(dp)
