

n = "asdkas~@"

def comprobarNick(x):
	for c in x:
		ordc = ord(c)
		if(ordc > 65 and ordc < 90  or #Mayusculas
		   ordc > 95 and ordc < 122 or #Minusculas
		   ordc > 48 and ordc < 57  or  #Numeros
		   ordc == 95):	#guion bajo
			   pass
		else:
			return c
	return True

print(comprobarNick("asd."))
