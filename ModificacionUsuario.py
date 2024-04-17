from tkinter import *
from tkinter import simpledialog, messagebox
from Controlador import *
from tkinter import PhotoImage

class ModificacionUsuario:
    def __init__(self, frame):
        self.frame = frame # frame para la modificación de usuarios
        self.objControlador = Controlador() # objeto de la clase Controlador
        self.departamento = StringVar() # Variable para el nombre del departamento
        self.modificarDepartamento = None # Variable para el Checkbutton
        self.modificarContrasena = None     # Variable para el Checkbutton
        self.modificarButton = None        # Variable para el botón de modificar
        self.label_modificar = None       # Variable para el label de modificar
        self.image = PhotoImage(file="imagenes/editar.png") # Imagen para la modificación de usuarios
        self.image = self.image.subsample(4, 4) # Tamaño de la imagen
        self.create_widgets() # Llamada al método create_widgets

    def create_widgets(self):
        Label(self.frame, text="Modificación de usuarios", fg="blue", font=("modern", 18)).pack() 
        Label(self.frame, image=self.image).pack()
        Label(self.frame, text="Se buscará el departamento y se modificará la contraseña y/o el nombre del departamento", fg="black", font=("arial", 8)).pack()

        Label(self.frame, text="Nombre del departamento:").pack() 
        Entry(self.frame, textvariable=self.departamento).pack()

        Button(self.frame, text="Buscar Usuario", command=self.buscar, bg="green", fg="white").pack()

    def buscar(self):
        departamento = self.departamento.get()
        
        if not departamento:
            messagebox.showinfo("Error", "El campo está vacío")
            return

        if self.objControlador.buscar(departamento):
            self.update_modificaciones()
        else:
            messagebox.showinfo("Error", "El departamento no existe")
            self.departamento.set("") # Limpia el campo de texto
            self.hide_modificaciones() # Llamada al método hide_modificaciones

    def hide_modificaciones(self): # Método para ocultar los widgets de modificación
        if self.label_modificar: # Si el label de modificar existe
            self.label_modificar.pack_forget() # Oculta el label de modificar
        if self.modificarDepartamento:
            self.check_modificarDepartamento.pack_forget()
        if self.modificarContrasena:
            self.check_modificarContrasena.pack_forget()
        if self.modificarButton:
            self.modificarButton.pack_forget()

    def update_modificaciones(self):
        self.hide_modificaciones()

        self.label_modificar = Label(self.frame, text="Selecciona lo que desees modificar: ", fg="black", font=("arial", 10))
        self.label_modificar.pack()

        self.modificarDepartamento = IntVar(value=0)
        self.check_modificarDepartamento = Checkbutton(self.frame, text="Modificar nombre del departamento", variable=self.modificarDepartamento)
        self.check_modificarDepartamento.pack()

        self.modificarContrasena = IntVar(value=0)
        self.check_modificarContrasena = Checkbutton(self.frame, text="Modificar contraseña", variable=self.modificarContrasena)
        self.check_modificarContrasena.pack()

        self.modificarButton = Button(self.frame, text="Modificar", command=self.realizarModificacion, bg="green", fg="white")
        self.modificarButton.pack()

    def realizarModificacion(self):
        departamento = self.departamento.get()
        antiguoDepartamento = departamento

        if not departamento:
            messagebox.showinfo("Error", "El campo está vacío")
            return

        if self.modificarDepartamento.get() == 0 and self.modificarContrasena.get() == 0:
            messagebox.showinfo("Error", "Debe seleccionar al menos una opción")
            return

        if self.modificarDepartamento.get() == 1 and self.modificarContrasena.get() == 1:
            nuevoDepartamento = simpledialog.askstring("Modificar departamento", "Ingrese el nuevo nombre del departamento:")
            if not nuevoDepartamento:
                messagebox.showinfo("Error", "Debe ingresar un nombre")
                return
            nuevaContrasena = simpledialog.askstring("Modificar contraseña", "Ingrese la nueva contraseña:")
            if not nuevaContrasena:
                messagebox.showinfo("Error", "Debe ingresar una contraseña")
                return
            try:
                self.objControlador.modificar(departamento, nuevoDepartamento, nuevaContrasena)
                messagebox.showinfo("Modificación", "El departamento " + antiguoDepartamento + " ha sido modificado a " + nuevoDepartamento + " y la contraseña ha sido modificada")
                self.hide_modificaciones()
                self.departamento.set("")
            except Exception as e:
                messagebox.showinfo("Error", "Error al modificar: " + str(e))

        elif self.modificarDepartamento.get() == 1:
            nuevoDepartamento = simpledialog.askstring("Modificar departamento", "Ingrese el nuevo nombre del departamento:")
            if not nuevoDepartamento:
                messagebox.showinfo("Error", "Debe ingresar un nombre")
                return
            try:
                self.objControlador.modificar(departamento, nuevoDepartamento)
                messagebox.showinfo("Modificación", "El departamento " + antiguoDepartamento + " ha sido modificado a " + nuevoDepartamento)
                self.hide_modificaciones()
                self.departamento.set("")
            except Exception as e:
                messagebox.showinfo("Error", "Error al modificar: " + str(e))

        elif self.modificarContrasena.get() == 1:
            nuevaContrasena = simpledialog.askstring("Modificar contraseña", "Ingrese la nueva contraseña:")
            if not nuevaContrasena:
                messagebox.showinfo("Error", "Debe ingresar una contraseña")
                return
            try:
                self.objControlador.modificar(departamento, None, nuevaContrasena)
                messagebox.showinfo("Modificación", "La contraseña del departamento " + antiguoDepartamento + " ha sido modificada")
                self.hide_modificaciones()
                self.departamento.set("")
            except Exception as e:
                messagebox.showinfo("Error", "Error al modificar: " + str(e))

if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack(fill="both", expand=True)
    app = ModificacionUsuario(frame)
    root.mainloop()
