


def simulation(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end):
    if mode == 'trace':
        ##########################################################
        #compute the service tiem of fog and also service time of cloud
        ##########################################################
        service_fog = []
        service_cloud = []
        for i in service:
            if i >= fogTimeLimit:
                service_fog.append(2)
                service_cloud.append(round(fogTimeToCloudTime * (i-fogTimeLimit), 4))
            else:
                service_fog.append(round(i))
                service_cloud.append(0)

        ##########################################################
        #Accounting parameters use to calculate the mrt
        ##########################################################
        response_time_cumulative = 0
        num_customer_served = 0



        ##########################################################
        #events: there are five events,
        ##########################################################
        #1. next arrival the fog, and service time in fog
        #2. next depart the fog, arrival time of next dep fog
        #3. next arrival the network, service time of the network latency
        #4. next depart the network, arrival service time of the cloud
        #5. next depart the cloud, arrival time of next dep cloud
        n_arrival_fog = arrival[0]
        service_time_n_arrival_fog = service_fog[0]
        #point to the next job
        job_counter = 0
        num_of_jobs = len(arrival)


        n_departure_fog = float('inf')
        n_arrival_net = float('inf')
        n_departure_net = float('inf')
        n_departure_cloud = float('inf')


        ##########################################################
        #to store information of departrue
        ##########################################################
        departure_fog_info = []
        departure_net_info = []
        departure_cloud_info = []


        ##########################################################
        #to store the jobs inside each list
        ##########################################################
        job_list_fog = []
        job_list_net = []
        job_list_cloud = []


        ##########################################################
        #Initialize the master clock time
        ##########################################################
        last_master_clock = 0
        master_clock = 0




        while 1:
##########################################################
#find out the next event type
##########################################################
            if n_arrival_fog == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_arrival_fog
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 1
            elif n_departure_fog == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_departure_fog
                next_event_type = 2
            elif n_arrival_net == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_arrival_net
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 3
            elif n_departure_net == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_departure_net
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 4
            else:
                next_event_time = n_departure_cloud
                next_event_type = 5

            last_master_clock = master_clock
            master_clock = next_event_time
            #time difference
            difference = master_clock - last_master_clock

            print(master_clock)
            print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)

#arival the fog
            if next_event_type == 1:
                #print(1)
                #insert new job into job_list_fog and update the information of the fog job list
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_fog.append((job_counter, arrival[job_counter], service_fog[job_counter]))
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]

                #print(job_list_fog)
                #check wether have next job, and update the n_arrival_fog and all the times
                if job_counter < num_of_jobs-1:
                    job_counter += 1
                    n_arrival_fog = arrival[job_counter]
                    #print(master_clock, job_counter, n_arrival_fog)
                else:
                    n_arrival_fog = float('inf')
                    break

                #update the n_departure_fog and n_arrival_net
                job_list_fog_service = [i[2] for i in job_list_fog]
                min_value = min(job_list_fog_service)
                min_index = job_list_fog_service.index(min_value)
                counter1 = job_list_fog[min_index][0]
                if network[counter1] != 0:
                    n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                    n_departure_fog = float('inf')
                else:
                    n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                    n_arrival_net = float('inf')

                #update the departure network latency and departure cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)


#departure from fog
            elif next_event_type == 2:
                #print(2)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]

                #update the departrue_fog_info
                min_net = min([i[2] for i in job_list_fog])
                for i in range(len(job_list_fog)):
                    if job_list_net[i][2] == min_net:
                        departure_fog_item = job_list_fog.pop(i)
                        departure_fog_info.append((departure_fog_item[1], master_clock))



                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]
                #update the events times
                #n_arrival_fog unchange
                #update the n_departure_fog and n_arrival_fog
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')


                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)


                response_time_cumulative += master_clock - departure_fog_item[1]
                num_customer_served += 1


#from fog to network
            elif next_event_type == 3:
                #print(3)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                #uout of job_list_fog
                for i in range(len(job_list_fog)):
                    if job_list_fog[i][2] == 0:
                        departure_fog_item = job_list_fog.pop(i)
                        departure_fog_info.append((departure_fog_item[1], master_clock))


                #into the job_list_net
                job_counter3 = departure_fog_item[0]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_net.append((job_counter3, arrival[job_counter3], network[job_counter3]))

                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]


                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')


                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)





#from network to cloud
            elif next_event_type == 4:
                #print(4)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]

                min_net = min([i[2] for i in job_list_net])
                for i in range(len(job_list_net)):
                    if job_list_net[i][2] == min_net:
                        departure_net_item = job_list_net.pop(i)
                        departure_net_info.append((departure_net_item[1], master_clock))

                job_counter4 = departure_net_item[0]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]
                job_list_cloud.append((job_counter4, arrival[job_counter4], service_cloud[job_counter4]))


                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')



                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)





#departure from cloud
            elif next_event_type == 5:
                #print(5)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]


                min_cloud = min([i[2] for i in job_list_cloud])
                for i in range(len(job_list_cloud)):
                    if job_list_cloud[i][2] == min_cloud:
                        departure_cloud_item = job_list_cloud.pop(i)
                        departure_cloud_info.append((departure_cloud_item[1], master_clock))

                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')



                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)



                response_time_cumulative += master_clock
                num_customer_served += 1

                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)



            if num_customer_served == num_of_jobs:
                break


##########################################################
#the random mode
##########################################################
    elif mode == 'random':
        ##########################################################
        #compute the service tiem of fog and also service time of cloud
        ##########################################################
        service_fog = []
        service_cloud = []
        for i in service:
            if i >= fogTimeLimit:
                service_fog.append(2)
                service_cloud.append(round(fogTimeToCloudTime * (i-fogTimeLimit), 4))
            else:
                service_fog.append(round(i))
                service_cloud.append(0)

        ##########################################################
        #Accounting parameters use to calculate the mrt
        ##########################################################
        response_time_cumulative = 0
        num_customer_served = 0



        ##########################################################
        #events: there are five events,
        ##########################################################
        #1. next arrival the fog, and service time in fog
        #2. next depart the fog, arrival time of next dep fog
        #3. next arrival the network, service time of the network latency
        #4. next depart the network, arrival service time of the cloud
        #5. next depart the cloud, arrival time of next dep cloud
        n_arrival_fog = arrival[0]
        service_time_n_arrival_fog = service_fog[0]
        #point to the next job
        job_counter = 0
        num_of_jobs = len(arrival)


        n_departure_fog = float('inf')
        n_arrival_net = float('inf')
        n_departure_net = float('inf')
        n_departure_cloud = float('inf')


        ##########################################################
        #to store information of departrue
        ##########################################################
        departure_fog_info = []
        departure_net_info = []
        departure_cloud_info = []


        ##########################################################
        #to store the jobs inside each list
        ##########################################################
        job_list_fog = []
        job_list_net = []
        job_list_cloud = []


        ##########################################################
        #Initialize the master clock time
        ##########################################################
        last_master_clock = 0
        master_clock = 0




        while 1:
##########################################################
#find out the next event type
##########################################################
            if n_arrival_fog == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_arrival_fog
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 1
            elif n_departure_fog == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_departure_fog
                next_event_type = 2
            elif n_arrival_net == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_arrival_net
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 3
            elif n_departure_net == min([n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud]):
                next_event_time = n_departure_net
                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)
                next_event_type = 4
            else:
                next_event_time = n_departure_cloud
                next_event_type = 5

            last_master_clock = master_clock
            master_clock = next_event_time
            #time difference
            difference = master_clock - last_master_clock

            print(master_clock)
            print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)

#arival the fog
            if next_event_type == 1:
                #print(1)
                #insert new job into job_list_fog and update the information of the fog job list
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_fog.append((job_counter, arrival[job_counter], service_fog[job_counter]))
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]

                #print(job_list_fog)
                #check wether have next job, and update the n_arrival_fog and all the times
                if job_counter < num_of_jobs-1:
                    job_counter += 1
                    n_arrival_fog = arrival[job_counter]
                    #print(master_clock, job_counter, n_arrival_fog)
                else:
                    n_arrival_fog = float('inf')
                    break

                #update the n_departure_fog and n_arrival_net
                job_list_fog_service = [i[2] for i in job_list_fog]
                min_value = min(job_list_fog_service)
                min_index = job_list_fog_service.index(min_value)
                counter1 = job_list_fog[min_index][0]
                if network[counter1] != 0:
                    n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                    n_departure_fog = float('inf')
                else:
                    n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                    n_arrival_net = float('inf')

                #update the departure network latency and departure cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)


#departure from fog
            elif next_event_type == 2:
                #print(2)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]

                #update the departrue_fog_info
                min_net = min([i[2] for i in job_list_fog])
                for i in range(len(job_list_fog)):
                    if job_list_net[i][2] == min_net:
                        departure_fog_item = job_list_fog.pop(i)
                        departure_fog_info.append((departure_fog_item[1], master_clock))



                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]
                #update the events times
                #n_arrival_fog unchange
                #update the n_departure_fog and n_arrival_fog
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')


                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)


                response_time_cumulative += master_clock - departure_fog_item[1]
                num_customer_served += 1


#from fog to network
            elif next_event_type == 3:
                #print(3)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                #uout of job_list_fog
                for i in range(len(job_list_fog)):
                    if job_list_fog[i][2] == 0:
                        departure_fog_item = job_list_fog.pop(i)
                        departure_fog_info.append((departure_fog_item[1], master_clock))


                #into the job_list_net
                job_counter3 = departure_fog_item[0]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_net.append((job_counter3, arrival[job_counter3], network[job_counter3]))

                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]


                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')


                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)





#from network to cloud
            elif next_event_type == 4:
                #print(4)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]

                min_net = min([i[2] for i in job_list_net])
                for i in range(len(job_list_net)):
                    if job_list_net[i][2] == min_net:
                        departure_net_item = job_list_net.pop(i)
                        departure_net_info.append((departure_net_item[1], master_clock))

                job_counter4 = departure_net_item[0]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]
                job_list_cloud.append((job_counter4, arrival[job_counter4], service_cloud[job_counter4]))


                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')



                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)





#departure from cloud
            elif next_event_type == 5:
                #print(5)
                #update the job lists
                job_list_fog = [(i[0], i[1], i[2] - difference/len(job_list_fog)) for i in job_list_fog]
                job_list_net = [(i[0], i[1], i[2] - difference) for i in job_list_net]
                job_list_cloud = [(i[0], i[1], i[2] - difference/len(job_list_cloud)) for i in job_list_cloud]


                min_cloud = min([i[2] for i in job_list_cloud])
                for i in range(len(job_list_cloud)):
                    if job_list_cloud[i][2] == min_cloud:
                        departure_cloud_item = job_list_cloud.pop(i)
                        departure_cloud_info.append((departure_cloud_item[1], master_clock))

                #update the events times
                job_list_fog_service = [i[2] for i in job_list_fog]
                if len(job_list_fog_service) == 0:
                    n_arrival_net = float('inf')
                    n_departure_fog = float('inf')
                else:
                    min_value = min(job_list_fog_service)
                    min_index = job_list_fog_service.index(min_value)
                    counter3 = job_list_fog[min_index][0]
                    if network[counter3] != 0:
                        n_arrival_net = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_departure_fog = float('inf')
                    else:
                        n_departure_fog = master_clock + min([i[2] for i in job_list_fog]) * len(job_list_fog)
                        n_arrival_net = float('inf')



                #update the departure network latency and departrue cloud
                if len(job_list_net) == 0:
                    n_departure_net = float('inf')
                else:
                    n_departure_net = master_clock + min([i[2] for i in job_list_net])
                if len(job_list_cloud) == 0:
                    n_departure_cloud = float('inf')
                else:
                    n_departure_cloud = master_clock + min([i[2] for i in job_list_cloud]) * len(job_list_cloud)



                response_time_cumulative += master_clock
                num_customer_served += 1

                #print(n_arrival_fog, n_departure_fog, n_arrival_net, n_departure_net, n_departure_cloud)



            if num_customer_served == num_of_jobs:
                break

    mrt = response_time_cumulative/num_customer_served
    return (departure_fog_info, departure_net_info, departure_cloud_info, mrt)
