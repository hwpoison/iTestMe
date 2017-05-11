#iTestMe:https://github.com/sRBill90/iTestMe/
from models.examen import Examinar, dbUsers, examenesActuales
from functools import wraps
from flask import *
import random
import json
import os        

#Inicio de app    
iTestMe = Flask(__name__)

#Creacion cuenta de prueba
dbUsers.registrarUsuario("admin123","administrador de itestme", "admin123")

datosGenerales = { 
        "titulo":"iTestMe",
}

def validarDatos_get(datos={}):
    datosTemporal = datosGenerales
    for datoD in datos:
        datosTemporal[datoD] = datos[datoD]
    return datosTemporal

#Verifica si el visitante es un usuario logeado
def enLogin(route):
    @wraps(route)
    def verificarSesion(*args, **kwargs):
        if(request.cookies.get("tokenSesion")):
            nombre = request.cookies.get("usuarioID")
            tokenSesion = request.cookies.get("tokenSesion")
            tokenUsuario = dbUsers.obtenerUsuario(nombre)[4]
            if(tokenUsuario == tokenSesion):
                return route(*args, **kwargs)
        print("No estas logeado!")
        return redirect(url_for("logear"))
    return verificarSesion


#Evitar entrar en lugares si el usuario esta logeado (como paginas de registro o login)
def enSesion(route):
    @wraps(route)
    def verificarLogin(*args, **kwargs):
        if(request.cookies.get("tokenSesion")):
            return redirect(url_for("home"))
        else:
            return route(*args, **kwargs)
    return verificarLogin
    
#Internal error intensional
@iTestMe.route("/internal")
def internal():
    return render_template("errores/internalError.html", **validarDatos_get( 
                                                         {"titulo":"Auch!"} ))
    
#Pagina de inicio
@iTestMe.route("/")
@enLogin
def home():
    cooki = request.cookies.get("tokenSesion")
    usuarioID = request.cookies.get("usuarioID")
    datosUsuario = dbUsers.obtenerUsuario(usuarioID)
    nombreUsuarioActual = datosUsuario[1].split(" ")[0]
    datosGenerales["usuario"] = nombreUsuarioActual
    datosGenerales["titulo"] = "Inicio"
    if(examenesActuales.obtenerExamen(datosUsuario[0])):
        estado = "Continuar examen.."
    else:
        estado = "Iniciar examen rapido!"
        
    return render_template("home/home.html",
                        **validarDatos_get({
                                            "estadoExamen":estado
                                            }))
                                            
#Desloguear
@iTestMe.route("/deslogear")
def deslogear():
    resp = iTestMe.make_response(redirect("/"))
    resp.set_cookie("tokenSesion", "", expires=0)
    return resp
    
    
#Pagina de login
@iTestMe.route("/login",        methods=["GET", "POST"])
@enSesion
def logear():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        if(dbUsers.verificarDatos(usuario,password)):
                print("[+]Usuario %s logeado correctamente"%usuario)
                resp = iTestMe.make_response(json.dumps({"status":"OK"}))
                tokenGen = dbUsers.asignarToken(str(usuario))
                resp.set_cookie("usuarioID", value=usuario)
                resp.set_cookie("tokenSesion",value=tokenGen)
                return resp
        else:
                return json.dumps({"status":"FAIL"})
                                
    if request.method == "GET":
        resp = iTestMe.make_response(render_template("login/login.html",
                                    **validarDatos_get( 
                                    {"titulo":"Iniciar Sesión"} )))
        resp.set_cookie("tokenSesion", value="")
        return resp 


#Pagina registro
@iTestMe.route("/registro",     methods=["GET", "POST"])
@enSesion
def registro():
    if(request.method == "GET"):
        return render_template("/registro/registro.html", **validarDatos_get( 
                                                          {"titulo":"Registrarse"} ))
    
    if(request.method == "POST"):
        nombreUsuario = request.form.get("usuario")
        password = request.form.get("password")
        nick = request.form.get("nick")
        datos = dbUsers.registrarUsuario(nick, nombreUsuario, password)
        return json.dumps(datos)


@iTestMe.route("/examen")
def examen():
    return render_template("/examen/examen.html", **validarDatos_get(
                                                  {"titulo":"En examen.."} ))
    
#Pagina inicio(o continuacion) de examen
@iTestMe.route("/examinar",     methods=["GET", "POST"])
@enLogin
def examaminar():
    usuarioActual = request.cookies.get("usuarioID")
    if request.method == "GET":
        examenActual = Examinar(usuarioActual).Examen()
        if(examenActual["tipo"] == "examenFinalizado"):
            datosGenerales["titulo"] = "Resumen"
            return render_template("examen/resumenExamen.html", 
                                    **validarDatos_get(examenActual) )
        
        #Si se va a enviar una consigna multiple choice
        if(examenActual["tipo"] == "choice"):               
            return render_template("examen/multipleChoice.html", 
                                    **validarDatos_get(examenActual) )                                      
        
        #Si se va a enviar una consigna tipo Escrita
        if(examenActual["tipo"] == "escrita"):
            return render_template("examen/consignaEscrita.html", 
                                    **validarDatos_get(examenActual) )
    
    if request.method == "POST":
        examinado = Examinar(usuarioActual)
        respuestaRecibida = request.form.get("respuestaEscrita")
        #Si se recibio una respuesta, verificar
        if(respuestaRecibida):
            verificacion = examinado.gConsigna(respuesta=respuestaRecibida)
            return render_template("examen/consignaVerificada.html", **validarDatos_get(
                                                                     verificacion ))

                
#Interal error
@iTestMe.errorhandler(500)
def internalError(error):
    return render_template("errores/internalError.html", **validarDatos_get( 
                                                         {"titulo":"Auch!"} ))
    

#404 not found error
@iTestMe.errorhandler(404)
def fError(error):
    return render_template("errores/notFound.html", **validarDatos_get( 
                                                    {"titulo":"WANTED!"} ))
    
if __name__ == "__main__":
    print("[+]Iniciando iTestMe")
    iTestMe.run()
