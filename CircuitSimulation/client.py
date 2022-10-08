import json

with open("e:\ELTE\V. Felev\Telekommunikacios halozatok\Beadandok\TelCom-Projects\CircuitSimulation\cs1.json", "r") as read_file:
    data = json.load(read_file)
    
    endpoints = data["end-points"]
    switches = data["switches"]
    links = data["links"]
    possible_circuits = data["possible-circuits"]
    simulation = data["simulation"]

for link in links:
    link["reserved"] = False

number = 1
for i in range(1, simulation["duration"] + 1):
    for demand in simulation["demands"]:
        event_number = number

        event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
        
        event_start_time = i
        
        event_name = ""
        event_successful = False
        if demand["start-time"] == i:
            event_name = "igény foglalás"
            
            for circuit in possible_circuits:
                # If there's a route between the end points
                if circuit[0] == demand["end-points"][0] and circuit[len(circuit) - 1] == demand["end-points"][1]:
                    # Iterate through the points in the route
                    for i in range(0, len(circuit) - 1):
                        # Reserve the relevant link in the route
                        for link in links:
                            if link["points"][0] == circuit[i] and link["points"][1] == circuit[i + 1]:
                                if link["reserved"] == False:
                                    link["reserved"] = True
                                    event_successful = True
                                else:
                                    event_successful = False

        elif demand["end-time"] == i:
            event_name = "igény felszabadítás"

        print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - " + "sikeres" if event_successful else "sikertelen")
    number = number + 1