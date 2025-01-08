import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import json
import zipfile
import toml

def obtener_ruta_base():
    if getattr(sys, 'frozen', False):  # Si el programa está empaquetado
        return sys._MEIPASS  # Carpeta temporal creada por PyInstaller
    else:
        return os.path.dirname(__file__)  # Usar la ubicación del script durante el desarrollo

# Definir rutas a los archivos de recursos
ruta_base = obtener_ruta_base()
ruta_icono = os.path.join(ruta_base, "logo-exe.ico")
ruta_app = os.path.join(ruta_base, "logoApp.png")
ruta_creador = os.path.join(ruta_base, "logoCreador.png")

# Función para mostrar la imagen
def mostrar_imagen(img_path, label, window):
    # Cargar la imagen
    img = Image.open(img_path)
    
    # Obtener las dimensiones de la ventana
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    # Verificar si la ventana tiene dimensiones válidas
    if window_width == 1 or window_height == 1:
        window.update_idletasks()
        window.update()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
    
    # Definir un porcentaje del tamaño de la ventana para el tamaño máximo de la imagen
    max_width = int(window_width * 0.8)  # 80% del ancho de la ventana
    max_height = int(window_height * 0.8)  # 80% de la altura de la ventana
    
    # Obtener el tamaño original de la imagen
    img_width, img_height = img.size
    
    # Calcular el ratio para redimensionar la imagen proporcionalmente
    ratio = min(max_width / img_width, max_height / img_height)
    
    # Calcular las nuevas dimensiones
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    
    # Redimensionar la imagen manteniendo la proporción
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convertir la imagen final a formato adecuado para tkinter
    img_tk = ImageTk.PhotoImage(img)
    
    # Actualizar la etiqueta para mostrar la nueva imagen
    label.config(image=img_tk)
    label.image = img_tk
    
    # Mostrar la imagen
    window.update_idletasks()
    window.update()

# Función para limpiar el texto predeterminado
def clear_default_text(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)  # Borrar el texto predeterminado

# Función para restaurar el texto predeterminado si el cuadro está vacío
def restore_default_text(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)  # Volver a insertar el texto predeterminado

# Función para mostrar la pantalla de inicio y luego cargar la ventana principal
def mostrar_pantalla_inicio():
    # Crear la ventana de inicio
    window = tk.Tk()
    window.title("Welcome, Loading MMMP...")
    window.geometry("800x600")
    window.iconbitmap(ruta_icono)
    window.configure(bg="#2E3440")

    # Crear una etiqueta para mostrar las imágenes
    label = tk.Label(window)
    label.pack(pady=100)  # Centrar la etiqueta

    # Mostrar el logo de la aplicación
    mostrar_imagen(ruta_app, label, window)

    # Esperar 1.5 segundos (1500 ms) y luego mostrar el logo del creador
    window.after(1500, lambda: mostrar_imagen(ruta_creador, label, window))

    # Esperar 1.5 segundos más y luego cerrar la ventana de inicio y continuar con la ventana principal
    window.after(3000, lambda: iniciar_ventana_principal(window))

    # Ejecutar la ventana de inicio
    window.mainloop()

# Función para iniciar la ventana principal con el gestor de mods
def iniciar_ventana_principal(window):
    window.destroy()  # Cerrar la ventana de inicio
    
    # Crear la ventana principal para gestionar los mods de Minecraft
    root = tk.Tk()
    root.title("Minecraft Mod Manager Program (MMMP) - By MA_Dev (1.0)")
    root.geometry("800x600")
    root.iconbitmap(ruta_icono)
    root.configure(bg="#2E3440")  # Fondo oscuro

    # Estilo de botones y widgets
    style = ttk.Style()
    style.theme_use("clam")  # Tema moderno
    style.configure("TButton", font=("Arial", 12, "bold"), padding=10, background="#88C0D0", foreground="#2E3440")
    style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#ECEFF4", fieldbackground="#ECEFF4")
    style.configure("Treeview.Heading", font=("Arial Bold", 12), background="#4C566A", foreground="#ECEFF4")

    # Crear un marco (frame) para contener el Treeview y la barra de desplazamiento
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Crear un Treeview para mostrar los mods
    tree = ttk.Treeview(frame, columns=("name", "version", "author"), show="headings", selectmode="browse")
    tree.heading("name", text="Nombre del Mod")
    tree.heading("version", text="Versión")
    tree.heading("author", text="Autor/res")
    tree.column("name", width=350, anchor="w")
    tree.column("version", width=100, anchor="center")
    tree.column("author", width=200, anchor="center")

    # Crear la barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Empaquetar el Treeview y la barra de desplazamiento
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    # Crear un campo de texto para ingresar la versión
    version_var = tk.StringVar()
    version_entry = ttk.Entry(root, textvariable=version_var, font=("Arial", 12), width=20)
    version_entry.insert(0, "Versión del Mod...")  # Texto predeterminado
    version_entry.bind("<FocusIn>", lambda event: clear_default_text(version_entry, "Versión del Mod..."))
    version_entry.bind("<FocusOut>", lambda event: restore_default_text(version_entry, "Versión del Mod..."))
    version_entry.pack(pady=10)

    # Crear un campo de texto para ingresar el nombre del mod
    name_var = tk.StringVar()
    name_entry = ttk.Entry(root, textvariable=name_var, font=("Arial", 12), width=20)
    name_entry.insert(0, "Nombre del Mod...")  # Texto predeterminado
    name_entry.bind("<FocusIn>", lambda event: clear_default_text(name_entry, "Nombre del Mod..."))
    name_entry.bind("<FocusOut>", lambda event: restore_default_text(name_entry, "Nombre del Mod..."))
    name_entry.pack(pady=10)

    # Botón estilizado para cargar los mods
    load_button = ttk.Button(root, text="Buscar y mostrar Mods", command=lambda: display_mods(tree))
    load_button.pack(pady=10)

    # Botón para filtrar los mods por la versión
    filter_button = ttk.Button(root, text="Filtrar por Versión", command=lambda: filter_mods_by_version(tree, version_var.get()))
    filter_button.pack(pady=10)

    # Botón para buscar por nombre
    search_button = ttk.Button(root, text="Buscar por Nombre", command=lambda: search_mod_by_name(tree, name_var.get()))
    search_button.pack(pady=10)

    # Iniciar la interfaz gráfica
    root.mainloop()

# Funciones de manejo de mods (las mismas que tenías)
appdata_path = os.getenv('APPDATA')  # Esto obtiene la variable de entorno APPDATA
minecraft_path = os.path.join(appdata_path, '.minecraft', 'mods')  # Ruta completa a la carpeta mods

def get_mod_info(mod_path):
    mod_info = {
        "name": "Desconocido",
        "version": "Desconocido",
        "author": "Desconocido"
    }

    try:
        with zipfile.ZipFile(mod_path, 'r') as jar_file:
            # Intentar leer `fabric.mod.json`
            if "fabric.mod.json" in jar_file.namelist():
                with jar_file.open("fabric.mod.json") as f:
                    fabric_data = json.load(f)
                    mod_info["name"] = fabric_data.get("name", "Desconocido")
                    mod_info["version"] = fabric_data.get("version", "Desconocido")
                    authors = fabric_data.get("authors", [])
                    mod_info["author"] = parse_authors(authors)
            # Intentar leer `mcmod.info`
            elif "mcmod.info" in jar_file.namelist():
                with jar_file.open("mcmod.info") as f:
                    mcmod_data = json.load(f)
                    if isinstance(mcmod_data, list):
                        mcmod_data = mcmod_data[0]
                    mod_info["name"] = mcmod_data.get("name", "Desconocido")
                    mod_info["version"] = mcmod_data.get("version", "Desconocido")
                    authors = mcmod_data.get("authors", [])
                    mod_info["author"] = parse_authors(authors)
            # Intentar leer `META-INF/mods.toml`
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

    # Filtrar los mods por versión
    filtered_mods = [mod for mod in mods if version_filter.lower() in mod["version"].lower()]

    if not filtered_mods:
        messagebox.showinfo("No hay resultados", f"No se encontraron mods con la versión '{version_filter}'")
        return

    # Limpiar el Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Mostrar los mods filtrados
    for mod in filtered_mods:
        tree.insert("", "end", values=(mod['name'], mod['version'], mod['author']))

def search_mod_by_name(tree, name_filter):
    mods = get_mods_list()
    if not mods:
        messagebox.showinfo("Sin mods", "No se han encontrado mods en ./minecraft/mods")
        return

    # Filtrar los mods por nombre
    filtered_mods = [mod for mod in mods if name_filter.lower() in mod["name"].lower()]

    if not filtered_mods:
        messagebox.showinfo("No hay resultados", f"No se encontraron mods con el nombre '{name_filter}'")
        return

    # Limpiar el Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Mostrar los mods filtrados
    for mod in filtered_mods:
        tree.insert("", "end", values=(mod['name'], mod['version'], mod['author']))

# Llamar a la pantalla de inicio
mostrar_pantalla_inicio()
