import customtkinter as ctk
import json
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FILE_NAME = "tabs.json"

selected_name = None

# ---------- DATA ----------
def load_tabs():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

        fixed = {}
        for name, value in data.items():
            if isinstance(value, dict):
                fixed[name] = value
            else:
                fixed[name] = {"amount": float(value), "date": "unknown"}
        return fixed
    return {}

def save_tabs():
    with open(FILE_NAME, "w") as f:
        json.dump(tabs, f, indent=4)

tabs = load_tabs()

# ---------- FUNCTIONS ----------
def select(name):
    global selected_name
    selected_name = name
    selected_label.configure(text=f"selected: {name}")

def add_tab():
    name = name_entry.get().strip()
    try:
        amount = float(amount_entry.get())
    except:
        return

    now = datetime.now().strftime("%Y-%m-%d")

    if name in tabs:
        tabs[name]["amount"] += amount
        tabs[name]["date"] = now
    else:
        tabs[name] = {"amount": amount, "date": now}

    save_tabs()
    update_list()

def pay_tab():
    if not selected_name:
        return

    try:
        amount = float(amount_entry.get())
    except:
        return

    tabs[selected_name]["amount"] -= amount

    if tabs[selected_name]["amount"] <= 0:
        del tabs[selected_name]

    save_tabs()
    update_list()

def delete_tab():
    if not selected_name:
        return

    del tabs[selected_name]
    save_tabs()
    update_list()

def update_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    total = 0

    for name, data in sorted(tabs.items(), key=lambda x: -x[1]["amount"]):
        total += data["amount"]

        row = ctk.CTkFrame(list_frame)
        row.pack(fill="x", pady=5, padx=5)

        label = ctk.CTkLabel(row, text=f"{name} - ${data['amount']:.2f}")
        label.pack(side="left", padx=10)

        btn = ctk.CTkButton(row, text="select", width=70,
                            command=lambda n=name: select(n))
        btn.pack(side="right", padx=10)

    total_label.configure(text=f"total: ${total:.2f}")

# ---------- UI ----------
app = ctk.CTk()
app.title("judds tab counter")
app.geometry("500x550")

ctk.CTkLabel(app, text="judds tab counter", font=("Arial", 22)).pack(pady=10)

name_entry = ctk.CTkEntry(app, placeholder_text="name")
name_entry.pack(pady=5)

amount_entry = ctk.CTkEntry(app, placeholder_text="amount")
amount_entry.pack(pady=5)

btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="add", command=add_tab).grid(row=0, column=0, padx=5)
ctk.CTkButton(btn_frame, text="pay", command=pay_tab).grid(row=0, column=1, padx=5)
ctk.CTkButton(btn_frame, text="delete", command=delete_tab).grid(row=0, column=2, padx=5)

selected_label = ctk.CTkLabel(app, text="selected: none")
selected_label.pack(pady=5)

list_frame = ctk.CTkScrollableFrame(app, height=300)
list_frame.pack(fill="both", expand=True, padx=10, pady=10)

total_label = ctk.CTkLabel(app, text="")
total_label.pack(pady=5)

update_list()

app.mainloop()