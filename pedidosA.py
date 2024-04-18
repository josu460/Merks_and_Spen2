from tkinter import Tk, Label, Frame, Button, ttk, LabelFrame, messagebox
from Controlador import Controlador

class ConsultarPedidos:
    db_name = 'BDMerksandSpendall.db'
    
    def __init__(self, ventana):
        self.conexion = Controlador()
        self.ventana = ventana
        self.ventana.title('Consulta de Pedidos')
        self.ventana.geometry('800x670')

        titulo = Label(ventana, text="CONSULTA DE PEDIDOS", fg="black", font=("Comic Sans", 17, "bold"), pady=10)
        titulo.pack()

        # mostrar los resultados de la consulta
        self.tree = ttk.Treeview(ventana, height=13, columns=("columna1", "columna2"))
        self.tree.heading("#0", text="ID de Pedido", anchor="center")
        self.tree.column("#0", width=150, minwidth=75, stretch="no")

        self.tree.heading("columna1", text="Nombre articulo", anchor="center")
        self.tree.column("columna1", width=150, minwidth=75, stretch="no")

        self.tree.heading("columna2", text="Cantidad", anchor="center")
        self.tree.column("columna2", width=150, minwidth=75, stretch="no")

        self.tree.pack()

        frame_boton = Frame(ventana)
        frame_boton.pack(padx=10, pady=10)

        self.boton_consultar = Button(frame_boton, text="CONSULTAR PEDIDOS", command=self.consultar_pedidos, height=2, width=20, bg="green", fg="white", font=("Comic Sans", 10, "bold"))
        self.boton_consultar.pack(pady=8)

    def consultar_pedidos(self):
        # Limpiar árbol antes de realizar la consulta
        self.limpiar_arbol()

        # Consultar todos los pedidos
        query = "SELECT * FROM pedidos"
        db_rows = self.conexion.ejecutar_consulta(self.conexion.conexion(), query)

        # Mostrar los pedidos en el árbol
        for row in db_rows:
            self.tree.insert("", 0, text=row[0], values=(row[1], row[2]))

        # Mostrar mensaje si no hay pedidos
        if not self.tree.get_children():
            messagebox.showinfo("Consulta de Pedidos", "No hay pedidos registrados.")

    def limpiar_arbol(self):
        # Limpiar todos los elementos del árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == '__main__':
    ventana = Tk()
    aplicacion = ConsultarPedidos(ventana)
    ventana.mainloop()
