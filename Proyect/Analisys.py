import re 

def services_analisys(services):
    diccionario_services = {}
    lista_servicios = []
    contador = 0
    services = re.split('\s', services)
    for data in services:
        if data != '':
            contador += 1
            if contador == 1:
                diccionario_services["service"] = data
            elif contador == 2:
                diccionario_services["status"] = data
            elif contador == 3:
                diccionario_services["Vendor"] = data
                lista_servicios.append(diccionario_services.copy())
                contador = 0
    return lista_servicios