from tkinter import *
from tkinter import messagebox
from Controlador import *
from tkinter import ttk

class ConsultaUsuarios:
    def __init__(self, frame):
        self.frame = frame
        self.objControlador = Controlador()
        self.create_widgets()
        
    def create_widgets(self):
        tree = ttk.Treeview(self.frame, columns=("Departamento"), show='headings') 
        tree.heading("Departamento", text="Departamento")
        tree.pack()
        
        # Llenar el treeview
        departamentos = self.objControlador.consultarUsuarios()
        if departamentos:
            for departamento in departamentos:
                tree.insert("", "end", values=(departamento,))
        else:
            messagebox.showinfo("Info", "No hay departamentos para mostrar")


# Para probar el frame por separado
if __name__ == "__main__":
    root = Tk()
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    app = ConsultaUsuarios(frame)
    root.mainloop()
