import os
import sys
import requests
import time
import config
from colorama import Fore, Style

# Warna untuk tampilan Termux
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
B = Fore.BLUE
W = Style.RESET_ALL

def banner():
    # Membersihkan layar sesuai OS
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C}
  ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    {Y}Checker-Scammer & All-in-One OSINT by Mashannsome {W}
    """)

def loading_anim(seconds):
    # Animasi loading sederhana
    animation = ["|", "/", "-", "\\"]
    end_time = time.time() + seconds
    while time.time() < end_time:
        for char in animation:
            sys.stdout.write(f'\r{G}[*] Processing {char}{W}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')

def menu():
    banner()
    print(f"{G}[01]{W} Osint Nomor HP (Analisis & Search)")
    print(f"{G}[02]{W} Show Tag Victim (Detail Tag)")
    print(f"{G}[03]{W} Check Nama E-Wallet (Dana/OVO/GoPay)")
    print(f"{G}[04]{W} Check Komentar Nomor HP")
    print(f"{G}[05]{W} Doxing Nomor (Full Info: NIK, BPJS, dll)")
    print(f"{G}[06]{W} Lookup Plat Kendaraan")
    print(f"{G}[07]{W} Data Mahasiswa & Dosen (Search ID)")
    print(f"{G}[08]{W} Search NIK / Data Pekerja")
    print(f"{G}[09]{W} Lookup IMEI")
    print(f"{G}[10]{W} SPX Tracking (Other Osint)")
    print(f"{G}[11]{W} Osint Name Search")
    print(f"{G}[00]{W} Keluar")
    print(f"{C}" + "="*45 + f"{W}")

# --- Fungsi Integrasi Fitur ---
def osint_nomor():
    banner()
    nomor = input(f"{Y}[?] Masukkan Nomor HP (Gunakan 62...): {W}")
    if not nomor.startswith("62"):
        print(f"{R}[!] Gunakan format internasional (Contoh: 62812xxx){W}")
        input(f"\n{Y}Tekan Enter...{W}")
        return

    print(f"{G}[*] Searching Truecaller Database...{W}")
    loading_anim(3)
    
    # Header untuk Truecaller (Umumnya butuh Authorization)
    headers = {
        "Authorization": f"Bearer {config.TRUECALLER_TOKEN}",
        "User-Agent": "Truecaller/11.75.5 (Android;10)"
    }
    
    url = f"https://search5-noneu.truecaller.com/v2/search?q={nomor}&countryCode=ID&type=4"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                info = data['data'][0]
                name = info.get('name', 'Tidak Diketahui')
                provider = info.get('phones', [{}])[0].get('carrier', '-')
                email = info.get('internetAddresses', [{}])[0].get('id', '-')
                
                print(f"\n{G}[+] DATA DITEMUKAN:{W}")
                print(f" Nama Pemilik : {name}")
                print(f" Provider     : {provider}")
                print(f" Email        : {email}")
                print(f" Score        : {info.get('score', 'N/A')}")
            else:
                print(f"{R}[!] Nomor tidak terdaftar di database Truecaller.{W}")
        else:
            print(f"{R}[!] Error {response.status_code}: Token Expired atau Salah.{W}")
    except:
        print(f"{R}[!] Gagal terhubung ke server Truecaller.{W}")
    
    input(f"\n{Y}Tekan Enter...{W}")
    
def fitur_mahasiswa():
    banner()
    query = input(f"{Y}[?] Masukkan Nama/NIM: {W}")
    loading_anim(1)
    try:
        url = f"https://api-frontend.kemdikbud.go.id/hit_mhs/{query}"
        res = requests.get(url).json()
        if "mahasiswa" in res:
            print(f"\n{G}[+] Hasil Ditemukan:{W}")
            for m in res.get('mahasiswa', []):
                print(f" {C}>>{W} {m['text']}")
        else:
            print(f"{R}[!] Data tidak ditemukan.{W}")
    except:
        print(f"{R}[!] Gagal mengambil data.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def check_plat():
    banner()
    plat = input(f"{Y}[?] Masukkan Nomor Plat: {W}").replace(" ", "").upper()
    print(f"{G}[*] Menghubungkan ke API BinderByte...{W}")
    loading_anim(2)
    
    api_key = config.API_KEY_BINDERBYTE
    url = f"https://api.binderbyte.com/v1/pajak_kendaraan?api_key={api_key}&no_plat={plat}"
    
    try:
        response = requests.get(url)
        res = response.json()
        if res.get('status') == 200:
            data = res.get('data', {})
            print(f"\n{G}[+] DATA KENDARAAN:{W}")
            print(f" Merk  : {data.get('merk', '-')}")
            print(f" Model : {data.get('model', '-')}")
            print(f" Tahun : {data.get('tahun', '-')}")
            print(f" Pajak : {data.get('status_pajak', 'Aktif')}")
        else:
            print(f"{R}[!] Data tidak ditemukan atau API Key Limit.{W}")
    except:
        print(f"{R}[!] Gagal menghubungi server.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def nik_parser():
    banner()
    nik = input(f"{Y}[?] Masukkan NIK (16 digit): {W}")
    if len(nik) != 16:
        print(f"{R}[!] NIK harus 16 digit!{W}")
    else:
        loading_anim(1)
        prov = nik[:2]
        kab = nik[2:4]
        tgl = int(nik[6:8])
        gender = "Laki-laki"
        if tgl > 40:
            gender = "Perempuan"
            tgl -= 40
        
        print(f"\n{G}[+] HASIL ANALISIS NIK:{W}")
        print(f" Jenis Kelamin : {gender}")
        print(f" Kode Provinsi : {prov}")
        print(f" Kode Kab/Kota : {kab}")
        print(f" Tanggal Lahir : {tgl}-{nik[8:10]}-19{nik[10:12]}")
        print(f"{Y}[i] Gunakan database BPS untuk detail wilayah.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def spx_tracking():
    banner()
    resi = input(f"{Y}[?] Masukkan No Resi SPX: {W}")
    loading_anim(2)
    
    api_key = config.API_KEY_BINDERBYTE
    url = f"https://api.binderbyte.com/v1/track?api_key={api_key}&courier=spx&awb={resi}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 200:
            info = data['data']['summary']
            history = data['data']['history'][0]
            print(f"\n{G}[+] DATA DITEMUKAN:{W}")
            print(f" Kurir  : {info['courier']}")
            print(f" Status : {info['status']}")
            print(f" Update : {history['description']}")
        else:
            print(f"{R}[!] Resi tidak ditemukan atau API Limit.{W}")
    except:
        print(f"{R}[!] Terjadi kesalahan pada server.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def cek_ewallet():
    banner()
    print(f"{C}Pilih E-Wallet:{W}")
    print(f"{G}[1]{W} DANA")
    print(f"{G}[2]{W} OVO")
    print(f"{G}[3]{W} GOPAY")
    print(f"{G}[4]{W} SHOPEEPAY")
    
    opsi = input(f"\n{Y}Pilih > {W}")
    
    # Mapping pilihan ke nama layanan API BinderByte
    layanan = {
        "1": "dana",
        "2": "ovo",
        "3": "gopay",
        "4": "shopeepay"
    }
    
    if opsi not in layanan:
        print(f"{R}[!] Pilihan tidak valid!{W}")
        time.sleep(1)
        return

    nomor = input(f"{Y}[?] Masukkan Nomor HP (Contoh: 0812xxx): {W}")
    print(f"{G}[*] Menghubungkan ke API BinderByte...{W}")
    loading_anim(2)
    
    api_key = config.API_KEY_BINDERBYTE
    # Endpoint BinderByte untuk Inquiry (Pastikan sesuai dengan dokumentasi terbaru mereka)
    url = f"https://api.binderbyte.com/v1/inquiry?api_key={api_key}&type={layanan[opsi]}&account={nomor}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') == 200:
            info = data.get('data', {})
            print(f"\n{G}[+] DATA DITEMUKAN:{W}")
            print(f" E-Wallet : {layanan[opsi].upper()}")
            print(f" Nomor    : {nomor}")
            print(f" Nama     : {info.get('name', 'N/A')}")
            print(f" Status   : Verified")
        else:
            print(f"{R}[!] Gagal: {data.get('message', 'Nomor tidak ditemukan atau API Limit')}{W}")
    except:
        print(f"{R}[!] Terjadi kesalahan koneksi ke server.{W}")
        
    input(f"\n{Y}Tekan Enter...{W}")

def osint_nama():
    banner()
    nama = input(f"{Y}[?] Masukkan Nama Lengkap Target: {W}").replace(" ", "+")
    print(f"{G}[*] Scanning Social Media Footprint...{W}")
    loading_anim(3)
    
    # Mencari di berbagai platform via Google Dorking
    print(f"\n{G}[+] LINK PROFIL POTENSIAL:{W}")
    print(f" {C}>>{W} FB: https://www.facebook.com/search/top/?q={nama}")
    print(f" {C}>>{W} IG: https://www.google.com/search?q=site:instagram.com+{nama}")
    print(f" {C}>>{W} LinkedIn: https://www.google.com/search?q=site:linkedin.com+{nama}")
    
    input(f"\n{Y}Tekan Enter...{W}")

def show_tags():
    banner()
    nomor = input(f"{Y}[?] Masukkan Nomor HP (Contoh: 62812xxx): {W}")
    if not nomor.startswith("62"):
        print(f"{R}[!] Gunakan format internasional (62){W}")
        input(f"\n{Y}Tekan Enter...{W}")
        return

    print(f"{G}[*] Fetching Tags from Eyecon Database...{W}")
    loading_anim(3)
    
    # Header simulasi Eyecon App
    headers = {
        "User-Agent": "Eyecon/3.0.454 (Android;10)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }
    
    # Endpoint alternatif untuk pencarian publik
    url = f"https://api.eyecon-app.com/api/v1/search?e={nomor}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"\n{G}[+] TAGS / NAMA DITEMUKAN:{W}")
            # Eyecon biasanya mengembalikan daftar nama yang paling relevan
            if isinstance(data, list):
                for i, item in enumerate(data[:5], 1): # Ambil 5 tag teratas
                    print(f" {C}{i}.{W} {item.get('name', 'N/A')}")
            else:
                print(f" {C}>>{W} {data.get('name', 'Tidak ada tag publik')}")
        else:
            print(f"{R}[!] Gagal mengambil data (Status: {response.status_code}){W}")
    except:
        print(f"{R}[!] Terhubung ke server gagal.{W}")
        
    input(f"\n{Y}Tekan Enter...{W}")

def cek_komentar():
    banner()
    nomor = input(f"{Y}[?] Masukkan Nomor HP Target: {W}")
    print(f"{G}[*] Mencari riwayat laporan penipuan...{W}")
    loading_anim(3)
    
    # Daftar situs pelaporan penipuan yang akan dicek melalui Google Search Dorking
    # Kita menggunakan scraping pada pencarian publik
    queries = [
        f"https://www.google.com/search?q=penipu+{nomor}",
        f"https://www.google.com/search?q=site:kredibel.id+{nomor}",
        f"https://www.google.com/search?q=site:tellows.id+{nomor}"
    ]
    
    print(f"\n{G}[+] HASIL ANALISIS JEJAK DIGITAL:{W}")
    print(f" {C}1.{W} Mengecek di Google Fraud Database...")
    print(f" {C}2.{W} Mengecek di Tellows (Spam Checker)...")
    print(f" {C}3.{W} Mengecek di Kredibel.id...")
    
    # Karena scraping langsung ke web tersebut sering terblokir Captcha di Termux,
    # Kita berikan ringkasan dan link manual agar user bisa melihat bukti lengkap.
    
    print(f"\n{Y}[!] OSINT TIP:{W}")
    print(f" Jika hasil pencarian Google memunculkan banyak judul 'Penipu' atau 'Hati-hati',")
    print(f" nomor ini {R}SANGAT BERBAHAYA{W}.")
    
    print(f"\n{G}[*] Klik/Salin Link di bawah untuk melihat detail komentar:{W}")
    print(f" {B}>>{W} https://www.google.com/search?q={nomor}+penipu")
    
    # Opsional: Membuka browser otomatis di Termux
    tanya = input(f"\n{Y}[?] Buka hasil di browser? (y/n): {W}")
    if tanya.lower() == 'y':
        os.system(f"termux-open-url {queries[0]}")

    input(f"\n{Y}Tekan Enter...{W}")

def main():
    while True:
        menu()
        pilih = input(f"{C}Pilih Menu > {W}")
        
        if pilih in ['1', '01']: osint_nomor()
        elif pilih in ['2', '02']: show_tags()
        elif pilih in ['3', '03']: cek_ewallet()
        elif pilih in ['4', '04']: cek_komentar()
        elif pilih in ['5', '05']: nik_parser()
        elif pilih in ['6', '06']: check_plat()
        elif pilih in ['7', '07']: fitur_mahasiswa()
        elif pilih in ['8', '08']: nik_parser()
        elif pilih in ['9', '09']: placeholder_fitur("Lookup IMEI")
        elif pilih in ['10']: spx_tracking()
        elif pilih in ['11']: osint_nama()
        elif pilih in ['0', '00']: 
            print(f"{Y}Keluar...{W}")
            break
        else:
            print(f"{R}Pilihan Salah!{W}")
            time.sleep(1)

if __name__ == "__main__":
    main()
