from tkinter import Tk, Label, Frame, Button, Entry, ttk, LabelFrame, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import sqlite3
from Controlador import Controlador

class Graficas:
    def __init__(self, ventana):
        self.conexion = Controlador()
        self.ventana = ventana
        self.ventana.title('Graficas')
        self.ventana.geometry('800x670')

        titulo = Label(ventana, text="GRÁFICAS", fg="black", font=("Comic Sans", 17, "bold"), pady=10)
        titulo.pack()

        imagen_grafica = Image.open("C:\\Users\\josuu\\OneDrive\\Documentos\\POO\\merks_and_spen_2\\imagenes\\grafica.png")
        nueva_img = imagen_grafica.resize((60, 60))
        render = ImageTk.PhotoImage(nueva_img)
        label_image = Label(ventana, image=render)
        label_image.image = render
        label_image.pack(pady=10)

        #  área de búsqueda
        frame_buscador = Frame(ventana)
        frame_buscador.pack(padx=10, pady=10)

        # LabelFrame para encerrar el área de búsqueda
        label_frame_buscador = LabelFrame(frame_buscador, text="Generar Gráfica", font=("Comic Sans", 12, "bold"))
        label_frame_buscador.pack()

        self.frame_generar_grafica = Frame(label_frame_buscador)
        self.frame_generar_grafica.pack()

        self.label_parametro = Label(self.frame_generar_grafica, text="Seleccionar Parámetro: ", font=("Comic Sans", 10, "bold"))
        self.label_parametro.grid(row=0, column=0, sticky='s', padx=5, pady=5)

        self.combo_parametro = ttk.Combobox(self.frame_generar_grafica, values=["Artículos", "Pedidos"], width=22, state="readonly")
        self.combo_parametro.current(0)
        self.combo_parametro.grid(row=0, column=1, padx=5, pady=5)

        self.boton_generar_grafica = Button(self.frame_generar_grafica, text="Generar", command=self.generar_grafica, height=2, width=20, bg="green", fg="white", font=("Comic Sans", 10, "bold"))
        self.boton_generar_grafica.grid(row=0, column=2, padx=10, pady=5)

    def generar_grafica(self):
        parametro = self.combo_parametro.get()
        if parametro:
            if parametro == "Artículos":
                self.generar_grafica_articulos()
            elif parametro == "Pedidos":
                self.generar_grafica_pedidos()
        else:
            messagebox.showerror("Error", "Por favor selecciona un parámetro")

    def generar_grafica_articulos(self):
        # Conexión a la base de datos SQLite
        conn = self.conexion.conexion()
        cursor = conn.cursor()

        # Ejecutar una consulta SQL para seleccionar los datos
        cursor.execute("SELECT nombre, cantidad FROM articulos")
        data = cursor.fetchall()

        # Cerrar la conexión
        conn.close()

        # Preparar los datos para trazar
        nombres = [row[0] for row in data]
        cantidades = [row[1] for row in data]

        # Trazar los datos
        plt.bar(nombres, cantidades)
        plt.xlabel("Artículo")
        plt.ylabel("Cantidad")
        plt.title("Demandas de Artículos")
        plt.xticks(rotation=90)  
        plt.tight_layout()  
        plt.show()

    def generar_grafica_pedidos(self):
        # Conexión a la base de datos SQLite
        conn = self.conexion.conexion()
        cursor = conn.cursor()

        # Ejecutar una consulta SQL para seleccionar los pedidos más solicitados
        cursor.execute("SELECT id_articulo, COUNT(*) AS total_pedidos FROM pedidos GROUP BY id_articulo")


        data = cursor.fetchall()

        # Cerrar la conexión
        conn.close()

        # Preparar los datos para trazar
        nombres = [row[0] for row in data]
        cantidades = [row[1] for row in data]

        # Trazar los datos
        plt.bar(nombres, cantidades, color='skyblue')
        plt.xlabel("Artículo")
        plt.ylabel("Número de Pedidos")
        plt.title("Artículos Más Solicitados")
        plt.xticks(rotation=45)  
        plt.tight_layout()  
        plt.show()

if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Graficas(ventana)
    ventana.mainloop()
