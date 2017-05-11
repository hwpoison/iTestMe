from models.examen import *


d = Examinar("admin123")
for i in range(0,9):
	print(d.Examen()["progresoActual"])
	d.gConsigna(respuesta="apnea")



