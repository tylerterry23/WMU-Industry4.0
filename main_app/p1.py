from tkinter import *
from tkinter import ttk
import socket
import time



#list for ip address
#[ip address for station1, ip address for station2,.....]

port_n = 7800


def settablet_for5(station):
    # UI
   # main_window = Tk()
    
    global station_list
    station_list = [] 
    station_list = station
    ##########################
    #    conecct with tablets
    #########################

    while True:
        #create socket and wait for the data to be sent
        r = socket.socket()
        r.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        r.bind(('',port_n))
        r.listen(5)
        print("listing....")

        #accept the data and get ip address of the tablet
        c, addr = r.accept()
        print('got connection from', addr[0])
        #global station_list
        rcvD = c.recv(1024).decode()
        
        # get data from tablet (station number)
        # based on the table number, add the ip address for the station number
        # then send the sverage time for the station number
        match rcvD:
            # case "data recieved (station #)
            #       assign the ip address to the corresponding item in s_l list
            #       #c.send(bytesz("average time\nstep 1\nstep2\nstep3....",'UTF-8'));
            case "Station 1":
                station_list[0] = addr[0] 
                c.send(bytes("120\nInsert the drive axle into the lower axle housing. Make sure that it is properly seated.\nInsert the reduction gear into the lower axle body. Make sure that this gear is in mesh with the gear from the drive axle.\nPlace the DC motor into the lower axle body. Make sure that this gear is in mesh with the gear from the drive axle.\nPlace both suspension link bars into the spherical slots. Make sure that the link bars are facing down.\nFlip over the lower axle housing and place the upper axle housing. Take 2 axle housing screws and use the electric screwdriver tot screw the upper and lower axle housing togeather.\n",'UTF-8'));

            case "Station 2":
                station_list[1] = addr[0]
                c.send(bytes("105\nLine up your station 1 assembly with the main body making sure that the 3 suspension links are lined up properly.\nPop the Chasis Link Bar mount onto the Chasis Body encasing the 2 suspension links. Use the electric screwdriver to screw the pieces togeather.\nMake sure all parts are snapped in place correctly and have the suspension links in place.\n",'UTF-8'));

            case "Station 3":
                station_list[2] = addr[0]
                c.send(bytes("90\nPlace the completed Station 2 assmebly into the provided fixture. Place thestrut assmblies in the correct spots as shown. DO NOT PUT THEM IN UPSIDE DOWN!!\nPlace 8 Strut Screws ( 2 on each of the strut assmeblies ) and use the electric screwdriver to screw them tightly\nMake sure that all four strut assmevlies are propely assmebled.\n",'UTF-8'));

            case "Station 4":
                station_list[3] = addr[0]
                c.send(bytes("75\nTake the completed Station 3 assembly and affix all 4 tires onto the axles as shown\nUse the electric screwdriver to tightly secure the tires to the axles from the chasis body.\n",'UTF-8'));

            case "Station 5":
                station_list[4] = addr[0]
                c.send(bytes("120\nConnect the battery to the relief on the bottom side of the station 4 assembly. Make sure the connection is secure. The battery should sit at an angle in the housing.\nAffix the batttery cover screw and place it in the slot as shown\nUse the electric screwdriver to tassembly to the battery cover to the station 4 assembly.\nSlide the body onto the station 4 assembly. Use the 4 posts to allign it.\nUse the elevtric screwdriver to secure the body onto the chasis. There are 4 screws.\n",'UTF-8'));
        
        print("connected with ",rcvD)

        #close socket
        c.close()
        r.close()
        print(station_list)
        
        if(station_list[0] != 0 and station_list[1] != 0 and station_list[2] != 0 and station_list[3] != 0 and station_list[4] != 0):
            return station_list  

  
def settablet_for1(station):
    # UI
   # main_window = Tk()
    
    #station_list = [0,0,0,0,0]
    ##########################
    #    conecct with tablets
    #########################
    global station_list
    station_list = [] 
    station_list = station
    while True:
        #create socket and wait for the data to be sent
        r = socket.socket()
        r.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        r.bind(('',port_n))
        r.listen(5)
        print("listing....")

        #accept the data and get ip address of the tablet
        c, addr = r.accept()
        print('got connection from', addr[0])
        #global station_list
        rcvD = c.recv(1024).decode()
        
        # get data from tablet (station number)
        # based on the table number, add the ip address for the station number
        # then send the sverage time for the station number
        match rcvD:
            # case "data recieved (station #)
            #       assign the ip address to the corresponding item in s_l list
            #       #c.send(bytesz("average time\nstep 1\nstep2\nstep3....",'UTF-8'));
            case "Station 1":
                station_list[0] = addr[0] 
                c.send(bytes("120\nInsert the drive axle into the lower axle housing. Make sure that it is properly seated.\nInsert the reduction gear into the lower axle body. Make sure that this gear is in mesh with the gear from the drive axle.\nPlace the DC motor into the lower axle body. Make sure that this gear is in mesh with the gear from the drive axle.\nPlace both suspension link bars into the spherical slots. Make sure that the link bars are facing down.\nFlip over the lower axle housing and place the upper axle housing. Take 2 axle housing screws and use the electric screwdriver tot screw the upper and lower axle housing togeather.\n",'UTF-8'));

            case "Station 2":
                station_list[1] = addr[0]
                c.send(bytes("105\nLine up your station 1 assembly with the main body making sure that the 3 suspension links are lined up properly.\nPop the Chasis Link Bar mount onto the Chasis Body encasing the 2 suspension links. Use the electric screwdriver to screw the pieces togeather.\nMake sure all parts are snapped in place correctly and have the suspension links in place.\n",'UTF-8'));

            case "Station 3":
                station_list[2] = addr[0]
                c.send(bytes("90\nPlace the completed Station 2 assmebly into the provided fixture. Place thestrut assmblies in the correct spots as shown. DO NOT PUT THEM IN UPSIDE DOWN!!\nPlace 8 Strut Screws ( 2 on each of the strut assmeblies ) and use the electric screwdriver to screw them tightly\nMake sure that all four strut assmevlies are propely assmebled.\n",'UTF-8'));

            case "Station 4":
                station_list[3] = addr[0]
                c.send(bytes("75\nTake the completed Station 3 assembly and affix all 4 tires onto the axles as shown\nUse the electric screwdriver to tightly secure the tires to the axles from the chasis body.\n",'UTF-8'));

            case "Station 5":
                station_list[4] = addr[0]
                c.send(bytes("120\nConnect the battery to the relief on the bottom side of the station 4 assembly. Make sure the connection is secure. The battery should sit at an angle in the housing.\nAffix the batttery cover screw and place it in the slot as shown\nUse the electric screwdriver to tassembly to the battery cover to the station 4 assembly.\nSlide the body onto the station 4 assembly. Use the 4 posts to allign it.\nUse the elevtric screwdriver to secure the body onto the chasis. There are 4 screws.\n",'UTF-8'));
        
        print("connected with ",rcvD)

        #close socket
        c.close()
        r.close()
        print(station_list)
        
      
        return station_list
    #################################################
    #    for UI 
    ################################################
    #l1 = Label(main_window, text="X_0 project")
    #bc = Button(main_window, text ="connect tablets...", command = connec)
    #b1 = Button(main_window, text ="start/stop station 1",command = lambda: stime(1))
    #b2 = Button(main_window, text ="start/stop station 2",command = lambda: stime(2))
    #b3 = Button(main_window, text ="start/stop station 3",command = lambda: stime(3))
    #b4 = Button(main_window, text ="start/stop station 4",command = lambda: stime(4))
    #b5 = Button(main_window, text ="start/stop station 5",command = lambda: stime(5))
    #l1.pack()
    #bc.pack()
    #b1.pack()
    #b2.pack()
    #b3.pack()
    #b4.pack()
    #b5.pack()
    #main_window.mainloop()

def stime(arg, station_list):  
    s = socket.socket()
    port_n = 7800
    data="ss\n" #any value is fine
    #global station_list #list of ip address
    #connect with tablet that has the corresponding ip address of the station number
    print(station_list)
    print(arg)
    s.connect((str(station_list[arg-1]),port_n))
    s.send(bytes(data,'UTF-8'))
    s.close()

