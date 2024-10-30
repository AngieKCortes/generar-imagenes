import requests
from tkinter import Tk, Label, Entry, Button, StringVar, Frame, messagebox
from io import BytesIO
from PIL import Image, ImageTk

# Clave de la API de Pixabay (reemplázala con la tuya)
API_KEY = '46798241-0499ac0066547af7cdd8c6d65'

# Función para obtener imágenes de Pixabay
def obtener_imagenes():
    palabra_clave = entrada_palabra.get().strip()
    
    if not palabra_clave:
        messagebox.showerror("Error", "Por favor, ingresa una palabra clave.")
        return

    # Realiza la búsqueda sin restringir la categoría, solicitando hasta 8 imágenes
    url = f'https://pixabay.com/api/?key={API_KEY}&q={palabra_clave}&image_type=photo&per_page=8'
    respuesta = requests.get(url)
    datos = respuesta.json()

    # Elimina cualquier imagen anterior
    for widget in marco_imagenes.winfo_children():
        widget.destroy()

    if datos['totalHits'] > 0:
        # Cargar y mostrar hasta 8 imágenes obtenidas
        for imagen_info in datos['hits']:
            imagen_url = imagen_info['webformatURL']
            imagen_respuesta = requests.get(imagen_url)
            imagen_datos = BytesIO(imagen_respuesta.content)

            # Convertir la imagen
            imagen_pil = Image.open(imagen_datos)
            imagen_pil = imagen_pil.resize((100, 100))  # Redimensionar para 8 imágenes en pantalla
            imagen_tk = ImageTk.PhotoImage(imagen_pil)

            # Crear etiqueta de imagen en el marco
            etiqueta_imagen = Label(marco_imagenes, image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
            etiqueta_imagen.pack(side="left", padx=5, pady=5)
        
        etiqueta_mensaje.config(text=f"Mostrando resultados para '{palabra_clave}'")
    else:
        etiqueta_mensaje.config(text="No se encontraron imágenes para tu búsqueda.")

# Configuración de la ventana de la aplicación
ventana = Tk()
ventana.title("Buscador de Imágenes con Pixabay")
ventana.geometry("800x600")

# Entrada de texto para palabra clave
entrada_palabra = StringVar()
label = Label(ventana, text="Ingresa una palabra clave:", font=("Arial", 12))
label.pack(pady=10)
entrada = Entry(ventana, textvariable=entrada_palabra, font=("Arial", 12), width=30)
entrada.pack()

# Botón de búsqueda
boton = Button(ventana, text="Buscar Imágenes", command=obtener_imagenes, font=("Arial", 12))
boton.pack(pady=10)

# Mensaje para resultados
etiqueta_mensaje = Label(ventana, text="", font=("Arial", 12))
etiqueta_mensaje.pack()

# Marco para organizar múltiples imágenes
marco_imagenes = Frame(ventana)
marco_imagenes.pack(pady=10)

ventana.mainloop()
