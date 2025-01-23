import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys, os
from pathlib import Path

process_output = False

# sanity checks
if Path("./output.csv").is_file():
    inp = input("File output.csv already exists, continuing will override this file. Are you sure you want to continue? (Y/N): ")

    if(inp.lower() != 'y' and inp.lower() != 'yes'):
        sys.exit(1)

    inp = input("Since output.csv already exists, would you like to only process rows that are Unknown or TBD? [Will only update last column] (Y/N): ")

    if(inp.lower() == 'y' or inp.lower() == 'yes'):
        process_output = True


# create chrome hooks
options = webdriver.ChromeOptions()
options.add_argument("--log-level=0")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# data formatting inits
dates = []
statuses = ['Open', 'Closed', 'Early Release', 'Late Start', 'Virtual', 'To Be Determined', 'Unknown']
fields = ['Location', 'School(s)']


# open 
output_file = open('output_tmp.csv', 'w',newline='')
output_file_writer = csv.writer(output_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

for arg in sys.argv[1:]:
    dates.append(arg)
    fields.append(arg)

output_file_writer.writerow(fields) # write header

school_data = []

file_name = 'schools.csv'

with open(file_name, 'r') as csvfile:
    if(process_output):
        output_data = open('output.csv', 'r',newline='')
        out_r = csv.reader(output_data)
        next(out_r) # skip header
        output_dict = {row[1]:row for row in out_r} #0: location,1: school, 2,3,4,etc..: dates
        output_data.close()

    school_data = csv.DictReader(csvfile, delimiter=',')

    processed_rows = 0
    for row in school_data:
        if(process_output): # are we using output.csv?
            if(row['School(s)'] in output_dict.keys()): # make sure the school exists
                processed_rows += 1 # school is in output we are processing this row
                if(output_dict[row['School(s)']][-1] != 'Unknown' and output_dict[row['School(s)']][-1] != 'To Be Determined'):
                    output_file_writer.writerow(output_dict[row['School(s)']]) # then write to file
                    continue
            else:
                continue # school doesnt exist, don't process row
        else:
            processed_rows += 1 # we are processing rows


        row_out = [row['Location'], row['School(s)']]

        driver.get(row['Primary'])
        for date in dates:
            print("")
            print(row['School(s)'] + " Status on " + date)
            for i in range(len(statuses)):
                print(str(i) + ": " + statuses[i])

            response = ""
            while(not response.isdigit() or int(response) >= len(statuses)):
                response = input("#> ")
            
            row_out.append(statuses[int(response)])

        output_file_writer.writerow(row_out)

output_file.close()

if(Path("./output.csv").is_file()):
    os.remove('output.csv')

os.rename('output_tmp.csv', 'output.csv')

print("Processed " + str(processed_rows) + " rows.")