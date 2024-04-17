from tkinter import *
from noteBookAdmin import noteBookAdmin
from crud_articulosA import Articulo
from graficas_A import Graficas

class MenuAdministrador:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("900x700")
        self.ventana.title("Menu Administrador")
        
        # Frame principal que contenga todo
        self.frame_principal = Frame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True)

        # Frame superior con el título
        self.frame_superior = Frame(self.frame_principal, bg="#065535", height=50)
        self.frame_superior.pack(fill="both", expand=False)

        # Título dentro del Frame superior
        self.titulo = Label(self.frame_superior, text="MERKS AND SPEN", fg="white", bg="#065535", font=("Arial", 30))
        self.titulo.pack(padx=10, pady=10)

        # Frame inferior
        self.frame_inferior = Frame(self.frame_principal, bg="white")
        self.frame_inferior.pack(fill="both", expand=True)

        self.imagen_usuario = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\usuario.png")
        self.imagen_usuario = self.imagen_usuario.subsample(3)
        self.imagen_usuario_label = Label(self.frame_inferior, bg="white", image=self.imagen_usuario)
        self.imagen_usuario_label.grid(row=0, column=0)

        self.boton_admin = Button(self.frame_inferior, text="Usuarios", width=20, height=3, bg="#065535", fg="white", font=("Arial", 15), command=self.abrir_administrador)
        self.boton_admin.grid(row=1, column=0)

        self.espacio = Label(self.frame_inferior, bg="white", width=40)
        self.espacio.grid(row=0, column=1)

        self.imagen_articulo = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\lapiz2.png")
        self.imagen_articulo = self.imagen_articulo.subsample(3)
        self.imagen_articulo_label = Label(self.frame_inferior, bg="white", image=self.imagen_articulo)
        self.imagen_articulo_label.grid(row=0, column=2)

        self.botonarticulo = Button(self.frame_inferior, text="Articulos", width=13, height=3, bg="#065535", fg="white", font=("Arial", 15),command=self.abrir_articulos)
        self.botonarticulo.grid(row=1, column=2)

        self.espacio2 = Label(self.frame_inferior, bg="white", width=45, height=16)
        self.espacio2.grid(row=2, column=0)

        self.imagen_graficas = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\grafica.png")
        self.imagen_graficas = self.imagen_graficas.subsample(3)
        self.imagen_graficas_label = Label(self.frame_inferior, bg="white", image=self.imagen_graficas)
        self.imagen_graficas_label.grid(row=2, column=1)

        self.botongraficas = Button(self.frame_inferior, text="Graficas", width=13, height=3, bg="#065535", fg="white", font=("Arial", 15),command=self.abrir_graficas)
        self.botongraficas.grid(row=3, column=1)

        self.notebook_admin = None
        self.crud_articulos = None

    def abrir_administrador(self):
        self.noteBookAdminWindow = Toplevel(self.ventana)  # Crea una nueva ventana para la interfaz de búsqueda de artículos
        self.noteBookAdminWindow.title("Usuarios")
        self.notebook_admin = noteBookAdmin(self.noteBookAdminWindow)  # Pasa la nueva ventana como argumento
        self.notebook_admin.mostrar_interfaz()

    def abrir_articulos(self):
        self.articulos = Toplevel(self.ventana)  # Crea una nueva ventana para la interfaz de búsqueda de artículos
        self.articulos.title("Articulos")
        self.crud_articulos = Articulo(self.articulos)  # Pasa la nueva ventana como argumento
        self.crud_articulos.mostrar_interfaz()  # Muestra la interfaz de creación de artículos
        
    def abrir_graficas(self):
        self.graficas = Toplevel(self.ventana)
        self.graficas.title("Graficas")
        self.graficas= Graficas(self.graficas)
        self.graficas.mostrar_interfaz()
        

# Para usar la clase MenuAdministrador:
menu_administrador = MenuAdministrador()
menu_administrador.ventana.mainloop()
