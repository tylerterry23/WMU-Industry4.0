import csv
import datetime
import os

def ExportCSV(table, data):
    # Create a csv file with name as todays date
    filepath = f"C:\\Users\\tmp\\Desktop\\Reports\\{datetime.date.today()}.csv"


    # Open the file in write mode
    with open(filepath, 'w', newline='') as file:
        # Create a csv writer object
        writer = csv.writer(file)

        # Write the first row as th table name
        writer.writerow([table])


        # Write the data
        writer.writerows(data)

