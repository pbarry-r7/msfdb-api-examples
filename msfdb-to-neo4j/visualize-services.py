#!/usr/bin/env python
#
# Retrieve a list of services from an MSFDB service API via JSON RPC
# and add them to a neo4j database.
#
# THIS SCRIPT IS NOT FANCY, PROBABLY BUGGY, AND ONLY SERVES AS AN EXAMPLE!

import urllib3
import json
from neo4j import GraphDatabase

# MSFDB values
msfdb_system = "<IP or name>"
msfdb_rpc_port = 8081
msfdb_api_token = "<MSF web service user API token>"

# neo4j values
neo4j_system = "localhost"
neo4j_port = 7687
neo4j_auth_user = "<user>"
neo4j_auth_pass = "<password>"

# Setup the connection to the neo4j DB...
uri = "bolt://" + neo4j_system + ":" + str(neo4j_port)
driver = GraphDatabase.driver(uri, auth=(neo4j_auth_user, neo4j_auth_pass))

# Setup the POST request for services in the MSFDB,...
post_data = {"jsonrpc": "2.0", "method": "db.services", "id": 1, "params": {}}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
c = urllib3.HTTPSConnectionPool(msfdb_system, msfdb_rpc_port, cert_reqs="CERT_NONE")

# Retrieve the list of services...
res = c.request('POST', '/api/v1/json-rpc', headers={'Content-Type':'application/json', 'Authorization':'Bearer ' + msfdb_api_token}, body=json.dumps(post_data))
if res.status != 200:
	raise SystemExit("HTTP status code " + str(res.status) + ": " + str(res.data))

# Parse each service name, host, and port, then add them to the neo4J DB...
res_json = json.loads(res.data)
for s in res_json["result"]["services"]:
	cypher_cmd = "merge (c:computer {name:\"" + str(s["host"]) + "\"}) merge (s:service {name: \"" + str(s["name"]) + "\"}) merge (c)-[:serves {port: \"" + str(s["port"]) + "\"}]->(s)"
	driver.session().run(cypher_cmd)
