import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Controlador import Controlador
import sys
from subprocess import call

class LoginTkinter:
    def __init__(self, controlador, root=None):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x500")
        self.entry_nombre = tk.StringVar()
        self.entry_contraseña = tk.StringVar()
        self.controlador = controlador
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Login Merks and Spend", fg="blue", font=("arial", 20)).pack()
        
        # Cargar la imagen
        imagen = PhotoImage(file="C:\\Users\\josuu\\OneDrive\\Documentos\\POO\\merks_and_spen_2\\imagenes\\perfil-del-usuario.png")
        imagen = imagen.subsample(3)
        label_imagen = tk.Label(self.root, image=imagen)
        label_imagen.image = imagen  # Guardar una referencia a la imagen para evitar que se elimine por el recolector de basura
        label_imagen.pack(pady=10)

        tk.Label(self.root, text="Nombre del departamento:").pack()
        tk.Entry(self.root, textvariable=self.entry_nombre).pack()
        
        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=self.entry_contraseña, show="*").pack()
       
        self.button_login = tk.Button(self.root, text="Login", command=self.login, bg="blue", fg="white")
        self.button_login.pack()
        
    def login(self):
        contraPlana = self.entry_contraseña.get()
        departamento = self.entry_nombre.get()

        if contraPlana == "" or departamento == "":
            messagebox.showerror("Error", "No puedes dejar campos vacíos")
            return

        password_encriptada = self.controlador.obtenerContraseña(departamento)

        if password_encriptada:
            if self.controlador.desencriptar(contraPlana, password_encriptada):
                messagebox.showinfo("Login", "Login exitoso del departamento: " + departamento)

                # Obtener el tipo de usuario
                tipo_usuario = self.controlador.tipo_usuario(departamento)
                print("Tipo de usuario:", tipo_usuario)  # Depuración
                
                if tipo_usuario == "administrador":
                    self.llamar_menu_admin()
                elif tipo_usuario == "usuario":
                    self.llamar_menu_usuario()
                    
                self.root.withdraw() # Mantiene la ventana abierta pero no visible
            else:
                messagebox.showinfo("Error", "Contraseña incorrecta")
                self.entry_contraseña.set("")
        else:
            messagebox.showinfo("Error", "El departamento no existe")
            self.entry_nombre.set("")
            self.entry_contraseña.set("")
        
    def llamar_menu_admin(self):
        self.root.destroy()  # Destruye la ventana de login
        call([sys.executable, r'C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\menu_A.py'])

    def llamar_menu_usuario(self):
        self.root.destroy()  # Destruye la ventana de login
        call([sys.executable, r'C:\Users\josuu\OneDrive\Documentos\POO\merks_and_spen_2\menu_U.py'])

if __name__ == "__main__":
    root = tk.Tk()
    controlador = Controlador()
    app = LoginTkinter(controlador, root)
    root.mainloop()
