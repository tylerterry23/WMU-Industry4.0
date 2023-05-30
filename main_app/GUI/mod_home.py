from tkinter import *
from tkinter import ttk, font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from GUI.backend.Database import *
from GUI.helpwin import *
from GUI.export import *
from printer import *
from p1 import *
from datetime import date, timedelta, datetime
import ResetDB
import time
import socket

from threading import *

# For django server 
import os
from os.path import abspath, dirname, join

# Global Variables
station_list = [0,0,0,0,0]
port_n = 7800


class DjangoServer:

    def __init__(self):
        self.start_server()

    def start_server(self):
        try:
            print('Loading Live Dashboard...')

            # Determine the current directory
            current_dir = abspath(dirname(__file__))

            # Change the working directory to the Django project
            os.chdir(join(current_dir, '..', '..', 'dashboard', 'Version 2 - Django (Scalable)', 'industry4'))

            # Run the Django server in a separate PowerShell window
            server_command = 'start powershell -WindowStyle Minimized -Command "python manage.py runserver"'
            os.system(server_command)

            # Wait for a few seconds to ensure the server has started
            time.sleep(3)

            # Open the specified URL in the default web browser
            url = 'http://127.0.0.1:8000/dashboard/'
            os.startfile(url)

            print('Dashboard loaded succesfully!')

        except Exception as e:
            print(f"Error starting Django server: {e}")


class MainWindow:
    def __init__(self):
        """
        This class creates the main window for the application. Upon initialization,
        the class creates
        a new fullscreen window and places the tabs containing each frames functionalities.
        """
        # Lab pass
        # self.db = Database('localhost', 'root', 'industry4')
        # Home Pass
        self.db = Database('localhost', 'root', 'industry4')
        if (self.db.connect()) == 1:
            ResetDB.resetDB(0)
            self.db.connect()
        else:
            pass



        self.vehicleID = self.db.selection("Product", "Max(ProductID)")[0][0] + 1

        self.flag = 0
        self.char_buffer = []
        self.session_cars = {}

        
        # Creating the Main Window
        self.win = Tk()
        self.win.attributes('-fullscreen', True)
        self.win.title('Industry 4.0')
        self.win.configure(background='#dcdad5')
        
        # Creating a Font Object of TkDefaultFont
        self.defaultFont = font.nametofont("TkDefaultFont")

        # Overriding the default font
        self.defaultFont.configure(family="Times", size=16)

        # change the ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Frame1.TButton', background='#fd3535')
        self.style.map('Frame1.TButton', background=[('active', '#ff5f5f')])
        self.style.configure('Frame1.TFrame', background='grey')
        self.style.configure('Frame1.TLabel', background='grey')

        self.style.configure('Frame2.TFrame', background='cyan')
        self.style.configure('Frame2.TLabel', background='cyan')
        self.style.configure('Frame3.TFrame', background='blue')
        self.style.configure('Frame3.TLabel', background='blue')
        self.style.configure('Frame4.TFrame', background='green')
        self.style.configure('Frame4.TLabel', background='green')
        self.style.configure('Frame5.TFrame', background='yellow')
        self.style.configure('Frame5.TLabel', background='yellow')
        self.style.configure('Frame6.TFrame', background='red')
        self.style.configure('Frame6.TLabel', background='red')

        # Configure style for a progress bar to be green
        self.style.configure('green.Horizontal.TProgressbar', background='green')

        # Primary Quit button
        self.quit_btn = ttk.Button(self.win, text='X', command=self.exitApp, width=5, style='Frame1.TButton')
        self.quit_btn.pack(anchor='e')

        # Creaing the tabs
        self.CreateNotebook()
        self.win.update_idletasks()
        self.hometab = HomeTab(self.home_frame, self.db)
        self.processtab = ProcessTab(self.process_frame, self.db)
        self.qualtab = QualityTab(self.quality_frame, self.db, self.session_cars)
        # Add functionality to the unaccept button
        self.qualtab.quality_frame3.unaccept.config(command=lambda: self.removeVehicle(self.qualtab.quality_frame1.vehicleID.get()))

        self.dbtab = DBTab(self.db_frame, self.db)

        # Create binding for when the Qualitytab is selected
        self.sections.bind('<<NotebookTabChanged>>', lambda event, tab=self.qualtab: self.tabChanged(event, tab))

        # Bind to detect Barcode scanner
        self.win.bind('<Key>', lambda event, number=self.hometab.run_time_num, label=self.hometab.run_time: self.Timer(event,number,label))
        
        self.win.mainloop() 

    
    def CreateNotebook(self):
        """
        Creates the notebook widget to contain the tabs for each frame.
        """
        self.sections = ttk.Notebook(self.win)
        self.sections.pack(fill='both', expand=1,pady=10)
        self.AddSections()


    def AddSections(self):
        """
        Addition to the CreateNotebook function, this function is creating and placing each tab into
        the notebook.
        """
        # Creating all of the Tabs
        self.home_frame = ttk.Frame(self.sections, width=10, height=10)
        self.process_frame = ttk.Frame(self.sections, width=10, height=10)
        self.quality_frame = ttk.Frame(self.sections, width=10, height=10)
        self.db_frame = ttk.Frame(self.sections, width=10, height=10)
        
        # Packing the frames
        self.home_frame.pack(fill='both', expand=1)
        self.process_frame.pack(fill='both', expand=1)
        self.quality_frame.pack(fill='both', expand=1)
        self.db_frame.pack(fill='both', expand=1)

        # Making the frames into tabs
        self.sections.add(self.home_frame, text='Home')
        self.sections.add(self.process_frame, text='Process')
        self.sections.add(self.quality_frame, text='Quality Check')
        self.sections.add(self.db_frame, text='Search Database')


    def Timer(self, event, number, label):
        """
        When proper barcode is scanned, the timer will begin.
        This works by creating a buffer of 14 characters, checking if the barcodes "code" is in the
        buffer, if not, it will scrap the 14 characters and wait for new input. This is to lower the
        memory cost of constantly checking characters.
        """
        self.char_buffer.append(event.char)

        # If the barcode is scanned and begins with the token '@' examine the string buffer
        if '@' in self.char_buffer:

            if '@start' in ''.join(self.char_buffer):
                # Start Scan Detected, Print new label
                self.hometab.process_box.config(state='normal')
                self.hometab.process_box.insert(1.0,f'Printing new label: {self.vehicleID}\n')
                self.hometab.process_box.config(state='disabled')
                self.session_cars[self.vehicleID] = [0]
                
                # Create new row in Product table
                self.db.insert_into('Product', 
                    'ProductID, ProcessID, Completed, Accepted, StartTime, EndTime, TotalTime',
                    (self.vehicleID, 100, False, False, datetime.now(), None, '0:00.00'))
                
                # Create new row in ProductTime table
                self.db.insert_into('ProductTime',
                    'ProductID, StationOne, StationTwo, StationThree, StationFour, StationFive, TotalTime',
                    (self.vehicleID, '0:00', '0:00', '0:00', '0:00', '0:00', '0:00.00'))



                print_barcode(f'@{self.vehicleID}') 
                self.vehicleID += 1
                self.char_buffer = []

            # Itereate through the session cars to see if a vehicle is scanned
            for ids in self.session_cars:
                if '@' + str(ids) in ''.join(self.char_buffer):
                    # start stop current vehicle
                    self.VehicleScan(ids)
                    self.char_buffer=[]
                    break

        # Clear the buffer if length 14
        if len(self.char_buffer) > 14:
            self.char_buffer = []


    def VehicleScan(self,vehicleID):
        # If flag is off
        if self.session_cars[vehicleID][0] == 0:
            
            # Check the list length
            # If less than 6 (5 stations plus flag)
            if len(self.session_cars[vehicleID]) < 6:
                
                # Checking if the next station is currently active
                if self.checkNextStation(len(self.session_cars[vehicleID])):

                    # Change Flag
                    self.session_cars[vehicleID][0] = 1

                    # Update DB
                    self.db.updateTable("Stations", ("Active"), ("True"), f'StationID = {len(self.session_cars[vehicleID])}')
                    # Append new value (times)
                    self.session_cars[vehicleID].append(time.time())
                    
                    # Start time on GUI
                   
                    #len(self.session_cars[vehicleID])
                    self.hometab.process_box.config(state='normal')
                    self.hometab.process_box.insert(1.0, f'Starting vehicle: {vehicleID} at station: {len(self.session_cars[vehicleID]) - 1}\n')
                    self.hometab.process_box.config(state='disabled')
                    self.GUItime(len(self.session_cars[vehicleID])-2, vehicleID)
            
                    ############ tablet start time  #############################
                    if station_list[len(self.session_cars[vehicleID])-2] != 0:
                        try:
                            print("start tablet time")
                            stime(len(self.session_cars[vehicleID])-1, station_list)
                        except:
                            print("no tablet")
                    ##########################################################


                else:
                    self.hometab.process_box.config(state='normal')
                    self.hometab.process_box.insert(1.0, f'Cannot Start vehicle: {vehicleID} at station: {len(self.session_cars[vehicleID])}. Ensure Station is cleared.\n')
                    self.hometab.process_box.config(state='disabled')
            else:
                self.hometab.process_box.config(state='normal')
                self.hometab.process_box.insert(1.0, f'Vehicle: {vehicleID} is finished. No more times to be added\n')
                self.hometab.process_box.config(state='disabled')
        
        # If flag is on
        else:
            

            # Switch flag off, which will stop GUI timer loop
            self.session_cars[vehicleID][0] = 0
            
            # Change the last value in the dict[vehicleID] with the end time - start time
            self.session_cars[vehicleID][len(self.session_cars[vehicleID])-1] = time.time() - self.session_cars[vehicleID][len(self.session_cars[vehicleID])-1]

            # Update DB
            self.db.updateTable("Stations", ("Active"), ("False"), f'StationID = {len(self.session_cars[vehicleID])-1}')

            ############### tablet to stop time #######################
            if station_list[len(self.session_cars[vehicleID])-2] != 0:
                try:
                    print("stop tablet time")
                    stime(len(self.session_cars[vehicleID])-1, station_list)
                except:
                    print("no tablet")
            ###########################################################

            temp = len(self.session_cars[vehicleID]) - 1
            temp = "StationOne" if temp == 1 else temp
            temp = "StationTwo" if temp == 2 else temp
            temp = "StationThree" if temp == 3 else temp
            temp = "StationFour" if temp == 4 else temp
            temp = "StationFive" if temp == 5 else temp

            # Update the ProductTime with the station time, rounded to two decimal places
            try:
                temp_total = datetime.strptime(str(timedelta(seconds=round(self.session_cars[vehicleID][-1],2))), '%H:%M:%S.%f').strftime('%H:%M:%S.%f')
            except ValueError:
                # When the time doesn't have decimals
                temp_total = datetime.strptime(str(timedelta(seconds=round(self.session_cars[vehicleID][-1],2))), '%H:%M:%S').strftime('%H:%M:%S.%f')
            
            self.db.updateTable("ProductTime", (temp), (f'\'{temp_total[0:11]}\''), f"ProductID = {vehicleID}")
            
            # Update the TotalTime
            temp_total = str(self.db.selection("ProductTime", "TotalTime", f"ProductID = {vehicleID}")[0][0])

            # Ensure the first value at 0 has the two decimal places
            if len(temp_total) == 7:
                temp_total = f'{temp_total}.00'
            
            
            # Convert to datetime
            temp_total = datetime.strptime(temp_total, '%H:%M:%S.%f')
            temp_total = temp_total + timedelta(seconds=round(self.session_cars[vehicleID][-1],2))
            temp_total = temp_total.strftime('%H:%M:%S.%f')


            self.db.updateTable("ProductTime", ("TotalTime"), (f'\'{temp_total}\''), f"ProductID = {vehicleID}")
            self.db.updateTable("Product", ("TotalTime"), (f'\'{temp_total}\''), f"ProductID = {vehicleID}")


            # Add history to the StationHistory table
            self.db.insert_into("StationHistory", "StationID, ProductID, Accepted, DateCompleted, TimeTaken", ((len(self.session_cars[vehicleID])-1, vehicleID, True, date.today(), f'{self.session_cars[vehicleID][-1]:.2f}'))) 

            # Check to see if the product is completed
            if temp == "StationFive":

                # Check to see if product is compelted, if so update the Process completion table
                temp_completed = str(self.db.selection("Process", "TimesCompleted", f"ProcessID = {100}")[0][0] + 1)
                self.db.updateTable("Process", ("TimesCompleted"), (temp_completed), f"ProcessID = {100}")
                self.hometab.total_cars.config(text=int(self.hometab.total_cars['text'])+1)

                # Update product table to show completed on the products
                self.db.updateTable("Product", ("EndTime"), (f'\'{datetime.now()}\''), f"ProductID = {vehicleID}")
                self.db.updateTable("Product", ("Completed"), ("True"), f"ProductID = {vehicleID}")
                self.db.updateTable("Product", ("Accepted"), ("True"), f"ProductID = {vehicleID}")

                # Update the quality progress bar
                temp_completed = str(self.db.selection("Process", "TimesCompleted", f"ProcessID = {100}")[0][0])
                temp_accepted = self.db.selection("Product", "Accepted")
                temp_accepted = sum([x[0] for x in temp_accepted])
                temp_percentage = int((int(temp_accepted)/int(temp_completed))*100, )
                self.hometab.quality_bar['value'] = temp_percentage

            self.hometab.process_box.config(state='normal')
            self.hometab.process_box.insert(1.0, f'Vehicle: {vehicleID} has completed station: {len(self.session_cars[vehicleID])-1} with the time {self.session_cars[vehicleID][len(self.session_cars[vehicleID])-1]:.2f}\n')
            self.hometab.process_box.config(state='disabled')


    def GUItime(self, pos, vehicleID):
        # Check Flag is on
        if self.session_cars[vehicleID][0] != 0:
            if pos > 3:
                # Tile 5
                self.hometab.active_stations[4] = 1
                self.hometab.tile5_vehicleID.config(text=str(vehicleID))
                current_runtime = int(time.time() - self.session_cars[vehicleID][5])
                self.tileColorChange(current_runtime,5)
                current_runtime = datetime.strptime(str(timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
                self.hometab.tile5_runtime.config(
                        text=current_runtime)
                self.hometab.tile5_runtime.after(500, lambda pos=pos, vehicleID=vehicleID:
                        self.GUItime(pos, vehicleID))
            elif pos > 2:
                # Tile 4
                self.hometab.active_stations[3] = 1
                self.hometab.tile4_vehicleID.config(text=str(vehicleID))
                current_runtime = int(time.time() - self.session_cars[vehicleID][4])
                self.tileColorChange(current_runtime,4)
                current_runtime = datetime.strptime(str(timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
                self.hometab.tile4_runtime.config(
                        text=current_runtime)
                self.hometab.tile4_runtime.after(500, lambda pos=pos, vehicleID=vehicleID:
                        self.GUItime(pos, vehicleID))
            elif pos > 1:
                # Tile 3
                self.hometab.active_stations[2] = 1
                self.hometab.tile3_vehicleID.config(text=str(vehicleID))
                current_runtime = int(time.time() - self.session_cars[vehicleID][3])
                self.tileColorChange(current_runtime,3)
                current_runtime = datetime.strptime(str(timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
                self.hometab.tile3_runtime.config(
                       text=current_runtime)
                self.hometab.tile3_runtime.after(500, lambda pos=pos, vehicleID=vehicleID:
                        self.GUItime(pos, vehicleID))
            elif pos > 0:
                # Tile 2
                self.hometab.active_stations[1] = 1
                self.hometab.tile2_vehicleID.config(text=str(vehicleID))
                current_runtime = int(time.time() - self.session_cars[vehicleID][2])
                self.tileColorChange(current_runtime,2)
                current_runtime = datetime.strptime(str(timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
                self.hometab.tile2_runtime.config(
                       text=current_runtime)
                self.hometab.tile2_runtime.after(500, lambda pos=pos, vehicleID=vehicleID:
                        self.GUItime(pos, vehicleID))
            else:
                # Tile 1
                self.hometab.active_stations[0] = 1
                self.hometab.tile1_vehicleID.config(text=str(vehicleID))
                current_runtime = int(time.time() - self.session_cars[vehicleID][1])
                self.tileColorChange(current_runtime,1)
                current_runtime = datetime.strptime(str(timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
                
                self.hometab.tile1_runtime.config(
                       text=current_runtime)
                self.hometab.tile1_runtime.after(500, lambda pos=pos, vehicleID=vehicleID:
                        self.GUItime(pos, vehicleID))
        else:
            if pos > 3:
                self.hometab.active_stations[4] = 0
                self.hometab.updateTile5BG(0)
                self.hometab.tile5_vehicleID.config(text='None')
                self.hometab.tile5_runtime.config(text='00:00')
            elif pos > 2:
                self.hometab.active_stations[3] = 0
                self.hometab.updateTile4BG(0)
                self.hometab.tile4_vehicleID.config(text='None')
                self.hometab.tile4_runtime.config(text='00:00')
            elif pos > 1:
                self.hometab.active_stations[2] = 0
                self.hometab.updateTile3BG(0)
                self.hometab.tile3_vehicleID.config(text='None')
                self.hometab.tile3_runtime.config(text='00:00')
            elif pos > 0:
                self.hometab.active_stations[1] = 0
                self.hometab.updateTile2BG(0)
                self.hometab.tile2_vehicleID.config(text='None')
                self.hometab.tile2_runtime.config(text='00:00')
            else:
                self.hometab.active_stations[0] = 0
                self.hometab.updateTile1BG(0)
                self.hometab.tile1_vehicleID.config(text='None')
                self.hometab.tile1_runtime.config(text='00:00')


    def checkNextStation(self, next_station):
        """
        Function to check the next station the vehicle will begin at, if a vehicle is currently there, the function will return false, not allowing the time to begin at that station.

        Param:
            next_station (int):
                Integer containing the number value for the next station the vehicle is attempting to begin at. 

        Returns:
            bool:
                True if there is no vehicle at the next station
                False if there is a vehicle at the next station
        """

        if next_station == 5:
            if self.hometab.tile5_vehicleID['text'] == 'None':
                return True
            else:
                return False
        elif next_station == 4:
            if self.hometab.tile4_vehicleID['text'] == 'None':
                return True
            else:
                return False
        elif next_station == 3:
            if self.hometab.tile3_vehicleID['text'] == 'None':
                return True
            else:
                return False
        elif next_station == 2:
            if self.hometab.tile2_vehicleID['text'] == 'None':
                return True
            else:
                return False
        else:
            if self.hometab.tile1_vehicleID['text'] == 'None':
                return True
            else:
                return False


    def tabChanged(self, event, tab):
        """
        This function is called when the tab is changed. It will check if the tab is the Quality tab,
        if so, it will update the table with the current session cars.
        """
        if self.sections.index('current') == 2:
            tab.updateList()
        else:
            pass


    def removeVehicle(self, vehicleID):
        """
        Removes the vehicle from the session
        """
        if vehicleID != None:
            # Make sure the flag is set to false
            self.session_cars[int(vehicleID)][0] = 0
            
            # Check the length of the session_cars[vehicleID] list
            if len(self.session_cars[int(vehicleID)]) == 6:
                # output to the textbox on the hometab that the vehicle has been removed
                self.hometab.process_box.config(state=NORMAL)
                self.hometab.process_box.insert(1.0, f"Vehicle {vehicleID} has been removed from the session\n")
                self.hometab.process_box.config(state=DISABLED)
            else:
                while len(self.session_cars[int(vehicleID)]) != 6:
                    self.session_cars[int(vehicleID)].append(0)
                self.hometab.process_box.config(state=NORMAL)
                self.hometab.process_box.insert(1.0, f"Vehicle {vehicleID} has been removed from the session\n")
                self.hometab.process_box.config(state=DISABLED)

            # Change the accepted column to false in the database
            self.db.updateTable('Product', 'Accepted', '0', f'ProductID=\'{vehicleID}\'')

            # To find the accepted, query the product table, look for the accepted column and add up the true values
            temp_completed = str(self.db.selection("Process", "TimesCompleted", f"ProcessID = {100}")[0][0])
            temp_accepted = self.db.selection("Product", "Accepted")
            temp_accepted = sum([x[0] for x in temp_accepted])
            temp_percentage = int((int(temp_accepted)/int(temp_completed))*100)

            # Update the Quality progress bar in the home tab with the percentage
            self.hometab.quality_bar['value'] = temp_percentage


    def tileColorChange(self, current_time, tile):
        if tile == 1:
            if current_time < int((self.hometab.tile1_goaltime*0.4)):
                self.hometab.updateTile1BG(1)
            elif current_time < int((self.hometab.tile1_goaltime*0.8)):
                self.hometab.updateTile1BG(2)
            elif current_time < int((self.hometab.tile1_goaltime*1.2)):
                self.hometab.updateTile1BG(3)
            elif current_time < int((self.hometab.tile1_goaltime*1.6)):
                self.hometab.updateTile1BG(4)
            elif current_time < int((self.hometab.tile1_goaltime*2)):
                self.hometab.updateTile1BG(5)
        elif tile == 2:
            if current_time < int((self.hometab.tile2_goaltime*0.4)):
                self.hometab.updateTile2BG(1)
            elif current_time < int((self.hometab.tile2_goaltime*0.8)):
                self.hometab.updateTile2BG(2)
            elif current_time < int((self.hometab.tile2_goaltime*1.2)):
                self.hometab.updateTile2BG(3)
            elif current_time < int((self.hometab.tile2_goaltime*1.6)):
                self.hometab.updateTile2BG(4)
            elif current_time < int((self.hometab.tile2_goaltime*2)):
                self.hometab.updateTile2BG(5)
        elif tile == 3:
            if current_time < int((self.hometab.tile3_goaltime*0.4)):
                self.hometab.updateTile3BG(1)
            elif current_time < int((self.hometab.tile3_goaltime*0.8)):
                self.hometab.updateTile3BG(2)
            elif current_time < int((self.hometab.tile3_goaltime*1.2)):
                self.hometab.updateTile3BG(3)
            elif current_time < int((self.hometab.tile3_goaltime*1.6)):
                self.hometab.updateTile3BG(4)
            elif current_time < int((self.hometab.tile3_goaltime*2)):
                self.hometab.updateTile3BG(5)
        elif tile == 4:
            if current_time < int((self.hometab.tile4_goaltime*0.4)):
                self.hometab.updateTile4BG(1)
            elif current_time < int((self.hometab.tile4_goaltime*0.8)):
                self.hometab.updateTile4BG(2)
            elif current_time < int((self.hometab.tile4_goaltime*1.2)):
                self.hometab.updateTile4BG(3)
            elif current_time < int((self.hometab.tile4_goaltime*1.6)):
                self.hometab.updateTile4BG(4)
            elif current_time < int((self.hometab.tile4_goaltime*2)):
                self.hometab.updateTile4BG(5)
        elif tile == 5:
            if current_time < int((self.hometab.tile5_goaltime*0.4)):
                self.hometab.updateTile5BG(1)
            elif current_time < int((self.hometab.tile5_goaltime*0.8)):
                self.hometab.updateTile5BG(2)
            elif current_time < int((self.hometab.tile5_goaltime*1.2)):
                self.hometab.updateTile5BG(3)
            elif current_time < int((self.hometab.tile5_goaltime*1.6)):
                self.hometab.updateTile5BG(4)
            elif current_time < int((self.hometab.tile5_goaltime*2)):
                self.hometab.updateTile5BG(5)


    def exitApp(self):
        # TODO: Insert the data from the session in the database
        self.win.destroy()


class HomeTab:
    def __init__(self, master, db):
        """
        The HomeTab class creates the HomeTab frame inside the main window. The HomeTab is the only
        tab that the 'guest' user should be able to see. The class takes the master widget, which should
        be the home frame in the notebook, and places the proper widgets on the frame.
        """
        self.master = master
        self.db = db
        self.seconds = 0
        self.active_stations = [0,0,0,0,0]

        self.master.rowconfigure((0,1,2), weight=1)
        self.master.columnconfigure((0,1,2,3), weight=1)


        # Creating the Home frame

        self.HomeTabFrame1()
        self.HomeTabFrame2()
        self.HomeTabFrame3()
        self.HomeTabFrame4()
        self.HomeTabFrame5()

        self.master.after(1000, self.totalTimer)
        self.run_time.after(1000, self.runTimer)
        self.full_prod_time.after(1000, self.fullProductiveTimer)
        self.availability_bar.after(1000, self.updateAvailabilityBar)


    def HomeTabFrame1(self):
        """
        Creates the top left frame on the HomeTab. This frame contains all of the timer information
        for the application.
        """
        self.oee_frame = ttk.LabelFrame(self.master, width=10, height=10, text='Time Anlaysis')
        
        # Configuring the layout
        self.oee_frame.grid_propagate(0)
        self.oee_frame.columnconfigure((0,1), weight=1)
        self.oee_frame.rowconfigure((0,1,3), weight=1)

        # Adding all the necessary Labels
        ttk.Label(self.oee_frame, text='Total Time', justify=LEFT).grid(row=0, column=0, sticky=W, padx=30)
        self.total_time_num = 0
        self.total_time = ttk.Label(self.oee_frame, text='0:00:00', justify=LEFT)
        self.total_time.grid(row=0, column=1,sticky=W)
        

        self.run_time_lab = ttk.Label(self.oee_frame, text='Run Time', justify=LEFT).grid(row=2, column=0, sticky=W, padx=30, pady=10)
        self.run_time_num = 0
        self.run_time = ttk.Label(self.oee_frame, text='0:00:00', justify=LEFT)
        self.run_time.grid(row=2,column=1,sticky=W)

        self.oee_lab8 = ttk.Label(self.oee_frame, text='Fully Productive Time', justify=LEFT).grid(row=4, column=0, sticky=W, padx=30, pady=10)
        self.full_prod_time_num = 0
        self.full_prod_time = ttk.Label(self.oee_frame, text='0:00:00', justify=LEFT)
        self.full_prod_time.grid(row=4, column=1, sticky=W, pady=10)


        # Places the home frame
        self.oee_frame.grid(row=0,column=0, columnspan=2, sticky='NSEW', padx=10, pady=10)


    def HomeTabFrame2(self):
        """
        Creates the top right frame for the HomeTab. This frame will contain statistical information
        about the assembly process. Progress bars are created for visual representation of data
        """
        self.stat_frame = ttk.LabelFrame(self.master, width=10, height=10, text='Statistics')
        
        # Configuring the layout
        self.stat_frame.grid_propagate(0)
        self.stat_frame.columnconfigure(0, weight=1)
        self.stat_frame.columnconfigure(1, weight=3)
        self.stat_frame.rowconfigure((0,1,2), weight=1)

        # Label for total Cars Built
        self.stat_lab1 = ttk.Label(self.stat_frame, text='Total Cars Built:', justify=LEFT).grid(row=0,column=0, sticky=W, padx=30, pady=10)
        self.total_cars_num = self.db.selection('process', 'TimesCompleted')[0][0]
        self.total_cars = ttk.Label(self.stat_frame, text=f'{self.total_cars_num}', justify=LEFT)
        self.total_cars.grid(row=0,column=1, sticky=W, padx=30, pady=10)

        # Progress bars and labels
        self.stat_lab3 = ttk.Label(self.stat_frame, text='Availability', justify=LEFT).grid(row=1, column=0, sticky=W, padx=30, pady=10)     
        self.stat_lab5 = ttk.Label(self.stat_frame, text='Quality', justify=LEFT).grid(row=2, column=0, sticky=W, padx=30, pady=10)

        self.availability_bar = ttk.Progressbar(self.stat_frame, orient='horizontal', mode='determinate', length=250, value=100, maximum=100, style='green.Horizontal.TProgressbar')
        self.availability_bar.grid(row=1,column=1, sticky=W)
        self.quality_bar = ttk.Progressbar(self.stat_frame, orient='horizontal', mode='determinate', length=250, value=100, maximum=100, style='green.Horizontal.TProgressbar')
        self.quality_bar.grid(row=2, column=1, sticky=W)

        # Update the Quality Bar
        temp_completed = self.db.selection('process', 'TimesCompleted')[0][0]
        temp_accepted = self.db.selection('product', 'Accepted')
        temp_accepted = [i[0] for i in temp_accepted]
        temp_accepted = sum(temp_accepted)
        try:
            self.quality_bar['value'] = int((int(temp_accepted)/int(temp_completed))*100)
        except ZeroDivisionError:
            self.quality_bar['value'] = 100
        
        # Placing the frame
        self.stat_frame.grid(row=0, column=2, columnspan=2, sticky='NSEW', padx=10, pady=10)


    def HomeTabFrame3(self):
        """
        Creates the bottom left frame of the HomeTab. This frame contains the graph for the data being
        tracked throughout the assembly process.
        """
        self.tile_frame = ttk.Frame(self.master, width=10, height=10)
       
        self.tile_frame.grid_propagate(0)
        self.tile_frame.columnconfigure((0,1,2,3,4), weight=1)
        self.tile_frame.rowconfigure(0,weight=1)

        # Tile1
        self.tile1 = ttk.Frame(self.tile_frame, width=10, height=10, style='Frame1.TFrame')
        self.tile1.rowconfigure((0,1,2,3,4), weight=1)
        self.tile1.columnconfigure((0,1), weight=1)
        self.tile1.grid_propagate(0)

        self.tile1_lab1 = ttk.Label(self.tile1, text='Station 1', style='Frame1.TLabel', font=('Times', 20, 'bold'))
        self.tile1_lab1.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.tile1_lab2 = ttk.Label(self.tile1, text='Active:', style='Frame1.TLabel')
        self.tile1_lab2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.tile1_lab3 = ttk.Label(self.tile1, text='Run Time:', style='Frame1.TLabel')
        self.tile1_lab3.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.tile1_lab4 = ttk.Label(self.tile1, text='Time Goal:', style='Frame1.TLabel')
        self.tile1_lab4.grid(row=3, column=0, padx=10, pady=10, sticky='W', )
        self.tile1_lab5 = ttk.Label(self.tile1, text='Inventory Request:', style='Frame1.TLabel')
        self.tile1_lab5.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        
        self.tile1_vehicleID = ttk.Label(self.tile1, text='None', style='Frame1.TLabel')
        self.tile1_vehicleID.grid(row=1, column=1, padx=10, pady=10, sticky='W') 
        
        self.tile1_runtime = ttk.Label(self.tile1, text='00:00', style='Frame1.TLabel')
        self.tile1_runtime.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.tile1_goaltime = self.db.selection('stations', 'EstimatedTime', 'StationID=1')
        self.tile1_goaltime = str(self.tile1_goaltime[0][0])
        self.tile1_goaltime = self.tile1_goaltime.split(':')
        self.tile1_goaltime = f'{self.tile1_goaltime[1]}:{self.tile1_goaltime[2]}'

        self.tile1_goaltime_lab = ttk.Label(self.tile1, text=self.tile1_goaltime, style='Frame1.TLabel')
        self.tile1_goaltime_lab.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Convert tile1_goal time to seconds
        self.tile1_goaltime = self.tile1_goaltime.split(':')
        self.tile1_goaltime = int(self.tile1_goaltime[0])*60 + int(self.tile1_goaltime[1])

        


        # Tile2
        self.tile2 = ttk.Frame(self.tile_frame, width=10, height=10, style='Frame1.TFrame')
        self.tile2.rowconfigure((0,1,2,3,4), weight=1)
        self.tile2.columnconfigure((0,1), weight=1)
        self.tile2.grid_propagate(0)
        
        self.tile2_lab1 = ttk.Label(self.tile2, text='Station 2', style='Frame1.TLabel', font=('Times', 20, 'bold'))
        self.tile2_lab1.grid(row=0, column=0, padx=10, pady=10,sticky='W')
        self.tile2_lab2 = ttk.Label(self.tile2, text='Active:', style='Frame1.TLabel')
        self.tile2_lab2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.tile2_lab3 = ttk.Label(self.tile2, text='Run Time:', style='Frame1.TLabel')
        self.tile2_lab3.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.tile2_lab4 = ttk.Label(self.tile2, text='Time Goal:', style='Frame1.TLabel')
        self.tile2_lab4.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.tile2_lab5 = ttk.Label(self.tile2, text='Inventory Request:', style='Frame1.TLabel')
        self.tile2_lab5.grid(row=4, column=0, padx=10, pady=10, sticky='W')
    
        self.tile2_vehicleID = ttk.Label(self.tile2, text='None', style='Frame1.TLabel')
        self.tile2_vehicleID.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.tile2_runtime = ttk.Label(self.tile2, text='00:00', style='Frame1.TLabel')
        self.tile2_runtime.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.tile2_goaltime = self.db.selection('stations', 'EstimatedTime', 'StationID=2')
        self.tile2_goaltime = str(self.tile2_goaltime[0][0])
        self.tile2_goaltime = self.tile2_goaltime.split(':')
        self.tile2_goaltime = f'{self.tile2_goaltime[1]}:{self.tile2_goaltime[2]}'

        self.tile2_goaltime_lab = ttk.Label(self.tile2, text=self.tile2_goaltime, style='Frame1.TLabel')
        self.tile2_goaltime_lab.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Convert tile2_goal time to seconds
        self.tile2_goaltime = self.tile2_goaltime.split(':')
        self.tile2_goaltime = int(self.tile2_goaltime[0])*60 + int(self.tile2_goaltime[1])


        # Tile3
        self.tile3 = ttk.Frame(self.tile_frame, width=10, height=10, style='Frame1.TFrame')
        self.tile3.rowconfigure((0,1,2,3,4), weight=1)
        self.tile3.columnconfigure((0,1), weight=1)
        self.tile3.grid_propagate(0)

        self.tile3_lab1 = ttk.Label(self.tile3, text='Station 3', style='Frame1.TLabel', font=('Times', 20, 'bold'))
        self.tile3_lab1.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.tile3_lab2 = ttk.Label(self.tile3, text='Active:', style='Frame1.TLabel')
        self.tile3_lab2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.tile3_lab3 = ttk.Label(self.tile3, text='Run Time:', style='Frame1.TLabel')
        self.tile3_lab3.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.tile3_lab4 = ttk.Label(self.tile3, text='Time Goal:', style='Frame1.TLabel')
        self.tile3_lab4.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.tile3_lab5 = ttk.Label(self.tile3, text='Inventory Request:', style='Frame1.TLabel')
        self.tile3_lab5.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        
        self.tile3_vehicleID = ttk.Label(self.tile3, text='None', style='Frame1.TLabel')
        self.tile3_vehicleID.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.tile3_runtime = ttk.Label(self.tile3, text='00:00', style='Frame1.TLabel')
        self.tile3_runtime.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.tile3_goaltime = self.db.selection('stations', 'EstimatedTime', 'StationID=3')
        self.tile3_goaltime = str(self.tile3_goaltime[0][0])
        self.tile3_goaltime =self.tile3_goaltime.split(':')
        self.tile3_goaltime = f'{self.tile3_goaltime[1]}:{self.tile3_goaltime[2]}'

        self.tile3_goaltime_lab = ttk.Label(self.tile3, text=self.tile3_goaltime, style='Frame1.TLabel')
        self.tile3_goaltime_lab.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Convert tile3_goal time to seconds
        self.tile3_goaltime =self.tile3_goaltime.split(':')
        self.tile3_goaltime = int(self.tile3_goaltime[0])*60 + int(self.tile3_goaltime[1])



        # Tile4
        self.tile4 = ttk.Frame(self.tile_frame, width=10, height=10, style='Frame1.TFrame')
        self.tile4.rowconfigure((0,1,2,3,4), weight=1)
        self.tile4.columnconfigure((0,1), weight=1)
        self.tile4.grid_propagate(0)

        self.tile4_lab1 = ttk.Label(self.tile4, text='Station 4', style='Frame1.TLabel', font=('Times', 20, 'bold'))
        self.tile4_lab1.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.tile4_lab2 = ttk.Label(self.tile4, text='Active:', style='Frame1.TLabel')
        self.tile4_lab2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.tile4_lab3 = ttk.Label(self.tile4, text='Run Time:', style='Frame1.TLabel')
        self.tile4_lab3.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.tile4_lab4 = ttk.Label(self.tile4, text='Time Goal:', style='Frame1.TLabel')
        self.tile4_lab4.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.tile4_lab5 = ttk.Label(self.tile4, text='Inventory Request:', style='Frame1.TLabel')
        self.tile4_lab5.grid(row=4, column=0, padx=10, pady=10, sticky='W')

        self.tile4_vehicleID = ttk.Label(self.tile4, text='None', style='Frame1.TLabel')
        self.tile4_vehicleID.grid(row=1, column=1, padx=10, pady=10, sticky='W')
        
        self.tile4_runtime = ttk.Label(self.tile4, text='00:00', style='Frame1.TLabel')
        self.tile4_runtime.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.tile4_goaltime = self.db.selection('stations', 'EstimatedTime', 'StationID=4')
        self.tile4_goaltime = str(self.tile4_goaltime[0][0])
        self.tile4_goaltime = self.tile4_goaltime.split(':')
        self.tile4_goaltime = f'{self.tile4_goaltime[1]}:{self.tile4_goaltime[2]}'

        self.tile4_goaltime_lab = ttk.Label(self.tile4, text=self.tile4_goaltime, style='Frame1.TLabel')
        self.tile4_goaltime_lab.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Convert tile4_goal time to seconds
        self.tile4_goaltime = self.tile4_goaltime.split(':')
        self.tile4_goaltime = int(self.tile4_goaltime[0])*60 + int(self.tile4_goaltime[1])



        # Tile5
        self.tile5 = ttk.Frame(self.tile_frame, width=10, height=10, style='Frame1.TFrame')
        self.tile5.rowconfigure((0,1,2,3,4), weight=1)
        self.tile5.columnconfigure((0,1), weight=1)
        self.tile5.grid_propagate(0)

        self.tile5_lab1 = ttk.Label(self.tile5, text='Station 5', style='Frame1.TLabel', font=('Times', 20, 'bold'))
        self.tile5_lab1.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.tile5_lab2 = ttk.Label(self.tile5, text='Active:', style='Frame1.TLabel')
        self.tile5_lab2.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.tile5_lab3 = ttk.Label(self.tile5, text='Run Time:', style='Frame1.TLabel')
        self.tile5_lab3.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.tile5_lab4 = ttk.Label(self.tile5, text='Time Goal:', style='Frame1.TLabel')
        self.tile5_lab4.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.tile5_lab5 = ttk.Label(self.tile5, text='Inventory Request:', style='Frame1.TLabel')
        self.tile5_lab5.grid(row=4, column=0, padx=10, pady=10, sticky='W')
        
        self.tile5_vehicleID = ttk.Label(self.tile5, text='None', style='Frame1.TLabel')
        self.tile5_vehicleID.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        self.tile5_runtime = ttk.Label(self.tile5, text='00:00', style='Frame1.TLabel')
        self.tile5_runtime.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        self.tile5_goaltime = self.db.selection('stations', 'EstimatedTime', 'StationID=5')
        self.tile5_goaltime = str(self.tile5_goaltime[0][0])
        self.tile5_goaltime = self.tile5_goaltime.split(':')
        self.tile5_goaltime = f'{self.tile5_goaltime[1]}:{self.tile5_goaltime[2]}'

        self.tile5_goaltime_lab = ttk.Label(self.tile5, text=self.tile5_goaltime, style='Frame1.TLabel')
        self.tile5_goaltime_lab.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        # Convert tile5_goal time to seconds
        self.tile5_goaltime = self.tile5_goaltime.split(':')
        self.tile5_goaltime = int(self.tile5_goaltime[0])*60 + int(self.tile5_goaltime[1])

        
        self.tile1.grid(row=0,column=0, sticky='NSEW', padx=10, pady=10)
        self.tile2.grid(row=0,column=1, sticky='NSEW', padx=10, pady=10)
        self.tile3.grid(row=0,column=2, sticky='NSEW', padx=10, pady=10)
        self.tile4.grid(row=0,column=3, sticky='NSEW', padx=10, pady=10)
        self.tile5.grid(row=0,column=4, sticky='NSEW', padx=10, pady=10)

        self.tile_frame.grid(row=1, column=0, rowspan=2, columnspan=3, sticky='NSEW', padx=10, pady=10)


    def HomeTabFrame4(self):
        """
        Creates the middle right frame of the HomeTab. This frame contains information about whether
        the application has associated tablet connected and communicating with the app.
        """
        self.tablet_frame = ttk.LabelFrame(self.master, width=10, height=10, text= "Tablet Online Status")
        
        # Configuring the layout
        self.tablet_frame.grid_propagate(0)
        self.tablet_frame.columnconfigure(0,weight=1)
        self.tablet_frame.columnconfigure(1,weight=2)
        self.tablet_frame.rowconfigure((0,1,2,3,4,5),weight=1)

        # Creating the necessary Labels
        self.tablet_lab1 = ttk.Label(self.tablet_frame, text='Tablet 1').grid(row=0,column=0, sticky=E)
        self.tablet_lab2 = ttk.Label(self.tablet_frame, text='Tablet 2').grid(row=1,column=0, sticky=E)
        self.tablet_lab3 = ttk.Label(self.tablet_frame, text='Tablet 3').grid(row=2,column=0, sticky=E)
        self.tablet_lab4 = ttk.Label(self.tablet_frame, text='Tablet 4').grid(row=3,column=0, sticky=E)
        self.tablet_lab5 = ttk.Label(self.tablet_frame, text='Tablet 5').grid(row=4,column=0, sticky=E)

        # Add two buttons to the frame for connecting one tablet and connecting all tablets
        self.tablet_connect1 = ttk.Button(self.tablet_frame, text='Connect', command=self.connect_tablet1).grid(row=5, column=0, padx=10, pady=10)
        self.tablet_connectall = ttk.Button(self.tablet_frame, text='Connect All', command=self.connect_all_tablets).grid(row=5, column=1, padx=10, pady=10)
    
        """    
        # Initializing the button photos
        self.click_btn = PhotoImage(file='images/redbutton.png')
        self.green_btn = PhotoImage(file='images/greenbutton.png')

        # Placing the buttons on the frame, currently as labels
        self.tablet_light1 = Label(self.tablet_frame, image=self.click_btn).grid(row=0, column=1)
        self.tablet_light2 = Label(self.tablet_frame, image=self.green_btn).grid(row=1, column=1)
        self.tablet_light3 = Label(self.tablet_frame, image=self.green_btn).grid(row=2, column=1)
        self.tablet_light4 = Label(self.tablet_frame, image=self.click_btn).grid(row=3, column=1)
        self.tablet_light5 = Label(self.tablet_frame, image=self.click_btn).grid(row=4, column=1)
        """
        # Placing the frame
        self.tablet_frame.grid(row=1, column=3, sticky='NSEW', padx=10, pady=10)


    def connect_tablet1(self):
        """
        This function is called when the Connect button is pressed. It will attempt to connect to the
        tablet and change the button to a green checkmark if successful.
        """
        global station_list
        thread = Thread(target=settablet_for1, args=(station_list,))
        thread.start()
        thread.join()

        print(station_list)
        print('Connected to a Tablet')
    

    def connect_all_tablets(self):
        """
        This function is called when the Connect All button is pressed. It will attempt to connect to
        all tablets and change the buttons to green checkmarks if successful.
        """
        global station_list
        thread = Thread(target=settablet_for5, args=(station_list,))
        thread.start()
        thread.join()

        print(station_list)
        print('Connecting to all tablets')
    
        
    def HomeTabFrame5(self):
        """
        Creates the bottom right frame of the HomeTab. This frame contains the help button and a 
        quit button. The help button will create another window displaying information about how
        to read and use the HomeTab. The quit button will end the application.
        """
        self.button_frame = ttk.Frame(self.master, width=10, height=10)
        
        # Configuring the layout
        self.button_frame.grid_propagate(0)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure((0,1), weight=1)

        # Placing the buttons.
        # TODO: The Help Button Still needs to be set up
        self.help_button = ttk.Button(self.button_frame, text='Help', command=self.HelpButton).grid(row=0, column=0)
        

        # Adding text box which will contain process information
        self.process_box = Text(self.button_frame, width=10, height=10, wrap=WORD, state='disabled')
        self.process_box.grid(row=1, column=0, sticky='NSEW')

        # Placing the button frame
        self.button_frame.grid(row=2, column=3, sticky='NSEW', padx=10, pady=10)


    def totalTimer(self):
        """
        This function is called every second by the timer. It will update the runtime of the entire program
        """
        #pass
        self.total_time_num += 1
        # Format the time MM:SS
        # timedelta(seconds=current_runtime)), '%H:%M:%S').strftime('%M:%S')
        self.total_time.config(text=str(timedelta(seconds=self.total_time_num)))
        self.master.after(1000, self.totalTimer)


    def runTimer(self):
        """
        This function is called every second by the timer. It will update the runtime of the current vehicle
        """
        #pass
        # Check to see if there are any active stations
        if 1 in self.active_stations:  
            self.run_time_num += 1
             # Format the time H:MM:SS
            self.run_time.config(text=str(timedelta(seconds=self.run_time_num)))
            self.run_time.after(1000, self.runTimer)
        else:
            self.run_time.after(1000, self.runTimer)


    def fullProductiveTimer(self):
        """
        This function is called every second by the timer. It will update the runtime of the current vehicle
        """
        #pass
        # Check to see if all stations are active
        if self.active_stations == [1,1,1,1,1]:
            self.full_prod_time_num += 1
             # Format the time H:MM:SS
            self.full_prod_time.config(text=str(timedelta(seconds=self.full_prod_time_num)))
            self.full_prod_time.after(1000, self.fullProductiveTimer)
        else:
            self.full_prod_time.after(1000, self.fullProductiveTimer)


    def updateAvailabilityBar(self):
        """
        Checks to see if stations are active, the progress bar will decrease if a station is active
        """
        #pass
        self.availability_bar['value'] = 100
        for i in range(5):
            if self.active_stations[i] == 1:
                self.availability_bar['value'] -= 20
            
        self.availability_bar.after(1000, self.updateAvailabilityBar)


    def HelpButton(self):
        HelpWindow("home")


    def updateTile1BG(self, stage):
        if stage == 1:
            self.tile1.config(style='Frame2.TFrame')
            self.tile1_lab1.config(style='Frame2.TLabel')
            self.tile1_lab2.config(style='Frame2.TLabel')
            self.tile1_lab3.config(style='Frame2.TLabel')
            self.tile1_lab4.config(style='Frame2.TLabel')
            self.tile1_lab5.config(style='Frame2.TLabel')
            self.tile1_vehicleID.config(style='Frame2.TLabel')
            self.tile1_runtime.config(style='Frame2.TLabel')
            self.tile1_goaltime_lab.config(style='Frame2.TLabel')
        elif stage == 2:
            self.tile1.config(style='Frame3.TFrame')
            self.tile1_lab1.config(style='Frame3.TLabel')
            self.tile1_lab2.config(style='Frame3.TLabel')
            self.tile1_lab3.config(style='Frame3.TLabel')
            self.tile1_lab4.config(style='Frame3.TLabel')
            self.tile1_lab5.config(style='Frame3.TLabel')
            self.tile1_vehicleID.config(style='Frame3.TLabel')
            self.tile1_runtime.config(style='Frame3.TLabel')
            self.tile1_goaltime_lab.config(style='Frame3.TLabel')
        elif stage == 3:
            self.tile1.config(style='Frame4.TFrame')
            self.tile1_lab1.config(style='Frame4.TLabel')
            self.tile1_lab2.config(style='Frame4.TLabel')
            self.tile1_lab3.config(style='Frame4.TLabel')
            self.tile1_lab4.config(style='Frame4.TLabel')
            self.tile1_lab5.config(style='Frame4.TLabel')
            self.tile1_vehicleID.config(style='Frame4.TLabel')
            self.tile1_runtime.config(style='Frame4.TLabel')
            self.tile1_goaltime_lab.config(style='Frame4.TLabel')
        elif stage == 4:
            self.tile1.config(style='Frame5.TFrame')
            self.tile1_lab1.config(style='Frame5.TLabel')
            self.tile1_lab2.config(style='Frame5.TLabel')
            self.tile1_lab3.config(style='Frame5.TLabel')
            self.tile1_lab4.config(style='Frame5.TLabel')
            self.tile1_lab5.config(style='Frame5.TLabel')
            self.tile1_vehicleID.config(style='Frame5.TLabel')
            self.tile1_runtime.config(style='Frame5.TLabel')
            self.tile1_goaltime_lab.config(style='Frame5.TLabel')
        elif stage == 5:
            self.tile1.config(style='Frame6.TFrame')
            self.tile1_lab1.config(style='Frame6.TLabel')
            self.tile1_lab2.config(style='Frame6.TLabel')
            self.tile1_lab3.config(style='Frame6.TLabel')
            self.tile1_lab4.config(style='Frame6.TLabel')
            self.tile1_lab5.config(style='Frame6.TLabel')
            self.tile1_vehicleID.config(style='Frame6.TLabel')
            self.tile1_runtime.config(style='Frame6.TLabel')
            self.tile1_goaltime_lab.config(style='Frame6.TLabel')
        else:
            self.tile1.config(style='Frame1.TFrame')
            self.tile1_lab1.config(style='Frame1.TLabel')
            self.tile1_lab2.config(style='Frame1.TLabel')
            self.tile1_lab3.config(style='Frame1.TLabel')
            self.tile1_lab4.config(style='Frame1.TLabel')
            self.tile1_lab5.config(style='Frame1.TLabel')
            self.tile1_vehicleID.config(style='Frame1.TLabel')
            self.tile1_runtime.config(style='Frame1.TLabel')
            self.tile1_goaltime_lab.config(style='Frame1.TLabel')


    def updateTile2BG(self, stage):
        if stage == 1:
            self.tile2.config(style='Frame2.TFrame')
            self.tile2_lab1.config(style='Frame2.TLabel')
            self.tile2_lab2.config(style='Frame2.TLabel')
            self.tile2_lab3.config(style='Frame2.TLabel')
            self.tile2_lab4.config(style='Frame2.TLabel')
            self.tile2_lab5.config(style='Frame2.TLabel')
            self.tile2_vehicleID.config(style='Frame2.TLabel')
            self.tile2_runtime.config(style='Frame2.TLabel')
            self.tile2_goaltime_lab.config(style='Frame2.TLabel')
        elif stage == 2:
            self.tile2.config(style='Frame3.TFrame')
            self.tile2_lab1.config(style='Frame3.TLabel')
            self.tile2_lab2.config(style='Frame3.TLabel')
            self.tile2_lab3.config(style='Frame3.TLabel')
            self.tile2_lab4.config(style='Frame3.TLabel')
            self.tile2_lab5.config(style='Frame3.TLabel')
            self.tile2_vehicleID.config(style='Frame3.TLabel')
            self.tile2_runtime.config(style='Frame3.TLabel')
            self.tile2_goaltime_lab.config(style='Frame3.TLabel')
        elif stage == 3:
            self.tile2.config(style='Frame4.TFrame')
            self.tile2_lab1.config(style='Frame4.TLabel')
            self.tile2_lab2.config(style='Frame4.TLabel')
            self.tile2_lab3.config(style='Frame4.TLabel')
            self.tile2_lab4.config(style='Frame4.TLabel')
            self.tile2_lab5.config(style='Frame4.TLabel')
            self.tile2_vehicleID.config(style='Frame4.TLabel')
            self.tile2_runtime.config(style='Frame4.TLabel')
            self.tile2_goaltime_lab.config(style='Frame4.TLabel')
        elif stage == 4:
            self.tile2.config(style='Frame5.TFrame')
            self.tile2_lab1.config(style='Frame5.TLabel')
            self.tile2_lab2.config(style='Frame5.TLabel')
            self.tile2_lab3.config(style='Frame5.TLabel')
            self.tile2_lab4.config(style='Frame5.TLabel')
            self.tile2_lab5.config(style='Frame5.TLabel')
            self.tile2_vehicleID.config(style='Frame5.TLabel')
            self.tile2_runtime.config(style='Frame5.TLabel')
            self.tile2_goaltime_lab.config(style='Frame5.TLabel')
        elif stage == 5:
            self.tile2.config(style='Frame6.TFrame')
            self.tile2_lab1.config(style='Frame6.TLabel')
            self.tile2_lab2.config(style='Frame6.TLabel')
            self.tile2_lab3.config(style='Frame6.TLabel')
            self.tile2_lab4.config(style='Frame6.TLabel')
            self.tile2_lab5.config(style='Frame6.TLabel')
            self.tile2_vehicleID.config(style='Frame6.TLabel')
            self.tile2_runtime.config(style='Frame6.TLabel')
            self.tile2_goaltime_lab.config(style='Frame6.TLabel')
        else:
            self.tile2.config(style='Frame1.TFrame')
            self.tile2_lab1.config(style='Frame1.TLabel')
            self.tile2_lab2.config(style='Frame1.TLabel')
            self.tile2_lab3.config(style='Frame1.TLabel')
            self.tile2_lab4.config(style='Frame1.TLabel')
            self.tile2_lab5.config(style='Frame1.TLabel')
            self.tile2_vehicleID.config(style='Frame1.TLabel')
            self.tile2_runtime.config(style='Frame1.TLabel')
            self.tile2_goaltime_lab.config(style='Frame1.TLabel')
    

    def updateTile3BG(self, stage):
        if stage == 1:
            self.tile3.config(style='Frame2.TFrame')
            self.tile3_lab1.config(style='Frame2.TLabel')
            self.tile3_lab2.config(style='Frame2.TLabel')
            self.tile3_lab3.config(style='Frame2.TLabel')
            self.tile3_lab4.config(style='Frame2.TLabel')
            self.tile3_lab5.config(style='Frame2.TLabel')
            self.tile3_vehicleID.config(style='Frame2.TLabel')
            self.tile3_runtime.config(style='Frame2.TLabel')
            self.tile3_goaltime_lab.config(style='Frame2.TLabel')
        elif stage == 2:
            self.tile3.config(style='Frame3.TFrame')
            self.tile3_lab1.config(style='Frame3.TLabel')
            self.tile3_lab2.config(style='Frame3.TLabel')
            self.tile3_lab3.config(style='Frame3.TLabel')
            self.tile3_lab4.config(style='Frame3.TLabel')
            self.tile3_lab5.config(style='Frame3.TLabel')
            self.tile3_vehicleID.config(style='Frame3.TLabel')
            self.tile3_runtime.config(style='Frame3.TLabel')
            self.tile3_goaltime_lab.config(style='Frame3.TLabel')
        elif stage == 3:
            self.tile3.config(style='Frame4.TFrame')
            self.tile3_lab1.config(style='Frame4.TLabel')
            self.tile3_lab2.config(style='Frame4.TLabel')
            self.tile3_lab3.config(style='Frame4.TLabel')
            self.tile3_lab4.config(style='Frame4.TLabel')
            self.tile3_lab5.config(style='Frame4.TLabel')
            self.tile3_vehicleID.config(style='Frame4.TLabel')
            self.tile3_runtime.config(style='Frame4.TLabel')
            self.tile3_goaltime_lab.config(style='Frame4.TLabel')
        elif stage == 4:
            self.tile3.config(style='Frame5.TFrame')
            self.tile3_lab1.config(style='Frame5.TLabel')
            self.tile3_lab2.config(style='Frame5.TLabel')
            self.tile3_lab3.config(style='Frame5.TLabel')
            self.tile3_lab4.config(style='Frame5.TLabel')
            self.tile3_lab5.config(style='Frame5.TLabel')
            self.tile3_vehicleID.config(style='Frame5.TLabel')
            self.tile3_runtime.config(style='Frame5.TLabel')
            self.tile3_goaltime_lab.config(style='Frame5.TLabel')
        elif stage == 5:
            self.tile3.config(style='Frame6.TFrame')
            self.tile3_lab1.config(style='Frame6.TLabel')
            self.tile3_lab2.config(style='Frame6.TLabel')
            self.tile3_lab3.config(style='Frame6.TLabel')
            self.tile3_lab4.config(style='Frame6.TLabel')
            self.tile3_lab5.config(style='Frame6.TLabel')
            self.tile3_vehicleID.config(style='Frame6.TLabel')
            self.tile3_runtime.config(style='Frame6.TLabel')
            self.tile3_goaltime_lab.config(style='Frame6.TLabel')
        else:
            self.tile3.config(style='Frame1.TFrame')
            self.tile3_lab1.config(style='Frame1.TLabel')
            self.tile3_lab2.config(style='Frame1.TLabel')
            self.tile3_lab3.config(style='Frame1.TLabel')
            self.tile3_lab4.config(style='Frame1.TLabel')
            self.tile3_lab5.config(style='Frame1.TLabel')
            self.tile3_vehicleID.config(style='Frame1.TLabel')
            self.tile3_runtime.config(style='Frame1.TLabel')
            self.tile3_goaltime_lab.config(style='Frame1.TLabel')


    def updateTile4BG(self, stage):
        if stage == 1:
            self.tile4.config(style='Frame2.TFrame')
            self.tile4_lab1.config(style='Frame2.TLabel')
            self.tile4_lab2.config(style='Frame2.TLabel')
            self.tile4_lab3.config(style='Frame2.TLabel')
            self.tile4_lab4.config(style='Frame2.TLabel')
            self.tile4_lab5.config(style='Frame2.TLabel')
            self.tile4_vehicleID.config(style='Frame2.TLabel')
            self.tile4_runtime.config(style='Frame2.TLabel')
            self.tile4_goaltime_lab.config(style='Frame2.TLabel')
        elif stage == 2:
            self.tile4.config(style='Frame3.TFrame')
            self.tile4_lab1.config(style='Frame3.TLabel')
            self.tile4_lab2.config(style='Frame3.TLabel')
            self.tile4_lab3.config(style='Frame3.TLabel')
            self.tile4_lab4.config(style='Frame3.TLabel')
            self.tile4_lab5.config(style='Frame3.TLabel')
            self.tile4_vehicleID.config(style='Frame3.TLabel')
            self.tile4_runtime.config(style='Frame3.TLabel')
            self.tile4_goaltime_lab.config(style='Frame3.TLabel')
        elif stage == 3:
            self.tile4.config(style='Frame4.TFrame')
            self.tile4_lab1.config(style='Frame4.TLabel')
            self.tile4_lab2.config(style='Frame4.TLabel')
            self.tile4_lab3.config(style='Frame4.TLabel')
            self.tile4_lab4.config(style='Frame4.TLabel')
            self.tile4_lab5.config(style='Frame4.TLabel')
            self.tile4_vehicleID.config(style='Frame4.TLabel')
            self.tile4_runtime.config(style='Frame4.TLabel')
            self.tile4_goaltime_lab.config(style='Frame4.TLabel')
        elif stage == 4:
            self.tile4.config(style='Frame5.TFrame')
            self.tile4_lab1.config(style='Frame5.TLabel')
            self.tile4_lab2.config(style='Frame5.TLabel')
            self.tile4_lab3.config(style='Frame5.TLabel')
            self.tile4_lab4.config(style='Frame5.TLabel')
            self.tile4_lab5.config(style='Frame5.TLabel')
            self.tile4_vehicleID.config(style='Frame5.TLabel')
            self.tile4_runtime.config(style='Frame5.TLabel')
            self.tile4_goaltime_lab.config(style='Frame5.TLabel')
        elif stage == 5:
            self.tile4.config(style='Frame6.TFrame')
            self.tile4_lab1.config(style='Frame6.TLabel')
            self.tile4_lab2.config(style='Frame6.TLabel')
            self.tile4_lab3.config(style='Frame6.TLabel')
            self.tile4_lab4.config(style='Frame6.TLabel')
            self.tile4_lab5.config(style='Frame6.TLabel')
            self.tile4_vehicleID.config(style='Frame6.TLabel')
            self.tile4_runtime.config(style='Frame6.TLabel')
            self.tile4_goaltime_lab.config(style='Frame6.TLabel')
        else:
            self.tile4.config(style='Frame1.TFrame')
            self.tile4_lab1.config(style='Frame1.TLabel')
            self.tile4_lab2.config(style='Frame1.TLabel')
            self.tile4_lab3.config(style='Frame1.TLabel')
            self.tile4_lab4.config(style='Frame1.TLabel')
            self.tile4_lab5.config(style='Frame1.TLabel')
            self.tile4_vehicleID.config(style='Frame1.TLabel')
            self.tile4_runtime.config(style='Frame1.TLabel')
            self.tile4_goaltime_lab.config(style='Frame1.TLabel')


    def updateTile5BG(self, stage):
        if stage == 1:
            self.tile5.config(style='Frame2.TFrame')
            self.tile5_lab1.config(style='Frame2.TLabel')
            self.tile5_lab2.config(style='Frame2.TLabel')
            self.tile5_lab3.config(style='Frame2.TLabel')
            self.tile5_lab4.config(style='Frame2.TLabel')
            self.tile5_lab5.config(style='Frame2.TLabel')
            self.tile5_vehicleID.config(style='Frame2.TLabel')
            self.tile5_runtime.config(style='Frame2.TLabel')
            self.tile5_goaltime_lab.config(style='Frame2.TLabel')
        elif stage == 2:
            self.tile5.config(style='Frame3.TFrame')
            self.tile5_lab1.config(style='Frame3.TLabel')
            self.tile5_lab2.config(style='Frame3.TLabel')
            self.tile5_lab3.config(style='Frame3.TLabel')
            self.tile5_lab4.config(style='Frame3.TLabel')
            self.tile5_lab5.config(style='Frame3.TLabel')
            self.tile5_vehicleID.config(style='Frame3.TLabel')
            self.tile5_runtime.config(style='Frame3.TLabel')
            self.tile5_goaltime_lab.config(style='Frame3.TLabel')
        elif stage == 3:
            self.tile5.config(style='Frame4.TFrame')
            self.tile5_lab1.config(style='Frame4.TLabel')
            self.tile5_lab2.config(style='Frame4.TLabel')
            self.tile5_lab3.config(style='Frame4.TLabel')
            self.tile5_lab4.config(style='Frame4.TLabel')
            self.tile5_lab5.config(style='Frame4.TLabel')
            self.tile5_vehicleID.config(style='Frame4.TLabel')
            self.tile5_runtime.config(style='Frame4.TLabel')
            self.tile5_goaltime_lab.config(style='Frame4.TLabel')
        elif stage == 4:
            self.tile5.config(style='Frame5.TFrame')
            self.tile5_lab1.config(style='Frame5.TLabel')
            self.tile5_lab2.config(style='Frame5.TLabel')
            self.tile5_lab3.config(style='Frame5.TLabel')
            self.tile5_lab4.config(style='Frame5.TLabel')
            self.tile5_lab5.config(style='Frame5.TLabel')
            self.tile5_vehicleID.config(style='Frame5.TLabel')
            self.tile5_runtime.config(style='Frame5.TLabel')
            self.tile5_goaltime_lab.config(style='Frame5.TLabel')
        elif stage == 5:
            self.tile5.config(style='Frame6.TFrame')
            self.tile5_lab1.config(style='Frame6.TLabel')
            self.tile5_lab2.config(style='Frame6.TLabel')
            self.tile5_lab3.config(style='Frame6.TLabel')
            self.tile5_lab4.config(style='Frame6.TLabel')
            self.tile5_lab5.config(style='Frame6.TLabel')
            self.tile5_vehicleID.config(style='Frame6.TLabel')
            self.tile5_runtime.config(style='Frame6.TLabel')
            self.tile5_goaltime_lab.config(style='Frame6.TLabel')
        else:
            self.tile5.config(style='Frame1.TFrame')
            self.tile5_lab1.config(style='Frame1.TLabel')
            self.tile5_lab2.config(style='Frame1.TLabel')
            self.tile5_lab3.config(style='Frame1.TLabel')
            self.tile5_lab4.config(style='Frame1.TLabel')
            self.tile5_lab5.config(style='Frame1.TLabel')
            self.tile5_vehicleID.config(style='Frame1.TLabel')
            self.tile5_runtime.config(style='Frame1.TLabel')
            self.tile5_goaltime_lab.config(style='Frame1.TLabel')


class ProcessTab:
    def __init__(self, master, db):
        # When the Process tab is initialized, save the width and height of the notebook frame
        self.master = master
        self.db = db

        # Configuring the layout for the different frames
        self.master.columnconfigure((0,1,2,3),weight=1)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=3)

        # Create the frames
        self.ProcessFrame1() 
        self.ProcessFrame2()
        self.ProcessFrame3()
        self.ProcessFrame4()

        # Query has to happen after frames are build due to the fact that they will impact
        # widgets in other frames
        self.process_box.bind("<<ComboboxSelected>>", lambda event: self.ProcessQuery(event))
        self.statID.bind("<<ComboboxSelected>>", self.StationQuery)


    def ProcessFrame1(self):
        # Create the Frame
        self.process_frame = ttk.LabelFrame(self.master, width=10, height=10, text='Processes')
        self.process_frame.grid_propagate(0)

        # Configure the frame for widgets
        self.process_frame.columnconfigure(0, weight=1)
        self.process_frame.columnconfigure(1, weight=1)
        self.process_frame.rowconfigure((0,1,2), weight=1)
        self.process_frame.rowconfigure(3, weight=2)

        processes = self.db.selection('Process','ProcessName')
        processes = [i[0] for i in processes]
        self.process_box = ttk.Combobox(self.process_frame,
                values=processes, width=20, height=5, state='readonly')
        self.process_box.grid(row=0, column=0, sticky='W', padx=10, pady=10)

        ttk.Label(self.process_frame, text='Process ID:').grid(row=1, column=0,
                sticky='W', padx=10, pady=10)
        ttk.Label(self.process_frame, text='Process Description:').grid(row=2,column=0,
                sticky='W', padx=10, pady=10)

        self.process_lab = ttk.Label(self.process_frame, text='')
        self.process_lab.grid(row=1, column=1, sticky='W', pady=10)
        self.desc_lab = ttk.Label(self.process_frame, text='')
        self.desc_lab.grid(row=3, column=0, sticky='W', padx=10, pady=10)


        # Place the listboxframe onto the process tab
        self.process_frame.grid(row=0, column=0, columnspan=2, sticky='NSEW', padx=20, pady=20)


    def ProcessFrame2(self):
        # Create the frame for the Process information
        self.process_info_frame = ttk.LabelFrame(self.master, width=10, height=10, text="Process Information")
        self.process_info_frame.grid_propagate(0)
        self.process_info_frame.columnconfigure((0,1,2,3), weight=1)
        self.process_info_frame.rowconfigure((0,1), weight=1)

        # NumStations
        ttk.Label(self.process_info_frame, text='Number of Stations:').grid(row=0, column=0,
                padx=10, pady=10, sticky='W')
        self.numstations = ttk.Label(self.process_info_frame, text='')
        self.numstations.grid(row=0, column=1, padx=10, pady=10, sticky='W')

        # DateCreated
        ttk.Label(self.process_info_frame, text='Date Created:').grid(row=1, column=0,
                padx=10, pady=10, sticky='W')
        self.proc_creation_date = ttk.Label(self.process_info_frame, text='')
        self.proc_creation_date.grid(row=1,column=1, padx=10,pady=10, sticky='W')

        # TimesCompleted
        ttk.Label(self.process_info_frame, text='Times Completed:').grid(row=0, column=2,
                padx=10, pady=10, sticky='W')
        self.proc_completion = ttk.Label(self.process_info_frame, text='')
        self.proc_completion.grid(row=0, column=3, padx=10, pady=10, sticky='W')

        # TimesRan
        ttk.Label(self.process_info_frame, text='Times Ran:').grid(row=1, column=2,
                padx=10, pady=10, sticky='W')
        self.proc_ran = ttk.Label(self.process_info_frame, text='')
        self.proc_ran.grid(row=1, column=3, padx=10, pady=10, sticky='W')

        # Finally place frame
        self.process_info_frame.grid(row=0, column=2, columnspan=2, sticky='NSEW', padx=20, pady=20)


    def ProcessFrame3(self):
        # Create and configure ttk.LabelFrame for layout
        self.station_frame = ttk.LabelFrame(self.master, width=10, height=10, text='Stations')
    
        self.station_frame.grid_propagate(0)
        self.station_frame.columnconfigure((0,1,2,3), weight=1)
        self.station_frame.rowconfigure((0,1,2,3,4), weight=1)
    
        # StationID combobox
        self.statID = ttk.Combobox(self.station_frame, values=[], width=20, height=20, state='readonly')
        self.statID.grid(row=0, column=0, sticky='W', padx=10, pady=10)

        # ProcessID pulled from the process selected
        ttk.Label(self.station_frame, text="ProcessID:").grid(row=1, column=0, sticky='W', padx=10, pady=10)
        self.stat_procID = ttk.Label(self.station_frame, text='')
        self.stat_procID.grid(row=1, column=1, sticky='W', padx=10, pady=10)

        # NumSteps
        ttk.Label(self.station_frame, text='Number Of Steps:').grid(row=2, column=0, sticky='W', padx=10, pady=10)
        self.stat_steps = ttk.Label(self.station_frame, text='')
        self.stat_steps.grid(row=2, column=1, sticky='W', padx=10, pady=10)

        # EstimatedTime
        ttk.Label(self.station_frame, text='Estimated Time:').grid(row=1, column=2, sticky='W', padx=10, pady=10)
        self.stat_esttime = ttk.Label(self.station_frame, text='')
        self.stat_esttime.grid(row=1, column=3, sticky='W', padx=10, pady=10)

        # DateCreated
        ttk.Label(self.station_frame, text='Date Created:').grid(row=2, column=2, sticky='W', padx=10, pady=10)
        self.stat_date = ttk.Label(self.station_frame, text='')
        self.stat_date.grid(row=2, column=3, sticky='W', padx=10, pady=10)

        # StationDesc
        ttk.Label(self.station_frame, text='Station Description:').grid(row=3, column=0, sticky='W', padx=10, pady=10)
        self.stat_desc = ttk.Label(self.station_frame, text='')
        self.stat_desc.grid(row=4, column=0, columnspan=4, sticky='W', padx=10, pady=10)

        # AverageTime
        ttk.Label(self.station_frame, text='Average Time:').grid(row=3, column=2, sticky='W', padx=10, pady=10)
        self.stat_avgtime = ttk.Label(self.station_frame, text='')
        self.stat_avgtime.grid(row=3, column=3, sticky='W', padx=10, pady=10)
        
        self.station_frame.grid(row=1,column=0, columnspan=3, sticky='NSEW', padx=20, pady=20)


    def ProcessFrame4(self):
        # Create and configure ttk.LabelFrame
        self.step_frame = ttk.LabelFrame(self.master, width=10, height=10, text='Steps')
        self.step_frame.grid_propagate(0)
        self.step_frame.columnconfigure(0, weight=1)
        self.step_frame.rowconfigure(0, weight=1)


        # Create a text widget for the step description
        self.step_desc = Text(self.step_frame, width=50, height=10, wrap='word', state='disabled', font=('Times', 16), bg='#dcdad5')
        # Grid the text widget making it extend the size of the frame
        self.step_desc.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)



        self.step_frame.grid(row=1, column=3, sticky='NSEW', padx=20, pady=20)


    def ProcessQuery(self, event):
        # Query for process information
        temp = event.widget.get()
        info = self.db.selection('Process', '*', f'ProcessName=\'{temp}\'')
        info = info[0]
        self.process_lab.config(text=str(info[0]))
        self.desc_lab.config(text=str(info[3]))
        self.numstations.config(text=str(info[2]))
        self.proc_creation_date.config(text=str(info[4]).split(' ')[0])
        self.proc_completion.config(text=str(info[5]))
        self.proc_ran.config(text=str(info[6]))
        
        # Getting the proc ID for the station information
        info = self.db.selection('Stations', 'StationID', f'ProcessID={info[0]}')
        self.statID.config(values=[i[0] for i in info])


    def StationQuery(self, event):
        # Query for station information
        temp = event.widget.get()
        info = self.db.selection('Stations', '*', f'StationID={temp}')
        info = info[0]
        self.stat_procID.config(text=str(info[1]))
        self.stat_steps.config(text=str(info[2]))
        self.stat_esttime.config(text=str(info[3]))
        self.stat_date.config(text=str(info[4]))
        self.stat_desc.config(text=str(info[5]))
        self.stat_avgtime.config(text=str(info[6]))

        # Run the step query
        self.StepQuery(temp)


    def StepQuery(self, stationID):
        # Query for step information
        info = self.db.selection('Steps', '*', f'StationID={stationID}')
        
        # Clear the text widget
        self.step_desc.config(state='normal')
        self.step_desc.delete('1.0', 'end')

        # Insert the step information
        count=1
        for i in info:
            # Insert the step number
            self.step_desc.insert('end', f'Step {count}: ')
            # Insert the step description
            self.step_desc.insert('end', f'{i[2]}')
            # Insert a new line
            self.step_desc.insert('end', '\n\n')
            count+=1
        
        # Disable the text widget
        self.step_desc.config(state='disabled')


class QualityTab:
    def __init__(self, master, db, session_cars: dict):
        self.master = master
        self.db = db
        self.session_cars = session_cars

        # Configure the master frame
        self.master.rowconfigure((0,1), weight=1)
        self.master.columnconfigure((0,1), weight=1)
        self.master.grid_propagate(0)

        # Create functions to create 4 frames
        self.QualityFrame1()
        self.QualityFrame2()
        self.QualityFrame3()
        self.QualityFrame4()

    def QualityFrame1(self):
        self.quality_frame1 = ttk.LabelFrame(self.master, text = 'Session Vehicles', width=10, height=10)

        # Configure the frame
        self.quality_frame1.rowconfigure((0,1), weight=1)
        self.quality_frame1.columnconfigure((0,1), weight=1)
        self.quality_frame1.grid_propagate(0)



        # Create combo box containing all the vehicle IDs in the session_cars
        ttk.Label(self.quality_frame1, text='Session Vehicle IDs:').grid(row=0, column=0, sticky='W', padx=10, pady=10)
        self.quality_frame1.vehicleID = ttk.Combobox(self.quality_frame1, values=[list(self.session_cars.keys())], width=20, height=20, state='readonly')
        self.quality_frame1.vehicleID.grid(row=1, column=0, sticky='NW', padx=10, pady=10)

        # Add button next to the combo box that will be used to select the vehicle that is selected in the combo box. Command self.updateVehicleInfo given the selected Vehicle ID as an argument
        self.quality_frame1.selectVehicle = ttk.Button(self.quality_frame1, text='Select Vehicle', command=lambda: self.updateVehicleInfo(self.quality_frame1.vehicleID.get()))
        self.quality_frame1.selectVehicle.grid(row=1, column=1, sticky='NW', padx=10, pady=10)

        self.quality_frame1.grid(row=0, column=0, sticky='NSEW', padx=20, pady=20)


    def QualityFrame2(self):
        self.quality_frame2 = ttk.LabelFrame(self.master, text='Selected Vehicle Information', width=10, height=10)

        # Configure the frame
        self.quality_frame2.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.quality_frame2.columnconfigure((0,1), weight=1)
        self.quality_frame2.grid_propagate(0)


        # Add labels to the frame to display the station times for the for the selected vehicle
        ttk.Label(self.quality_frame2, text='Selected Vehicle ID:').grid(row=0, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station Times:').grid(row=1, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station 1:').grid(row=2, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station 2:').grid(row=3, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station 3:').grid(row=4, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station 4:').grid(row=5, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='Station 5:').grid(row=6, column=0, sticky='W', padx=10, pady=10)
        ttk.Label(self.quality_frame2, text='TotalTime:').grid(row=7, column=0, sticky='W', padx=10, pady=10)

        # Add blank labels to be filled with the station times for the selected vehicle
        self.vehicleID_lab = ttk.Label(self.quality_frame2, text='')
        self.vehicleID_lab.grid(row=0, column=1, sticky='W', padx=10, pady=10)
        self.station1_time = ttk.Label(self.quality_frame2, text='')
        self.station1_time.grid(row=2, column=1, sticky='W', padx=10, pady=10)
        self.station2_time = ttk.Label(self.quality_frame2, text='')
        self.station2_time.grid(row=3, column=1, sticky='W', padx=10, pady=10)
        self.station3_time = ttk.Label(self.quality_frame2, text='')
        self.station3_time.grid(row=4, column=1, sticky='W', padx=10, pady=10)
        self.station4_time = ttk.Label(self.quality_frame2, text='')
        self.station4_time.grid(row=5, column=1, sticky='W', padx=10, pady=10)
        self.station5_time = ttk.Label(self.quality_frame2, text='')
        self.station5_time.grid(row=6, column=1, sticky='W', padx=10, pady=10)
        self.total_time = ttk.Label(self.quality_frame2, text='')
        self.total_time.grid(row=7, column=1, sticky='W', padx=10, pady=10)


        self.quality_frame2.grid(row=0, column=1, sticky='NSEW', padx=20, pady=20)


    def QualityFrame3(self):
        self.quality_frame3 = ttk.LabelFrame(self.master, width=10, height=10)

        # Configure the frame
        self.quality_frame3.rowconfigure(0, weight=1)
        self.quality_frame3.columnconfigure((0,1,2,3), weight=1)
        self.quality_frame3.grid_propagate(0)

        # Add a button to the frame that will print the data for the selected vehicle
        self.quality_frame3.printData = ttk.Button(self.quality_frame3, text='Print Data')
        
        # Add a button to the frame that will allow the user to unaccept the selected vehicle
        self.quality_frame3.unaccept = ttk.Button(self.quality_frame3, text='Unaccept')

        # Add a button to export the data to a csv file
        self.quality_frame3.export = ttk.Button(self.quality_frame3, text='Export Data')

        # Add a help button to the frame that will display a help window
        self.quality_frame3.help = ttk.Button(self.quality_frame3, text='Help')


        self.quality_frame3.printData.grid(row=0, column=0, padx=20, pady=20)
        self.quality_frame3.unaccept.grid(row=0, column=1, padx=20, pady=20)
        self.quality_frame3.export.grid(row=0, column=2, padx=20, pady=20)
        self.quality_frame3.help.grid(row=0, column=3, padx=20, pady=20)


        self.quality_frame3.grid(row=1, column=0, sticky='NSEW', padx=20, pady=20)


    def QualityFrame4(self):
        self.quality_frame4 = ttk.LabelFrame(self.master, width=10, height=10)
        self.quality_frame4.grid_propagate(0)


        self.quality_frame4.grid(row=1, column=1, sticky='NSEW', padx=20, pady=20)
    

    def updateList(self):
        """
        Updates the list of vehicles in the session
        """
        self.quality_frame1.vehicleID.config(values=list(self.session_cars.keys()))


    def updateVehicleInfo(self, vehicleID):
        """
        Updates the information for the selected vehicle. Calls the database to get the time information from the vehicle selected
        """
        info = self.db.selection('ProductTime', '*', f'ProductID=\'{vehicleID}\'')
        self.vehicleID_lab.config(text=vehicleID)

        # Configure the time information in the format of HH:MM:SS.mm
        temp = str(info[0][1])
        self.station1_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')
        temp = str(info[0][2])
        self.station2_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')
        temp = str(info[0][3])
        self.station3_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')
        temp = str(info[0][4])
        self.station4_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')
        temp = str(info[0][5])
        self.station5_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')
        temp = str(info[0][6])
        self.total_time.config(text=f'{temp[0:1]}:{temp[2:4]}:{temp[5:7]}.{temp[8:10]}')


class DBTab:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.rowconfigure(0,weight=1)
        self.master.columnconfigure(0,weight=1)

        self.DBFrame1()

        # Selecting the Combobox
        self.db_box.bind("<<ComboboxSelected>>", lambda event: self.DBQuery(event))
        


    def DBFrame1(self):
        self.db_frame = ttk.Frame(self.master, width=10, height=10)
        self.db_frame.rowconfigure(0,weight=1)
        self.db_frame.rowconfigure(1,weight=4)
        self.db_frame.columnconfigure((0,1,2,3),weight=1)

        info = self.db.getTables()
        self.db_box = ttk.Combobox(self.db_frame, values = [i[0] for i in info], width=5, state='readonly')
        self.db_box.grid(row=0,column=0, sticky='EW', padx=5)

        self.select_btn = ttk.Button(self.db_frame, text='Select', command = lambda: self.selectBox(self.db_box.get()))
        self.export_btn = ttk.Button(self.db_frame, text='Export', command = lambda: self.exportBox(self.db_box.get()))

        self.select_btn.grid(row=0, column=1, padx=5, sticky='W')
        self.export_btn.grid(row=0, column=3, padx=5, sticky='W')

        self.db_view = ttk.Treeview(self.db_frame, columns=['Industry', '4', '.', '0'], show='headings')
        self.db_view.heading('Industry', text='Industry')
        self.db_view.heading('4', text='4')
        self.db_view.heading('.', text='.')
        self.db_view.heading('0', text='0')
        
        self.db_view.grid(row=1, column=0, columnspan=4, sticky='NSEW', padx=10)
        self.db_frame.grid(row=0,column=0, sticky='NSEW')


    def DBQuery(self, event):
        for item in self.db_view.get_children():
            self.db_view.delete(item)
        temp = event.widget.get()
        columns = self.db.showColumns(temp)
        columns = [i[0] for i in columns]
        self.db_view["columns"] = columns
        for i in range(len(columns)):
                self.db_view.column(i, anchor='c', stretch=YES)
                self.db_view.heading(i, text=columns[i])
        data = self.db.selection(temp, '*')
        for row in data:
            # Check the type of each row
            for item in row:
                if type(item) == timedelta:
                    row = list(row)
                    row[row.index(item)] = str(item)[0:10]
                    row = tuple(row)
            
            self.db_view.insert('', 'end', values=row)
    
    def selectBox(self, selected):
        for item in self.db_view.get_children():
            self.db_view.delete(item)
        columns = self.db.showColumns(selected)
        columns = [i[0] for i in columns]
        self.db_view["columns"] = columns
        for i in range(len(columns)):
                self.db_view.column(i, anchor='c', stretch=YES)
                self.db_view.heading(i, text=columns[i])
        data = self.db.selection(selected, '*')
        for row in data:
            # Check the type of each row
            for item in row:
                if type(item) == timedelta:
                    row = list(row)
                    row[row.index(item)] = str(item)[0:10]
                    row = tuple(row)
            self.db_view.insert('', 'end', values=row)
        
    def exportBox(self, selected):
        # Check if selected is empty
        if selected == '':
            pass
        else:
            data = self.db.selection(selected, '*')
            ExportCSV(selected, data)
