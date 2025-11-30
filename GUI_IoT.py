import customtkinter as ctk
import os 
from PIL import Image, ImageTk
from pymongo import MongoClient
from datetime import datetime
import webbrowser

class devices(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Header del panel
        title = ctk.CTkLabel(self, text="Dispositivos IoT conectados", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Configuración interna
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Contenido placeholder
        body = ctk.CTkLabel(self, text="Aquí aparecerán los dispositivos...")
        body.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

class log(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Título vacío
        title = ctk.CTkLabel(self, text="")
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Título real centrado
        title = ctk.CTkLabel(
            self,
            text="Registro de actividad",
            font=("Arial", 20, "bold"),
            text_color="#cccccc"
        )
        title.place(relx=0.5, rely=0.1, anchor="center")

        # Configurar grid interno
        self.grid_columnconfigure(0, weight=1)  # hace que la columna permita centrar
        self.grid_rowconfigure(2, weight=1)

        # Botón centrado
        self.btn_leer = ctk.CTkButton(
            self,
            text="Mostrar lecturas",
            command=self.master.mostrar_lecturas
        )
        self.btn_leer.grid(row=1, column=0, pady=10)  # sin sticky, queda centrado

        # Cuadro donde se mostrarán los logs
        self.log_box = ctk.CTkTextbox(self, height=250, font=("Consolas", 15))
        self.log_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")



class graphs(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuración del grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #IMAGEN DE FONDO CON OPACIDAD 
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "ImagenesProyecto", "grafanaframe.png")
        
        try:
            self.bg_image = Image.open(image_path)
        except Exception as e:
            print(f"No se pudo cargar la imagen de fondo: {e}")
            self.bg_image = None

        # Label que será el fondo
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Actualizar fondo al inicio y cada vez que cambie el tamaño
        self.after(100, self.update_background)  # Pequeño retraso para que el frame tenga tamaño
        self.bind("<Configure>", lambda e: self.update_background())

        # ==================== BOTÓN CENTRADO ====================
        self.grafana_button = ctk.CTkButton(
            self,
            text="Mostrar gráficos en Grafana",
            font=("Arial", 18, "bold"),
            width=400,
            height=40,
            corner_radius=15,
            fg_color="#1f6aa5",           # Azul típico de Grafana
            hover_color="#144a7d",
            border_width=2,
            border_color="#2d8cff",
            command=self.open_grafana  # Aquí pondrás tu función real
        )
        self.grafana_button.place(relx=0.5, rely=0.5, anchor="center")

        # ==================== TÍTULO (opcional, puedes mantenerlo o quitarlo) ====================
        title = ctk.CTkLabel(
            self,
            text="Gráficos en tiempo real",
            font=("Arial", 20, "bold"),
            text_color="#cccccc"
        )
        title.place(relx=0.5, rely=0.1, anchor="center")

    def update_background(self):
        if not self.bg_image:
            return

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return  # Todavía no tiene tamaño real

        # Redimensionar imagen
        img = self.bg_image.copy()
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Aplicar opacidad 
        opacity = 0.3
        if img.mode != 'RGBA':
            img = img.convert("RGBA")
        
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        img.putalpha(alpha)

        # Crear CTkImage y aplicar
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
        self.bg_label.configure(image=ctk_img)
        self.bg_label.image = ctk_img  # Mantener referencia

    def open_grafana(self):
        import webbrowser
        # Cambia esta URL por la tuya real de Grafana
        grafana_url = "http://localhost:3000"  # o tu dashboard específico
        webbrowser.open(grafana_url)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1300x800")
        self.title("Energo App")

        # Conexión MongoDB
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["iot_data"]
        self.mongo_collection = self.mongo_db["lecturas"]   

        # CONFIGURACIÓN DE GRID PRINCIPAL

        self.grid_rowconfigure(0, weight=0)   # Fila 0: logo NO se expande
        self.grid_rowconfigure(1, weight=1)   # Fila 1: paneles SÍ se expanden
        self.grid_columnconfigure(0, weight=1)  # Columna izquierda
        self.grid_columnconfigure(1, weight=4)  # Columna derecha (más grande)

        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "ImagenesProyecto", "logo.png") 
        self.logo_image = ctk.CTkImage(Image.open(image_path), size=(300, 300))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, padx=10, pady=20, sticky="nw")

        # COLUMNA IZQUIERDA: Dispositivos
        
        self.devices_panel = devices(master=self, fg_color="#2b2b2b", corner_radius=15)
        self.devices_panel.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Panel inferior: logs
        self.log_panel = log(master=self, fg_color="#2b2b2b", corner_radius=15)
        self.log_panel.grid(row=1, column=1, pady=(10, 0), sticky="nsew")

        # Panel superior: gráficos
        self.graph_panel = graphs(master=self, fg_color="#2b2b2b", corner_radius=15)
        self.graph_panel.grid(row=0, column=1, pady=(0, 10), sticky="nsew")
        
    def mostrar_lecturas(self):
        # Leer últimas 5 lecturas
        lecturas = list(self.mongo_collection.find().sort("timestamp", -1).limit(9))

        # Limpiar texto del log
        self.log_panel.log_box.delete("1.0", "end")

        # Añadir registros
        for l in lecturas:
            linea = f"[{l['timestamp']}] {l['serial']} → Volt:{l['voltaje']}V | Corr:{l['corriente']}A | Pot:{l['potencia']}W\n"
            self.log_panel.log_box.insert("end", linea)


        # Actualizar automáticamente cada 2 segundos
        self.after(1500, self.mostrar_lecturas)


if __name__ == "__main__":
    app = App()   
    app.mainloop() 

