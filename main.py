import os
import sys
import requests
import time
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
        elif pilih in ['3', '03']: placeholder_fitur("Cek E-Wallet")
        elif pilih in ['4', '04']: placeholder_fitur("Cek Komentar")
        elif pilih in ['5', '05']: placeholder_fitur("Doxing Nomor")
        elif pilih in ['6', '06']: placeholder_fitur("Lookup Plat")
        elif pilih in ['7', '07']: fitur_mahasiswa()
        elif pilih in ['8', '08']: placeholder_fitur("NIK Search")
        elif pilih in ['9', '09']: placeholder_fitur("Lookup IMEI")
        elif pilih in ['10']: placeholder_fitur("SPX Tracking")
        elif pilih in ['11']: placeholder_fitur("Osint Name")
        elif pilih in ['0', '00']: 
            print(f"{Y}Program Berhenti.{W}"); break
        else:
            print(f"{R}Pilihan Salah!{W}"); time.sleep(1)

if __name__ == "__main__":
    main()
