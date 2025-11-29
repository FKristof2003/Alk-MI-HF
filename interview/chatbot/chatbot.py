# chatbot.py

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from google import genai
from google.genai.errors import APIError # Hibakezeléshez

# --- Globális Változók ---
# Gemini modellt hívjuk meg (pl. gemini-2.5-flash)
MODEL_NAME = "gemini-2.5-flash" 
# Az API klienst a beszélgetés indításakor inicializáljuk
client = None
chat_session = None
GEMINI_API_KEY = 'AIzaSyAmyj2Sqi9g_Cuxh8uAAs2QaARwdy3VD74'
# --- Gemini Logika és API Kezelés ---

def initialize_gemini():
    """Inicializálja a Gemini API klienst."""
    global client
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        return True
    except Exception as e:
        messagebox.showerror("Gemini Inicializálási Hiba", f"Hiba történt a Gemini API inicializálásakor: {e}")
        return False

def start_interview(cv_content, interview_text_widget):
    """
    Elindítja a beszélgetési munkamenetet (chat session) és elküldi az első promptot
    a betöltött CV tartalmával.
    """
    global client, chat_session
    
    if not initialize_gemini():
        return

    # A Gemini Chat History API-t használjuk a kontextus megtartásához
    chat_session = client.chats.create(model=MODEL_NAME)
    
    # Részletes Prompt a Gemini-nak
    system_prompt = (
        "Te egy professzionális magyar állásinterjú felkészítő chatbot vagy. "
        "A feladatod, hogy a megadott önéletrajz alapján interjúztasd a jelöltet. "
        "Kérdezz releváns, mélyreható kérdéseket, de egyszerre csak egy kérdést tegyél fel. "
        "Kérdezz a Tanulmányokról, Munkatapasztalatokról, az Erősségekről és Gyengeségekről. "
        "A válaszokat ne értékeld, csak kérdezz tovább a beszélgetés irányának megfelelően."
    )
    
    initial_user_prompt = (
        f"{system_prompt}\n\n"
        f"Kezdd el az interjút. Az interjúalany önéletrajza a következő:\n\n"
        f"--- CV TARTALOM ---\n{cv_content}"
        f"\n--- CV TARTALOM VÉGE ---\n\n"
        "Tedd fel az első interjúkérdést."
    )
    
    # Az első üzenet elküldése
    try:
        response = chat_session.send_message(initial_user_prompt)
        
        # UI frissítése a Gemini válaszával
        interview_text_widget.config(state=tk.NORMAL)
        interview_text_widget.insert(tk.END, "🤖 Gemini Interjúztató:\n", 'bot')
        interview_text_widget.insert(tk.END, response.text + "\n\n", 'bot')
        interview_text_widget.config(state=tk.DISABLED)
        
    except APIError as e:
        messagebox.showerror("Gemini Hiba", f"API hiba történt: {e}")
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem várt hiba a beszélgetés indításakor: {e}")

# --- Chat UI Logika ---

def send_message(entry_widget, text_widget):
    """Elküldi a felhasználó üzenetét a Gemini-nak és megjeleníti a választ."""
    global chat_session
    
    user_input = entry_widget.get().strip()
    entry_widget.delete(0, tk.END) # Tisztítja a beviteli mezőt
    
    if not user_input:
        return

    if chat_session is None:
        messagebox.showwarning("Interjú állapota", "Kérlek, tölts be egy CV-t az interjú indításához.")
        return

    # UI frissítése a felhasználó üzenetével
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, "👤 Te:\n", 'user')
    text_widget.insert(tk.END, user_input + "\n\n")
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END) # Görgetés a végére

    # Gemini válasz kérése
    try:
        response = chat_session.send_message(user_input)
        
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, "🤖 Gemini Interjúztató:\n", 'bot')
        text_widget.insert(tk.END, response.text + "\n\n", 'bot')
        text_widget.config(state=tk.DISABLED)
        text_widget.see(tk.END) # Görgetés a végére
        
    except APIError as e:
        messagebox.showerror("Gemini Hiba", f"API hiba történt: {e}. Próbáld meg újraindítani az interjút.")
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba a válasz kérésekor: {e}")

# --- Fő UI (Chat Ablak) Létrehozása ---

def create_chatbot_ui(cv_content):
    """Létrehozza a Chatbot ablakot és elindítja az interjút a CV tartalommal."""
    
    chat_root = tk.Tk()
    chat_root.title("🤖 Gemini Interjú Szimuláció")
    chat_root.geometry("700x600")

    main_frame = ttk.Frame(chat_root, padding="10")
    main_frame.pack(fill="both", expand=True)

    # 1. Beszélgetési Előzmények Terület (scrolledtext)
    interview_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, height=20, font=('Arial', 10))
    interview_text.tag_config('bot', foreground='blue')
    interview_text.tag_config('user', foreground='green')
    interview_text.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Kezdő üdvözlés
    interview_text.config(state=tk.NORMAL)
    interview_text.insert(tk.END, "🎉 Interjú elindítva. Betöltött CV tartalom alapján kezdődik a beszélgetés...\n\n")
    interview_text.config(state=tk.DISABLED)

    # 2. Beviteli Terület
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(padx=5, pady=5, fill="x")

    user_entry = ttk.Entry(input_frame, width=70, font=('Arial', 10))
    # A küldés gombot az Enter lenyomásával is lehessen aktiválni
    user_entry.bind("<Return>", lambda event: send_message(user_entry, interview_text))
    user_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))

    send_button = ttk.Button(
        input_frame, 
        text="Küldés", 
        command=lambda: send_message(user_entry, interview_text)
    )
    send_button.pack(side=tk.RIGHT)
    
    # 3. Interjú elindítása a Gemini-val
    start_interview(cv_content, interview_text)

    chat_root.mainloop()

# A chatbot.py nem indul el magától, csak a select_cv.py hívja meg a függvényét!
# if __name__ == "__main__":
#     create_chatbot_ui("Teszt CV tartalom.")