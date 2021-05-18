#!/usr/bin/env python

import metodos

print("INICIO - SCRIPT - VIVIENDAS BOE - SEVILLA") 

#VARIABLES
# urlBD='https://appfire-picada.firebaseio.com/subastas'
urlBD='https://subastasboe-88ea1-default-rtdb.firebaseio.com/'
#HUELVA-PROVINCIA
#urlSubastaBOE='https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=21&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
#SEVILLA-SEVILLA
urlSubastaBOE='https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=J&campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&dato%5B3%5D=501&campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&campo%5B5%5D=BIEN.CODPOSTAL&dato%5B5%5D=&campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=sevilla&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=41&campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B9%5D=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B11%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D=&campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15%5D%5B1%5D=&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=500&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
tablaBD='/subastasViviendas'

#CONECTAMOS A LA BD
firebase = metodos.conexionBD(urlBD) 

#CARGAMOS DATOS DESDE LA BD
listaDatosBD = metodos.cargarDatosBD(urlBD, firebase, tablaBD)

#SACAMOS LAS KEYS Y LOS VALUES DE LA BD
if metodos.esListaVacia(listaDatosBD) :
    listaValuesBD = []
else:
    listaKeyBD = metodos.listarKeyBD(listaDatosBD)
    listaValuesBD = metodos.listarValuesBD(listaDatosBD, listaKeyBD)
    numElem = len(listaKeyBD)
    

#CARGAMOS NUEVOS DATOS DE LA WEB DE SUBASTAS BOE
listadoObjetosSubastas = metodos.buscarNovedasdesWebSubasta(urlSubastaBOE)

contadorI=0
contadorE=0
contadorO=0
for objetoSubasta in listadoObjetosSubastas:              
    insertado = metodos.insertarDatosBD(firebase, tablaBD, objetoSubasta, listaValuesBD, listaDatosBD)
    if insertado == "ERROR" :
        contadorE = contadorE + 1
        #print("Error en el proceso en el insert.")        
    elif insertado == "OMITIDO" :
        contadorO = contadorO + 1
        #print("Elemento ya existente, se omite.")        
    else :
        contadorI = contadorI + 1
        #print("Elemento " + str(insertado) + " insertado en BD.")  

metodos.mostrarEstadisticas(contadorI,contadorO,contadorE)
print("FIN - SCRIPT - VIVIENDAS BOE - SEVILLA")

metodos.os.system("pause")