from models.DBExamenes import ExamenesActuales, examenesActuales
from models.DBConsignas import Consignas, consignas
from models.DBUsuarios import Usuarios, dbUsers
import random
import json

dbUsers = dbUsers

class Examinar():
	__slots__  = ['log', 'db', 'datosExamen', 'id_examen',
				  'idUsuario', 'datosActual']
	
	def __init__(self, ID_USUARIO):
		self.log = True
		self.db = consignas
		self.datosExamen = examenesActuales.obtenerExamen(ID_USUARIO)
		if(self.datosExamen is False):
			print("(+)Iniciando examen para %s"%ID_USUARIO)
			examenesActuales.iniciarExamen(ID_USUARIO, dbUsers)
			
		self.datosExamen = examenesActuales.obtenerExamen(ID_USUARIO)
		self.id_examen = self.datosExamen[0]
		self.idUsuario = self.datosExamen[1]
		self.datosActual = eval(self.datosExamen[2])
		
			
	def logmsg(self, msg, tipo=True):
		"""Mensages log"""
		if(self.log):
			if(tipo):
				print("[+]" , msg, " < - ", self.idUsuario)
			else:
				print("[-]" , msg, " < - ", self.idUsuario)
	
	
	def guardarEstadoExamen(self):
		
		datosActualizar = [
							self.id_examen,
							self.idUsuario,
							json.dumps(self.datosActual),
		]
		examenesActuales.actualizarExamen(datosActualizar)	
	
			
	def gConsigna(self, respuesta=None):
		actual = self.datosActual["progresoActual"]
		idActual = self.datosActual["examenGenerado"][actual-1]
		datosConsigna = self.db.obtenerPorId(idActual)
		#POSICIONES
		TIPO = datosConsigna[2]
		CONSIGNA = datosConsigna[1]
		DIFICULTAD = datosConsigna[3]
		ACLARACION = datosConsigna[5]
		IMAGEN = datosConsigna[7]
		RESPUESTA = datosConsigna[4]
		##########
		if(respuesta is None):
			self.logmsg("Enviando datos de consigna")
			plantilla = {
				"tipo":TIPO,
				"consigna":CONSIGNA,
				"dificultad":DIFICULTAD,
				"imagen":"noimagen" if IMAGEN == "noimagen" else IMAGEN,
				#
				"respuestasAcertadas":self.datosActual["Acertadas"],
				"respuestasDesacertadas":self.datosActual["Invalidas"],
				"progresoActual":self.datosActual["progresoActual"],
				"cantidadPreguntas":self.datosActual["cantidadPreguntas"]
			}
			if(TIPO == "choice"):
				opciones = RESPUESTA.split("//")
				plantilla["opcionesChoice"] = random.sample(opciones, len(opciones))
				
			self.datosActual["enPregunta"] = "si"
			self.guardarEstadoExamen()
			return plantilla
		else:
			self.logmsg("Verificando respuesta..")
			dConsigna = self.db.obtenerPorId(idActual)
			respuestaValida = dConsigna[4].split("//")[0] if TIPO == "choice" else dConsigna[4]
			comparacion = respuesta == respuestaValida if TIPO == "choice" else self.compararDatos(respuestaValida,
																								   respuesta)
			datosVerificacion = {
				"consigna":TIPO,
				"valida":"respuestaValida" if comparacion is True else "respuestaInvalida",
				"aclaracion":ACLARACION,
				"respuestaDada":respuesta,
				"imagen":IMAGEN
			}							
			if(comparacion):
				self.datosActual["progresoActual"] += 1
				self.datosActual["Acertadas"] +=1
				self.datosActual["enPregunta"] = "no"
				self.guardarEstadoExamen()
			else:
				self.datosActual["progresoActual"] += 1
				self.datosActual["Invalidas"] +=1
				self.datosActual["enPregunta"] = "no"
				self.guardarEstadoExamen()
				
			return datosVerificacion
	
	
	def compararDatos(self, original, tipeado):
		"""Compara dos datos y lanza true si la mitad 
		de los elementos coinciden"""
		original = original.lower()
		usuario = tipeado.lower().replace(".",",")
		coinc = 0
		for b in usuario.split(" "):
			if(b in original.split(" ")):
				coinc+=1
		if(coinc >= len(original.split(" "))/2):
			return True
		else:
			return False
	
			
	def notaFinal(self, acertadas, invalidas):
		if(invalidas == 0):
			return "A"#bien
		elif(acertadas == 0):
			return "D"#mal sin ninguna acertada
		elif(acertadas > invalidas):
			return "B"#mas acertadas que invalidas
		elif(acertadas == invalidas):
			return "C"#iguales de acertadas e invalidas
		elif(invalidas > acertadas):
			return "F"#mas invalidas que acertadas
		else:
			return "No se como calificarlo."
		
					
	def Examen(self, respuesta=None):
		if(self.datosActual):
			progresoActual = self.datosActual["progresoActual"]
			cantidadPreguntas = self.datosActual["cantidadPreguntas"]
			if(progresoActual > cantidadPreguntas):
				evaluacion = self.notaFinal(self.datosActual["Acertadas"], self.datosActual["Invalidas"])
				examenesActuales.detenerExamen(self.idUsuario)
				examenesActuales.guardarExamen(self.idUsuario, evaluacion)
				print("Examen finalizado %s"%evaluacion)
				return 	{
					"tipo":"examenFinalizado",
					"evaluacion":evaluacion,
					"respuestasAcertadas":self.datosActual["Acertadas"],
					"respuestasDesacertadas":self.datosActual["Invalidas"],
					"cantidadPreguntas":self.datosActual["cantidadPreguntas"],
					"progresoActual":self.datosActual["cantidadPreguntas"],
			}
			else:
				return self.gConsigna()
				
					
		else:
			examenActual = self.datosActual
			examenActual["progresoActual"] = 1
			examenActual["cantidadPreguntas"] = 10
			examenActual["examenGenerado"] = self.construirExamen("facil",["medicina"])
			examenActual["Acertadas"] = 0
			examenActual["Invalidas"] = 0
			examenActual["enPregunta"] = "no"
			self.datosActual = examenActual
			self.guardarEstadoExamen()
			return self.gConsigna()
	
		
	def compararTags(self, tag, tag2, estricto=False):
		comp = 0
		for tg in tag2:
			if(tg in tag):comp+=1
		if(estricto):
			if(comp == len(tag)):return True
			else:return False
		else:
			if(comp):return True


	def construirExamen(self, dificultad=None, tags=[], cantidadPreguntas = 10):
		if(dificultad):quer = consignas.db.execute("SELECT * FROM consignas WHERE \
																	(dificultad=?)",(dificultad,)).fetchall()
		else:quer = consignas.db.execute("SELECT * FROM consignas").fetchall()
		localizadas = []
		if(quer):
			for consigna_loc in quer:
				if(tags):
					tagC = consigna_loc[6].split(",")
					comparacion = self.compararTags(tags, tagC)
					if(comparacion):localizadas.append(consigna_loc[0])
				else:
					localizadas.append(consigna_loc)
			return random.sample(localizadas, cantidadPreguntas)
		return False
if __name__ == "__main__":
	pass
