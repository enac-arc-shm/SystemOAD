import paramiko
from paramiko.client import SSHClient

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
    return stdout.read().decode()

if __name__ == '__main__':
    #Create conecction ssh. - Host - User - Password
    conn = conection("localhost", "enac-arc-shm", "P0wd3r!", "22")
    #Exctrac information
    users = query_device(conn, "cat /etc/passwd | grep bin/bash")
    services = query_device(conn, "systemctl list-unit-files --type service --all")