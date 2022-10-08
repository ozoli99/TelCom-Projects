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
for i in range(0, simulation["duration"] + 1):
    for demand in simulation["demands"]:
        if demand["start-time"] == i + 1:
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_start_time = demand["start-time"]     
            event_name = "igény foglalás"
            event_successful = False

            demand["switches"] = []
            
            for circuit in possible_circuits:
                # If there's a route between the end points
                if circuit[0] == demand["end-points"][0] and circuit[len(circuit) - 1] == demand["end-points"][1]:
                    # Iterate through the points in the route
                    for j in range(0, len(circuit) - 1):
                        # Reserve the relevant link in the route
                        for link in links:
                            if link["points"][0] == circuit[j] and link["points"][1] == circuit[j + 1]:
                                if link["reserved"] == False and link["capacity"] >= demand["demand"]:
                                    link["reserved"] = True
                                    event_successful = True
                                    demand["switches"].append(link["points"][1])
                                    break
                                else:
                                    event_successful = False
                                    break
                if event_successful:
                    print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikeres")
                else:
                    print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikertelen")
            number = number + 1
        elif demand["end-time"] == i + 1:
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_end_time = demand["end-time"]     
            event_name = "igény felszabadítás"

            print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time))
            number = number + 1