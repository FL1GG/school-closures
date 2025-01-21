import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys

options = webdriver.ChromeOptions()
options.add_argument("--log-level=0")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

#got a facebook api account but it lacks ability to scan public posts, so no scraping :(



dates = []
statuses = ['Open', 'Closed', 'Early Release', 'Late Start', 'Virtual', 'To Be Determined', 'Unknown']


output_file = open('output.csv', 'w',newline='')
output_file_writer = csv.writer(output_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

fields = ['Location', 'School(s)']

"""
processes a url into a csv output
"""
def process_url(row):
    row_out = [row['Location'], row['School']]

    driver.get(row['Primary'])
    for date in dates:
        print("")
        print(row['School'] + " Status on " + date)
        for i in range(len(statuses)):
            print(str(i) + ": " + statuses[i])

        response = ""
        while(not response.isdigit() or int(response) >= len(statuses)):
            response = input("#> ")
        
        row_out.append(statuses[int(response)])

    output_file_writer.writerow(row_out)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        dates.append(arg)
        fields.append(arg)

    output_file_writer.writerow(fields) # write header

    school_data = []
    with open('schools.csv', 'r') as csvfile:
        school_data = csv.DictReader(csvfile, delimiter=',')

        for row in school_data:
            if(row['Type'] == 'NA' or row['Type'] == None):
                continue

            process_url(row)


    output_file.close()