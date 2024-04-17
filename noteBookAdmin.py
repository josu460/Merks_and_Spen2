import tkinter as tk
from tkinter import ttk
from Controlador import *
from Registro import *
from ModificacionUsuario import *
from ConsultaUsuarios import *
from EliminarUsuario import *

class noteBookAdmin:
    def __init__(self, ventana=None):
        self.ventana = ventana
        self.ventana.title("Panel de Administración MerksandSpend")
        self.ventana.geometry("600x300")
        
        # Creación de la barra de menú
        self.panel = ttk.Notebook(self.ventana)
        self.panel.pack(fill='both', expand='yes')
        
        # Creación de las pestañas del panel de administración con frames
        
        registroFrame = ttk.Frame(self.panel)  # Frame para el registro de usuarios
        self.panel.add(registroFrame, text="Registro")  # Agregar la pestaña de registro al panel de administración
        Registro(registroFrame)  # Crear el objeto de la clase Registro
        
        modificacionFrame = ttk.Frame(self.panel)
        self.panel.add(modificacionFrame, text="Modificación")
        ModificacionUsuario(modificacionFrame)
        
        consultaFrame = ttk.Frame(self.panel)
        self.panel.add(consultaFrame, text="Consulta")
        ConsultaUsuarios(consultaFrame)
        
        eliminacionFrame = ttk.Frame(self.panel)
        self.panel.add(eliminacionFrame, text="Eliminación")
        EliminarUsuario(eliminacionFrame)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = noteBookAdmin(root)
    root.mainloop()
