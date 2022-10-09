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
    
    # DEBUG
    print("i: " + str(i))
    
    for demand in simulation["demands"]:
        
        # DEBUG
        print("-Current demand: " + str(demand))
        
        if demand["start-time"] == i + 1:
            
            # DEBUG
            print("--Starting a demand reserving")
            
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_start_time = demand["start-time"]     
            event_name = "igény foglalás"
            event_successful = False

            demand["switches"] = []
            demand["switches"].append(demand["end-points"][0])
            
            # DEBUG
            print("--Demand switches: " + str(demand["switches"]))

            for circuit in possible_circuits:
                
                # DEBUG
                print("---Current circuit: " + str(circuit))
                
                # If there's a route between the end points
                if circuit[0] == demand["end-points"][0] and circuit[len(circuit) - 1] == demand["end-points"][1]:
                    
                    # DEBUG
                    print("----Matching circuit")
                    
                    # Iterate through the points in the route
                    for j in range(0, len(circuit) - 1):
                        
                        # DEBUG
                        print("----j: " + str(j))
                        
                        # Reserve the relevant link in the route
                        for link in links:
                            
                            # DEBUG
                            print("-----Current link: " + str(link))
                            
                            if link["points"][0] == circuit[j] and link["points"][1] == circuit[j + 1]:
                                
                                # DEBUG
                                print("------Matching link")
                                
                                if link["reserved"] == False and link["capacity"] >= demand["demand"]:
                                    
                                    # DEBUG
                                    print("------Reserve link")
                                    
                                    link["reserved"] = True
                                    event_successful = True
                                    demand["switches"].append(link["points"][1])
                                    link["capacity"] = link["capacity"] - demand["demand"]
                                    
                                    # DEBUG
                                    print("------Demand switches: " + str(demand["switches"]))
                                    
                                    break
                                else:
                                    
                                    # DEBUG
                                    print("-------Refuse reserving link")
                                    
                                    event_successful = False
                                    break
                    break
            if event_successful:
                print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikeres")
            else:
                print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time) + " - sikertelen")
            number = number + 1
        elif demand["end-time"] == i + 1:
            
            # DEBUG
            print("--Starting a demand releasing")
            
            event_number = number
            event_endpoints = demand["end-points"][0] + "<->" + demand["end-points"][1]
            event_end_time = demand["end-time"]     
            event_name = "igény felszabadítás"
                
            # DEBUG
            print("--Demand switches: " + str(demand["switches"]))
            
            for j in range(0, len(demand["switches"]) - 1):
                
                # DEBUG
                print("---j: " + str(j))
                
                for link in links:
                    
                    # DEBUG
                    print("----Current link: " + str(link))
                    
                    if link["points"][0] == demand["switches"][0] and link["points"][1] == demand["switches"][1]:
                        
                        # DEBUG
                        print("-----Release link")
                        
                        link["reserved"] = False
                        link["capacity"] = link["capacity"] + demand["demand"]
                        demand["switches"].remove(demand["switches"][0])
                        
                        # DEBUG
                        print("-----Demand switches: " + str(demand["switches"]))
                        
                        break
            demand["switches"].remove(demand["switches"][0])

            print(str(event_number) + ". " + event_name + ": " + event_endpoints + " st:" + str(event_start_time))
            number = number + 1

# DEBUG
print("\nDemands:")
for demand in simulation["demands"]:
    print(demand)

print("\nLinks:")
for link in links:
    print(link)