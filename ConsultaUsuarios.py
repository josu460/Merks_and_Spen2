from tkinter import *
from tkinter import messagebox, ttk
from Controlador import *

class ConsultaUsuarios:
    def __init__(self, frame):
        self.frame = frame
        self.objControlador = Controlador()
        self.image = PhotoImage(file="imagenes/ConsultaUsuarios.png")
        self.image = self.image.subsample(4,4)
        self.create_widgets()
        
    def create_widgets(self):
        Label(self.frame, text="Consulta de usuarios", fg="blue", font=("modern", 18)).pack()
        Label(self.frame, image=self.image).pack()
        Label(self.frame, text="Departamentos activos:", fg="black", font=("arial", 10)).pack()
        self.tree = ttk.Treeview(self.frame, columns=("Departamento",), show='headings') 
        self.tree.heading("Departamento", text="Departamento")
        self.tree.pack()
    
        # Llenar el treeview
        departamentos = self.objControlador.consultarUsuarios()
        if departamentos is not None:
            for departamento in departamentos:
                self.tree.insert("", "end", values=(departamento,))
        else:
            messagebox.showinfo("Información", "No hay departamentos activos.")

    def actualizar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        departamentos = self.objControlador.consultarUsuarios()
        if departamentos is not None:
            for departamento in departamentos:
                self.tree.insert("", "end", values=(departamento,))
        else:
            messagebox.showinfo("Información", "No hay departamentos activos.")


# Para probar el frame por separado
if __name__ == "__main__":
    root = Tk()
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    app = ConsultaUsuarios(frame)
    root.mainloop()
