#!/usr/bin/env python

import metodos


#VARIABLES
# urlBD='https://appfire-picada.firebaseio.com/subastas'
urlBD='https://subastasboe-88ea1-default-rtdb.firebaseio.com/'
tablaBDviviendas='/subastasViviendas'
tablaBDvehiculos='/subastasVehiculos'



def busquedaViviendas(urlBD,firebase,tablaBDviviendas) :
    
    print(" ")
    print(" ************************* ")
    print(" ")

    # print(" CARGADA URL HUELVA ")
    #HUELVA-PROVINCIA
    urlSubastaBOEh='https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=21&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
    
    # print(" CARGADA URL SEVILLA ")
    #SEVILLA-SEVILLA
    urlSubastaBOEs='https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=J&campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&dato%5B3%5D=501&campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&campo%5B5%5D=BIEN.CODPOSTAL&dato%5B5%5D=&campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=sevilla&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=41&campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B9%5D=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B11%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D=&campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15%5D%5B1%5D=&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=500&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
    
    # print(" CARGAMOS DATOS DESDE LA BD ")
    #CARGAMOS DATOS DESDE LA BD
    listaDatosBD = metodos.cargarDatosBD(urlBD, firebase, tablaBDviviendas)

    #SACAMOS LAS KEYS Y LOS VALUES DE LA BD
    if metodos.esListaVacia(listaDatosBD) :
        listaValuesBD = []
    else:
        listaKeyBD = metodos.listarKeyBD(listaDatosBD)
        listaValuesBD = metodos.listarValuesBD(listaDatosBD, listaKeyBD)
        numElem = len(listaKeyBD)        
        

    #CARGAMOS NUEVOS DATOS DE LA WEB DE SUBASTAS BOE
    print("INICIO - SCRIPT - VIVIENDAS BOE ")
    print("     TRABAJANDO...") 

    print("     ANALIZANDO...Subastas Viviendas Sevilla") 
    listadoObjetosSubastas = metodos.buscarNovedasdesWebSubasta(urlSubastaBOEs,"Sevilla")
    print("     ANALIZANDO...Subastas Viviendas Huelva") 
    listadoObjetosSubastas.extend(metodos.buscarNovedasdesWebSubasta(urlSubastaBOEh,"Huelva"))

    contadorI=0
    contadorE=0
    contadorO=0
    for objetoSubasta in listadoObjetosSubastas:              
        insertado = metodos.insertarDatosBD(firebase, tablaBDviviendas, objetoSubasta, listaValuesBD, listaDatosBD)
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
    print("FIN - SCRIPT - VIVIENDAS BOE ")
    



def actualizarFinalizadas(urlBD,firebase,tablaBDviviendas,tablaBDvehiculos) : 
    print(" ")
    print(" ************************* ")
    print(" ")

    print("INICIO - SCRIPT - ACTUALIZAR SUBASTAS FINALIZADAS BOE ")
    fechaHoy = metodos.fechaActual()
    print("     Filtrar elementos con fecha anterior a: " + metodos.fechaToString(fechaHoy))
    print(" ")
    listaKeyBorradoBD = []
    
    print("     BUSCANDO...  Subastas viviendas concluidas")
    listaKeyBorradoBD = metodos.eliminarDatosBD(urlBD, firebase, tablaBDviviendas)      
    if not metodos.esListaVacia(listaKeyBorradoBD):   
        for keyObject in listaKeyBorradoBD: 
            print("     * Vivienda eliminada con ID:" + str(keyObject)) 
            metodos.borrarObjetoBD(firebase,tablaBDviviendas,keyObject) 
    else:
        print("     * Aun no existen subastas de viviendas concluidas")


    print(" ")
    print("     BUSCANDO...  Subastas vehiculos concluidas")
    listaKeyBorradoBD = metodos.eliminarDatosBD(urlBD, firebase, tablaBDvehiculos)
    if not metodos.esListaVacia(listaKeyBorradoBD): 
        for keyObject in listaKeyBorradoBD: 
            print("     * Vehiculo eliminado con ID:" + str(keyObject))
            metodos.borrarObjetoBD(firebase,tablaBDvehiculos,keyObject)     
    else:
        print("     * Aun no existen subastas de vehiculos concluidas")
    print(" ")
    print("FIN - SCRIPT - FINALIZAR SUBASTAS BOE ")
    print(" ")
    print(" ")
    



def busquedaCoches(urlBD,firebase,tablaBDvehiculos) :
    #VEHICULOS

    print(" ")
    print(" ************************* ")
    print(" ")

    # print(" CARGADA URL VEHICULOS ")
    urlSubastasBOEvehiculos='https://subastas.boe.es/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=V&dato%5B3%5D=9101&campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&campo%5B5%5D=BIEN.CODPOSTAL&dato%5B5%5D=&campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=&campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B9%5D=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B11%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D=&campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15%5D%5B1%5D=&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=500&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
    
    
    print("INICIO - SCRIPT - VEHICULOS BOE ")
    listaDatosBDvehiculos = metodos.cargarDatosBD(urlBD, firebase, tablaBDvehiculos)
    #SACAMOS LAS KEYS Y LOS VALUES DE LA BD
    print("     TRABAJANDO...") 
    
    if metodos.esListaVacia(listaDatosBDvehiculos) :
        listaValuesBDoches = []
    else:
        listaKeyBDCoches = metodos.listarKeyBD(listaDatosBDvehiculos)
        listaValuesBDoches = metodos.listarValuesBD(listaDatosBDvehiculos, listaKeyBDCoches)
        numElem = len(listaKeyBDCoches)  
             
    print("     ANALIZANDO... Subastas Vehiculos España")
    listadoObjetosSubastasCoches = metodos.buscarNovedasdesWebSubasta(urlSubastasBOEvehiculos,"España")

    # # print("Listado objetos subastas")
    # # print(len(listadoObjetosSubastasCoches))
    contadorI=0
    contadorE=0
    contadorO=0
    for objetoSubasta in listadoObjetosSubastasCoches:             
        # # print(objetoSubasta)
        # # print("++++++++++ INSERTAR COCHE") 
        insertado = metodos.insertarDatosCochesBD(firebase, tablaBDvehiculos, objetoSubasta, listaValuesBDoches, listaDatosBDvehiculos)
        if insertado == "ERROR" :
            contadorE = contadorE + 1
            # # print("Error en el proceso en el insert.")        
        elif insertado == "OMITIDO" :
            contadorO = contadorO + 1
            # # print("Elemento ya existente, se omite.")        
        else :
            contadorI = contadorI + 1
            # # print("Elemento " + str(insertado) + " insertado en BD.")  

    metodos.mostrarEstadisticas(contadorI,contadorO,contadorE)
    print("FIN - SCRIPT - VEHICULOS BOE ")
    

#CONECTAMOS A LA BD
firebase = metodos.conexionBD(urlBD) 
print(" ")

##INFORMACION RELEVANTE, LAS PESTAÑAS DENTRO DE LA INFORMACION DEL VEHICULO VIENEN INFORMADAS POR LA VARIABLE VER;
##SIENDO VER=1 INFORMACION GENERAL Y VER=3 BIENES
#https://subastas.boe.es/detalleSubasta.php?idSub=SUB-JA-2021-176800&ver=3

busquedaViviendas(urlBD,firebase,tablaBDviviendas)
busquedaCoches(urlBD, firebase, tablaBDvehiculos)
actualizarFinalizadas(urlBD,firebase,tablaBDviviendas,tablaBDvehiculos)

# try:
#     d1 = metodos.fechaActual()
#     tipode = type(d1)
#     print(tipode)
#     print(d1)
#     metodos.os.system("pause")
#     d2 = metodos.fechaFromStr('27/05/2021')
#     d3 = metodos.fechaFromStr('10/06/2021')
#     tipode = type(d3)
#     print(tipode)
#     print(d2)
#     print(d3)
#     dd1 = metodos.fechaDatetimeToFechaDate(d1)
#     dd2 = metodos.fechaDatetimeToFechaDate(d2)
#     dd3 = metodos.fechaDatetimeToFechaDate(d3)
#     print(str(d2) + '<' + str(d1))
#     if d2 < d1 :
#         print(str(d2) + " es menor.")
#     else: 
#         print(str(d2) + " es Mayor.")

#     print(str(d3) + '<' + str(d1))
#     if d1 < d3 :
#         print(str(d3) + " es menor.")
#     else: 
#         print(str(d2) + " es Mayor.")

#     print(str(dd2) + '<' + str(dd1))
#     print(str(dd3) + '<' + str(dd1))


#     metodos.os.system("pause")
# except:
#     print("Error en el main")
#     metodos.os.system("pause")

metodos.os.system("pause")
