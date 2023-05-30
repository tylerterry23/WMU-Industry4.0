import GUI.backend.Database as DB
import GUI.backend.tables as Tables
import datetime
import os


def generateValues():
    dict1 = {'ProcessID': 100, 'ProcessName':'RC Assembly', 'NumStations':5,
            'ProcessDesc':'Main assembly process for assembling an RC car.',
            'DateCreated':'2023-02-20', 'TimesCompleted':0, 'GoalTime':'00:25:00.00', 'AvgTime':'00:25:00.00'}
    values = [('Process', dict1)]


    dict2 = {'ProductID': 100, 'ProcessID':100, 'Completed':False, 'Accepted':False,
            'StartTime':f'{datetime.datetime(2023, 4, 20, 12, 20, 00)}','EndTime':f'{datetime.datetime(2023, 4, 20, 12, 25, 00)}', 'TotalTime':'00:05:00.00'}
    values.append(('Product', dict2))


    dict3 = {'StationID': 1, 'ProcessID':100, 'NumSteps':5, 'EstimatedTime':'00:01:00.00',
            'DateCreated':'2023-02-20', 'StationDesc':'Axle Housing Assembly',
            'AverageTime':'00:05:00.00', 'Active':False}
    values.append(('Stations', dict3))


    dict4 = {'StationID': 2, 'ProcessID':100, 'NumSteps':4, 'EstimatedTime':'00:02:00.00',
            'DateCreated': '2023-02-20', 'StationDesc':'Front Axle to Chasis Body',
            'AverageTime':'00:05:00.00', 'Active':False}
    values.append(('Stations', dict4))


    dict5 = {'StationID': 3, 'ProcessID':100, 'NumSteps':3, 'EstimatedTime':'00:03:00.00',
            'DateCreated': '2023-02-20', 'StationDesc':'Back Axle to Chasis Body',
            'AverageTime':'00:05:00.00', 'Active':False}
    values.append(('Stations', dict5))


    dict6 = {'StationID': 4, 'ProcessID':100, 'NumSteps':2, 'EstimatedTime':'00:04:00.00',
            'DateCreated': '2023-02-20', 'StationDesc':'Tire Addition',
            'AverageTime':'00:05:00.00', 'Active':False}
    values.append(('Stations', dict6))


    dict7 = {'StationID': 5, 'ProcessID':100, 'NumSteps':5, 'EstimatedTime':'00:05:00.00',
            'DateCreated': '2023-02-20', 'StationDesc':'Chasis to Body',
            'AverageTime':'00:05:00.00', 'Active':False}
    values.append(('Stations', dict7))

    dict8 = {'StepID': 1, 'StationID':1, 'StepDesc':'Insert the drive axle into the lower axle housing. Make sure that it is properly seated.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict8))

    dict9 = {'StepID': 2, 'StationID':1, 'StepDesc':'Insert the reduction gear into the lower axle body. Make sure that this gear is in mesh with the gear from the drive axle.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict9))

    dict10 = {'StepID': 3, 'StationID':1, 'StepDesc':'Place the DC motor into the lower axle body. Make sure that the wires are facing up and the attaached gear in mesh with the drive axle.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict10))

    dict11 = {'StepID': 4, 'StationID':1, 'StepDesc':'Place both suspension link bars into the spherical slots. Make sure that the link bars are facing down.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict11))

    dict12 = {'StepID': 5, 'StationID':1, 'StepDesc':'Flip over the lower axle housing and place the ipper axel housing. Take 2 axle housing screws and use the electric screwdriver to screw the upper and lower axle housings together.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict12))

    dict13 = {'StepID': 6, 'StationID':2, 'StepDesc':'Line up your station 1 assembly wiht the main body making sure that the 3 suspension links are lined up properly.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict13))

    dict14 = {'StepID': 7, 'StationID':2, 'StepDesc':'Pop the Chasis Link Bar Mount onto the Chasis Body encasing the 2 suspension links. Use the electric screwdriver to screw the pieces together (Axle Link Bar Screws).',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict14))

    dict15 = {'StepID': 8, 'StationID':2, 'StepDesc':'Pop the Axle Link Bar Mount onto the Station 1 assembly encasing the suspension bar link. Use the electric screwdriver to screw the pieces together (Chasis Link Bar Screws).',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict15))

    dict16 = {'StepID': 9, 'StationID':2, 'StepDesc':'Make sure all parts are snapped in place correctly and have the suspension links in place.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict16))

    dict17 = {'StepID': 10, 'StationID':3, 'StepDesc':'Place the completed Station 2 assembly into the provided fixture. Place the strut assemblies in the correct spots as shows. (4 places). DO NOT PUT THEM IN UPSIDE DOWN.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict17))

    dict18 = {'StepID': 11, 'StationID':3, 'StepDesc':'Place 8 Strut Screws (2 on each of the strut assemblies) and use the electric screwdriver to screw them tightly.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict18))

    dict19 = {'StepID': 12, 'StationID':3, 'StepDesc':'Make sure that all four strut assemblies are properly assembled.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict19))

    dict20 = {'StepID': 13, 'StationID':4, 'StepDesc':'Take the completed Station 3 assembly and affix all 4 tires onto the axles as shown.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict20))

    dict21 = {'StepID': 14, 'StationID':4, 'StepDesc':'Use the electric screwdriver to tightly secure the tires to the axles from the chasis body.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict21))

    dict22 = {'StepID': 15, 'StationID':5, 'StepDesc':'Connect the battery to the relief on the bottom side of the station 4 assembly. Make sure that the connection is secure. The battery should sit at an angle in the housing.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict22))

    dict23 = {'StepID': 16, 'StationID':5, 'StepDesc':'Affix the battery cover over the housing. Take 1 battery cover screw and place it in the slot as shown.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict23))

    dict24 = {'StepID': 17, 'StationID':5, 'StepDesc':'Use the electric screwdriver to assmble to the battery cover to the station 4 assembly.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict24))

    dict25 = {'StepID': 18, 'StationID':5, 'StepDesc':'Slide the body onto the station 4 assembly. Use the 4 posts to align it.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict25))

    dict26 = {'StepID': 19, 'StationID':5, 'StepDesc':'Use the electric screwdriver to secure the body onto the chasis. There are 4 screws required on each corner.',
            'PhotoLink':'', 'InfoLink':''}
    values.append(('Steps', dict26))

    return values


def djangoReset():
	'''
	Whenever the database is reset, this function will be called to reset the Django database. 
	'''

	# traverse to manage.py (../dashboard/Version 2 - Django (Scalable)/industry4)
	directory = 'cd ../dashboard/Version 2 - Django (Scalable)/industry4'
	os.system(directory)
	os.system('python manage.py migrate')

	# Create superuser username: admin, password: adminpass email: admin@gmail.com
	os.system('python manage.py createsuperuser --username admin --email admin@gmail.com --password adminpass')






def resetDB(user_choice):
    # Connecting to db
    if user_choice == 1:
        user_input = input('Are you sure you want to reset the Database? All data will be lost. Y or N): ')
        user_input = user_input.upper()
    else:
        user_input = 'Y'
    
    if user_input[0] == 'Y':
        db = DB.Database("localhost", "root", "industry4")
        db.connect()
        db.dropDB()
        db.connect()
        db.create_tables(Tables.TABLES)
        for value in generateValues():
            table = value[0]
            tab_cols = ''
            tab_vals = []
            for i in value[1]:
                if tab_cols == '':
                    tab_cols += f'{i}'
                else:
                    tab_cols += f', {i}'
                tab_vals.append(value[1][i])
            tab_vals = tuple(tab_vals)
            db.insert_into(table, tab_cols, tab_vals)

        # djangoReset()

        print("Database reset complete.")

    else:
        print("Closing program. Data not deleted.")

def main():
    resetDB(1)

if __name__ == '__main__':
    main()