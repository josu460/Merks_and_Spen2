from tkinter import messagebox
import sqlite3
import bcrypt

class Controlador:
    
    def normalizar(self, departamento): #metodo para normalizar el departamento a minúsculas
        return departamento.lower() if departamento else departamento
    
    def conexion(self):
        try:
            conex = sqlite3.connect("DBMerksandSpend2.db")
            
            print("Conectado")
            return conex
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            
    def encriptar(self, password):
        passplana = password
        passplana = passplana.encode()
        sal = bcrypt.gensalt()
        passhash = bcrypt.hashpw(passplana, sal)
        return passhash
    
    def obtenerContraseña(self, departamento):
        try:
            conexion = self.conexion() 
            cursor = conexion.cursor()
            sqlInsert = "SELECT password FROM tbUsuarios WHERE departamento = ?" #obtener la contraseña encriptada de la base de datos
            cursor.execute(sqlInsert, (departamento,))
            password = cursor.fetchone() #obtener la contraseña encriptada de la base de datos, se obtiene como una tupla y su primer elemento es la contraseña
            
            if password: #si se encontro la contraseña en la base de datos
                passwordEncriptada = password[0] #obtener la contraseña encriptada de la base de datos, se obtiene como una tupla y su primer elemento es la contraseña
                return passwordEncriptada #retornar la contraseña encriptada
            else:
                messagebox.showinfo("Error", "No se encontro la contraseña encriptada del departamento: "  + departamento +" en la base de datos") #si no se encontro la contraseña en la base de datos
                return None
            
        except sqlite3.Error as error:
            messagebox.showinfo("Error", "Error al obtener la contraseña", error) #si hay un error al obtener la contraseña
            return None
        
        finally:
            if conexion:
                conexion.close() #cerrar la conexión a la base de datos
            
    def desencriptar(self, password_plana, password_encriptada):
        try:
            password_plana = password_plana.encode() #convertir la contraseña plana a bytes, la contraseña plana es la que el usuario ingresó en el campo de texto
            if bcrypt.checkpw(password_plana, password_encriptada): #comparar la contraseña plana con la contraseña encriptada, checkpw devuelve True si son iguales
                return True #si son iguales, la contraseña es correcta
            else: #si no son iguales, la contraseña es incorrecta
                return False #si son diferentes, la contraseña es incorrecta
        except sqlite3.Error as error: #si hay un error al desencriptar
            print("Error al desencriptar", error) #imprimir el error
            return False #la contraseña es incorrecta
        
    def login(self, departamento, password_plana):
        departamentoNormalizado = self.normalizar(departamento)
        try:
            usuario = self.buscar(departamentoNormalizado)
            if usuario:
                password_encriptada = usuario[0][1]
                if self.desencriptar(password_plana, password_encriptada):
                    messagebox.showinfo("Login", "Login exitoso del departamento: " + departamentoNormalizado)
                    usuario_nombre = usuario[0][1]  # Almacenar el tipo de usuario antes de retornar True
                    return True, usuario_nombre
                else:
                    messagebox.showinfo("Error", "Contraseña incorrecta")
                    return False
            else:
                messagebox.showinfo("Error", "El departamento no existe")
                return False
        except sqlite3.Error as error:
            print("Error al hacer login", error)
            return False

            
    def registrar(self, departamento, password, tipo_usuario):
            conexion = None
            departamentoNormalizado = self.normalizar(departamento)
            tipo_usuario_normalizado = self.normalizar_tipo_usuario(tipo_usuario)
            
            if departamentoNormalizado and password and tipo_usuario_normalizado: #verificar que los campos no estén vacíos
                try:
                    # verificar si el usuario ya existe
                    existing_user = self.buscar(departamentoNormalizado)
                    if existing_user:
                        messagebox.showinfo("Error", "El usuario ya existe")
                        return

                    conexion = self.conexion()
                    cursor = conexion.cursor()
                    conHash = self.encriptar(password)
                    datos = (departamentoNormalizado, conHash, tipo_usuario_normalizado)
                    sqlInsert = "INSERT INTO tbUsuarios (departamento, password, tipo_usuario) VALUES (?, ?, ?)"
                    cursor.execute(sqlInsert, datos)
                    conexion.commit()
                    messagebox.showinfo("Registro", "Registro exitoso del departamento: " + departamentoNormalizado + "\nEl usuario tendra permisos de: " + tipo_usuario)
                except sqlite3.Error as error:
                    print("Error al registrar", error)
                finally:
                    if conexion:
                        conexion.close()
            else:
                messagebox.showinfo("Error", "Todos los campos son obligatorios")
        
    def modificar(self, departamento, nuevo_departamento=None, nueva_password=None):
        departamentoNormalizado = self.normalizar(departamento)
        usuario = self.buscar(departamentoNormalizado)
        if usuario:
            try:
                conexion = self.conexion()
                cursor = conexion.cursor()
                if nuevo_departamento:
                    nuevo_departamento = self.normalizar(nuevo_departamento)
                    sqlUpdate = "UPDATE tbUsuarios SET departamento = ? WHERE LOWER(departamento) = ?"
                    cursor.execute(sqlUpdate, (nuevo_departamento, departamentoNormalizado))
                if nueva_password:
                    nueva_password = self.encriptar(nueva_password)
                    sqlUpdate = "UPDATE tbUsuarios SET password = ? WHERE LOWER(departamento) = ?"
                    cursor.execute(sqlUpdate, (nueva_password, departamentoNormalizado))
                conexion.commit()
                messagebox.showinfo("Modificación", "Modificación exitosa del departamento: " + departamentoNormalizado)
            except sqlite3.Error as error:
                print("Error al modificar", error)
            finally:
                if conexion:
                    conexion.close()
        else:
            messagebox.showinfo("Error", "El departamento no existe")
            
    def eliminar(self, departamento):
        departamentoNormalizado = self.normalizar(departamento)
        usuario = self.buscar(departamentoNormalizado)
        if usuario:
            try:
                conexion = self.conexion()
                cursor = conexion.cursor()
                sqlDelete = "DELETE FROM tbUsuarios WHERE LOWER(departamento) = ?"
                cursor.execute(sqlDelete, (departamentoNormalizado,))
                conexion.commit()
                messagebox.showinfo("Eliminación", "Eliminación exitosa del departamento: " + departamentoNormalizado)
            except sqlite3.Error as error:
                print("Error al eliminar", error)
            finally:
                if conexion:
                    conexion.close()
        else:
            messagebox.showinfo("Error", "El departamento no existe")
            
    def consultarUsuarios(self):
            conexion = self.conexion()
            try:
                cursor = conexion.cursor()
                sqlSelect = "SELECT departamento FROM tbUsuarios"
                cursor.execute(sqlSelect)
                usuarios = cursor.fetchall()
                conexion.close()
                usuarios = [usuario[0] for usuario in usuarios] #convertir la lista de tuplas en una lista de strings
                return usuarios
            except sqlite3.Error as error:
                print("Error al consultar", error)
                return None
    def ejecutar_consulta(self,conexion, query, parametros=()):
        try:
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            conexion.commit()
            return cursor
        except sqlite3.Error as e:
            print("Error al ejecutar la consulta:", e)
            return None
    def ejecutar_modificacion(self, query, parametros=()):
        try:
            conexion = self.conexion()
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            conexion.commit()
        except sqlite3.Error as e:
            print("Error al ejecutar la modificación:", e)
        finally:
            if conexion:
                conexion.close()

    def normalizar_tipo_usuario(self, tipo_usuario): #metodo para normalizar el tipo de usuario a minúsculas
            return tipo_usuario.lower() if tipo_usuario else tipo_usuario

        
    def tipo_usuario(self, departamento):
        departamentoNormalizado = self.normalizar(departamento)
        usuario = self.buscar(departamentoNormalizado)
        if usuario:
            tipo_usuario = usuario[0][3] #obtener el tipo de usuario de la base de datos
            return tipo_usuario #retornar el tipo de usuario
        else:
            return None

    def buscar(self, departamento):
            departamentoNormalizado = self.normalizar(departamento)
            try:
                conexion = self.conexion()
                cursor = conexion.cursor()
                sqlSelect = "SELECT * FROM tbUsuarios WHERE LOWER(departamento) = ?"
                cursor.execute(sqlSelect, (departamentoNormalizado,))
                usuario = cursor.fetchall()
                conexion.close()
                return usuario
            except sqlite3.Error as error:
                print("Error al buscar", error)
                return None