from tkinter import *
from articulos_U import BuscadorArticulos
from pedidos import Pedidos

class MenuUsuarios:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("900x700")
        self.ventana.title("Menu Usuarios")

        # Frame principal que contenga todo
        self.frame_principal = Frame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True)

        # Frame superior con el título
        self.frame_superior = Frame(self.frame_principal, bg="#f77900", height=50)
        self.frame_superior.pack(fill="both", expand=False)

        # Título dentro del Frame superior
        self.titulo = Label(self.frame_superior, text="MERKS AND SPEN", fg="white", bg="#f77900", font=("Arial", 30))
        self.titulo.pack(padx=10, pady=10)

        # Frame inferior
        self.frame_inferior = Frame(self.frame_principal, bg="white")
        self.frame_inferior.pack(fill="both", expand=True)

        self.imagen_usuario = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\usuario.png")
        self.imagen_usuario = self.imagen_usuario.subsample(3)
        self.imagen_usuario_label = Label(self.frame_inferior, bg="white", image=self.imagen_usuario)
        self.imagen_usuario_label.grid(row=0, column=0)

        self.botonusuario = Button(self.frame_inferior, text="Usuarios", width=13, height=3, bg="#f77900", fg="white", font=("Arial", 15))
        self.botonusuario.grid(row=1, column=0)

        self.espacio = Label(self.frame_inferior, bg="white", width=40)
        self.espacio.grid(row=0, column=1)

        self.imagen_articulo = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\lapiz2.png")
        self.imagen_articulo = self.imagen_articulo.subsample(3)
        self.imagen_articulo_label = Label(self.frame_inferior, bg="white", image=self.imagen_articulo)
        self.imagen_articulo_label.grid(row=0, column=2)

        self.botonarticulo = Button(self.frame_inferior, text="Articulos", width=13, height=3, bg="#f77900", fg="white", font=("Arial", 15), command=self.abrir_articulosU)
        self.botonarticulo.grid(row=1, column=2)

        self.espacio2 = Label(self.frame_inferior, bg="white", width=45, height=16)
        self.espacio2.grid(row=2, column=0)

        self.imagen_solicitar = PhotoImage(file=r"C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\imagenes\pedir.png")
        self.imagen_solicitar = self.imagen_solicitar.subsample(4)
        self.imagen_solicitar_label = Label(self.frame_inferior, bg="white", image=self.imagen_solicitar)
        self.imagen_solicitar_label.grid(row=2, column=1)

        self.botonsolicitar = Button(self.frame_inferior, text="Solicitar", width=13, height=3, bg="#f77900", fg="white", font=("Arial", 15),command=self.abrir_pedidos)
        self.botonsolicitar.grid(row=3, column=1)

    def iniciar(self):
        self.ventana.mainloop()
        
    def abrir_articulosU(self):
        self.articulosU = Toplevel(self.ventana)  # Crea una nueva ventana para la interfaz de búsqueda de artículos
        self.articulosU.title("Buscar Artículos")
        buscador_articulos = BuscadorArticulos(self.articulosU)  # Pasa la nueva ventana como argumento
        buscador_articulos.mostrar_interfaz()  # Muestra la interfaz de búsqueda de artículos

    def abrir_pedidos(self):
        self.pedidos = Toplevel(self.ventana)
        self.pedidos.title("Pedidos")
        pedidos = Pedidos(self.pedidos)
        pedidos.mostrar_interfaz()

# Para usar la clase MenuUsuarios:
menu_usuarios = MenuUsuarios()
menu_usuarios.iniciar()
