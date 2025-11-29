import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import re
from cv_creator import *
# --- UI Építés (A korábban megadott UI struktúra) ---

root = tk.Tk()
root.title("🇭🇺 CV Készítő Chatbot Előkészítő")

root.geometry("600x800")

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 1. Személyes és Cél Adatok
basic_info_frame = ttk.LabelFrame(scrollable_frame, text="1. Személyes és Cél Adatok")
basic_info_frame.pack(padx=10, pady=10, fill="x")

ttk.Label(basic_info_frame, text="Név:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(basic_info_frame, width=60)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(basic_info_frame, text="Születési dátum:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
dob_entry = ttk.Entry(basic_info_frame, width=60)
dob_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(basic_info_frame, text="Jelentkezett állás/Pozíció:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
job_entry = ttk.Entry(basic_info_frame, width=60)
job_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# 2. Dinamikus Szekciók - Tanulmányok
education_section_frame = ttk.LabelFrame(scrollable_frame, text="2. Tanulmányok")
education_section_frame.pack(padx=10, pady=5, fill="x")
education_entries_frame = ttk.Frame(education_section_frame)
education_entries_frame.pack(fill="x", padx=5, pady=5)
add_edu_button = ttk.Button(education_section_frame, text="+ Új Tanulmány hozzáadása", 
                            command=lambda: add_education_entry(education_entries_frame))
add_edu_button.pack(pady=5)
add_education_entry(education_entries_frame) 

# 3. Dinamikus Szekciók - Munkatapasztalatok
experience_section_frame = ttk.LabelFrame(scrollable_frame, text="3. Munkatapasztalatok")
experience_section_frame.pack(padx=10, pady=5, fill="x")
experience_entries_frame = ttk.Frame(experience_section_frame)
experience_entries_frame.pack(fill="x", padx=5, pady=5)
add_exp_button = ttk.Button(experience_section_frame, text="+ Új Munkatapasztalat hozzáadása", 
                            command=lambda: add_experience_entry(experience_entries_frame))
add_exp_button.pack(pady=5)
add_experience_entry(experience_entries_frame) 

# 4. Képességek és Egyéb Adatok
skills_frame = ttk.LabelFrame(scrollable_frame, text="4. Erősségek, Gyengeségek, Jogosítványok")
skills_frame.pack(padx=10, pady=10, fill="x")

# Erősségek (Text widget)
ttk.Label(skills_frame, text="Erősségek (rövid felsorolás):").pack(padx=5, pady=5, anchor="w")
strengths_text = tk.Text(skills_frame, height=5, width=70)
strengths_text.pack(padx=5, pady=5, fill="x")

# Gyengeségek (Text widget)
ttk.Label(skills_frame, text="Gyengeségek (rövid felsorolás):").pack(padx=5, pady=5, anchor="w")
weaknesses_text = tk.Text(skills_frame, height=5, width=70)
weaknesses_text.pack(padx=5, pady=5, fill="x")

## Jogosítványok (Dinamikus)
licenses_section_frame = ttk.LabelFrame(skills_frame, text="Jogosítványok")
licenses_section_frame.pack(padx=5, pady=5, fill="x")
license_entries_frame = ttk.Frame(licenses_section_frame)
license_entries_frame.pack(fill="x", padx=5, pady=5)
add_lic_button = ttk.Button(licenses_section_frame, text="+ Új Jogosítvány hozzáadása", 
                            command=lambda: add_license_entry(license_entries_frame))
add_lic_button.pack(pady=5)
add_license_entry(license_entries_frame) 

# --- Adatok Mentése Gomb (Automatikus Mentés) ---
save_button = ttk.Button(
    scrollable_frame, 
    text="CV Mentése", 
    command=lambda: save_data_automatically(
        name_entry, 
        dob_entry, 
        job_entry, 
        strengths_text, 
        weaknesses_text
    )
)
save_button.pack(pady=20)

# Futtatás
root.mainloop()