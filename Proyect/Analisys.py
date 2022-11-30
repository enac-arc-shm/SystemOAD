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

def service_status(status):
    if re.search(" active ", status) != None:
        return "green"
    else:
        return "red"

def users_analisys(data):
    list_users = []
    data = data.split("\n")
    for user in data:
        user = user.split(":")
        if len(user) > 1:
            list_users.append(user.copy())
    return list_users

#if __name__ == "__main__":
#    print(service_status("Active: active (running) since Mon 2022-11-28 12:09:10 CST; 59s ago"))