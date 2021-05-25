#!/usr/bin/env python
from bs4 import BeautifulSoup
from firebase import firebase
import re
import os
import time
import logging
import requests
from clases import Subasta
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


def listarKeyBD(listaDatosBD):
    listaKeyBD = []
    for datoBD in listaDatosBD:
        listaKeyBD.append(datoBD)
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


def buscarBloquesSubastas(soup):
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
            #cadena =  str(contador) + '. '  + parrafo.text.strip()
                
        subasta = Subasta()
        subasta.id = limpiarIdSubasta(idSubasta.text.strip())
        subasta.lugar = lugar.text.strip()
        subasta.expediente = limpiarExpediente(informacion[0])
        subasta.estado = limpiarEstado(informacion[1])
        subasta.fechaFin = limpiarFecha(informacion[1])
        subasta.horaFin = limpiarHora(informacion[1])
        subasta.tipoFinca = informacion[2]
        subasta.url = "https://subastas.boe.es" + link[1:]
        listadoObjetosSubastas.append(subasta)

    return listadoObjetosSubastas

def limpiarExpediente(expediente):
    partes = expediente.split("Expediente: ")
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


def buscarNovedasdesWebSubasta(host_url):    
    soup = buscarWebCompleta(host_url)
    listadoObjetosSubastas = buscarBloquesSubastas(soup)
    return listadoObjetosSubastas

def limpiarIdSubasta(idSubasta):
    sinEspacios = limpiarEspacios(idSubasta)
    sinCaracteres = limpiarCaracteresEspeciales(sinEspacios)
    sinSaltos = limpiarSaltosLinea(sinCaracteres)
    #print("Limpio: " + sinSaltos)
    return sinSaltos
    
def limpiarEspacios(cadena):
    sinEspacios = cadena.split(" ")
    #print("Paso 1, espacios: " + sinEspacios[1])
    return sinEspacios[1]

def limpiarCaracteresEspeciales(cadena):
    sinEspacios = cadena.strip()
    reemplazo= sinEspacios.replace("\'","")
    #print("Paso 2, reemplazo " + reemplazo )
    sinCaracteresEspeciales = re.split(r'[`\=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', reemplazo)
    #print("Paso 3, caracteres especiales " + str(sinCaracteresEspeciales))

    if len(sinCaracteresEspeciales) == 1 :
        return sinCaracteresEspeciales[0]
    elif len(sinCaracteresEspeciales) > 4:
        return sinCaracteresEspeciales[2]
    

def limpiarSaltosLinea(cadena):
    sinSaltosLinea = cadena.split('\n')
    #print("Paso 4, Saltos Linea " + sinSaltosLinea[0])
    return sinSaltosLinea[0]

def existeElementoBD(listadoObjetosSubastas, elementoBuscado):   
    print(elementoBuscado)         
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
                'horaFin' : objetoSubasta.horaFin
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


    