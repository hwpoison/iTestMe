from models.DBUsuarios import Usuarios
import sqlite3
import random
import time

class ExamenesActuales():
	def __init__(self):
		self.db = sqlite3.connect("db/examenes.db")
		self.iniciar()
	
	def iniciar(self):
		self.db.execute("""CREATE TABLE IF NOT EXISTS examenesActuales
					(
					  id_examen primary key,
					  nick varchar,
					  datosBuffer varchar
					);""")
		self.db.execute("""CREATE TABLE IF NOT EXISTS examenesFinalizados
					(
					  id_examen integer primary key,
					  nick varchar,
					  evaluacion varchar,
					   fecha varchar
					);""")
					
		print("[+]Memoria ExamenesActuales iniciada")
	
	def iniciarExamen(self, usuarioID, usuarios):
		usuarioExiste = usuarios.verificarExistencia(usuarioID)
		idObtenida = self.db.execute("SELECT id_examen FROM examenesActuales where\
									id_examen = (select max(id_examen) from examenesActuales)").fetchall()
		if(idObtenida):
			ID= idObtenida[0][0]
		else:
			ID = 0
		if(usuarioExiste):
			self.db.execute("INSERT INTO examenesActuales values(?,?,?)",(int(ID)+1,usuarioID,"{}"))
			self.db.commit()
			return ID+1
		else:
			print("[-]El usuario no existe")
			return False #id del examen iniciado
										
	def detenerExamen(self, usuarioID):
		ID = self.db.execute("SELECT * FROM examenesActuales where nick=?",(usuarioID,)).fetchall()
		if(ID):
			datosFinales = list(ID[0])
			self.db.execute("DELETE FROM examenesActuales where nick=?",(usuarioID,))
			self.db.commit()
			return datosFinales
			
	def verTodo(self):
		for m in self.db.execute("SELECT * FROM examenesActuales"):
			print(m)	
					
	def guardarExamen(self, userID, calificacion):
		#Guardar en historial de examenes
		print("Guardando")
		id_histo = self.db.execute("SELECT * FROM examenesFinalizados where\
								id_examen = (select max(id_examen) from examenesFinalizados)").fetchall()
		if(id_histo):
			id_ = id_histo[0][0]
		else:
			id_ = 0
		
		self.db.execute("INSERT INTO examenesFinalizados values(?, ?, ?, ?)",\
							(id_+1,userID,calificacion,time.strftime("%d/%m/%y")))		
		self.db.commit()		
		
	def actualizarExamen(self, params):
		ID = self.db.execute("SELECT * FROM examenesActuales where\
															(nick=?)",(params[1],)).fetchall()
		if(ID):
			self.db.execute(" UPDATE examenesActuales SET 	\
											datosBuffer=? \
											where nick=? ",(str(params[2]),params[1],))
			self.db.commit()
		else:
			print("[-]No existe el examen '%s'"%params[0])
			
	def obtenerExamen(self, nick):
		ID = self.db.execute("SELECT * FROM examenesActuales where nick='%s'"%nick).fetchall()
		if(ID):
			datos = ID[0]
			return list(datos)
		else:
			return False
		
if __name__ == "__main__":
	dbUsers = Usuarios()
	dbUsers.registrarUsuario("admin","admin123")

	dbExamenes = ExamenesActuales()
	dbExamenes.iniciarExamen("admin", dbUsers)
	dbExamenes.verTodo()
	
	
	dbExamenes.verTodo()
	print(dbExamenes.obtenerExamen(1))
else:
	examenesActuales = ExamenesActuales()
	
	
	
	

