import paramiko
import os
import sys
import getpass
import time
from paramiko.client import SSHClient
from Analisys import services_analisys, service_status, users_analisys
from Scann_ports import scann_ports
from colorama import Fore
from tqdm import tqdm
from API_Firebase import agregar_registros_lista, agregar_registros_lista_unique, agregar_registros_diccionarios,agregar_registros_diccionario

list_users = []
services_enabled = ""
services_disabled = ""
document_dhcp_confi = ""
document_dns_confi = ""
status_dhcpd = {}
status_dns = {}
scan_ports = {}

def get_scan_ports():
    return scan_ports

def set_scan_ports(data):
    global scan_ports
    scan_ports = data

def get_list_users():
    return list_users

def set_list_users(data):
    global list_users
    list_users = data

def get_status_dhcpd():
    return status_dhcpd

def set_status_dhcpd(index, data):
    global status_dhcpd
    status_dhcpd[index] = data

def get_status_dns():
    return status_dns

def set_status_dns(index, data):
    global status_dns
    status_dns[index] = data

def get_document_dhcp_confi():
    return document_dhcp_confi

def set_document_dhcp_confi(data):
    global document_dhcp_confi
    document_dhcp_confi = data

def get_document_dns_confi():
    return document_dns_confi

def set_document_dns_confi(data):
    global document_dns_confi
    document_dns_confi = data

def get_services_enabled():
    return services_enabled

def set_services_enabled(data):
    global services_enabled
    services_enabled = data

def get_services_disabled():
    return services_disabled

def set_services_disabled(data):
    global services_disabled
    services_disabled = data

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def conection(host, user, psswd, portssh):
    #Create instan SSH
    conection = paramiko.SSHClient()
    #Configuration paramiko policy
    conection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #Autentucation conect 
    conection.connect(host, username=user,password=psswd, port=portssh, timeout=10)
    print(Fore.GREEN + "[+] Conexión exitosa" + Fore.WHITE)
    return conection

def query_device(conection, command):
    stdin, stdout, stderr = conection.exec_command(command)
    return stdout.read().decode("utf-8")

def constrant():
    while True:
        clear()
        ip = input("[?] Ingrese la ip/hostname del servidor remoto: ")
        usr = input("[?] Ingrese el usuario: ")
        contraseña = getpass.getpass("[!] Contraseña: ")
        port = input("[?] Puerto de comunicación: ")
        try:
            conn = conection(ip, usr, contraseña, port)
            break
        except:
            print(Fore.RED + '[X] Error de conexión, compruebe las credenciales de autenticación')
            continuar = str(input(Fore.WHITE + "[?] Quiere seguir intentando (yes/no): "))
            while True:
                if continuar.lower() == "yes" or continuar.lower() == "y":
                    break
                elif continuar.lower() == "no" or continuar.lower() == "n":
                    sys.exit()
                else:
                    continuar = input("[X] Teclee una opción correcta (yes/no): ")
    loop = tqdm(total=21, position=0, leave=False)
    loop.set_description("[+] Obteniendo registros de usuarios".format(1))
    loop.update(1)
    users = query_device(conn, "cat /etc/passwd | grep bin/bash")
    loop.set_description("[+] Obteniendo información de usuarios".format(2))
    loop.update(1)
    services_enabled_local = query_device(conn, "systemctl list-unit-files --type service --all | grep enabled")
    loop.set_description("[+] Obteniendo servicios habilitados".format(3))
    loop.update(1)
    services_disabled_local = query_device(conn, "systemctl list-unit-files --type service --all | grep disabled")
    loop.set_description("[+] Obteniendo servicios deshabilitados".format(4))
    loop.update(1)
    status_dhcp_local = query_device(conn, "systemctl status dhcpd | grep Active")
    loop.set_description("[+] Obteniendo archivos de configuración".format(5))
    loop.update(1)
    status_dns_local = query_device(conn, "systemctl status named | grep Active")
    loop.set_description("[+] Obteniendo archivos de configuración".format(6))
    loop.update(1)
    document_dhcp_confi = query_device(conn, "cat /etc/dhcp/dhcpd.conf")
    loop.set_description("[+] Obteniendo archivos de configuracións".format(7))
    loop.update(1)
    document_dns_confi = query_device(conn, "cat /etc/named.conf")
    loop.set_description("[+] Obteniendo archivos de configuración".format(8))
    loop.update(1)
    data_enabled = services_analisys(services_enabled_local)
    loop.set_description("[+] Analisando información".format(9))
    loop.update(1)
    data_disaled = services_analisys(services_disabled_local)
    loop.set_description("[+] Analisando información".format(10))
    loop.update(1)
    set_list_users (users_analisys(users))
    loop.set_description("[+] Obteniendo información".format(11))
    loop.update(1)
    set_services_enabled(data_enabled)
    loop.set_description("[+] Obteniendo información".format(12))
    loop.update(1)
    set_services_disabled(data_disaled)
    loop.set_description("[+] Obteniendo información".format(13))
    loop.update(1)
    set_status_dhcpd("status",status_dhcp_local)
    loop.set_description("[+] Obteniendo información".format(14))
    loop.update(1)
    set_status_dns("status", status_dns_local)
    loop.set_description("[+] Obteniendo información".format(15))
    loop.update(1)
    set_status_dhcpd("color",service_status(status_dhcp_local))
    loop.set_description("[+] Obteniendo información".format(16))
    loop.update(1)
    set_status_dns("color",service_status(status_dns_local))
    loop.set_description("[+] Obteniendo información".format(17))
    loop.update(1)
    set_document_dhcp_confi(document_dhcp_confi)
    loop.set_description("[+] Obteniendo información".format(18))
    loop.update(1)
    set_document_dns_confi(document_dns_confi)
    loop.set_description("[+] Ecaneando puertos".format(19))
    loop.update(1)
    set_scan_ports(scann_ports(ip))
    loop.update(1)
    loop.set_description("[+] Iniciando terminal line interface".format(19))
    time.sleep(3)
    loop.close()


def upload_user_list():
    try:
        agregar_registros_lista("Lista de usuarios servidores", list_users)
        return "[b green][+] List de usuarios cargada correctamente"
    except:
        return"[b red][X] Error al subir lista de usuarios"

def upload_services_enabled():
    try:
        agregar_registros_diccionarios("Servicios","Lista de servicios habilitados", services_enabled)
        return "[b green][+] Servicios enables subidos correctamente"
    except:
        return"[b red][X] Error al subir lista de servicios enabled"

def upload_services_disabled():
    try:
        agregar_registros_diccionarios("Servicios", "Lista de servicios habilitados", services_disabled)
        return "[b green][+] Servicios disabled subidos correctamente"
    except:
        return"[b red][X] Error al subir lista de servicios disabled"

def upload_document_dhcp():
    try:
        agregar_registros_lista_unique("Document Confi", "Documents DHCP", str(document_dhcp_confi))
        return "[b green][+] Documento de configuración DHCP subido correctamente"
    except:
        return"[b red][X] Error al subir documento de configuración DHCP"

def upload_document_dns():
    try:
        agregar_registros_lista_unique("Document Confi", "Documents DNS", str(document_dhcp_confi))
        return "[b green][+] Documento de configuración DNS subido correctamente"
    except:
        return"[b red][X] Error al subir documento de configuración DNS"

def upload_scann_ports():
    try:
        agregar_registros_diccionario("Escaeno de puertos", scan_ports)
        return "[b green][+] Escaneo de puertos subido correctamente"
    except:
        return"[b red][X] Error al subir el escaneo de puertos"
