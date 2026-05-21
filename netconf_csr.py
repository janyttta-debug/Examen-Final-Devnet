from ncclient import manager

router = {
    "host": "192.168.56.101",
    "port": 830,
    "username": "cisco",
    "password": "cisco",
    "hostkey_verify": False
}

netconf_config = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">

<hostname>ALEJANDRA_QUINTANA</hostname>

<interface>
<Loopback>
<name>11</name>
<ip>
<address>
<primary>
<address>11.11.11.11</address>
<mask>255.255.255.255</mask>
</primary>
</address>
</ip>
</Loopback>
</interface>

</native>
</config>
"""

with manager.connect(**router) as m:
    respuesta = m.edit_config(
        target="running",
        config=netconf_config
    )

    print("Configuración aplicada correctamente")
    print(respuesta)
