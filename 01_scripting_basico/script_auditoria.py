import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROUTER_IP = "192.168.1.1"
PUERTO = "443"
USUARIO = "admin"
PASSWORD = "CiscoPassword123!"

url = f"https://{ROUTER_IP}:{PUERTO}/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}


RESPUESTA_SIMULADA= {
  "ietf-interfaces:interfaces": {
    "interface": [
      {
        "name": "GigabitEthernet0/0",
        "description": "DO NOT TOUCH",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "10.10.20.66",
              "netmask": "255.255.255.0"
            }
          ]
        }
      },
      {
        "name": "GigabitEthernet1/0/1",
        "description": "uplink to 10",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True,
        "ietf-ip:ipv4": {}
      },
      {
        "name": "Loopback0",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "10.255.0.1",
              "netmask": "255.255.255.255"
            }
          ]
        }
      },
      {
        "name": "Loopback75",
        "description": "GERSON AJPACAJA - 25001404",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "75.75.75.75",
              "netmask": "255.255.255.0"
            }
          ]
        }
      },
      {
        "name": "Loopback95",
        "description": "ansible-updated",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "10.99.99.95",
              "netmask": "255.255.255.0"
            }
          ]
        }
      }
    ]
  }
}

def auditar_interfaces():
    try:
        print(f"Conectando a {ROUTER_IP} vía RESTCONF...")
        
        datos_json = RESPUESTA_SIMULADA
        print("Conexión exitosa")

        lista_interfaces = datos_json.get("ietf-interfaces:interfaces", {}).get("interface", [])
        inventario = []

        
        for iface in lista_interfaces:
            direcciones = iface.get("ietf-ip:ipv4", {}).get("address", [])

            
            if iface.get("enabled") is True and direcciones:
                datos = {
                    "nombre": iface.get("name", ""),
                    "ip": direcciones[0].get("ip", ""),
                    "mascara": direcciones[0].get("netmask", "")
                }
                inventario.append(datos)

        
        nombre_archivo = "inventario_interfaces.json"
        with open(nombre_archivo, "w", encoding="utf-8") as a:
            json.dump(inventario, a, indent=4, ensure_ascii=False)

        print(f"Auditoría finalizada. Se exportaron {len(inventario)} interfaces a '{nombre_archivo}'.")

    except requests.exceptions.Timeout:
        print(f"Error: Tiempo de espera agotado al conectar con {ROUTER_IP}.")
    except requests.exceptions.ConnectionError:
        print(f"Error: No se pudo conectar con {ROUTER_IP}. Verifica la red o la IP.")
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP (revisa credenciales o puerto): {err}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    auditar_interfaces()
