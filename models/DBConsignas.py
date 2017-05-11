import random
import sqlite3

dbs_index = ["consignas.txt","choices.txt"]
dbs_completa = {}
sesionesActuales = {

}
index = 0
for dbs in dbs_index:#Crear dbs
	with open(dbs, "r", encoding="utf-8") as archivo_p:
		for fila in archivo_p.read().split("\n"):
			if("=FIN=" in fila):break
			if("=" not in fila):
				if(index not in dbs_completa):
					dbs_completa[index] = [fila]
				else:
					dbs_completa[index].append(fila)
			else:
				index+=1
class Consignas():
	def __init__(self):
		#self.db = sqlite3.connect("dbPreguntas.db")
		self.db = sqlite3.connect(":memory:")
		self.iniciar()
		self.registrarDeTxt()
		self.cursor = self.db.cursor()
		
	def registrarConsigna(self,params):
		id_ = self.db.execute("SELECT id, consigna, tipo FROM consignas WHERE id = (select max(id) from consignas)")
		try:uid = int(id_.fetchall()[0][0])
		except:uid = 0	
		if(len(params) > 6):
			img = params[6]
		else:
			img = "noimagen"
		self.db.execute("INSERT INTO consignas(id,consigna,tipo,dificultad,respuesta,aclaracion,tags,imagen) \
					values (?,?,?,?,?,?,?,?)",(int(uid)+1, params[0],params[1],params[2],params[3],params[4],params[5],img))
		self.db.commit()
		return True
		
	def registrarDeTxt(self):
		for m in dbs_completa:
			self.registrarConsigna(dbs_completa[m])
		print("[+] %d Consignas cargadas en la memoria."%m)
		
	def iniciar(self):
		try:
			self.db.execute("""CREATE TABLE consignas(
					id integer primary key,
					consigna varchar,
					tipo varchar,
					dificultad varchar,
					respuesta varchar,
					aclaracion varchar,
					tags varchar,
					imagen varchar
					)""")
		except:
			pass
	
	def verTodo(self):
		for m in self.db.execute("SELECT * FROM consignas"):
			print(m)
	
	def consignaAleatoria(self,tipo=None, dificultad=None):	
		if(dificultad is None or dificultad == "cualquiera"):
			obtenida = self.db.execute("SELECT * FROM consignas where tipo=?",(tipo,))
		elif(dificultad is None and tipo is None):
			obtenida = self.db.execute("SELECT * FROM consignas")
		elif(tipo and dificultad):
			obtenida = self.db.execute("SELECT * FROM consignas where tipo=? and dificultad=?",(tipo,dificultad,))
		if(obtenida):
			return list(random.choice(obtenida.fetchall()))
		else:
			return False
	def obtenerPorId(self, idConsigna):
		consultaID = self.db.execute("SELECT * FROM consignas where id=?",(idConsigna,))
		obtenido = consultaID.fetchall()
		if(obtenido):
			return obtenido[0]
		else:
			return None
			
if __name__ == "__main__":
	dbConsignas = Consignas()
	dbConsignas.verTodo()
else:
	consignas = Consignas()
	#consignas.verTodo()
