from tkinter import Tk, Label, Frame, Button, Entry, ttk, LabelFrame, messagebox
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from Controlador import Controlador

class Pedidos:
    db_name = 'BDMerksandSpendall.db'
    
    def __init__(self, ventana):
        self.conexion = Controlador()
        self.ventana = ventana
        self.ventana.title('Articulos Usuarios')
        self.ventana.geometry('800x670')

        titulo = Label(ventana, text="BUSCADOR ARTICULOS", fg="black", font=("Comic Sans", 17, "bold"), pady=10)
        titulo.pack()

        imagen_articulo = Image.open("C:\\Users\\josuu\\OneDrive\\Documentos\\POO\\merks_and_spen_2\\imagenes\\online-shopping-mexico-800-3423d44e0.png")
        nueva_img = imagen_articulo.resize((60, 60))
        render = ImageTk.PhotoImage(nueva_img)
        label_image = Label(ventana, image=render)
        label_image.image = render
        label_image.pack(pady=10)

        #  área de búsqueda
        frame_buscador = Frame(ventana)
        frame_buscador.pack(padx=10, pady=10)

        # LabelFrame para encerrar el área de búsqueda
        label_frame_buscador = LabelFrame(frame_buscador, text="Buscar Articulos", font=("Comic Sans", 12, "bold"))
        label_frame_buscador.pack()

        self.frame_buscar_producto = Frame(label_frame_buscador)
        self.frame_buscar_producto.pack()

        self.label_buscar = Label(self.frame_buscar_producto, text="Buscar Por: ", font=("Comic Sans", 10, "bold"))
        self.label_buscar.grid(row=0, column=0, sticky='s', padx=5, pady=5)

        self.combo_buscar = ttk.Combobox(self.frame_buscar_producto, values=["Codigo", "Nombre"], width=22, state="readonly")
        self.combo_buscar.current(0)
        self.combo_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.label_codigo_nombre = Label(self.frame_buscar_producto, text="Codigo / Nombre del producto: ", font=("Comic Sans", 10, "bold"))
        self.label_codigo_nombre.grid(row=0, column=2, sticky='s', padx=5, pady=5)

        self.codigo_nombre = Entry(self.frame_buscar_producto, width=25)
        self.codigo_nombre.focus()
        self.codigo_nombre.grid(row=0, column=3, padx=10, pady=5)

        # mostrar los resultados de la búsqueda
        self.tree = ttk.Treeview(ventana, height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5"))
        self.tree.heading("#0", text="Codigo", anchor="center")
        self.tree.column("#0", width=90, minwidth=75, stretch="no")

        self.tree.heading("columna1", text="Nombre", anchor="center")
        self.tree.column("columna1", width=150, minwidth=75, stretch="no")

        self.tree.heading("columna2", text="Categoria", anchor="center")
        self.tree.column("columna2", width=150, minwidth=75, stretch="no")

        self.tree.heading("columna3", text="Cantidad", anchor="center")
        self.tree.column("columna3", width=150, minwidth=60, stretch="no")

        self.tree.heading("columna4", text="Precio", anchor="center")
        self.tree.column("columna4", width=150, minwidth=60, stretch="no")

        self.tree.heading("columna5", text="Descripcion", anchor="center")
        self.tree.pack()

       
        label_espacio = Label(frame_buscador, text="", font=("Comic Sans", 10, "bold"))
        label_espacio.pack(side="left", padx=80)  

       
        self.boton_buscar = Button(frame_buscador, text="BUSCAR", command=self.Buscar_articulos, height=2, width=20, bg="green", fg="white", font=("Comic Sans", 10, "bold"))
        self.boton_buscar.pack(side="left", padx=5, pady=8)

      
        # self.boton_generar_ticket = Button(frame_buscador, text="Generar Ticket", height=2, width=15, bg="blue", fg="white", font=("Comic Sans", 10, "bold"), command=self.pedir_articulo)
        # self.boton_generar_ticket.pack(side="left", padx=5, pady=8)
        
        self.boton_pedir = Button(frame_buscador, text="Pedir", height=2, width=15, bg="orange", fg="white", font=("Comic Sans", 10, "bold"), command=self.pedir_articulo)
        self.boton_pedir.pack(side="left", padx=5, pady=8)

    def Buscar_articulos(self):
        if(self.Validar_busqueda()):
            # Obtener todos los elementos con get_children(), que retorna una tupla de ID.
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            
            if (self.combo_buscar.get() == 'Codigo'):
                query = ("SELECT * FROM articulos WHERE Codigo LIKE ? ")
                parameters = (self.codigo_nombre.get() + "%")
                db_rows = self.conexion.ejecutar_consulta(self.conexion.conexion(), query, (parameters,))
                for row in db_rows:
                    self.tree.insert("", 0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))
                if(list(self.tree.get_children()) == []):
                    messagebox.showerror("ERROR", "Producto no encontrado")
            else:
                query = ("SELECT * FROM articulos WHERE Nombre LIKE ? ")
                parameters = ("%" + self.codigo_nombre.get() + "%")
                db_rows = self.conexion.ejecutar_consulta(self.conexion.conexion(), query, (parameters,))
                for row in db_rows:
                    self.tree.insert("", 0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))
                if(list(self.tree.get_children()) == []):
                    messagebox.showerror("ERROR", "Producto no encontrado")
                    
    def Validar_busqueda(self):
        if len(self.codigo_nombre.get()) != 0:
            return True
        else:
            self.tree.delete(*self.tree.get_children())
            messagebox.showerror("ERROR", "Complete todos los campos para la busqueda") 

    def generar_ticket(self, elementos_seleccionados):
        if not elementos_seleccionados:
            messagebox.showerror("Error", "Por favor selecciona al menos un artículo para generar el ticket.")
            return

        # Crear el documento PDF
        c = canvas.Canvas("ticket.pdf", pagesize=letter)
        
        # Escribir el contenido del ticket
        c.drawString(100, 750, "Ticket de Compra")
        c.drawString(100, 730, "--------------------------")
        y = 700
        for i, item_id in enumerate(elementos_seleccionados):
            articulo = self.tree.item(item_id)['values']
            c.drawString(100, y, f"Artículo {i + 1}: {articulo[0]} - ${articulo[3]} - Cantidad: {articulo[2]} - Categoria: {articulo[1]} ")
            y -= 20
        
       
        c.save()
        messagebox.showinfo("Ticket generado", "Se ha generado el ticket correctamente como 'ticket.pdf'")
        self.abrir_pdf()

    def abrir_pdf(self):
        filepath = os.path.abspath("ticket.pdf")
        os.system(f'start {filepath}')
        
    def pedir_articulo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor selecciona al menos un artículo para pedir.")
            return

        elementos_seleccionados = list(seleccion)
        self.generar_ticket(elementos_seleccionados)

        for item_id in seleccion:
            articulo = self.tree.item(item_id)
            # Obtener nombre, id y cantidad del artículo seleccionado
            nombre = articulo['text']
            valores = articulo['values']
            id = valores[0]  # ID del artículo
            cantidad = valores[2]
            # Agregar el artículo a la tabla de pedidos
            self.agregar_pedido(nombre, id, cantidad)

        messagebox.showinfo("Pedido enviado", "Tu solicitud ha sido enviada correctamente.")

    def agregar_pedido(self, nombre, id, cantidad):
        # Obtener la conexión a la base de datos
        conexion = self.conexion.conexion()
        # Insertar el artículo en la tabla de pedidos
        query = "INSERT INTO pedidos (id_articulo, cantidad) VALUES (?, ?)"
        parameters = (id, cantidad)
        self.conexion.ejecutar_modificacion(query, parameters)

if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Pedidos(ventana)
    ventana.mainloop()
