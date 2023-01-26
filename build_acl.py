"""Example: Cisco ASA ACL generation using the Aerleon Python API."""

networks = {
    "networks": {
        "WEB_NET": {"values": [{"address": "10.1.1.1/32"}]},
        "DB_NET": {"values": [{"address": "172.16.1.1/32"}]},
        "NTP_NET": {"values": [{"address": "100.1.1.1/30"}]},
        "DNS_NET": {"values": [{"address": "100.1.2.1/30"}]},
        "INFRA_SERVICE_NETS": {"values": ["DNS_NET", "NTP_NET"]},
    },
}


services = {
    "services": {
        "MYSQL": [{"protocol": "tcp", "port": 3306}],
        "HTTPS": [{"protocol": "tcp", "port": 443}],
        "DNS": [{"protocol": "udp", "port": 53}],
        "NTP": [{"protocol": "udp", "port": 123}],
    }
}


cisco_asa_policy = {
    "filename": "cisco_asa_policy",
    "filters": [
        {
            "header": {"targets": {"ciscoasa": "acl-outside"}},
            "terms": [
                {
                    "name": "client-to-web-https",
                    "source-address": "WEB_NET",
                    "destination-port": "HTTPS",
                    "protocol": "tcp",
                    "action": "accept",
                },
                {"name": "deny-all", "action": "deny"},
            ],
        },
        {
            "header": {"targets": {"ciscoasa": "acl-dmz"}},
            "terms": [
                {
                    "name": "web-to-db-mysql",
                    "source-address": "WEB_NET",
                    "destination-address": "DB_NET",
                    "destination-port": "MYSQL",
                    "protocol": "tcp",
                    "action": "accept",
                },
                {
                    "name": "web-to-infra-svcs",
                    "source-address": "WEB_NET",
                    "destination-address": "INFRA_SERVICE_NETS",
                    "destination-port": ["DNS", "NTP"],
                    "protocol": "udp",
                    "action": "accept",
                },
                {"name": "deny-all", "action": "deny"},
            ],
        },
        {
            "header": {"targets": {"ciscoasa": "acl-inside"}},
            "terms": [
                {
                    "name": "db-to-dns",
                    "source-address": "DB_NET",
                    "destination-address": "DNS_NET",
                    "destination-port": "DNS",
                    "protocol": "udp",
                    "action": "accept",
                },
                {
                    "name": "db-to-ntp",
                    "source-address": "DB_NET",
                    "destination-address": "NTP_NET",
                    "destination-port": "NTP",
                    "protocol": "udp",
                    "action": "accept",
                },
                {"name": "deny-all", "action": "deny"},
            ],
        },
    ],
}


# Import re for removing unwanted lines after render
import re  # no qa

# Import the naming module and the api module from the aerleon library.
from aerleon.lib import naming  # isort:skip
from aerleon import api  # isort:skip

# Create an instance of the Naming class
definitions = naming.Naming()

# Use the ParseDefinitionsObject method to parse the "networks" object
definitions.ParseDefinitionsObject(networks, "networks")

# Use the ParseDefinitionsObject method to parse the "services" object
definitions.ParseDefinitionsObject(services, "services")

# Use the Generate method from the api module to generate configurations
# from the "cisco_asa_policy" object, passing in the definitions object
# as an argument
configs = api.Generate([cisco_asa_policy], definitions)

# Render the the ASA configuration from the configs object
acl = configs["cisco_asa_policy.asa"]

# Remove additional blank lines from rendered ACLs
acl = re.sub("\n\n\n", "\n", acl)

if __name__ == "__main__":
    # Print the ACL
    print(acl)  # no qa
