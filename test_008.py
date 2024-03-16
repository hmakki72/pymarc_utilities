#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs


import unicodedata


import control_bib008
import control_auth008
from pymarc import *


test_bib008 = True
test_auth008 = not test_bib008
 
bib_marcfile='bibfiles/BooksAll.2014.part41.utf8'
auth_marcfile='authfiles/FASTPersonal_9.mrc'

if test_bib008:
   input_marcfile = bib_marcfile
else:
   input_marcfile = auth_marcfile   

#Open MARC file
with open(input_marcfile, 'rb') as fh:
    recnum = 0
    extractednum = 0
    reader = MARCReader(fh)
    for record in reader:
      recnum += 1 #record count
      
      if test_bib008:
        #Bibliographic records 008 data   
        print(f"Bib Field:=>{record['008'].data}<=")   
        ct_fld = control_bib008.Field008(record['008'].data)

        print (f"Length: {len(str(ct_fld))}")
        print (f"Date entered:=>{ct_fld.date_entered}<= Date Type:=>{ct_fld.date_type}<=")
        print (f"Date1:=>{ct_fld.date1}<= Date2:=>{ct_fld.date2}<=")
        print (f"Pub. Place:=>{ct_fld.publication_place}<= Language:=>{ct_fld.language}<=")
        print (f"Modified record:=>{ct_fld.modified_record}=Cat. source:=>{ct_fld.cataloging_source}<=")
        #Change values
        ct_fld.date1 = '??uu'
        ct_fld.date2 = '????'
        #Add modified data to records 008
        record['008'].data = ct_fld
        #Print modifications
        print("====")
        print (f"New Date1:=>{ct_fld.date1}<= New Date2:=>{ct_fld.date2}<=")
        print(f"Modified Field:=>{record['008'].data}<=") 
        user_input = input("Press any key to continue ")
        print("====")
        
        
      if test_auth008:
        #Authority records 008 data
        print(f"Auth Field: {record['008'].data}")      
        fld = record['008']
        ct_fld = control_auth008.Field008(record['008'].data)
        print (f"Field length: {len(str(ct_fld))}")
        print (f"Date entered: {ct_fld.date_entered}")
        #Change values
        ct_fld.date_entered = '123456'
        print (f"New Date entered{ct_fld.date_entered}")
        user_input = input("Press any key to continue ")
