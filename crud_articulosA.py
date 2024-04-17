from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter import filedialog
from Controlador import *
# para poder mostrar imagenes en la interfaz
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class Articulo:
    db_name = 'bd_merks.db'
    def __init__(self, ventana_articulo):
        
        self.conexion = Controlador()
        self.ventana_editar = None
        self.window = ventana_articulo
        self.window.title('Articulos Administrador')
        self.window.geometry("800x670") 
        self.window.resizable(0,0)
        self.window.config(bg="white")
        
        titulo = Label(ventana_articulo,text="Articulos",fg="black",font=("Comic Sans",17, "bold"),pady=10)
        titulo.pack()

        # Carga de imagen
        imagen_articulo = Image.open("C:\\Users\\josuu\\OneDrive\\Documentos\\POO\\merks_and_spen_2\\imagenes\\online-shopping-mexico-800-3423d44e0.png")


        nueva_img = imagen_articulo.resize((60,60))
        render = ImageTk.PhotoImage(nueva_img)
        label_image = Label(ventana_articulo, image=render)
        label_image.image = render
        label_image.pack(pady=10)

        # Formulario
        marco = LabelFrame(ventana_articulo,text="Informacion del articulo", font=("Comic Sans", 10, "bold"),pady=5)
        marco.config(bd=2)
        marco.pack()

        Label(marco, text="Codigo del articulo:", font=("Comic Sans", 10, "bold")).grid(row=0, column=0, sticky='e', padx=5, pady=8)
        self.codigo = Entry(marco, width=25)
        self.codigo.focus()
        self.codigo.grid(row=0, column=1, padx=5, pady=8)

        Label(marco, text="Nombre del articulo:", font=("Comic Sans", 10, "bold")).grid(row=1, column=0, sticky='e', padx=5, pady=8)
        self.nombre = Entry(marco, width=25)
        self.nombre.grid(row=1, column=1, padx=5, pady=8)

        Label(marco, text="Departamento:", font=("Comic Sans", 10, "bold")).grid(row=2, column=0, sticky='e', padx=5, pady=8)
        self.combo_categoria = ttk.Combobox(marco, values=["Administrador", "Sistemas", "Tics"], width=22)
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=8)

        Label(marco, text="Cantidad:", font=("Comic Sans", 10, "bold")).grid(row=0, column=2, sticky='e', padx=5, pady=8)
        self.cantidad = Entry(marco, width=25)
        self.cantidad.grid(row=0, column=3, padx=5, pady=8)

        Label(marco, text="Precio:", font=("Comic Sans", 10, "bold")).grid(row=1, column=2, sticky='e', padx=5, pady=8)
        self.precio = Entry(marco, width=25)
        self.precio.grid(row=1, column=3, padx=5, pady=8)

        Label(marco, text="Descripcion:", font=("Comic Sans", 10, "bold")).grid(row=2, column=2, sticky='e', padx=5, pady=8)
        self.descripcion = Text(marco, width=25, height=5)
        self.descripcion.grid(row=2, column=3, padx=10, pady=8)

        # Botones
        frame_botones = Frame(ventana_articulo)
        frame_botones.pack()

        Button(frame_botones, text="Agregar", height=2, width=10, bg="green", fg="white", font=("Comic Sans", 10, "bold"), command=self.agregar_articulo).grid(row=0, column=0, padx=5, pady=8)
        Button(frame_botones, text="Editar", height=2, width=10, bg="gray", fg="white", font=("Comic Sans", 10, "bold"), command=self.editar_articulo).grid(row=0, column=1, padx=5, pady=8)
        Button(frame_botones, text="Eliminar", height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"), command=self.eliminar_articulo).grid(row=0, column=2, padx=5, pady=8)
        Button(frame_botones, text="Generar Ticket", height=2, width=15, bg="blue", fg="white", font=("Comic Sans", 10, "bold"), command=self.generar_ticket).grid(row=0, column=3, padx=5, pady=8)

        # Tabla para ver los artículos
        self.tree = ttk.Treeview(ventana_articulo, height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5"))
        self.tree.heading("#0", text="Codigo", anchor=CENTER)
        self.tree.column("#0", width=90, minwidth=75, stretch=NO)

        self.tree.heading("columna1", text="Nombre", anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=NO)

        self.tree.heading("columna2", text="Categoria", anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=NO)

        self.tree.heading("columna3", text="Cantidad", anchor=CENTER)
        self.tree.column("columna3", width=150, minwidth=60, stretch=NO)

        self.tree.heading("columna4", text="Precio", anchor=CENTER)
        self.tree.column("columna4", width=150, minwidth=60, stretch=NO)

        self.tree.heading("columna5", text="Descripcion", anchor=CENTER)

        self.tree.pack()

        self.Obtener_articulos()


# CRUD

    def Obtener_articulos(self):
        self.tree.delete(*self.tree.get_children()) 
        conexion = self.conexion.conexion()
        if conexion:
            query = 'SELECT * FROM articulos ORDER BY Nombre DESC'
            cursor = self.conexion.ejecutar_consulta(conexion, query)
            if cursor:
                for row in cursor:
                    self.tree.insert("", 0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))
            conexion.close()
            
    def agregar_articulo(self):
        if self.conexion.conexion():
            if self.Validar_formulario_completo():
                query = 'INSERT INTO articulos (codigo, nombre, categoria, cantidad, precio, descripcion) VALUES (?, ?, ?, ?, ?, ?)'
                parameters = (self.codigo.get(), self.nombre.get(), self.combo_categoria.get(), self.cantidad.get(), self.precio.get(), self.descripcion.get("1.0", "end-1c"))
                self.conexion.ejecutar_consulta(self.conexion.conexion(), query, parameters) 
                messagebox.showinfo("REGISTRO EXITOSO", f'Producto registrado: {self.nombre.get()}')
                print('REGISTRADO')
                self.Limpiar_formulario()
                self.Obtener_articulos()
           

    def editar_articulo(self):
        try:
            item_text = self.tree.item(self.tree.selection())['text']
        # Convertir item_text a cadena de texto si es un entero
            codigo = str(item_text)
        except IndexError as e:
            messagebox.showerror("ERROR","Por favor selecciona un elemento") 
            return
        conexion = self.conexion.conexion()
        if conexion:
            codigo = self.tree.item(self.tree.selection())['text']
            nombre = self.tree.item(self.tree.selection())['values'][0]
            categoria = self.tree.item(self.tree.selection())['values'][1]
            cantidad = self.tree.item(self.tree.selection())['values'][2]
            precio = self.tree.item(self.tree.selection())['values'][3]
            descripcion = self.tree.item(self.tree.selection())['values'][4]
    
            if self.ventana_editar is None: 
                self.ventana_editar = Toplevel()
                self.ventana_editar.title('EDITAR ARTICULO')
                self.ventana_editar.resizable(0,0)

    
        label_codigo = Label(self.ventana_editar, text="Codigo:", font=("Comic Sans", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        nuevo_codigo = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo), width=25)
        nuevo_codigo.grid(row=0, column=1, padx=5, pady=8)
    
        label_nombre = Label(self.ventana_editar, text="Nombre:", font=("Comic Sans", 10, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        nuevo_nombre = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=nombre), width=25)
        nuevo_nombre.grid(row=1, column=1, padx=5, pady=8)

        label_categoria = Label(self.ventana_editar, text="Categoria:", font=("Comic Sans", 10, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        nueva_categoria = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=categoria), width=25)
        nueva_categoria.grid(row=2, column=1, padx=5, pady=0)
    

        label_cantidad = Label(self.ventana_editar, text="Cantidad:", font=("Comic Sans", 10, "bold")).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        nueva_cantidad = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=cantidad), width=25)
        nueva_cantidad.grid(row=3, column=1, padx=5, pady=8)
    

        label_precio = Label(self.ventana_editar, text="Precio:", font=("Comic Sans", 10, "bold")).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        nuevo_precio = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=precio), width=25)
        nuevo_precio.grid(row=4, column=1, padx=5, pady=8)

        label_descripcion = Label(self.ventana_editar, text="Descripcion:", font=("Comic Sans", 10, "bold")).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        nueva_descripcion = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=descripcion), width=25)
        nueva_descripcion.grid(row=5, column=1, padx=5, pady=8)

        boton_actualizar = Button(self.ventana_editar, text="Guardar Cambios", command=lambda: self.Actualizar(nuevo_codigo.get(), nuevo_nombre.get(), nueva_categoria.get(), nueva_cantidad.get(), nuevo_precio.get(), nueva_descripcion.get(), codigo, nombre), height=2, width=20, bg="black", fg="white", font=("Comic Sans", 10, "bold"))
        boton_actualizar.grid(row=6, column=1, columnspan=2, padx=10, pady=15)
        self.ventana_editar.mainloop()

        
    def Actualizar(self,nuevo_codigo,nuevo_nombre,nuevo_combo_categoria,nueva_cantidad,nuevo_precio,nueva_descripcion,codigo,nombre):
        query='UPDATE articulos SET Codigo = ?, Nombre = ?, Categoria = ?, Cantidad =?, Precio=?, Descripcion =? WHERE Codigo = ? AND Nombre =?'
        parameters=(nuevo_codigo,nuevo_nombre,nuevo_combo_categoria,nueva_cantidad,nuevo_precio,nueva_descripcion,codigo,nombre)
        self.conexion.ejecutar_consulta(self.conexion.conexion(), query, parameters)
        messagebox.showinfo('EXITO',f'Articulo actualizado:{nuevo_nombre}')
        self.ventana_editar.destroy()
        self.Obtener_articulos() 

    def eliminar_articulo(self):
        try:
            seleccion = self.tree.selection()
            if not seleccion:
                raise IndexError("No se ha seleccionado ningún elemento")
            dato = self.tree.item(seleccion[0])['text']
            nombre = self.tree.item(seleccion[0])['values'][0]
            respuesta = messagebox.askquestion("ADVERTENCIA", f"¿Seguro que desea eliminar el producto: {nombre}?")
            if respuesta == 'yes':
                conexion = self.conexion.conexion()
                if conexion:
                    query = "DELETE FROM articulos WHERE Codigo = ?"
                    self.conexion.ejecutar_consulta(conexion, query, (dato,))
                    conexion.close()
                    self.Obtener_articulos()
                    messagebox.showinfo('EXITO', f'Producto eliminado: {nombre}')
            else:
                messagebox.showerror('ERROR', f'Error al eliminar el producto: {nombre}')
        except IndexError as e:
            messagebox.showerror("ERROR", "Por favor selecciona un elemento")

#Otras funciones 
 
          
    def Validar_formulario_completo(self):
        if (len(self.codigo.get()) !=0 and len(self.nombre.get()) !=0 and len(self.combo_categoria.get()) !=0 and len(self.cantidad.get()) !=0 and len(self.precio.get()) !=0 and len(self.descripcion.get("1.0", "end-1c")) != 0):
            return True
        else:
             messagebox.showerror("ERROR", "Complete todos los campos del formulario") 
    
    def Limpiar_formulario(self):
        self.codigo.delete(0, END)
        self.nombre.delete(0, END)
        self.cantidad.delete(0, END)
        self.precio.delete(0, END)
        self.descripcion.delete('1.0', END)  

    def generar_ticket(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor selecciona al menos un artículo para generar el ticket.")
            return

        # Crear el documento PDF
        c = canvas.Canvas("ticket.pdf", pagesize=letter)
        
        # Escribir el contenido del ticket
        c.drawString(100, 750, "Ticket de Compra")
        c.drawString(100, 730, "--------------------------")
        y = 700
        for i, item_id in enumerate(seleccion):
            articulo = self.tree.item(item_id)['values']
            c.drawString(100, y, f"Artículo {i + 1}: {articulo[0]} - ${articulo[3]} - Cantidad: {articulo[2]} - Categoria: {articulo[1]} ")
            y -= 20
        
       
        c.save()
        messagebox.showinfo("Ticket generado", "Se ha generado el ticket correctamente como 'ticket.pdf'")
        self.abrir_pdf()

    def abrir_pdf(self):
        filepath = os.path.abspath("ticket.pdf")
        os.system(f'start {filepath}')

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for i, articulo in enumerate(self.articulos):
            self.tree.insert("", END, text=str(i), values=(articulo["nombre"], articulo["categoria"], articulo["cantidad"], articulo["precio"], articulo["descripcion"]))

    def obtener_articulos_tabla(self):
        articulos = []
        for item in self.application.tree.get_children():
            codigo = self.application.tree.item(item, "text")
            nombre = self.application.tree.item(item, "values")[0]
            categoria = self.application.tree.item(item, "values")[1]
            cantidad = self.application.tree.item(item, "values")[2]
            precio = self.application.tree.item(item, "values")[3]
            descripcion = self.application.tree.item(item, "values")[4]
            articulos.append((codigo, nombre, categoria, cantidad, precio, descripcion))
        return articulos
    
if __name__ == '__main__':
    ventana_articulo=Tk()
    application=Articulo(ventana_articulo)
    ventana_articulo.mainloop()