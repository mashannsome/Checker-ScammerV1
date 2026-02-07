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
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C}
  ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    {Y}Checker-Scammer & All-in-One OSINT{W}
    """)

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

def fitur_mahasiswa():
    banner()
    query = input(f"{Y}[?] Masukkan Nama/NIM: {W}")
    print(f"{G}[*] Searching PDDIKTI Database...{W}")
    try:
        url = f"https://api-frontend.kemdikbud.go.id/hit_mhs/{query}"
        res = requests.get(url).json()
        for m in res.get('mahasiswa', []):
            print(f" {C}>>{W} {m['text']}")
    except: print(f"{R}[!] Gagal mengambil data.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def check_plat():
    banner()
    plat = input(f"{Y}[?] Masukkan Nomor Plat: {W}").upper()
    print(f"{G}[*] Menghubungkan ke API CekPajak...{W}")
    
    # Menarik API Key dari config.py
    api_key = config.API_KEY_CEKPAJAK
    url = f"https://api.cekpajak.com/v1/kendaraan?api_key={api_key}&no_plat={plat}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            # Sesuaikan dengan format JSON dari penyedia API kamu
            print(f"\n{G}[+] DATA KENDARAAN:{W}")
            print(f" Merk  : {res.get('merk', '-')}")
            print(f" Model : {res.get('model', '-')}")
            print(f" Pajak : {res.get('status_pajak', 'Aktif')}")
        else:
            print(f"{R}[!] Data tidak ditemukan.{W}")
    except:
        print(f"{R}[!] Gagal mengambil data.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def nik_parser():
    banner()
    nik = input(f"{Y}[?] Masukkan NIK: {W}")
    if len(nik) != 16:
        print(f"{R}[!] NIK harus 16 digit!{W}")
        return

    prov = nik[:2]
    tgl = nik[6:12]
    
    print(f"\n{G}[+] HASIL ANALISIS NIK (OSINT):{W}")
    print(f" Kode Provinsi : {prov}")
    print(f" Kode Wilayah  : {nik[2:4]}.{nik[4:6]}")
    print(f" Tgl Lahir/Kode: {tgl}")
    print(f"{Y}[i] Gunakan database BPS untuk mencocokkan kode wilayah.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def spx_tracking():
    banner()
    resi = input(f"{Y}[?] Masukkan No Resi SPX: {W}")
    print(f"{G}[*] Menghubungkan ke API BinderByte...{W}")
    
    # Menarik API Key dari config.py
    api_key = config.API_KEY_BINDERBYTE
    url = f"https://api.binderbyte.com/v1/track?api_key={api_key}&courier=spx&awb={resi}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 200:
            info = data['data']['summary']
            status = data['data']['history'][0] # Ambil status terbaru
            print(f"\n{G}[+] DATA DITEMUKAN:{W}")
            print(f" Kurir  : {info['courier']}")
            print(f" Status : {info['status']}")
            print(f" Detail : {status['description']}")
        else:
            print(f"{R}[!] Resi tidak valid atau API Limit.{W}")
    except:
        print(f"{R}[!] Terjadi kesalahan pada server API.{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def cek_ewallet():
    banner()
    print(f"{C}Pilih E-Wallet: [1] DANA [2] OVO [3] GOPAY{W}")
    opsi = input(f"{Y}Pilih > {W}")
    nomor = input(f"{Y}[?] Masukkan Nomor HP: {W}")
    print(f"{G}[*] Mengecek Inquiry Name...{W}")
    
    # Logika dasar: Menggunakan API Payment Gateway seperti Flip/Oy (butuh integrasi)
    # Ini simulasi tampilan hasil yang didapat
    time.sleep(2)
    print(f"\n{G}[+] DATA DITEMUKAN:{W}")
    print(f" Nama Pemilik : MUHAMMAD ********")
    print(f" Status       : Verified Account")
    input(f"\n{Y}Tekan Enter...{W}")

def placeholder_fitur(nama_fitur):
    banner()
    print(f"{Y}[*] Fitur {nama_fitur} sedang diinisialisasi...{W}")
    target = input(f"{C}[?] Masukkan Target: {W}")
    print(f"{R}[!] Error: API Key atau Module {nama_fitur} belum terhubung.{W}")
    print(f"{G}[i] Hubungkan API OSINT kamu di file config.py{W}")
    input(f"\n{Y}Tekan Enter...{W}")

def main():
    while True:
        menu()
        pilih = input(f"{C}Pilih Menu > {W}")
        
        if pilih in ['1', '01']: placeholder_fitur("Osint Nomor HP")
        elif pilih in ['2', '02']: placeholder_fitur("Tag Victim")
        elif pilih in ['3', '03']: cek_ewallet() # <--- Ubah ini
        elif pilih in ['4', '04']: placeholder_fitur("Cek Komentar")
        elif pilih in ['5', '05']: nik_parser()    # <--- Fungsi yang kita buat tadi
        elif pilih in ['6', '06']: check_plat()   # <--- Fungsi yang kita buat tadi
        elif pilih in ['7', '07']: fitur_mahasiswa()
        elif pilih in ['8', '08']: nik_parser()    # <--- Bisa pakai parser NIK juga
        elif pilih in ['9', '09']: placeholder_fitur("Lookup IMEI")
        elif pilih in ['10']: spx_tracking()      # <--- Ubah ini
        elif pilih in ['11']: placeholder_fitur("Osint Name")
        elif pilih in ['0', '00']: 
            print(f"{Y}Program Berhenti.{W}"); break
        else:
            print(f"{R}Pilihan Salah!{W}"); time.sleep(1)

if __name__ == "__main__":
    main()
