import paramiko
import re
from paramiko.client import SSHClient
from Analisys import services_analisys, service_status

services_enabled = ""
services_disabled = ""
status_dhcpd = {}

def get_status_dhcpd():
    return status_dhcpd

def set_status_dhcpd(index, data):
    global status_dhcpd
    status_dhcpd[index] = data

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

def conection(host, user, psswd, portssh):
    #Create instan SSH
    conection = paramiko.SSHClient()
    #Configuration paramiko policy
    conection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #Autentucation conect 
    conection.connect(host, username=user,password=psswd, port=portssh, timeout=10)
    return conection

def query_device(conection, command):
    stdin, stdout, stderr = conection.exec_command(command)
    return stdout.read().decode("utf-8")


def constrant():
    #Create conecction ssh. - Host - User - Password
    #conn = conection("localhost", "enac-arc-shm", "P0wd3r!", "22")      Local
    conn = conection("localhost", "root", "ASAGE-x*", "22")    
    #Exctrac information
    users = query_device(conn, "cat /etc/passwd | grep bin/bash")
    services_enabled_local = query_device(conn, "systemctl list-unit-files --type service --all | grep enabled")
    services_disabled_local = query_device(conn, "systemctl list-unit-files --type service --all | grep disabled")
    status_dhcp_local = query_device(conn, "systemctl status dhcpd | grep Active")
    data_enabled = services_analisys(services_enabled_local)
    data_disaled = services_analisys(services_disabled_local)
    set_services_enabled(data_enabled)
    set_services_disabled(data_disaled)
    set_status_dhcpd("status",status_dhcp_local)
    set_status_dhcpd("color",service_status(status_dhcp_local))

if __name__ == "__main__":
    constrant()
    print(get_status_dhcpd())