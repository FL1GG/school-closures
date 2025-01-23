import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys, os
from pathlib import Path

process_output = 0

# sanity checks
if Path("./output.csv").is_file():
    inp = input("File output.csv already exists, continuing will override this file. Are you sure you want to continue? (Y/N): ")

    if(inp.lower() != 'y' and inp.lower() != 'yes'):
        sys.exit(1)

    inp = input("Since output.csv already exists, would you like to only process rows that are Unknown or TBD? (Y/N): ")

    if(inp.lower() != 'y' and inp.lower() != 'yes'):
        process_output = 1


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

if(process_output):
    file_name = 'output.csv'

with open(filename, 'r') as csvfile:
    school_data = csv.DictReader(csvfile, delimiter=',')

    for row in school_data:
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

if(Path("./output.csv").is_file())
    os.remove('output.csv')

os.rename('output_tmp.csv', 'output.csv')

