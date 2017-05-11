import random
import sqlite3
import base64
"""
En esta base de datos estan los usuarios con sus respectivas contraseñas
"""
class Usuarios():
	def __init__(self):
		self.db = sqlite3.connect("db/usuarios.db")
		self.iniciarDB()
		
	def iniciarDB(self):
		self.db.execute("""CREATE TABLE IF NOT EXISTS usuarios(
												nick varchar primary key,
												nombre varchar,
												password varchar,
												online varchar,
												token varchar
					  );
					  """)
		print("[+]Memoria usuarios iniciada")
		
	def lanzarStatus(self, msg):
		return {"status":msg}
		
	def registrarUsuario(self ,usuarioID, nombre, usuarioPassword):
		idObtenida = self.db.execute("SELECT nick FROM usuarios WHERE (nick=?)", (usuarioID,)).fetchall()
		#Comprobacion de datos
		if(len(usuarioPassword) < 6):
			return self.lanzarStatus("La contraseña es demasiado corta.")
					
		if(len(usuarioID) < 5):
			return self.lanzarStatus("El nick es demasiado corto.")
		
		def comprobarNick(x):
			#Comprueba que el nick no tenga simbolos extraños
			for c in x:
				ordc = ord(c)
				if(ordc >= 65 and ordc <= 90  or #Mayusculas
				   ordc >= 97 and ordc <= 122 or #Minusculas
				   ordc >= 48 and ordc <= 57  or  #Numeros
				   ordc == 95):	#guion bajo
					   pass
				else:
					return c
			return True
			
		comprobacionSimbolos = comprobarNick(usuarioID)
		if(comprobacionSimbolos is not True):
			return self.lanzarStatus("El nick no puede contener simbolos como '%s'"%comprobacionSimbolos)
		
		
		
		if(len(nombre) < 5):
			return self.lanzarStatus("El nombre es demasiado corto.")
			
		if(idObtenida == []):
			self.db.execute("INSERT INTO usuarios values(?, ?, ?, ?, ?)",
														(usuarioID.lower(), nombre ,usuarioPassword.lower(), 0, "null",))
			print("[+]Usuario '%s' registrado."%usuarioID)
			self.db.commit()
			return self.lanzarStatus("registrado_correctamente")	
		else:
			print("[-]Ya se encuentra registrado ese usuario")								
			return self.lanzarStatus("Ya se encuentra registrado ese nombre, prueba con otro")
			
	def obtenerUsuario(self, usuarioID):
		ob = self.db.execute("SELECT * FROM usuarios WHERE (nick=?)", (usuarioID,)).fetchall()
		if(ob):
			return ob[0]
	
	def generarToken(self, usuarioID):
		tabla = "aAbBcCeEdDfFgGhHi\
		IjJkKmMnNlLoOpPqQrRsStTuUvVwWx\
		yYzZ1234567890X"
		tabla.replace(random.choice(tabla), usuarioID)
		tokenFinal = "".join([random.choice(tabla) for m in range(128)])
		return tokenFinal

	def asignarToken(self, usuarioID):
		tokenSesion = self.generarToken(usuarioID)
		ob = self.db.execute("SELECT * FROM usuarios WHERE (nick=?)", (usuarioID,))
		if(ob):
			self.db.execute("UPDATE usuarios SET token=? WHERE(nick=?)", (tokenSesion ,usuarioID,))
			self.db.commit()
			return tokenSesion
		else:
			return False
		
	def eliminarToken(self, usuarioID):
		ob = self.db.execute("SELECT * FROM usuarios WHERE (nick=?)", (usuarioID,))
		if(ob):
			self.db.execute("UPDATE usuarios SET token=? WHERE(nick=?)", ("null" ,usuarioID,))
			self.db.commit()
			return True
		else:
			return False
			
	def estaLogeado(self, usuarioID):
		ob = self.db.execute("SELECT online, cookie FROM usuarios where nick=()?",(nick,))
		print(ob)
		
	def verificarDatos(self ,usuarioID, usuarioPassword):
		idObtenida = self.db.execute("SELECT * FROM usuarios WHERE \
										(nick=? and password=?)",
										(usuarioID.lower(),usuarioPassword.lower(),)).fetchall()
		if(idObtenida):
			print("Nombre y contraseña correcta.")
			return True
		else:
			print("Nombre o contraseña incorrecta.")
			return False
		
	def verificarExistencia(self, usuarioID):
		idObtenida = self.db.execute("SELECT nick from usuarios WHERE (nick=?)",(usuarioID,))
		if(idObtenida):
			return usuarioID
		else:
			return False
				
			
if __name__ == "__main__":
	dbUsers = Usuarios()
	dbUsers.registrarUsuario("admin","admin123")
	dbUsers.asignarToken("admin")
	print(dbUsers.obtenerUsuario("admin"))
else:
	dbUsers = Usuarios()




