# Energo  ⚡
### Sistema IoT para Monitoreo de Consumo Eléctrico en Tiempo Real

---

## Descripción General

Energo es una plataforma IoT diseñada para medir, almacenar y visualizar el consumo eléctrico en tiempo real. El sistema integra dispositivos basados en ESP32, un servicio intermedio en Python, almacenamiento híbrido con MySQL y MongoDB, visualización mediante Grafana y una interfaz gráfica desarrollada en CustomTkinter.

Su objetivo es proporcionar una herramienta completa para el análisis energético en hogares, laboratorios o entornos industriales, permitiendo comparar el comportamiento de distintos circuitos o dispositivos y detectar variaciones o picos de consumo.

---

## Características Principales

- Medición periódica de variables eléctricas (voltaje, corriente, potencia) mediante dispositivos ESP32.
- Registro automático de dispositivos IoT en MySQL con validación y control de acceso.
- Almacenamiento de lecturas en MongoDB como series temporales en formato JSON.
- Dashboard en Grafana con visualización en tiempo real y comparativa entre dispositivos.
- Aplicación gráfica (GUI) mediante CustomTkinter para monitoreo local.
- Log en vivo de las últimas lecturas recibidas desde MongoDB.
- Botón de acceso directo a Grafana.
- Integración a través de contenedores Docker mediante docker-compose.
- Arquitectura modular que permite añadir más sensores, dispositivos o paneles.

---

## Arquitectura del Sistema

El sistema completo sigue el siguiente flujo:

1. Los dispositivos ESP32 leen variables eléctricas mediante sensores.
2. Cada dispositivo solicita activación y registro en el servicio Python.
3. La API registra los dispositivos en MySQL y genera su identificador.
4. Los ESP32 envían lecturas periódicas al servicio Python.
5. Las lecturas validadas son almacenadas en MongoDB.
6. Grafana consulta MongoDB y visualiza los datos en tiempo real.
7. La aplicación GUI permite ver dispositivos, logs recientes y acceder al dashboard.

---

## Tecnologías Utilizadas

- ESP32 (nodos IoT)
- Python 3
- CustomTkinter
- MySQL
- MongoDB
- Grafana
- Docker y Docker Compose
- PIL (Pillow)
- Pymongo

---

## Estructura del Proyecto

/Proyecto
│
├── api/ # Servicio intermedio en Python
│
├── docker/ # Archivos y configuraciones de contenedores
│
├── grafana/ # Dashboards y configuración
│
├── mysql/ # Scripts de creación y datos iniciales
│
├── src/
│ ├── GUI_IoT.py # Interfaz gráfica Energo
│ ├── simulador.py # Envío simulado de lecturas (testing)
│ └── dispositivos/ # Código de ESP32 (si aplica)
│
└── README.md


---


## Instalación y Ejecución

### Requisitos previos

- Python 3.10 o superior  
- Docker y Docker Compose  
- MongoDB (local o en contenedor)  
- MySQL (local o en contenedor)

### 1. Clonar el repositorio


### 2. Crear entorno virtual


### 3. Levantar el sistema con Docker


### 4. Ejecutar la interfaz gráfica


---

## Uso de la Aplicación

### Interfaz principal

La aplicación Energo proporciona tres paneles principales:

- Panel de dispositivos: muestra los nodos ESP32 registrados.
- Panel de gráficos: permite acceder al dashboard de Grafana.
- Panel de logs: muestra en tiempo real las últimas lecturas recibidas desde MongoDB.

### Lecturas en vivo

Al presionar el botón "Mostrar lecturas", el sistema:

- Consulta los últimos cinco registros de MongoDB.
- Actualiza el panel de logs cada dos segundos.
- Muestra fecha, hora y valores recibidos.

### Visualización en Grafana

El botón "Abrir Grafana" abre el dashboard configurado.

---

## Autores

Gabriel Nuñez Morales-
Viviana Alfaro Brenes-
Greivin Carrillo Rodríguez-
José Loría Cordero-
Julio Varela Venegas.

Estudiantes de Ingeniería en Computadores  
Instituto Tecnológico de Costa Rica




