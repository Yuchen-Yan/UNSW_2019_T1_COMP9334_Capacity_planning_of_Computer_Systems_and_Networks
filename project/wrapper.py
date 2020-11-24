from project import simulation

dirname = "project_sample_files"

with open(dirname + "/num_tests.txt", 'r') as f:
    num_file = int(f.read().strip())

for i in range(1, 2):
    with open(dirname + "/mode_" + str(i)+ ".txt", 'r') as f:
        mode = f.read().strip()


    if mode == 'trace':
        time_end = None
        with open(dirname + "/arrival_" + str(i)+ ".txt", 'r') as f:
            arrival = []
            value = f.readline().strip()
            while value != '':
                arrival.append(float(value))
                value = f.readline().strip()
        with open(dirname + "/service_" + str(i)+ ".txt", 'r') as f:
            service = []
            value = f.readline().strip()
            while value != '':
                service.append(float(value))
                value = f.readline().strip()
        with open(dirname + "/network_" + str(i)+ ".txt", 'r') as f:
            network = []
            value = f.readline().strip()
            while value != '':
                network.append(float(value))
                value = f.readline().strip()
        with open(dirname + "/para_" + str(i)+ ".txt", 'r') as f:
            fogTimeLimit = float(f.readline().strip())
            fogTimeToCloudTime = float(f.readline().strip())



    elif mode == 'random':
        with open(dirname + "/para_" + str(i)+ ".txt", 'r') as f:
            fogTimeLimit = float(f.readline().strip())
            fogTimeToCloudTime = float(f.readline().strip())
            time_end = f.readline().strip()
        with open(dirname + "/arrival_" + str(i)+ ".txt", 'r') as f:
            arrival = float(f.readline().strip())
        with open(dirname + "/service_" + str(i)+ ".txt", 'r') as f:
            a1 = float(f.readline().strip())
            a2 = float(f.readline().strip())
            B = float(f.readline().strip())
            service = []
            service.append(a1)
            service.append(a2)
            service.append(B)
        with open(dirname + "/network_" + str(i)+ ".txt", 'r') as f:
            v1 = float(f.readline().strip())
            v2 = float(f.readline().strip())
            network = []
            network.append(v1)
            network.append(v2)




    (fog_dep, net_dep, cloud_dep, mrt) = simulation(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end)

'''
    with open(dirname + "/fog_dep_" + str(i)+ ".txt",'w') as f:
        for (,) in fog_dep:
            str = + +'\n'
            f.write(i)
    with open(dirname + "/net_dep_" + str(i)+ ".txt",'w') as f:
        for (,) in net_dep:
            str = + +'\n'
            f.write(i)
    with open(dirname + "/cloud_dep_" + str(i)+ ".txt",'w') as f:
        for (,) in cloud_dep:
            str = + +'\n'
            f.write(i)
    with open(dirname + "/mrt_" + str(i)+ ".txt",'w') as f:
        f.write(mrt)
'''
