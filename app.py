from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver  import ThreadingMixIn
import http.server
import socketserver
import threading
import time
import json
from io import BytesIO

errores={}
listas_ligadas={}
linea=0

variable="abcdefghijklmnopqrstuvwxyz_$"
variable_completa="abcdefghijklmnopqrstuvwxyz_$0123456789"
digito="0123456789"
caracter="0123456789abcdefghijklmnopqrstuvwxyz"
operador="+-^*|&<>"
signo="+-"
espacio=" \t\r\n"
entradas_validas="0123456789 abcdefghijklmnopqrstuvwxyz0123456789 +-^*|&<>= \t\r\n \"' ()[],:?;.\\"

def invalido(simbolo,i):
    errores[linea].append("simbolo invalido "+simbolo+" en la posicion "+str(i))
    print("simbolo invalido "+simbolo+" en la posicion "+str(i))


def automata_declaracion_o_expresion(cadena):
    global errores
    global listas_ligadas
    global linea
    lista=[]
    # cadena
    # print(cadena)
    estado=0
    i=-1
    ultimo=""
    z=0
    for simbolo in cadena:
        i+=1
        if entradas_validas.find(simbolo)==-1:
            if not simbolo in ["{","}"]:
                print("simbolo inesperado "+simbolo+" en la posicion "+str(i))
                errores[linea].append("simbolo inesperado "+simbolo+" en la posicion "+str(i))
        print(ultimo+"->"+str(estado))
        
        if estado==0:                                   #estado inicial, cadena vacia o simbolos de espacio
            if espacio.find(simbolo)!=-1:estado=0           #espacio (si detecta un espacio como inicio de secuencia, vuelve de nuevo al estado cero)
            elif simbolo in ["v"]:estado=1.0                  #v de var
            elif simbolo in ["l"]:estado=2.0                  #l de let
            elif simbolo in ["c"]:estado=3.0                  #c de const
            elif variable.find(simbolo)!=-1:estado=6
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==1.0:                               #estado 1.0 (llega al ingresar v de var)
            if simbolo in ["a"]:estado=1.1                  #a de var
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==1.1:                               #estado 1.1 (llega al ingresar a de var)
            if simbolo in ["r"]:estado=4                    #r de var
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==2.0:                               #estado 2.0 (llega al ingresar l de let )
            if simbolo in ["e"]:estado=2.1                  #e de let
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==2.1:                               #estado 2.1 (llega al ingresar e de let)
            if simbolo in ["t"]:estado=4                    #t de let
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==3.0:                               #estado 3.0 (llega al ingresar c de const)
            if simbolo in ["o"]:estado=3.1                  #o de const
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==3.1:                               #estado 3.1 (llega al ingresar o de const)
            if simbolo in ["n"]:estado=3.2                  #n de const
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==3.2:                               #estado 3.2 (llega al ingresar n de const)
            if simbolo in ["s"]:estado=3.3                  #s de const
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==3.3:                               #estado 3.3 (llega al ingresar s de const)
            if simbolo in ["t"]:estado=4                    #t de const
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo):estado=7
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==4:                                 #estado 4 (llega cuando se termina de escribir var, let o const)
            if espacio.find(simbolo)!=-1:estado=5           #espacio
            elif variable.find(simbolo)!=-1:estado=6
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif simbolo=='=':estado=8
            else:
                invalido(simbolo,i)
                estado=-1
        elif estado==5:                                 #estado 5 (llega cuando se ingresa un espacio despues de escribir var, let o const)
            lista.append(["tipo",cadena[z:i]])
            z=i
            if variable.find(simbolo)!=-1:estado=6          #x cualquier caracter que represente una variable
            elif variable_completa.find(simbolo)!=-1:estado=6
            elif espacio.find(simbolo)!=-1:estado=5         #si se ingresa otro espacio vuelve a si mismo
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==6:                                 #estado 6 (llega cuando se ingreso al menos un caracter que define la variable)
            if variable_completa.find(simbolo)!=-1:estado=6
            elif simbolo=="=":
                lista.append(["variable",cadena[z:i]])
                lista.append(["conector","="])
                z=i+1 
                estado=8
            elif espacio.find(simbolo)!=-1:
                estado=7
            elif operador.find(simbolo)!=-1:estado=7.0
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==7.0:
            if simbolo=='=':estado=8
            elif simbolo=="(":
                estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==7:                                 #llega despues de haberse terminado de definir la variable y se ingresa un espacio
            lista.append(["variable",cadena[z:i+1]])
            z=i+1
            if simbolo=='=':estado=8
            elif espacio.find(simbolo)!=-1:estado=7
            elif operador.find(simbolo)!=-1:estado=7.0
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==8.0:                                 #estado que indica que se va a definir el valor de la variable
            if signo.find(simbolo)!=-1:estado=12.0
            elif operador.find(simbolo)!=-1:
                invalido(simbolo, i)
                estado=-1
            elif simbolo=="(":
                estado=8
            elif simbolo=="'":estado=9.0                               
            elif simbolo=='"':estado=10.0
            elif variable.find(simbolo)!=-1:estado=11.0
            elif digito.find(simbolo)!=-1:estado=12.1
            elif simbolo==".":estado=12.2
            elif espacio.find(simbolo)!=-1:estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==8:                                 #estado que indica que se va a definir el valor de la variable
            lista.append(["separador","="])
            z=i
            if simbolo=="(":
                estado=8                                
            elif simbolo=="'":estado=9.0                               
            elif simbolo=='"':estado=10.0
            elif variable.find(simbolo)!=-1:estado=11.0
            elif signo.find(simbolo)!=-1:estado=12.0
            elif digito.find(simbolo)!=-1:estado=12.1
            elif simbolo==".":estado=12.2
            elif espacio.find(simbolo)!=-1:estado=8
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==12.0:
            if digito.find(simbolo)!=-1:estado=12.1
            elif simbolo==".":estado=12.2
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==12.1:
            if digito.find(simbolo)!=-1:estado=12.1
            elif simbolo==".":estado=12.2
            elif operador.find(simbolo)!=-1:estado=8
            else:estado=99
        elif estado==12.2:
            if digito.find(simbolo)!=-1:estado=12.3
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==12.3:
            if digito.find(simbolo)!=-1:estado=12.3
            elif simbolo=="e":estado=12.4
            else:estado=99
        elif estado==12.4:
            if signo.find(simbolo)!=-1:estado=12.5
            elif digito.find(simbolo)!=-1:estado=12.6
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==12.5:
            if digito.find(simbolo)!=-1:estado=12.6
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==12.6:
            if digito.find(simbolo)!=-1:estado=12.6
            else:estado=99
        
        elif estado==9.0:                               #llega despues de que se ingreso una comilla simple
            if simbolo=="\\":estado=9.1
            elif simbolo=="'":estado=99
            elif simbolo!="'":estado=9.0
        elif estado==9.1:                               #estado que indica que se ingreso un \\
            estado=9.0                                      #siempre regresara al estado anterior independientemente del caracter ingresado
        elif estado==10.0:
            if simbolo=="\\":estado=10.1
            elif simbolo!='"':estado=10.0
            elif simbolo=='"':estado=99
        elif estado==10.1:                              #estado que indica que se ingreso un \\
            estado=10.0                                     #siempre regresara al estado anterior independientemente del caracter ingresado
        elif estado==11.0:
            if variable_completa.find(simbolo)!=-1:estado=11.0
            elif simbolo==";":estado=100
            elif simbolo==")":estado=11.0
            elif espacio.find(simbolo)!=-1:estado=99
            else:
                # invalido(simbolo,i)
                estado=11.0
        elif estado==99:
            # lista.append(["valor",cadena[z:i+1]])
            # z=i
            if simbolo==";":estado=100
            elif simbolo==")":
                estado=99
            elif espacio.find(simbolo)!=-1:estado=99
            elif operador.find(simbolo)!=-1:estado=8.0
            else:
                invalido(simbolo, i)
                estado=-1
        elif estado==100:
            # lista.append(["valor",cadena[z:i-1]])
            # z=i
            if simbolo==";":estado=100
            elif espacio.find(simbolo)!=-1:estado=100
            else:
                invalido(simbolo, i)
                estado=-1
        
        ultimo=simbolo
    lista.append(["valor",cadena[z:i]])
    print("lista ligada : "+str(lista))
    listas_ligadas[linea]=lista
    return estado in [99,100]

def automata_palabra_clave(cadena):
    """se reconoceran las palabras clave: for while if do else"""
    cadena
    estado=0
    i=-1
    ultimo=""
    for simbolo in cadena:
        i+=1
        if entradas_validas.find(simbolo)==-1:
            if not simbolo in ["{","}"]:
                errores[linea].append("simbolo inesperado "+simbolo+" en la posicion "+str(i))
        # print("estado : "+str(estado)+" para "+ultimo)
        
        if estado==0:                                   
            if simbolo == "i":estado="i_if"
            elif simbolo == "f":estado="f_for"
            elif simbolo == "e":estado="e_else"
            elif simbolo == "w":estado="w_while"
            elif simbolo == "d":estado="d_do"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        
        elif estado==1:
            if variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        
        elif estado=="i_if":
            if simbolo=="f":estado="if_if"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
            
        elif estado=="if_if":
            if variable_completa.find(simbolo)==-1:
                invalido(simbolo, i)
                estado=-1
            else:
                estado=0
        
        elif estado=="d_do":
            if simbolo=="o":estado="do_do"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="do_do":
            if variable_completa.find(simbolo)==-1:
                invalido(simbolo, i)
                estado=-1
            else:
                estado=0
        
        elif estado=="f_for":
            if simbolo=="o":estado="fo_for"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="fo_for":
            if simbolo=="r":estado="for_for"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="for_for":
            if variable_completa.find(simbolo)==-1:
                invalido(simbolo, i)
                estado=-1
            else:
                estado=0
        
        elif estado=="e_else":
            if simbolo=="l":estado="el_else"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="el_else":
            if simbolo=="s":estado="els_else"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="els_else":
            if simbolo=="e":estado="else_else"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="else_else":
            if variable_completa.find(simbolo)==-1:
                invalido(simbolo, i)
                estado=-1
            else:
                estado=0
                
        elif estado=="w_while":
            if simbolo=="h":estado="wh_while"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="wh_while":
            if simbolo=="i":estado="whi_while"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="whi_while":
            if simbolo=="l":estado="whil_while"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="whil_while":
            if simbolo=="e":estado="while_while"
            elif variable_completa.find(simbolo)==-1:estado=0
            else:estado=1
        elif estado=="while_while":
            if variable_completa.find(simbolo)==-1:
                invalido(simbolo, i)
                estado=-1
            else:
                estado=0
        ultimo=simbolo
    # print("estado en palabra clave : "+str(estado))
    return estado != -1

def check_text(text):
    global linea
    lines = text.splitlines()
    i=0
    fallo=False
    for cadena in lines:
        i+=1
        linea=str(i)
        errores[linea]=[]
        listas_ligadas[linea]=[]
        if not(automata_palabra_clave(cadena) and automata_declaracion_o_expresion(cadena)):
            # print("Error:linea : "+str(i)+" no valida : "+cadena)
            # errores[linea].append("Error:linea : "+str(i)+" no valida : "+cadena)
            fallo=True
    if not fallo:
        print("***************Felicidades:el archivo no contine errores***********************")


def servicio_html():
    PORT = 5555
    
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()

threading.Thread(target=servicio_html).start()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        try:
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Request-Method', '*')
            self.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Content-type','application/json; charset=utf-8')
            self.end_headers()
        except:pass
        
    def log_message(self, format, *args):
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Request-Method', '*')
        self.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Content-type','application/json; charset=utf-8')        
        self.end_headers()
        self.path=self.path.replace("%20", " ")
        if self.path.find("/path?")!=-1:
            # print("el path completo es : "+self.path)
            ruta = self.path[self.path.rfind("path=")+5:]
            texto =  ""
            print("la ruta edel path es : "+ruta)
            if not os.path.exists(ruta):
                texto="null"
            response = BytesIO()
            response.write(bytes(texto, "utf-8"))
            self.wfile.write(response.getvalue())

    def do_POST(self):
        print("si llega perro")
        content_length = int(self.headers['Content-Length'])
        salida = "ok"
        body = self.rfile.read(content_length)
        # bytesa
        d = json.loads(body.decode("utf-8"))
        # print("EL BODY ES : "+body.decode("utf-8"))
        # print(body)
        # d={}
        # try:
            
        # except:pass
        print(d)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Request-Method', '*')
        self.send_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Content-type','application/json; charset=utf-8')        
        if d.get("code"):
            check_text(d.get("code"))
            salida={"listas_ligadas":listas_ligadas,"errores":errores}
            
        self.end_headers()
        response = BytesIO()
        response.write(bytes(json.dumps(salida), "utf-8"))
        try:
            self.wfile.write(response.getvalue())
        except:
            print("cliente abandonado")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def servidorHttp():
    server = ThreadedHTTPServer(('0.0.0.0', 5556), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=servidorHttp).start()
