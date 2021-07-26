#!/usr/bin/env python
from bs4 import BeautifulSoup
from firebase import firebase
import re
import os
import time
import logging
import requests
from clases import Subasta
from datetime import datetime
import json

try:
        from urllib2 import urlopen
        from urllib2 import Request
except ImportError:
        from urllib.request import urlopen
        from urllib.request import Request


# INICIO BD
#firebase = firebase.FirebaseApplication('https://appfire-picada.firebaseio.com/subastas', None)

#METODOS
def conexionBD(ruta):
    print("Conexion a:" + ruta)
    return firebase.FirebaseApplication(ruta, None)

def cargarDatosBD(ruta, firebase, tablaDB):
    listaDatosBD=''
    try:  
        listaDatosBD = firebase.get(tablaDB,'')                  
    except:
        print("No existe datos en la BD")
    return listaDatosBD

def eliminarDatosBD(ruta, firebase, tablaDB):
    # Carga los datos de la BD y los marca como borrado, y cambia el estado a finalizado.    
    listaDatosBD = cargarDatosBD(ruta, firebase, tablaDB)
    # print(len(listaDatosBD))
    # os.system("pause")
    # listaKeyBorradoBD = []
    listaKeyBD = listarKeyBD(listaDatosBD)
    # os.system("pause")
    # numElem = len(listaKeyBD)
    # print("Num elementos BD: ")
    # print(numElem)
    # os.system("pause")
    # print("Llamada a listado borrado BD")
    listaKeyBorradoBD = listarValuesBorradoBD(listaDatosBD,listaKeyBD)
    print("Elementos marcados como finalizados " + str(len(listaKeyBorradoBD)))
    return listaKeyBorradoBD

# def updateDatosBD(ruta, firebase, tablaDB, tipoUpdate):
#     firebase.firebaseio

def fechaActual() :
    return datetime.today().strftime('%Y-%m-%d')

def listarValuesBorradoBD(listaDatosBD,listaKeyBD):
    listaValuesBorradoBD = []
    
    # os.system("pause")
    fechaHoy = fechaActual()
    # print("Filtrar elementos con fecha anterior a: " + fechaHoy)
    # os.system("pause")
    numElem = len(listaKeyBD)
    for i in range(numElem):
        keyElementoBD=listaKeyBD[i]
        elementoBD = elementoValueBD(listaDatosBD, keyElementoBD)
        # print(elementoBD)
        # os.system("pause")

        # print(type(elementoBD))
        # os.system("pause")

        # print(len(elementoBD))
        # os.system("pause")

        ## EL ACESO A LOS ATRIBUTOS DEL DICCIONARIO SE 
        ## SE HACE A TRAVES DE SU KEY.
        fechaFin = elementoBD['fechaFin']
        idSubasta = elementoBD['idSubasta']
        # print(fechaFin)
        if fechaFin < fechaHoy :
            # print(fechaFin + '<' + fechaHoy)
            # print('El elemento con ID:' + idSubasta + ' ha terminado su periodo de pujas')
            # print('Vivienda: ' + elementoBD['tipoFinca'])
            # print(keyElementoBD)
            listaValuesBorradoBD.append(keyElementoBD)
        # os.system("pause")
    return listaValuesBorradoBD

def listarKeyBD(listaDatosBD):
    listaKeyBD = []
    for datoBD in listaDatosBD:
        listaKeyBD.append(datoBD)   
    # print(len(listaKeyBD)) 
    return listaKeyBD


def listarValuesBD(listaDatosBD,listaKeyBD):
    listaValuesBD = []
    numElem = len(listaKeyBD)
    for i in range(numElem):
        listaValuesBD.append(elementoValueBD(listaDatosBD, listaKeyBD[i]))
    return listaValuesBD


def elementoValueBD(listaDatosBD, keyBD):
    return listaDatosBD[keyBD]


def buscarWebCompleta(host_url):
    req = requests.get(host_url)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    soup.prettify()
    return soup


def buscarBloquesSubastas(soup, ubicacion):
    listadoObjetosSubastas = []
    listadoBloquesWebSubastas = soup.find_all(class_='resultado-busqueda')    
    for ing in listadoBloquesWebSubastas:        
        idSubasta = ing.find('h3')        
        lugar = ing.find('h4')
        listadoParrafos = ing.find_all('p')       
        link = ing.find('a')['href']
        numeroParrafos = len(ing.find_all('p'))    
        contador = 0

        if numeroParrafos < 3 :
            contador = 1
        
        informacion = ["0", "0", "0"]
        for parrafo in listadoParrafos:    
            informacion[contador] = parrafo.text.strip()
            contador = contador + 1   
            cadena =  str(contador) + '. '  + parrafo.text.strip()
            #print(cadena)
        subasta = Subasta()
        subasta.id = limpiarIdSubasta(idSubasta.text.strip())      
        subasta.lugar = lugar.text.strip()        
        subasta.expediente = limpiarExpediente(informacion[0])
        subasta.estado = limpiarEstado(informacion[1])        
        subasta.fechaFin = limpiarFecha(informacion[1])        
        subasta.horaFin = limpiarHora(informacion[1])        
        subasta.tipoFinca = informacion[2]        
        subasta.url = "https://subastas.boe.es" + link[1:]
        subasta.ubicacion = ubicacion
        listadoObjetosSubastas.append(subasta)
        #mostrarObjetoSubasta(subasta)    
    # print("Listado objetos subastas")
    # print(len(listadoObjetosSubastas))
    # os.system("pause")
    return listadoObjetosSubastas


def mostrarObjetoSubasta(subasta):
    print("ID -- " + subasta.id)
    print("LUGAR -- " + subasta.lugar)
    print("EXPEDIENTE -- " + subasta.expediente)
    print("FECHA FIN SUBASTA -- " + subasta.fechaFin)
    print("HORA FIN SUBASTA -- " + subasta.horaFin)
    print("DATOS VEHICULO -- " + subasta.tipoFinca)
    print("ENLACE -- " + subasta.url)
    print("UBICACION -- " + subasta.ubicacion)
    print("************************************")
    

def limpiarExpediente(expediente):        
    partes = expediente.split("Expediente: ")
    if len(partes) == 1:
        return "No Datos"
    else:
        return partes[1]
    
    

def limpiarEstado(estadoFecha):
    partes = estadoFecha.split(" - [Conclusión prevista: ")
    estado = partes[0].split("Estado: ")
    #print(estado[1])    
    return estado[1]

def limpiarFecha(estadoFecha): 
    partes = estadoFecha.split(" - [Conclusión prevista: ")
    fecha = partes[1].split(" a las ")
    #print(fecha[0])
    return fecha[0]

def limpiarHora(estadoFecha): 
    partes = estadoFecha.split(" - [Conclusión prevista: ")
    horaBasura = partes[1].split(" a las ")
    hora = horaBasura[1].split("]")
    #print(hora[0])
    return hora[0]

def numeroPaginasWebSubasta(soup):
    paginas = soup.find(class_='paginar')
    npaginas = paginas.find('p').getText()
    return npaginas


def buscarNovedasdesWebSubasta(host_url,ubicacion):    
    soup = buscarWebCompleta(host_url)
    # if ubicacion == "España" :
    #    print(soup)
    listadoObjetosSubastas = buscarBloquesSubastas(soup,ubicacion)    
    return listadoObjetosSubastas

def limpiarIdSubasta(idSubasta):
    sinEspacios = limpiarEspacios(idSubasta)    
    sinCaracteres = limpiarCaracteresEspeciales(sinEspacios)    
    sinSaltos = limpiarSaltosLinea(sinCaracteres)
    # print("Limpio: " + sinSaltos)
    return sinSaltos
    
def limpiarEspacios(cadena):
    sinEspacios = cadena.split(" ")
    # print("Paso 1, espacios: " + sinEspacios[1])
    return sinEspacios[1]

def limpiarCaracteresEspeciales(cadena):
    sinEspacios = cadena.strip()
    reemplazo= sinEspacios.replace("\'","")
    # print("Paso 2, reemplazo " + reemplazo )
    sinCaracteresEspeciales = re.split(r'[`\=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', reemplazo)
    # print("Paso 3, caracteres especiales " + str(sinCaracteresEspeciales))
    if len(sinCaracteresEspeciales) == 1 :
        return sinCaracteresEspeciales[0]
    elif len(sinCaracteresEspeciales) > 4:
        return sinCaracteresEspeciales[2]
    

def limpiarSaltosLinea(cadena):
    sinSaltosLinea = cadena.split('\n')
    # print("Paso 4, Saltos Linea " + sinSaltosLinea[0])
    return sinSaltosLinea[0]

def existeElementoBD(listadoObjetosSubastas, elementoBuscado):   
    #print(elementoBuscado)         
    for elementoLista in listadoObjetosSubastas:
        #print("ELEMENTO DE LA LISTA" + str(elementoLista))
        x = str(elementoLista).split(", ")
        y = limpiarIdSubasta(x[4])         
        if y == elementoBuscado:  
            #print(elementoBuscado + "EXISTE")          
            return True 

    #print(elementoBuscado + "NO ENCONTRADO EN LISTA")  
    return False

def esListaVacia(data_structure):
    if data_structure:
        #print("No está vacía")
        return False
    else:
        #print("Está vacía")
        return True


def insertarDatosBD(firebase, tabla, objetoSubasta, listaValuesBD, listaDatosBD):
    try:   
        existe = False   
        if not esListaVacia(listaDatosBD):  
            existe = existeElementoBD(listaValuesBD, objetoSubasta.id)
        if existe == False:
            datoBd = {
                'estado' : objetoSubasta.estado,
                'expediente' : objetoSubasta.expediente,
                'idSubasta' : objetoSubasta.id,
                'lugar' : objetoSubasta.lugar,
                'tipoFinca' : objetoSubasta.tipoFinca,
                'url' : objetoSubasta.url,
                'fechaFin' : objetoSubasta.fechaFin,
                'horaFin' : objetoSubasta.horaFin,
                'ubicacionCasa' : objetoSubasta.ubicacion
            }            
            result = firebase.post(tabla, datoBd) 

        else :
            result = "OMITIDO"           
    except:        
        result = "ERROR"

    return result

def mostrarEstadisticas(contadorI,contadorO,contadorE) :
    print("ESTADISTICAS:")
    print("Se han INSERTADO en BD " + str(contadorI) + " registros")      
    print("Se han OMITIDO en BD " + str(contadorO) + " registros") 
    print("Se han PRODUCIDO ERRORES en " + str(contadorE) + " registros") 


def insertarDatosCochesBD(firebase, tabla, objetoSubasta, listaValuesBD, listaDatosBD):
    try:   
        existe = False           
        if not esListaVacia(listaDatosBD):  
            existe = existeElementoBD(listaValuesBD, objetoSubasta.id)
        # # print("-------------------------")
        # # print(objetoSubasta)
        # # print(existe)
        if existe == False:
            datoBd = {
                'estado' : objetoSubasta.estado,
                'expediente' : objetoSubasta.expediente,
                'idSubasta' : objetoSubasta.id,
                'lugar' : objetoSubasta.lugar,
                'tipoFinca' : objetoSubasta.tipoFinca,
                'url' : objetoSubasta.url,
                'fechaFin' : objetoSubasta.fechaFin,
                'horaFin' : objetoSubasta.horaFin,
                'ubicacionCoche' : objetoSubasta.ubicacion
            }            
            result = firebase.post(tabla, datoBd) 

        else :
            result = "OMITIDO"           
    except:        
        result = "ERROR"

    return result