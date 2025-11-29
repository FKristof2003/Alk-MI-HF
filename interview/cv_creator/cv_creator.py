import os
import re
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

# --- Globális Adattároló Listák (Beviteli Mező Objektumok) ---
education_data = [] 
experience_data = []
license_data = []

# --- Segédfüggvények a fájlnevekhez ---

def sanitize_name(name):
    """
    Tisztítja a nevet a fájlnév generálásához:
    - Kisbetűre alakít.
    - Eltávolítja a magyar ékezeteket.
    - A szóközöket aláhúzásra cseréli.
    """
    sanitized = name.lower()
    
    # Magyar ékezetek eltávolítása
    accent_map = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 
        'ú': 'u', 'ü': 'u', 'ű': 'u'
    }
    for accent, replacement in accent_map.items():
        sanitized = sanitized.replace(accent, replacement)
        
    # Szóközök cseréje aláhúzásra
    sanitized = sanitized.replace(' ', '_')
    
    # Eltávolít minden nem engedélyezett karaktert (csak betű, szám, aláhúzás)
    sanitized = re.sub(r'[^\w-]', '', sanitized)
    
    return sanitized

def find_next_filename(base_filename, directory="cvs"):
    """Megkeresi a következő elérhető fájlnevet a számozás biztosításával."""
    # A legelső próbálkozás
    filename = f"{base_filename}.txt"
    counter = 1
    
    # Amíg a fájl létezik, növeli a számlálót
    while os.path.exists(os.path.join(directory, filename)):
        counter += 1
        filename = f"{base_filename}_{counter}.txt"
        
    return filename

# --- Dinamikus Mező Kezelő Függvények (megtartva) ---

def add_education_entry(frame):
    """Tanulmányi bejegyzés hozzáadása a kerethez."""
    row_num = len(education_data)
    entry_frame = ttk.Frame(frame)
    entry_frame.pack(fill="x", padx=5, pady=2)
    ttk.Label(entry_frame, text=f"Képzés/Intézmény {row_num + 1}:").pack(side="left", padx=5)
    institution_entry = ttk.Entry(entry_frame, width=30)
    institution_entry.pack(side="left", fill="x", expand=True)
    ttk.Label(entry_frame, text="Időpont:").pack(side="left", padx=5)
    date_entry = ttk.Entry(entry_frame, width=15)
    date_entry.pack(side="left", padx=5)
    education_data.append({"frame": entry_frame, "institution": institution_entry, "date": date_entry})
    
def add_experience_entry(frame):
    """Munkatapasztalat bejegyzés hozzáadása a kerethez."""
    row_num = len(experience_data)
    entry_frame = ttk.Frame(frame)
    entry_frame.pack(fill="x", padx=5, pady=2)
    ttk.Label(entry_frame, text=f"Cég/Pozíció {row_num + 1}:").pack(side="left", padx=5)
    company_entry = ttk.Entry(entry_frame, width=30)
    company_entry.pack(side="left", fill="x", expand=True)
    ttk.Label(entry_frame, text="Időpont:").pack(side="left", padx=5)
    date_entry = ttk.Entry(entry_frame, width=15)
    date_entry.pack(side="left", padx=5)
    experience_data.append({"frame": entry_frame, "company": company_entry, "date": date_entry})

def add_license_entry(frame):
    """Jogosítvány bejegyzés hozzáadása a kerethez."""
    row_num = len(license_data)
    entry_frame = ttk.Frame(frame)
    entry_frame.pack(fill="x", padx=5, pady=2)
    ttk.Label(entry_frame, text=f"Jogosítvány típusa {row_num + 1}:").pack(side="left", padx=5)
    license_entry = ttk.Entry(entry_frame, width=30)
    license_entry.pack(side="left", fill="x", expand=True)
    license_data.append(license_entry)

# --- Adatgyűjtő és Mentő Függvények ---

def get_all_data(name_entry, dob_entry, job_entry, strengths_text, weaknesses_text):
    """Összegyűjti az összes adatot a beviteli mezőkből."""
    data = {
        # A bemeneti paraméterek használata
        "Név": name_entry.get().strip(),
        "Születési dátum": dob_entry.get().strip(),
        "Jelentkezett állás": job_entry.get().strip(),
        "Erősségek": strengths_text.get("1.0", tk.END).strip(),
        "Gyengeségek": weaknesses_text.get("1.0", tk.END).strip(),
        
        # ... (Dinamikus listák (education_data, experience_data, license_data) maradnak globálisak) ...
        "Tanulmányok": [
            (entry['institution'].get().strip(), entry['date'].get().strip()) 
            for entry in education_data 
            if entry['institution'].get().strip() or entry['date'].get().strip()
        ],
        "Munkatapasztalatok": [
            (entry['company'].get().strip(), entry['date'].get().strip()) 
            for entry in experience_data 
            if entry['company'].get().strip() or entry['date'].get().strip()
        ],
        "Jogosítványok": [entry.get().strip() for entry in license_data if entry.get().strip()]
    }
    return data

def format_data_for_txt(data):
    """Formázza a begyűjtött adatokat szöveges fájlba íráshoz."""
    formatted_output = "=================================================\n"
    formatted_output += "           ÁLLÁSINTERJÚ FELKÉSZÍTŐ - CV ADATOK     \n"
    formatted_output += "=================================================\n\n"
    
    # Személyes adatok
    formatted_output += "--- SZEMÉLYES ÉS CÉL ADATOK ---\n"
    formatted_output += f"Név: {data['Név']}\n"
    formatted_output += f"Születési dátum: {data['Születési dátum']}\n"
    formatted_output += f"Jelentkezett állás: {data['Jelentkezett állás']}\n\n"
    
    # Tanulmányok
    formatted_output += "--- TANULMÁNYOK ---\n"
    if data['Tanulmányok']:
        for institution, date in data['Tanulmányok']:
            formatted_output += f"  - Képzés/Intézmény: {institution} | Időpont: {date}\n"
    else:
        formatted_output += "  Nincs megadva tanulmány.\n"
    formatted_output += "\n"
    
    # Munkatapasztalatok
    formatted_output += "--- MUNKATAPASZTALATOK ---\n"
    if data['Munkatapasztalatok']:
        for company, date in data['Munkatapasztalatok']:
            formatted_output += f"  - Cég/Pozíció: {company} | Időpont: {date}\n"
    else:
        formatted_output += "  Nincs megadva munkatapasztalat.\n"
    formatted_output += "\n"
    
    # Képességek
    formatted_output += "--- ERŐSSÉGEK ---\n"
    formatted_output += f"{data['Erősségek']}\n\n"
    
    formatted_output += "--- GYENGESÉGEK ---\n"
    formatted_output += f"{data['Gyengeségek']}\n\n"
    
    # Jogosítványok
    formatted_output += "--- JOGOSÍTVÁNYOK ---\n"
    if data['Jogosítványok']:
        for license_type in data['Jogosítványok']:
            formatted_output += f"  - {license_type}\n"
    else:
        formatted_output += "  Nincs megadva jogosítvány.\n"
    formatted_output += "\n"

    formatted_output += "=================================================\n"

    return formatted_output

def save_data_automatically(name_entry, dob_entry, job_entry, strengths_text, weaknesses_text):
    """Beggyűjti az adatokat, generálja a fájlnevet, és automatikusan elmenti."""
    try:
        # A függvény meghívása a paraméterekkel
        all_data = get_all_data(name_entry, dob_entry, job_entry, strengths_text, weaknesses_text)
        
        user_name = all_data['Név']
        if not user_name:
            messagebox.showwarning("Hiányzó adat", "Kérlek, add meg a neved a fájl mentéséhez.")
            return
            
        # ... (Célmappa, fájlnév generálás, mentés logikája marad) ...
        target_dir = "cvs"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        base_filename = sanitize_name(user_name)
        final_filename = find_next_filename(base_filename, target_dir)
        final_path = os.path.join(target_dir, final_filename)
        
        file_content = format_data_for_txt(all_data)
        
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        messagebox.showinfo("Mentés Sikeres", f"Az adatok sikeresen mentve a(z) \n'{final_path}' fájlba.")
            
    except Exception as e:
        messagebox.showerror("Hiba történt", f"Hiba a fájl mentésekor: {e}")
