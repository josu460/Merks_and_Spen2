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
        self.ventana.geometry("600x500")
        
        # Creación de la barra de menú
        self.panel = ttk.Notebook(self.ventana)
        self.panel.pack(fill='both', expand='yes')
        
        # Creación de las pestañas del panel de administración con frames
        
        #frame para el registro de usuarios
        registroFrame = ttk.Frame(self.panel)  # Frame para el registro de usuarios
        self.panel.add(registroFrame, text="Registro")  # Agregar la pestaña de registro al panel de administración
        Registro(registroFrame)  # Crear el objeto de la clase Registro
        
        #frame para la modificación de usuarios
        modificacionFrame = ttk.Frame(self.panel)
        self.panel.add(modificacionFrame, text="Modificación")
        ModificacionUsuario(modificacionFrame)
        
        #frame para la eliminación de usuarios
        eliminacionFrame = ttk.Frame(self.panel)
        self.panel.add(eliminacionFrame, text="Eliminación")
        EliminarUsuario(eliminacionFrame)
        
        #frame para la consulta de usuarios
        consultaFrame = ttk.Frame(self.panel)
        self.panel.add(consultaFrame, text="Consulta")
        self.consultaUsuarios = ConsultaUsuarios(consultaFrame)
        
        #vincular evento al cambio de pestaña
        self.panel.bind("<<NotebookTabChanged>>", self.actualizarConsulta)
        
    def actualizarConsulta(self, event):
        if self.panel.select() == self.panel.tabs()[3]:
            self.consultaUsuarios.actualizar()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = noteBookAdmin(root)
    root.mainloop()
