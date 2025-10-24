import json
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === CONFIG ===
with open("config.json", "r") as f:
    cfg = json.load(f)

TOKEN = cfg["TOKEN"]
OWNER_ID = cfg["OWNER_ID"]
LOG_FILE = "log.txt"


# === LOGGING ===
def write_log(user, action):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{waktu}] {user}: {action}\n")


# === /START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    username = user.username or user.full_name

    write_log(username, "/start")

    photo = open("assets/start.jpg", "rb")
    caption = (
        "📢 *Halo!* `" + username + "`\n\n"
        "> Litex-Userbot siap membantumu membuat Userbot dengan fitur Broadcast dan bonus menarik dari Loyalty Point dan Kode Referral.\n\n"
        "> 💵 *System Auto-Payment:*\n"
        "> Nikmati kemudahan sistem pembayaran otomatis (auto payment) tanpa perlu menunggu owner online!\n"
        "> Pilih button [🤖 Buat Userbot] dan ikuti instruksinya.\n\n"
        "> 🈂️ *Fitur Utama (via Button):*\n"
        "> • Fitur Broadcast.\n"
        "> • Fitur Auto PM.\n\n"
        "> 📋 *Syarat dan Ketentuan Akun Telegram!*\n"
        "> 👉🏻 [BACA DISINI ketentuannya!](https://telegra.ph/Syarat-Ketentuan-Akun-Telegram-03-26)\n\n"
        "> *Ads:* [List VPS](https://t.me/moire_market/5)"
    )

    keyboard = [
        [KeyboardButton("💎 Loyalti Poin"), KeyboardButton("🤖 Buat Userbot")],
        [KeyboardButton("📊 Status Akun"), KeyboardButton("🧩 Cek Fitur")],
        [KeyboardButton("🆘 Dukungan"), KeyboardButton("🌐 Bahasa Indonesia")],
        [KeyboardButton("♻️ Reset Emoji"), KeyboardButton("⚙️ Reset Prefix")],
        [KeyboardButton("💬 Reset Text"), KeyboardButton("🔁 Reset Userbot")],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )
    photo.close()


# === HANDLER PESAN ===
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    user = update.effective_user
    username = user.username or user.full_name

    write_log(username, text)

    # === LOYALTI POIN ===
    if text == "💎 Loyalti Poin":
        await update.message.reply_text(
            "Anda bukan pengguna userbot, silahkan lakukan pembuatan ubot jika sudah diberikan hak akses oleh owner atau seller."
        )

    # === BUAT USERBOT ===
    elif text == "🤖 Buat Userbot":
        msg = (
            "**🤖 Litex-Userbot**\n\n"
            "> **↪️ Kebijakan Pengembalian**\n"
            "> Setelah melakukan pembayaran, jika Anda belum memperoleh/menerima manfaat dari pembelian, "
            "Anda dapat menggunakan hak penggantian dalam waktu 2 hari setelah pembelian.\n\n"
            "> Namun, jika Anda telah menggunakan/menerima salah satu manfaat dari pembelian, termasuk akses ke fitur pembuatan userbot, "
            "maka Anda tidak lagi berhak atas pengembalian dana.\n\n"
            "> **🆘 Dukungan**\n"
            "> Untuk mendapatkan dukungan, Anda dapat:\n"
            "> ❍ Mengikuti prosedur pembelian di bot ini\n"
            "> ❍ Resiko userbot bisa [Baca Disini](https://telegra.ph/RESIKO-USERBOT-03-26-3)\n"
            "> ❍ Beli Userbot = SETUJU DAN PAHAM RESIKO\n\n"
            "> **👉🏻 Tekan tombol 📃 Saya Setuju** untuk melanjutkan.\n"
            "> **Jika tidak, tekan 🏠 Menu Utama.**\n\n"
            "> *Ads:* [List VPS](https://t.me/moire_market/5)"
        )
        keyboard = [
            [KeyboardButton("📃 Saya Setuju"), KeyboardButton("🏠 Menu Utama")],
        ]
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # === SETUJU ===
    elif text == "📃 Saya Setuju":
        keyboard = [
            [KeyboardButton("1 Bulan"), KeyboardButton("2 Bulan"), KeyboardButton("3 Bulan")],
            [KeyboardButton("4 Bulan"), KeyboardButton("5 Bulan"), KeyboardButton("6 Bulan")],
            [KeyboardButton("🏠 Menu Utama")],
        ]
        await update.message.reply_text("Berapa bulan yang ingin anda beli?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # === PEMBAYARAN QRIS DUMMY ===
    elif text in ["1 Bulan", "2 Bulan", "3 Bulan", "4 Bulan", "5 Bulan", "6 Bulan"]:
        bulan = text.split()[0]
        await update.message.reply_photo(
            photo="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://example.com/qris-demo",
            caption=(
                f"🧾 *Pembelian Userbot {bulan} Bulan*\n\n"
                "> Silakan lakukan pembayaran ke QRIS berikut 👇\n\n"
                "> **Nama Merchant:** Litex Official\n"
                "> **Total:** Rp50.000 (contoh)\n\n"
                "> Setelah pembayaran, kirim bukti ke owner.\n"
                "> ✅ Jika valid, Userbotmu akan segera aktif otomatis!"
            ),
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠 Menu Utama")]], resize_keyboard=True),
        )

    # === STATUS AKUN ===
    elif text == "📊 Status Akun":
        msg = (
            "**Litex-Userbot**\n\n"
            "> **Status Ubot:** tidak aktif\n"
            "> **Status Pengguna:** *Litex-Userbot [buyer]*\n"
            "> **Prefixes:** .\n"
            "> **Tanggal Kedaluwarsa:** None\n"
            "> **Uptime Ubot:** 50m:26s"
        )
        keyboard = [[KeyboardButton("🌐 Bahasa Indonesia"), KeyboardButton("🏠 Menu Utama")]]
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    # === BAHASA ===
    elif text == "🌐 Bahasa Indonesia":
        await update.message.reply_text("Bahasa telah disetel ke Indonesia 🇮🇩", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠 Menu Utama")]], resize_keyboard=True))

    # === CEK FITUR ===
    elif text == "🧩 Cek Fitur":
        await update.message.reply_text("Hanya owner/akses all termasuk owner pun.")

    # === DUKUNGAN ===
    elif text == "🆘 Dukungan":
        context.user_data["waiting_support"] = True
        await update.message.reply_text("✍️ Tulis pesan anda:", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠 Menu Utama")]], resize_keyboard=True))

    # === MENU UTAMA ===
    elif text == "🏠 Menu Utama":
        context.user_data["waiting_support"] = False
        await start(update, context)

    # === RESET ===
    elif text in ["♻️ Reset Emoji", "⚙️ Reset Prefix", "💬 Reset Text", "🔁 Reset Userbot"]:
        await update.message.reply_text("Hanya owner dan akses.")

    # === PESAN DUKUNGAN ===
    elif context.user_data.get("waiting_support"):
        pesan = f"📩 Pesan Dukungan dari {username} ({chat_id}):\n{text}"
        await context.bot.send_message(OWNER_ID, pesan)
        await update.message.reply_text("✅ Pesanmu sudah dikirim ke owner.")
        context.user_data["waiting_support"] = False


# === MAIN ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🤖 Litex-Bot aktif dan berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
