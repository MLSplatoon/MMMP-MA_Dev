import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json
import zipfile
import toml


# ╔╦╗╦╔╗╔╔═╗╔═╗╦═╗╔═╗╔═╗╔╦╗  ╔╦╗╔═╗╔╦╗        
# ║║║║║║║║╣ ║  ╠╦╝╠═╣╠╣  ║   ║║║║ ║ ║║        
# ╩ ╩╩╝╚╝╚═╝╚═╝╩╚═╩ ╩╚   ╩   ╩ ╩╚═╝═╩╝        
# ╔╦╗╔═╗╔╗╔╔═╗╔═╗╔═╗╦═╗  ╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔╦╗
# ║║║╠═╣║║║╠═╣║ ╦║╣ ╠╦╝  ╠═╝╠╦╝║ ║║ ╦╠╦╝╠═╣║║║
# ╩ ╩╩ ╩╝╚╝╩ ╩╚═╝╚═╝╩╚═  ╩  ╩╚═╚═╝╚═╝╩╚═╩ ╩╩ ╩




# ███▄ ▄███▓ ▄▄▄         ▓█████▄ ▓█████ ██▒   █▓
# ▓██▒▀█▀ ██▒▒████▄       ▒██▀ ██▌▓█   ▀▓██░   █▒
#▓██    ▓██░▒██  ▀█▄     ░██   █▌▒███   ▓██  █▒░
#▒██    ▒██ ░██▄▄▄▄██    ░▓█▄   ▌▒▓█  ▄  ▒██ █░░
#▒██▒   ░██▒ ▓█   ▓██▒   ░▒████▓ ░▒████▒  ▒▀█░  
#░ ▒░   ░  ░ ▒▒   ▓▒█░    ▒▒▓  ▒ ░░ ▒░ ░  ░ ▐░  
#░  ░      ░  ▒   ▒▒ ░    ░ ▒  ▒  ░ ░  ░  ░ ░░  
#░      ░     ░   ▒       ░ ░  ░    ░       ░░  
#       ░         ░  ░      ░       ░  ░     ░  
#                         ░                 ░   



def obtener_ruta_base():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS 
    else:
        return os.path.dirname(__file__)

ruta_base = obtener_ruta_base()
ruta_icono = os.path.join(ruta_base, "logo-exe.ico")
ruta_app = os.path.join(ruta_base, "logoApp.png")
ruta_creador = os.path.join(ruta_base, "logoCreador.png")


def mostrar_imagen(img_path, label, window):
    
    img = Image.open(img_path)
    
    
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    
    if window_width == 1 or window_height == 1:
        window.update_idletasks()
        window.update()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
    
    
    max_width = int(window_width * 0.8)  
    max_height = int(window_height * 0.8)  
    
    
    img_width, img_height = img.size
    
    
    ratio = min(max_width / img_width, max_height / img_height)
    
    
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    
    
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    
    img_tk = ImageTk.PhotoImage(img)
    
    
    label.config(image=img_tk)
    label.image = img_tk
    
    
    window.update_idletasks()
    window.update()


def clear_default_text(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END) 


def restore_default_text(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)


def mostrar_pantalla_inicio():
   
    window = tk.Tk()
    window.title("Welcome, Loading MMMP...")
    window.geometry("800x600")
    window.iconbitmap(ruta_icono)
    window.configure(bg="#2E3440")

    
    label = tk.Label(window)
    label.pack(pady=100)

    
    mostrar_imagen(ruta_app, label, window)

    
    window.after(1500, lambda: mostrar_imagen(ruta_creador, label, window))

    
    window.after(3000, lambda: iniciar_ventana_principal(window))

    
    window.mainloop()


def iniciar_ventana_principal(window):
    window.destroy() 
    
    
    root = tk.Tk()
    root.title("Minecraft Mod Manager Program (MMMP) - By MA_Dev (1.0)")
    root.geometry("800x600")
    root.iconbitmap(ruta_icono)
    root.configure(bg="#2E3440")

    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Arial", 12, "bold"), padding=10, background="#88C0D0", foreground="#2E3440")
    style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#ECEFF4", fieldbackground="#ECEFF4")
    style.configure("Treeview.Heading", font=("Arial Bold", 12), background="#4C566A", foreground="#ECEFF4")

    
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    
    tree = ttk.Treeview(frame, columns=("name", "version", "author"), show="headings", selectmode="browse")
    tree.heading("name", text="Nombre del Mod")
    tree.heading("version", text="Versión")
    tree.heading("author", text="Autor/res")
    tree.column("name", width=350, anchor="w")
    tree.column("version", width=100, anchor="center")
    tree.column("author", width=200, anchor="center")

   
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

   
    version_var = tk.StringVar()
    version_entry = ttk.Entry(root, textvariable=version_var, font=("Arial", 12), width=20)
    version_entry.insert(0, "Versión del Mod...") 
    version_entry.bind("<FocusIn>", lambda event: clear_default_text(version_entry, "Versión del Mod..."))
    version_entry.bind("<FocusOut>", lambda event: restore_default_text(version_entry, "Versión del Mod..."))
    version_entry.pack(pady=10)

    
    name_var = tk.StringVar()
    name_entry = ttk.Entry(root, textvariable=name_var, font=("Arial", 12), width=20)
    name_entry.insert(0, "Nombre del Mod...")  
    name_entry.bind("<FocusIn>", lambda event: clear_default_text(name_entry, "Nombre del Mod..."))
    name_entry.bind("<FocusOut>", lambda event: restore_default_text(name_entry, "Nombre del Mod..."))
    name_entry.pack(pady=10)

    
    load_button = ttk.Button(root, text="Buscar y mostrar Mods", command=lambda: display_mods(tree))
    load_button.pack(pady=10)

   
    filter_button = ttk.Button(root, text="Filtrar por Versión", command=lambda: filter_mods_by_version(tree, version_var.get()))
    filter_button.pack(pady=10)

    
    search_button = ttk.Button(root, text="Buscar por Nombre", command=lambda: search_mod_by_name(tree, name_var.get()))
    search_button.pack(pady=10)

    
    root.mainloop()


appdata_path = os.getenv('APPDATA') 
minecraft_path = os.path.join(appdata_path, '.minecraft', 'mods') 

def get_mod_info(mod_path):
    mod_info = {
        "name": "Desconocido",
        "version": "Desconocido",
        "author": "Desconocido"
    }

    try:
        with zipfile.ZipFile(mod_path, 'r') as jar_file:
            # `fabric.mod.json`
            if "fabric.mod.json" in jar_file.namelist():
                with jar_file.open("fabric.mod.json") as f:
                    fabric_data = json.load(f)
                    mod_info["name"] = fabric_data.get("name", "Desconocido")
                    mod_info["version"] = fabric_data.get("version", "Desconocido")
                    authors = fabric_data.get("authors", [])
                    mod_info["author"] = parse_authors(authors)
            #  `mcmod.info`
            elif "mcmod.info" in jar_file.namelist():
                with jar_file.open("mcmod.info") as f:
                    mcmod_data = json.load(f)
                    if isinstance(mcmod_data, list):
                        mcmod_data = mcmod_data[0]
                    mod_info["name"] = mcmod_data.get("name", "Desconocido")
                    mod_info["version"] = mcmod_data.get("version", "Desconocido")
                    authors = mcmod_data.get("authors", [])
                    mod_info["author"] = parse_authors(authors)
            # `META-INF/mods.toml`
            elif "META-INF/mods.toml" in jar_file.namelist():
                with jar_file.open("META-INF/mods.toml") as f:
                    toml_data = toml.load(f)
                    mod_data = toml_data.get("mods", [{}])[0]
                    mod_info["name"] = mod_data.get("displayName", "Desconocido")
                    mod_info["version"] = mod_data.get("version", "Desconocido")
                    authors = mod_data.get("authors", "Desconocido")
                    mod_info["author"] = parse_authors(authors)
    except Exception as e:
        print(f"Error leyendo el mod {mod_path}: {e}")

    return mod_info

def parse_authors(authors):
    if isinstance(authors, list):
        if all(isinstance(author, dict) for author in authors):
            return ", ".join(author.get("name", "Desconocido") for author in authors)
        return ", ".join(authors)
    elif isinstance(authors, str):
        return authors
    return "Desconocido"

def get_mods_list():
    mods = []
    if not os.path.exists(minecraft_path):
        messagebox.showerror("Error", f"No se encontró la carpeta de mods en: {minecraft_path}")
        return []

    for filename in os.listdir(minecraft_path):
        if filename.endswith(".jar"):
            mod_path = os.path.join(minecraft_path, filename)
            mod_info = get_mod_info(mod_path)
            mods.append(mod_info)
    return mods

def display_mods(tree):
    mods = get_mods_list()
    if not mods:
        messagebox.showinfo("Sin mods", "No se han encontrado mods en ./minecraft/mods")
        return

    for item in tree.get_children():
        tree.delete(item)

    for mod in mods:
        tree.insert("", "end", values=(mod['name'], mod['version'], mod['author']))

def filter_mods_by_version(tree, version_filter):
    mods = get_mods_list()
    if not mods:
        messagebox.showinfo("Sin mods", "No se han encontrado mods en ./minecraft/mods")
        return

    filtered_mods = [mod for mod in mods if version_filter.lower() in mod["version"].lower()]

    if not filtered_mods:
        messagebox.showinfo("No hay resultados", f"No se encontraron mods con la versión '{version_filter}'")
        return

    
    for item in tree.get_children():
        tree.delete(item)

    
    for mod in filtered_mods:
        tree.insert("", "end", values=(mod['name'], mod['version'], mod['author']))

def search_mod_by_name(tree, name_filter):
    mods = get_mods_list()
    if not mods:
        messagebox.showinfo("Sin mods", "No se han encontrado mods en ./minecraft/mods")
        return

    
    filtered_mods = [mod for mod in mods if name_filter.lower() in mod["name"].lower()]

    if not filtered_mods:
        messagebox.showinfo("No hay resultados", f"No se encontraron mods con el nombre '{name_filter}'")
        return

    
    for item in tree.get_children():
        tree.delete(item)

    
    for mod in filtered_mods:
        tree.insert("", "end", values=(mod['name'], mod['version'], mod['author']))


mostrar_pantalla_inicio()
# MA_DEV 2024 08/01/2025
