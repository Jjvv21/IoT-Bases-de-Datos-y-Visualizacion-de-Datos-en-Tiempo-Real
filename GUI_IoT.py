import customtkinter as ctk
import os 
from PIL import Image
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

    
        title = ctk.CTkLabel(self, text="Registro de actividad", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")


        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Botón para ver lecturas
        self.btn_leer = ctk.CTkButton(self, text="Mostrar lecturas",
                                    command=self.master.mostrar_lecturas)
        self.btn_leer.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Cuadro donde se mostrarán los logs
        self.log_box = ctk.CTkTextbox(self, height=200)
        self.log_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")




class graphs(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        title = ctk.CTkLabel(self, text="Gráficos en tiempo real", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        body = ctk.CTkLabel(self, text="Aquí se mostrará Grafana")
        body.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")


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
        lecturas = list(self.mongo_collection.find().sort("timestamp", -1).limit(5))

        # Limpiar texto del log
        self.log_panel.log_box.delete("1.0", "end")

        # Añadir registros
        for l in lecturas:
            linea = f"[{l['timestamp']}] {l['serial']} → Volt:{l['voltaje']}V | Corr:{l['corriente']}A | Pot:{l['potencia']}W\n"
            self.log_panel.log_box.insert("end", linea)

        # Actualizar automáticamente cada 2 segundos
        self.after(2000, self.mostrar_lecturas)


if __name__ == "__main__":
    app = App()   
    app.mainloop() 

