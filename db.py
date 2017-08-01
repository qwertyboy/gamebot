import csv
from collections import namedtuple

# desc: function to create a new database file
# args: fileName - the name of the file to create
# retn: 1 on success or 0 on failure
def createDB(fileName):
    try:
        # open file in create mode
        with open(fileName, 'w', newline='') as stats:
            # write some default headers to the file
            defaultHeaders = ['Name', 'Wins', 'Losses']
            writer = csv.writer(stats, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(defaultHeaders)
            print('[INFO] Database created successfully')
            return 1
    except PermissionError:
        print('[ERROR] Unable to open database file for writing')
        return 0


# desc: function to read database
# args: fileName - name of the file to open
# retn: a named tuple containing the header and rows from the file
def readDB(fileName):
    # open file and get rows
    with open(fileName, newline='') as stats:
        reader = csv.reader(stats, delimiter=',', quotechar='"')
        # get column headers
        headers = next(reader)
        # get rows
        rows = list(reader)
        print('[INFO] Database read successful')

    Data = namedtuple('Data', ['headers', 'rows'])
    r = Data(headers, rows)
    return r


# desc: function to wrte the database
# args: fileName - name of the file to write
#       headers - a list of strings containing the headers for each column
#       rows - a list of lists containing the data to be in each row
# retn: 1 on success or 0 on failure
def writeDB(fileName, headers, rows):
    try:
        # write the new data to the database file
        with open(fileName, 'w', newline='') as stats:
            writer = csv.writer(stats, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
            print('[INFO] Database write successful')
        return 1
    except PermissionError:
        print('[ERROR] Unable to open database file for writing')
        return 0
