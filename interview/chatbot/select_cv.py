import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from chatbot import create_chatbot_ui

# A mappa neve, ahonnan a CV-ket betöltjük
CV_DIRECTORY = "cvs"

def list_cv_files(cv_listbox):
    """Betölti a 'cvs' mappában található TXT fájlok nevét a ListBox-ba."""
    
    # 1. Ellenőrizzük, hogy létezik-e a mappa
    if not os.path.exists(CV_DIRECTORY):
        messagebox.showerror("Hiba", f"A '{CV_DIRECTORY}' mappa nem található!")
        return

    # 2. Kilistázzuk a TXT fájlokat
    try:
        files = [f for f in os.listdir(CV_DIRECTORY) if f.endswith('.txt')]
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba a fájlok listázása közben: {e}")
        return

    # 3. ListBox frissítése
    cv_listbox.delete(0, tk.END) # Tisztítja a ListBox-ot
    if not files:
        cv_listbox.insert(tk.END, "(Nincs CV fájl a mappában)")
    else:
        for file in files:
            cv_listbox.insert(tk.END, file)

def load_selected_cv(cv_listbox, current_root): # Hozzáadjuk a 'current_root' paramétert
    """Betölti a ListBox-ban kiválasztott CV tartalmát, majd indítja a Chatbotot."""
    
    selected_indices = cv_listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("Választás hiánya", "Kérlek, válassz ki egy CV fájlt a listából.")
        return

    selected_file = cv_listbox.get(selected_indices[0])
    
    if selected_file.startswith("("):
        messagebox.showwarning("Választás hiánya", "Nincs mit betölteni.")
        return
        
    file_path = os.path.join(CV_DIRECTORY, selected_file)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            cv_content = f.read()
        
        # 1. Bezárjuk a CV választó ablakot
        current_root.destroy() 
        
        # 2. Átadjuk a CV tartalmát a chatbotnak, és elindítjuk az interjút
        create_chatbot_ui(cv_content) 
        
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba a fájl betöltésekor: {e}")


# --- UI Építés ---

root = tk.Tk()
root.title("🤖 Chatbot - CV Választás")
root.geometry("400x450")

## Cím
ttk.Label(root, text="Válassz CV fájlt az Interjúhoz:", font=('Arial', 12, 'bold')).pack(pady=10)

## CV Lista (ListBox)
list_frame = ttk.Frame(root)
list_frame.pack(padx=20, pady=5, fill="both", expand=True)

# Görgetősáv hozzáadása
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
cv_listbox = tk.Listbox(list_frame, height=15, yscrollcommand=scrollbar.set)
scrollbar.config(command=cv_listbox.yview)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
cv_listbox.pack(side=tk.LEFT, fill="both", expand=True)

# Fájlok betöltése a ListBox-ba induláskor
list_cv_files(cv_listbox)


## Gombok
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Frissítés Gomb (ha közben mentenek új CV-t)
refresh_button = ttk.Button(
    button_frame, 
    text="Listázás frissítése", 
    command=lambda: list_cv_files(cv_listbox)
)
refresh_button.pack(side=tk.LEFT, padx=10)

# Betöltés és Indítás Gomb
load_button = ttk.Button(
    button_frame, 
    text="CV Betöltése és Interjú Indítása 🚀", 
    command=lambda: load_selected_cv(cv_listbox, root)
)
load_button.pack(side=tk.LEFT, padx=10)


root.mainloop()