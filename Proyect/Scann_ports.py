import nmap

def scann_ports(ip):
    info_protocols = {}
    # initialize the port scanner
    nmScan = nmap.PortScanner()
    # scan localhost for ports in range 21-443
    nmScan.scan(ip, '21-443')
    # run a loop to print all the found result about the ports
    for host in nmScan.all_hosts():
        info_protocols["Host"] = f"{host} - {nmScan[host].hostname()}"
        info_protocols["State"] = nmScan[host].state()
        for proto in nmScan[host].all_protocols():
            info_protocols["Protocol"] = proto
            lport = nmScan[host][proto].keys()
            info_ports = {}
            for port in lport:
                info_ports[str(port)] = nmScan[host][proto][port]['state']
            info_protocols["Ports"] = info_ports
    return info_protocols

if __name__ == "__main__":
    print(scann_ports("192.168.12.1"))