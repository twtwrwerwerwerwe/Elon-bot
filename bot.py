import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from telethon import TelegramClient, errors

# ======= SOZLAMALAR =======
API_ID = 22731419
API_HASH = '2e2a9ce500a5bd08bae56f6ac2cc4890'
BOT_TOKEN = '7936881674:AAFhO3rBeNLqCka4xDQ3UenJCF8PMpxf1cE'

GROUP_LINKS = [
    "https://t.me/buvayda_toshkentttt",
    "https://t.me/buvayda_bogdod_rishton_toshkend1",
    "https://t.me/BUVAYDA_YANGIQORGON_Toshkentt",
    "https://t.me/Toshkent_bogdod_buvayda_taksi",
    "https://t.me/buvayda_toshkent_bogdod_toshkent",
    "https://t.me/buvayda_toshkent_taksi2",
    "https://t.me/Buvayda_Bogdod_Toshkent",
    "https://t.me/Rishton_Toshkent2",
    "https://t.me/TOSHKENT_RISHTON_TAXI_745",
    "https://t.me/toshkentrishtonbagdod",
    "https://t.me/bagdod_rishton_toshkent_qoqon",
    "https://t.me/Toshkent_Rishton",
    "https://t.me/bagdod_rishton_qoqon_toshkent",
    "https://t.me/buvayda_toshkent_buvayda_taxi",
    "https://t.me/rishton_toshkent_24",
    "https://t.me/Rishton_Toshkent_Rishton",
    "https://t.me/pitagkr",
    "https://t.me/Bogdodtoshkenttaksi1",
    "https://t.me/Toshkent_Rishton24",
    "https://t.me/ToshkentRishtonTaxi",
    "https://t.me/Rishton_Toshkent",
    "https://t.me/rishton_toshkent_1",
    "https://t.me/taxichen",
    "https://t.me/toshkent_rishton_taxi",
    "https://t.me/Rishton_Toshkent_Bogdod_Taksi_01",
    "https://t.me/toshkent_rishtonn",
    "https://t.me/RishtonToshkenttaxiii",
    "https://t.me/Toshkent_Fargona_taxis",
    "https://t.me/RishtonGa",
    "https://t.me/toshkentlo",
    "https://t.me/rishton_toshkent_bogdod_n1",
    "https://t.me/toshkent_bogdod_rishton_buvayd",
    "https://t.me/toshkent_buvayda_bagdodd",
    "https://t.me/Bogdod_toshkent_yangiqorgonbuvay",
    "https://t.me/Toshkent_Bogdod_Toshken",
    "https://t.me/taxi_bogdod_toshken"
]

# ======= OBYEKTLAR =======
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client = TelegramClient('session_rozimuhammad', API_ID, API_HASH)

# ======= KLAVIATURALAR =======
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("📢 E'lon berish"))
confirm_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("✅ Ha"), KeyboardButton("❌ Yo‘q"))
stop_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("⛔ To‘xtatish"))

# ======= FSM HOLATLAR =======
class Form(StatesGroup):
    waiting_for_elon = State()
    waiting_for_confirm = State()

state_flag = {"active": False}

# ======= STATE FILE =======
def save_state(active: bool):
    with open("state.json", "w") as f:
        json.dump({"active": active}, f)

def load_state():
    try:
        with open("state.json") as f:
            return json.load(f).get("active", False)
    except:
        return False

# ======= /START HANDLER =======
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    save_state(False)
    await message.answer("Assalomu alaykum! E'lon berish uchun quyidagi tugmani bosing.", reply_markup=main_menu)

@dp.message_handler(lambda m: m.text == "📢 E'lon berish")
async def ask_elon(message: types.Message):
    await Form.waiting_for_elon.set()
    await message.answer("Iltimos, e'lon matnini yuboring:", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Form.waiting_for_elon, content_types=types.ContentTypes.TEXT)
async def receive_text(message: types.Message, state: FSMContext):
    await state.update_data(elon_text=message.text)
    await Form.waiting_for_confirm.set()
    await message.answer(f"E'lon tasdiqlaysizmi?\n\n{message.text}", reply_markup=confirm_menu)

@dp.message_handler(state=Form.waiting_for_confirm)
async def confirm_elon(message: types.Message, state: FSMContext):
    if message.text == "✅ Ha":
        data = await state.get_data()
        elon_text = data.get("elon_text")
        state_flag["active"] = True
        save_state(True)
        await message.answer("Yuborish boshlandi. To‘xtatish uchun ⛔ tugmasini bosing.", reply_markup=stop_menu)
        asyncio.create_task(send_ads(elon_text, message))
    else:
        await message.answer("Bekor qilindi.", reply_markup=main_menu)
    await state.finish()

@dp.message_handler(lambda m: m.text == "⛔ To‘xtatish")
async def stop_handler(message: types.Message):
    state_flag["active"] = False
    save_state(False)
    await message.answer("Yuborish to‘xtatildi.", reply_markup=main_menu)

# ======= XABAR YUBORISH FUNKSIYASI =======
async def send_ads(text: str, message: types.Message):
    await client.start()
    for i in range(0, len(GROUP_LINKS), 2):
        if not load_state():
            await message.answer("❌ Yuborish to‘xtatildi.")
            break
        batch = GROUP_LINKS[i:i+2]
        for link in batch:
            try:
                entity = await client.get_entity(link)
                msg = await client.send_message(entity, text)
                post_link = f"https://t.me/{entity.username}/{msg.id}" if entity.username else "Link topilmadi"
                await message.answer(f"✅ Yuborildi: {link} - {post_link}")
            except Exception as e:
                await message.answer(f"❌ Yuborilmadi: {link} - {e}")
        await asyncio.sleep(8)

# ======= RUN =======
if __name__ == "__main__":
    print("🚀 Bot ishga tushdi...")
    save_state(False)
    executor.start_polling(dp, skip_updates=True)
