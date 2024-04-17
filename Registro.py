import tkinter as tk
from tkinter import ttk
from Controlador import *
from tkinter import PhotoImage

class Registro:
    def __init__(self, frame):
        self.frame = frame
        
        self.objControlador = Controlador()

        self.departamento = tk.StringVar()
        self.password = tk.StringVar()
        self.tipo_usuario = tk.StringVar()
        self.image = PhotoImage(file="imagenes/agregar-usuario.png")
        self.image = self.image.subsample(4, 4)
        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(self.frame, text="Registro de usuarios", fg="blue", font=("modern", 18)).pack()

        tk.Label(self.frame, image=self.image).pack()
        
        tk.Label(self.frame, text="Nombre del departamento:").pack()
        tk.Entry(self.frame, textvariable=self.departamento).pack()

        tk.Label(self.frame, text="Contraseña:").pack()
        tk.Entry(self.frame, textvariable=self.password, show="*").pack()
        
        tk.Label(self.frame, text="Tipo de usuario:").pack()
        tk.OptionMenu(self.frame, self.tipo_usuario, "Administrador", "Usuario").pack()

        tk.Button(self.frame, text="Registrar", command=self.ejecutarInsert, bg="green", fg="white").pack()

    def ejecutarInsert(self):
        if not self.departamento.get() or not self.password.get() or not self.tipo_usuario.get():
            tk.messagebox.showinfo("Error", "Los campos son obligatorios")
            return
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas registrar el departamento?\nNombre del departamento: " + self.departamento.get() + "\nContraseña: " + self.password.get() + "\nTipo de usuario: " + self.tipo_usuario.get() + ""):
            self.objControlador.registrar(self.departamento.get(), self.password.get(), self.tipo_usuario.get())
            self.departamento.set("")
            self.password.set("")
        else:
            messagebox.showinfo("Información", "El registro ha sido cancelado")

# Para probar el frame por separado
if __name__ == "__main__":
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    app = Registro(frame)
    root.mainloop()
