import json
import sys

def reserve_relevant_links():
    global event_successful

    # Iterate through the points in the route
    for j in range(0, len(circuit) - 1):
        # Reserve the relevant link in the route
        for link in links:
            if link["points"][0] == circuit[j] and link["points"][1] == circuit[j + 1]:
                if link["reserved"] == False and link["capacity"] >= demand["demand"]:
                    link["reserved"] = True
                    event_successful = True
                    demand["switches"].append(link["points"][1])
                    link["capacity"] = link["capacity"] - demand["demand"]
                    break
                else:
                    event_successful = False
                    break

def release_relevant_links():
    for j in range(0, len(demand["switches"]) - 1):                
        for link in links:
            if link["points"][0] == demand["switches"][0] and link["points"][1] == demand["switches"][1]:
                link["reserved"] = False
                link["capacity"] = link["capacity"] + demand["demand"]
                demand["switches"].remove(demand["switches"][0])
                break
    demand["switches"].remove(demand["switches"][0])

with open(sys.argv[1], "r") as read_file:
    data = json.load(read_file)
    
    endpoints = data["end-points"]
    switches = data["switches"]
    links = data["links"]
    possible_circuits = data["possible-circuits"]
    simulation = data["simulation"]

for link in links:
    link["reserved"] = False

for demand in simulation["demands"]:
    demand["reserved"] = False

number = 1
for i in range(0, simulation["duration"] + 1):
    for demand in simulation["demands"]:        
        if demand["start-time"] == i + 1 and demand["reserved"] == False:
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_start_time = demand["start-time"]     
            event_name = "igény foglalás"
            event_successful = False

            demand["switches"] = []
            demand["switches"].append(demand["end-points"][0])

            for circuit in possible_circuits:    
                # If there's a route between the end points
                if circuit[0] == demand["end-points"][0] and circuit[len(circuit) - 1] == demand["end-points"][1]:
                    reserve_relevant_links()
                    break

            if event_successful:
                demand["reserved"] = True
                print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikeres")
            else:
                demand["reserved"] = False
                print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikertelen")
            
            number = number + 1
        elif demand["end-time"] == i + 1 and demand["reserved"]:
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_end_time = demand["end-time"]     
            event_name = "igény felszabadítás"

            release_relevant_links()

            print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_end_time))

            number = number + 1