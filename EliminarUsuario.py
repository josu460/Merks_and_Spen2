import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Controlador import *

class EliminarUsuario:
    def __init__(self, frame):
        self.frame = frame

        self.objControlador = Controlador()

        self.departamento = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Eliminación de usuarios", fg="blue", font=("modern", 18)).pack()
        tk.Label(self.frame, text="Se buscará el departamento y se eliminará", fg="black", font=("arial", 10)).pack()

        tk.Label(self.frame, text="Nombre del departamento:").pack()
        tk.Entry(self.frame, textvariable=self.departamento).pack()

        tk.Button(self.frame, text="Borrar usuario", command=self.borrarUsuario, bg="red", fg="black").pack()

    def borrarUsuario(self):
        self.objControlador.buscar(self.departamento.get())
        if self.objControlador.buscar(self.departamento.get()):
            if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar el departamento?"):
                self.objControlador.eliminar(self.departamento.get())
                self.departamento.set("")
            else:
                messagebox.showinfo("Información", "La eliminación ha sido cancelada")
        elif self.departamento.get() == "":
            messagebox.showinfo("Error", "El campo está vacío")
        else:
            messagebox.showinfo("Error", "El departamento no existe")

# Para probar el frame por separado
if __name__ == "__main__":
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    app = EliminarUsuario(frame)
    root.mainloop()
   