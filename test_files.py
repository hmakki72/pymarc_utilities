

#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs




import pymarc_utilities
from pymarc import *

value = 'bibfiles/BooksAll.2014.part41.utf8'
file = pymarc_utilities.File(value)
print (f"File name is set to: {file.marc_filename}")


#Count total number of records in a file
user_input = input("Get number of records in the file? 'y' ")
if user_input == 'y': 
   print("Start Counting")
   file.get_records_count()
   print(f"Total number of records is: {file.records_count}")

'''
start value must not be negative
end value must not be bigger
than total number of records in the file
'''
start = 5000
end = 5009

recs = file.get_records(5000,5009)
print (f"Total number of records in the list: {len(recs)}")
user_input = input("Display records? 'y' ")
if user_input == 'y': 
   count = 0
   for r in recs:
    count +=1
    print (f"Recod number {count}")
    print("====")
    print (r)
    user_input = input("Press any key to continue ")
    print("====")
