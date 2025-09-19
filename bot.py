
import os
# import csv
# import asyncio
# import asyncpg
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)

# ========= KONFIGURASI =========
BOT_TOKEN = "8263700932:AAH7yyTUzQ4hYtMMSDyPcdIRIHnbBXpVYDs"
BASE_DIR = "FormatSurat1"  # folder utama penyimpanan file surat
ITEMS_PER_PAGE = 10        # jumlah istilah glosarium per halaman

# ========= GLOSARIUM =========
GLOSARIUM = {
    "APBN": "Anggaran Pendapatan dan Belanja Negara, rencana keuangan tahunan pemerintah pusat yang ditetapkan bersama DPR untuk periode 1 tahun.",
    "APBD": "Anggaran Pendapatan dan Belanja Daerah, rencana keuangan tahunan pemerintah daerah yang disetujui bersama DPRD.",
    "ADK": "Arsip Data Komputer, arsip data dalam bentuk softcopy yang disimpan secara digital.",
    "BAPP": "Berita Acara Penyelesaian Pekerjaan, dokumen legalitas sebagai bukti pekerjaan telah selesai sesuai termin kontrak.",
    "BAS": "Bagan Akun Standar, daftar kodefikasi transaksi keuangan pemerintah sebagai pedoman anggaran dan pelaporan.",
    "BAST": "Berita Acara Serah Terima, dokumen legalitas penyerahan hasil pekerjaan dari Penyedia kepada instansi pemerintah.",
    "Belanja Pegawai (51)": "Pengeluaran untuk kompensasi pegawai, pejabat, pensiunan, atau honorer.",
    "Belanja Barang (52)": "Pengeluaran untuk barang/jasa habis pakai serta perjalanan dinas dan operasional lainnya.",
    "Belanja Modal (53)": "Pengeluaran untuk memperoleh/menambah aset tetap yang bernilai jangka panjang.",
    "Bendahara Penerimaan": "Pejabat yang menerima, menyimpan, dan menyetor penerimaan negara/daerah.",
    "Bendahara Pengeluaran": "Pejabat yang mengelola uang untuk membiayai belanja negara.",
    "Bendahara Pengeluaran Pembantu": "Membantu bendahara pengeluaran dalam proses pembayaran.",
    "Data Kontrak": "Informasi terkait perjanjian tertulis antara PPK dengan penyedia barang/jasa.",
    "Data Supplier": "Informasi pihak penerima pembayaran APBN yang memuat data pokok, lokasi, dan rekening.",
    "LRA": "Laporan Realisasi Anggaran, laporan realisasi pendapatan, belanja, dan pembiayaan dalam satu periode.",
    "LO": "Laporan Operasional, laporan penggunaan sumber daya ekonomi dalam kegiatan pemerintahan.",
    "Laporan Keuangan": "Pertanggungjawaban APBN yang disusun pemerintah sesuai standar akuntansi.",
    "DIPA": "Daftar Isian Pelaksanaan Anggaran, dokumen pelaksanaan anggaran yang disusun PA/KPA.",
    "LPE": "Laporan Perubahan Ekuitas, laporan kenaikan/penurunan ekuitas dibanding tahun sebelumnya.",
    "KKP": "Kartu Kredit Pemerintah, alat pembayaran belanja APBN di mana kewajiban awal ditanggung bank penerbit dan dilunasi Satker.",
    "KKI": "Kartu Kredit Indonesia, Kartu Kredit Pemerintah dengan skema pemrosesan domestik untuk transaksi di Indonesia."
    "Kontrak" "Kontrak Pengadaan Barang/Jasa, perjanjian tertulis antara PA/KPA/PPK dengan Penyedia atau pelaksana Swakelola.",
    "KPA": "Kuasa Pengguna Anggaran, pejabat yang diberi kuasa untuk menggunakan anggaran.",
    "KPB": "Kuasa Pengguna Barang, pejabat yang menggunakan barang milik negara dalam penguasaannya.",
    "LPJ Bendahara": "Laporan pertanggungjawaban bendahara atas uang/surat berharga yang dikelola.",
    "Neraca": "Laporan posisi keuangan (aset, kewajiban, ekuitas) pemerintah pada tanggal tertentu.",
    "CaLK": "Catatan atas Laporan Keuangan, informasi tambahan dan penjelasan atas laporan keuangan utama.",
    "PNBP": "Penerimaan Negara Bukan Pajak, penerimaan pemerintah dari sumber selain pajak (misalnya SDA, BUMN).",
    "PPABP": "Petugas Pengelola Administrasi Belanja Pegawai, petugas yang membantu KPA mengelola belanja pegawai.",
    "PPSPM": "Pejabat Penandatangan SPM, pejabat yang menguji dan menandatangani permintaan pembayaran.",
    "PPK": "Pejabat Pembuat Komitmen, pejabat yang berwenang membuat keputusan kontraktual dalam pelaksanaan anggaran.",
    "RKBMN": "Rencana Kebutuhan Barang Milik Negara, dokumen dasar untuk usulan anggaran barang milik negara.",
    "RKA-K/L": "Rencana Kerja dan Anggaran Kementerian/Lembaga, dokumen rencana program/kegiatan dalam satu tahun.",
    "RPD": "Rencana Penarikan Dana, rencana kebutuhan dana bulanan untuk pelaksanaan kegiatan.",
    "POK": "Petunjuk Operasional Kegiatan, dokumen rencana kerja dan biaya rinci sebagai turunan dari DIPA.",
    "Satker": "Satuan Kerja, unit organisasi pelaksana kegiatan pada kementerian/lembaga yang menggunakan APBN.",
    "KAK/TOR": "Kerangka Acuan Kegiatan/Term of Reference, dokumen berisi latar belakang, output, strategi, biaya, dan waktu kegiatan.",
    "RAB": "Rincian Anggaran Biaya, perhitungan rinci biaya untuk mencapai output kegiatan.",
    "SPBy": "Surat Perintah Pembayaran, dokumen yang diterbitkan PPK atas nama KPA untuk mengeluarkan uang persediaan yang dikelola Bendahara Pengeluaran.",
    "SPP": "Surat Permintaan Pembayaran, dokumen dari PPK untuk meminta pencairan dana.",
    "SPM": "Surat Perintah Membayar, dokumen pencairan dana dari DIPA yang ditandatangani PA/KPA.",
    "SPM-LS": "Surat Perintah Membayar Langsung, SPM untuk pembayaran langsung kepada penerima hak.",
    "SP2D": "Surat Perintah Pencairan Dana, perintah pencairan dana oleh KPPN berdasarkan SPM.",
    "SPM UP": "Surat Perintah Membayar Uang Persediaan, SPM untuk menyediakan uang operasional sehari-hari satker.",
    "SPM GUP": "Surat Perintah Membayar Penggantian Uang Persediaan, SPM untuk mengganti uang persediaan yang sudah terpakai.",
    "SPM TUP": "Surat Perintah Membayar Tambahan Uang Persediaan, SPM untuk menambah uang persediaan karena kebutuhan mendesak.",
    "Retur SP2D": "Pengembalian pencairan APBN akibat kesalahan rekening bank.",
    "SSP": "Surat Setoran Pajak, formulir penyetoran pajak ke kas negara.",
    "UP": "Uang Persediaan, uang yang disediakan untuk kebutuhan operasional satker sehari-hari.",
    "TUP": "Tambahan Uang Persediaan, uang tambahan di luar UP karena kebutuhan mendesak.",
    "UAKPA": "Unit Akuntansi Kuasa Pengguna Anggaran, unit akuntansi di tingkat satker untuk pelaporan keuangan.",
    "UAKPB": "Unit Akuntansi Kuasa Pengguna Barang, unit akuntansi pengguna barang milik negara.",
}

# # # ========= LOGGER KE CSV =========
# def log_usage(user_id, username, action):
#     with open("traffic_log.csv", "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, username, action])

# # ========== PostgreSQL Setup ==========
# DB_URL = os.getenv("DATABASE_URL")

# if not DB_URL:
#     raise ValueError("❌ DATABASE_URL tidak ditemukan. Pastikan sudah diset di Railway Env Var.")
# else:
#     print(f"✅ DATABASE_URL ke-load: {DB_URL}")

# async def init_db():
#     conn = await asyncpg.connect(DB_URL)
#     await conn.execute("""
#     CREATE TABLE IF NOT EXISTS logs (
#         id SERIAL PRIMARY KEY,
#         user_id BIGINT,
#         username TEXT,
#         action TEXT,
#         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     await conn.close()

# async def log_usage(user_id, username, action):
#     conn = await asyncpg.connect(DB_URL)
#     await conn.execute(
#         "INSERT INTO logs (user_id, username, action, timestamp) VALUES ($1, $2, $3, $4)",
#         user_id, username, action, datetime.now()
#     )
#     await conn.close()

# # ========== Handler ==========
# async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await log_usage(update.effective_user.id, update.effective_user.username, "Start bot")
#     await update.message.reply_text("Halo, selamat datang di Dokgen Bot 👋")

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await log_usage(query.from_user.id, query.from_user.username, f"Klik tombol: {query.data}")
#     await query.answer("Tercatat ✅")

# # ========== Main ==========
# def main():
#     app = Application.builder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", cmd_start))
#     app.add_handler(CallbackQueryHandler(button_handler))
#     # Tambahin handler lain di sini...

#     print("✅ Bot Telegram sedang berjalan...")
#     app.run_polling()

# if __name__ == "__main__":
#     asyncio.run(init_db())   # bikin tabel kalau belum ada
#     main()

# ========= UTIL & DATA LOADER =========
def ensure_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def get_kategori_list():
    ensure_base_dir()
    kategori = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    kategori.sort(key=str.lower)
    return kategori

def get_file_list(kategori):
    folder_path = os.path.join(BASE_DIR, kategori)
    if not os.path.exists(folder_path):
        return []
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort(key=str.lower)
    return files

def search_files(keyword):
    results = []
    key = keyword.strip().lower()
    if not key:
        return results
    for kategori in get_kategori_list():
        for filename in get_file_list(kategori):
            if key in filename.lower():
                results.append((kategori, filename))
    return results


def kb_start():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 Format Surat", callback_data="menu_formatsurat"),
            InlineKeyboardButton("❓ FAQ", callback_data="menu_faq"),
        ],
        [
            InlineKeyboardButton("📚 Glosarium", callback_data="menu_glosarium"),
            InlineKeyboardButton("📑 Juknis Aplikasi", callback_data="menu_juknis"),
        ],
        [
            InlineKeyboardButton("☎️ Contact Center", callback_data="menu_contact"),
        ]
    ])

def kb_kategori():
    keyboard = []
    kategori_list = get_kategori_list()
    for i in range(0, len(kategori_list), 2):
        row = []
        row.append(InlineKeyboardButton(kategori_list[i], callback_data=f"folder|{kategori_list[i]}"))
        if i + 1 < len(kategori_list):
            row.append(InlineKeyboardButton(kategori_list[i+1], callback_data=f"folder|{kategori_list[i+1]}"))
        keyboard.append(row)
    if not keyboard:
        keyboard = [[InlineKeyboardButton("— Belum ada kategori —", callback_data="noop")]]
    return InlineKeyboardMarkup(keyboard)

def kb_surat(kategori):
    keyboard = []
    file_list = get_file_list(kategori)
    for file_name in file_list:
        keyboard.append([
            InlineKeyboardButton(file_name, callback_data=f"file|{kategori}|{file_name}")
        ])
    if not file_list:
        keyboard.append([InlineKeyboardButton("— Belum ada file —", callback_data="noop")])
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_folder")])
    return InlineKeyboardMarkup(keyboard)

def kb_search_results(results):
    keyboard = []
    capped = results[:10]  # batasi 10 hasil
    for kategori, filename in capped:
        label = f"{filename}  ·  ({kategori})"
        # potong biar aman (max 64 byte)
        cb = f"file|{kategori[:15]}|{filename[:30]}"
        keyboard.append([InlineKeyboardButton(label, callback_data=cb)])
    if not keyboard:
        keyboard = [[InlineKeyboardButton("— Tidak ada hasil —", callback_data="noop")]]
    return InlineKeyboardMarkup(keyboard)

def kb_glosarium(page: int):
    total_items = len(GLOSARIUM)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    keyboard = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"glosarium|{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"glosarium|{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)

# ========= UTIL: SEARCH GLOSARIUM =========
def search_glosarium(keyword):
    results = []
    key = keyword.strip().lower()
    if not key:
        return results
    for istilah, arti in GLOSARIUM.items():
        if key in istilah.lower() or key in arti.lower():
            results.append((istilah, arti))
    return results

# ========= HANDLER: PESAN TEKS =========
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    lower = text.lower()

    reply_parts = []

    # 1. Cari istilah di GLOSARIUM
    glosarium_results = search_glosarium(lower)
    if glosarium_results:
        glosarium_text = "📚 *Hasil Pencarian Glosarium:*\n\n"
        for istilah, arti in glosarium_results[:5]:
            glosarium_text += f"*{istilah}* — {arti}\n\n"
        if len(glosarium_results) > 5:
            glosarium_text += f"⚠️ Menampilkan 5 dari {len(glosarium_results)} hasil. Persempit kata kunci."
        reply_parts.append(glosarium_text)

    # 2. Cari file format surat
    results = search_files(lower)
    if results:
        files_text = f"📄 *Ditemukan {len(results)} file terkait* *{text}*:\n(Pilih dari tombol di bawah)"
        reply_parts.append(files_text)

        # kirim teks + tombol file
        await update.message.reply_text(
            files_text,
            reply_markup=kb_search_results(results),
            parse_mode="Markdown"
        )

    # 3. Kalau ada hasil glosarium, kirim duluan
    if reply_parts:
        combined = "\n\n".join([p for p in reply_parts if not p.startswith("📄")])
        if combined:
            await update.message.reply_text(combined, parse_mode="Markdown")
        return

    # 4. Kalau sama sekali tidak ada hasil
    await update.message.reply_text(
        "❓ Tidak ada file/istilah glosarium yang cocok.\nCoba kata kunci lain atau pilih menu:",
        reply_markup=kb_start()
    )


# ========= HANDLERS: COMMAND =========
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Selamat datang di\n\n"
        "✨ *𝗗𝗢𝗞𝗚𝗘𝗡* ✨\n"
        "_(Dokumen dalam Genggaman)_\n"
        "-----------------------------------\n"
        "📌 Bot Layanan *KPPN Jakarta VI*\n\n" 
        "Melalui bot ini, Anda dapat dengan mudah mengakses layanan:\n" 
        "• 📄 Mengunduh format surat\n" 
        "• ❓ Mengakses FAQ (pertanyaan yang sering diajukan)\n" 
        "• 📚 Membaca glosarium istilah perbendaharaan\n" 
        "• 💻 Membaca Juknis Aplikasi (SAKTI & Gaji)\n\n"
        "Anda juga bisa langsung mengetik kata kunci untuk mencari dokumen yang dibutuhkan.\n" 
        "Contoh: *pengajuan UP*, *SPJ*, *permohonan*, dll."
    )
    await update.message.reply_text(text, reply_markup=kb_start(), parse_mode="Markdown")


async def cmd_formatsurat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📂 Pilih kategori format surat:", reply_markup=kb_kategori())

async def cmd_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 FAQ Kontrak", url="https://online.fliphtml5.com/lepbf/gmyx/")],
        [InlineKeyboardButton("📗 FAQ Gaji", url="https://online.fliphtml5.com/lepbf/ozcl/")],
        [InlineKeyboardButton("📙 FAQ SPM LS UP Koreksi SPM", url="https://online.fliphtml5.com/lepbf/oxkk/")],
        [InlineKeyboardButton("📕 FAQ Retur dan Supplier", url="https://online.fliphtml5.com/lepbf/eicq/")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_start")]
    ]
    await update.message.reply_text("📑 Pilih Kategori FAQ:", reply_markup=InlineKeyboardMarkup(keyboard))

async def cmd_juknis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💻 SAKTI", callback_data="juknis_sakti")],
        [InlineKeyboardButton("👤 Gaji", callback_data="juknis_gaji")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_start")]
    ]
    await update.message.reply_text("📑 Pilih Juknis Aplikasi:", reply_markup=InlineKeyboardMarkup(keyboard))
    

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "☎️ *Contact Center — Hai DJPb*\n\n"
        "Jika membutuhkan bantuan lebih lanjut, hubungi:\n\n"
        "• 📱 *WhatsApp*: +62 878-7711-4090\n"
        "• 🌐 *Website*: https://hai.kemenkeu.go.id/\n"
        "• ✉️ *Email*: hai.djpb@kemenkeu.go.id\n\n"
        "_Silakan pilih kanal yang paling nyaman untuk Anda._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ========= HELPER: SEND GLOSARIUM =========
async def send_glosarium_page(message, page: int):
    istilah_list = list(GLOSARIUM.items())
    total_items = len(istilah_list)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    start = page * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, total_items)

    reply = "📚 *Glosarium Perbendaharaan:*\n\n"
    for istilah, arti in istilah_list[start:end]:
        reply += f"*{istilah}* — {arti}\n\n"
    reply += f"📖 Halaman {page+1}/{total_pages}"

    await message.reply_text(reply, parse_mode="Markdown", reply_markup=kb_glosarium(page))

# ========= HANDLERS: CALLBACK =========
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    # log_usage(user.id, user.username or "-", f"Tombol: {data}")


    if data == "menu_formatsurat":
        await query.message.reply_text("📂 Pilih kategori format surat:", reply_markup=kb_kategori())

    elif data == "menu_faq":
        # reply = "❓ FAQ yang tersedia:\n" + "\n".join(f"- {key}" for key in FAQS)
        # await query.message.reply_text(reply)
        keyboard = [
            [InlineKeyboardButton("📘 FAQ Kontrak", url="https://online.fliphtml5.com/lepbf/gmyx/")],
            [InlineKeyboardButton("📗 FAQ Gaji", url="https://online.fliphtml5.com/lepbf/ozcl/")],
            [InlineKeyboardButton("📙 FAQ SPM LS UP Koreksi SPM", url="https://online.fliphtml5.com/lepbf/oxkk/")],
            [InlineKeyboardButton("📕 FAQ Retur dan Supplier", url="https://online.fliphtml5.com/lepbf/eicq/")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_start")]
        ]
        await query.message.reply_text("📑 Pilih Kategori FAQ:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "menu_contact":
        msg = (
            "☎️ *Contact Center — Hai DJPb*\n\n"
            "Jika membutuhkan bantuan lebih lanjut, hubungi:\n\n"
            "• 📱 *WhatsApp*: +62 878-7711-4090\n"
            "• 🌐 *Website*: https://hai.kemenkeu.go.id/\n"
            "• ✉️ *Email*: hai.djpb@kemenkeu.go.id\n\n"
            "_Silakan pilih kanal yang paling nyaman untuk Anda._"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif data == "menu_glosarium":
        await send_glosarium_page(query.message, 0)

    elif data.startswith("glosarium|"):
        page = int(data.split("|")[1])
        await send_glosarium_page(query.message, page)

    elif data == "menu_juknis":
        keyboard = [
            [InlineKeyboardButton("💻 SAKTI", callback_data="juknis_sakti")],
            [InlineKeyboardButton("👤 Gaji", callback_data="juknis_gaji")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_start")]
        ]
        await query.message.reply_text("📑 Pilih Juknis Aplikasi:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "juknis_sakti":
        keyboard = [
            [InlineKeyboardButton("📘 Modul Sakti Pelaksanaan", url="https://linktr.ee/juknissaktipelaksanaan")],
            [InlineKeyboardButton("📗 Modul Sakti Penganggaran", url="https://sites.google.com/view/saktipenganggaran")],
            [InlineKeyboardButton("📙 Modul Sakti Pelaporan", url="https://sites.google.com/view/saktipelaporan/home")],
            [InlineKeyboardButton("📕 Modul Sakti Admin", url="https://sites.google.com/view/saktiadm")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_juknis")]
        ]
        await query.message.reply_text("💻 Juknis SAKTI:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "juknis_gaji":
        keyboard = [
            [InlineKeyboardButton("📄 Gaji Satker", url="https://s.id/gajisatker")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_juknis")]
        ]
        await query.message.reply_text("👤 Juknis Gaji:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_to_start":
        await query.message.reply_text("🏠 Kembali ke menu utama:", reply_markup=kb_start())


    elif data.startswith("folder|"):
        kategori = data.split("|", 1)[1]
        await query.message.reply_text(
            f"📄 Daftar surat di kategori *{kategori}*:",
            reply_markup=kb_surat(kategori),
            parse_mode="Markdown"
        )

    elif data.startswith("file|"):
        _, kategori, filename = data.split("|", 2)
        file_path = os.path.join(BASE_DIR, kategori, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    await query.message.reply_document(f, filename=filename)
            except Exception as e:
                await query.message.reply_text(f"⚠️ Gagal mengirim file: {e}")
        else:
            await query.message.reply_text("⚠️ File tidak ditemukan.")

    elif data == "back_to_folder":
        await query.message.reply_text("📂 Pilih kategori format surat:", reply_markup=kb_kategori())

# # ========= HANDLER: PESAN TEKS =========
# async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = (update.message.text or "").strip()
#     lower = text.lower()

#     if lower in FAQS:
#         await update.message.reply_text(FAQS[lower])
#         return

#     results = search_files(lower)
#     if results:
#         await update.message.reply_text(
#             f"🔎 Ditemukan {len(results)} file terkait *{text}*. Pilih salah satu:",
#             reply_markup=kb_search_results(results),
#             parse_mode="Markdown"
#         )
#         return

#     await update.message.reply_text(
#         "❓ Tidak ada file/FAQ yang cocok.\nCoba kata kunci lain atau pilih menu:",
#         reply_markup=kb_start()
#     )

# ========= KEYBOARD HASIL PENCARIAN =========


# ========= HANDLER: PESAN TEKS =========
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    lower = text.lower()

    reply_parts = []

    # 2. Cari istilah di GLOSARIUM
    glosarium_results = search_glosarium(lower)
    if glosarium_results:
        glosarium_text = "📚 *Hasil Pencarian Glosarium:*\n\n"
        for istilah, arti in glosarium_results[:5]:
            glosarium_text += f"*{istilah}* — {arti}\n\n"
        if len(glosarium_results) > 5:
            glosarium_text += f"⚠️ Menampilkan 5 dari {len(glosarium_results)} hasil. Persempit kata kunci."
        reply_parts.append(glosarium_text)

    # 3. Cari file format surat
    results = search_files(lower)
    if results:
        files_text = f"📄 *Ditemukan {len(results)} file terkait* *{text}*:\n(Pilih dari tombol di bawah)"
        reply_parts.append(files_text)

        # kirim teks + tombol file
        await update.message.reply_text(
            files_text,
            reply_markup=kb_search_results(results),
            parse_mode="Markdown"
        )

    # 4. Kalau ada hasil glosarium, kirim duluan
    if reply_parts:
        # kirim gabungan (kecuali file sudah dikirim dengan tombol)
        combined = "\n\n".join([p for p in reply_parts if not p.startswith("📄")])
        if combined:
            await update.message.reply_text(combined, parse_mode="Markdown")
        return

    # 5. Kalau sama sekali tidak ada hasil
    await update.message.reply_text(
        "❓ Tidak ada file/FAQ/istilah glosarium yang cocok.\nCoba kata kunci lain atau pilih menu:",
        reply_markup=kb_start()
    )


# ========= MAIN =========
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("formatsurat", cmd_formatsurat))
    app.add_handler(CommandHandler("faq", cmd_faq))
    app.add_handler(CommandHandler("juknis", cmd_juknis))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    print("✅ Bot Telegram sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
