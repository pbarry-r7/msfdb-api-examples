# Using Neo4j to Visualize Hosts and Services stored in MSFDB

This is a walk-through guide and python script for doing the following:

* retrieving a list of hosts and services from a RESTFul instance of the MSFDB via JSON RPC
* populating that data into a graph database called neo4j
* view the visual represtation+relationships of that data in neo4j

I used VMs, FWIW, with the core being the following:

* a recent Kali Linux
* an Ubuntu 18.04 VM for my Metasploit Framework and MSFDB instance to exist

Note: commands given below in `this format` are intended to be run on a standard command line (e.g. in a teminal window) unless otherwise specified.

## MSFDB Instance

Ensure you have a VM/system with the following:

1. a recent version of the [Metasploit Framework](https://www.metasploit.com/) installed
1. an intialized MSFDB service
   * use the `msfdb reinit` command if you want to start with a clean slate (*WARNING: THIS WILL DELETE ALL DATA STORED IN YOUR MSFDB!*)
   * make sure to note the 'MSF web service user API token' value (required below)
1. services info stored in the MSFDB
   * I populated my MSFDB services by using the msfconsole `db_nmap -sV --top-ports 25 <IP addr>` command to scan both a Linux instance and a Windows instance of [Metasploitable3](https://blog.rapid7.com/2016/11/15/test-your-might-with-the-shiny-new-metasploitable3/).

Then do the following:

1. check the MSFDB service is running with `msfdb status`
   * if it is NOT running, start it with `msfdb start`
1. Start the JSON RPC service with `msfrpcd -j -p 8081`

At this point, the MSFDB instance is ready.

## Kali Instance

On your Kali instance, you'll need neo4j installed.  If you have BloodHound installed, you're good to go!  If not, install BloodHound with `apt-get install bloodhound`.

Then do the following:

1. install the neo4j driver python module: `pip install neo4j-driver`
1. start neo4j up: `neo4j console` (note that this will stay in the foreground of your terminal window)
1. once the `neo4j console` output says that the remote interface is available, open a web browser window and navigate to localhost:7474
   * verify you see the neo4j UI
1. log into the neo4j DB (default username:password is neo4j:neo4j)
   * if prompted to change the password, go ahead and do so
1. copy over the `visualize-services.py` script to your Kali instance
1. edit the `visualize-services.py` script and set the variable values in the 'MSFDB values' and 'neo4j values' sections to reflect your setup
1. run `./visualize-services.py`
1. in the neo4j web UI, type the following in the top query input: `MATCH p=()-[r:serves]->() RETURN p LIMIT 50`
1. assuming everything went as-expected, you'll see a graph repsentation of hosts and their services
   * hover over the "serves" edges to see the associated port number at the bottom of the window
   * see [this animation](neo4j-ui-example.gif) as an example

NOTE: if you want to reset your data being visualized, you can remove everything in the neo4j DB with the following command when the `neo4j console` is not running: `rm -rf /usr/share/neo4j/data/databases/graph.db/`
   * *WARNING: THIS WILL REMOVE ALL DATA STORED IN YOUR NEO4J DB!*
