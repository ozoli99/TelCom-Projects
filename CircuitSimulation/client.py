import json

with open("e:\ELTE\V. Felev\Telekommunikacios halozatok\Beadandok\TelCom-Projects\CircuitSimulation\cs1.json", "r") as read_file:
    data = json.load(read_file)
    
    endpoints = data["end-points"]
    switches = data["switches"]
    links = data["links"]
    possible_circuits = data["possible-circuits"]
    simulation = data["simulation"]
