import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys # Szükséges a Python futtatásához

# --- Segédfüggvények a Modulok Indításához ---

def run_script(script_name):
    """Új ablakban indítja el a megadott Python szkriptet."""
    try:
        # A Tkinter ablakokat a subprocess.Popen metódussal a legjobb indítani, 
        # így különálló folyamatként futnak.
        subprocess.Popen([sys.executable, script_name])
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült elindítani a(z) {script_name} fájlt: {e}")


def open_cv_creator():
    """Elindítja a cv_ui.py-ban definiált CV készítőt."""
    # Mivel a cv_ui.py indítja el a tkinter mainloop-ot, azt hívjuk
    run_script("./interview/cv_creator/cv_ui.py")

def open_cv_selector():
    """Elindítja a select_cv.py-ban definiált CV választót."""
    # Mivel a select_cv.py indítja el a tkinter mainloop-ot, azt hívjuk
    run_script("./interview/chatbot/select_cv.py")

# --- Fő UI Építés ---

def main_app():
    root = tk.Tk()
    root.title("🇭🇺 Állásinterjú Felkészítő Rendszer")
    root.geometry("450x250")
    
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(fill="both", expand=True)
    
    ttk.Label(main_frame, text="Válassz funkciót:", font=('Arial', 14, 'bold')).pack(pady=20)

    # 1. CV Készítő Gomb
    cv_creator_button = ttk.Button(
        main_frame, 
        text="📝 1. Új CV létrehozása / Szerkesztése", 
        command=open_cv_creator
    )
    cv_creator_button.pack(fill='x', pady=10)

    # 2. Interjú Chatbot Gomb
    cv_selector_button = ttk.Button(
        main_frame, 
        text="🤖 2. CV kiválasztása & Interjú Indítása", 
        command=open_cv_selector
    )
    cv_selector_button.pack(fill='x', pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_app()