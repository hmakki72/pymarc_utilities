#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs



import unicodedata
import pymarc_utilities
import control_bib008
from pymarc import *

'''

sample_field = Field(
               tag="100", indicators=["1", "?"], 
               subfields=[Subfield(code="d", value="^Zalis.*Elayne$")])
***Use regex patterns in subfield values
***https://www.w3schools.com/python/python_regex.asp

Find field indicators value:
  sample_field = Field(tag="100", indicators=["1", "?"])
***Using "?" means any value

Find field by field tag only:
  sample_field = Field(tag="900")

Find value in control fields:
sample_field = Field(tag="008", data='\Bara')
***Use regex patterns in data values

Sample control field:
Find data starts with OCoLC: sample_field = Field(tag='003', data='^OCoLC')
Find 007 in the record: sample_field = Field(tag='007')
Test a control field that does not exist: sample_field = Field(tag='009')
'''


findit = pymarc_utilities.FIND_AND_REPLACE

#input_marcfile='authfiles/FAST.mrc' #Authority file
input_marcfile='bibfiles/BooksAll.2014.part41.utf8' #Bib file


#The following boolean vars decide what function to run on this page
#If one var is True, then all other vars must be False
test_find = True
test_find_control = False
test_findreplace = False
test_notequalto = False
test_swap = False

#Menu
print("=============")
print("What function would you like to run?")
print("1) Find (default)")
print("2) Find value in a control field")
print("3) Find and replace")
print("4) Find value not equal to a var")
print("5) Swap linked fields")
print("=============")
user_input = input("Enter item number: ")

if user_input == '2':
   test_find = False
   test_find_control = True
   print("Find bib records that has language code ara in 008")
   print("=============")
   
if user_input == '3':
   test_find = False
   test_findreplace = True
   print("Find tag 040, any indicators values ??, and subfield $a starts with DLC")
   print("replace with tag 049 99 $9bbb (dummy data)")
   print("=============")

if user_input == '4':
   test_find = False
   test_notequalto = True
   print("Field 100 subfield $a starts with James")
   print("Check if record has no 490 field")
   print("=============")

if user_input == '5':
   test_find = False
   test_swap = True
   print("Swap linked fields in records where 008.language='ara'")
   print("=============")

if test_find:
   print("Find records have 040$dDLC AND 100$a starts with James")
   print("=============")
  

#Set default values
is_found = False
#Read MARC file
with open(input_marcfile, 'rb') as fh:
    recnum = 0
    extractednum = 0
    reader = MARCReader(fh)
    for record in reader:
      recnum += 1
      
      '''
      Test swap linked fields in bib records
      The swap function makes the 880 fields the main fields
      and converts the main fields into linked fields 880
      Use this function if you want to make the vernacular fields 
      the main fields, and the Romanized fields are the linked fields
      '''
      if test_swap:
        #Swap linked fields in records where 008.language='ara'
         
        ct_fld = control_bib008.Field008(record['008'].data)
        if ct_fld.language == 'ara':
           #Check if the record has any linked field 880
           sample_field = Field(tag="880")
           is_found880 = findit.find(record, sample_field)
           if is_found880:
           
            print("Original record: ")
            print(record)
            print ("========================")
            user_input = input("Press any key to continue ")
            print ("========================")
            rec = findit.swap_bib_linked_fields(record)
            print("Swaped record: ")
            print (rec)
            user_input = input("Press any key to continue ")
        
      if test_find_control:
        #Test find value in a control field
        #Extract bib records that has language code ara in 008
        sample_field = Field(tag="008", data='\Bara')
        is_found = findit.find(record, sample_field)
        if is_found:
           print (record)
           user_input = input("Press any key to continue")
        
      #Test find function 
      #Emulate AND operator
      if test_find:
             
        output_file ='bibfiles/exrct377aARA_Diac.mrc'
        
        #Find records have 040$dDLC AND 100$a starts with James

        sample_field2 = Field(tag="040", indicators=["?", "?"],
                    subfields=[Subfield(code="a", value="DLC")])
                    
        sample_field = Field(tag="100", indicators=["?", "?"],
                    subfields=[Subfield(code="a", value="^James")])
        
        is_found = findit.find(record, sample_field)
        
        if is_found:
            
            is_found2 = findit.find(record, sample_field2)
            if is_found2:
               print("Found record: ")
               print(record)
               print ("========================")   
               user_input = input("Press any key to continue.")
 
      if test_notequalto:
         #Field 100 subfield $a starts with James
         #and the record has no 490 field
        sample_field = Field(tag="100", indicators=["?", "?"],
                    subfields=[Subfield(code="a", value="^James")])
        is_found = findit.find(record, sample_field)
        output_file ='bibfiles/exrctNo377aARA_Diac.mrc'
        if is_found:
            #Check if record has no 490 field
            sample_field2 = Field(tag="490")
            
            is_found2 = findit.find(record, sample_field2)
            if not is_found2:
               print("!= Found record: ")
               print(record)
               print ("========================")
                  
               user_input = input("Save to MARC file? 'y' : ")
               if user_input == 'y':
                  extractednum += 1
                  with open(output_file, 'ab') as out:
                    out.write(record.as_marc())     
                    
      if test_findreplace :
        '''      
         Test find and replace
         find_and_replace(self, record, find_field, replace_with_field)
        '''
        
        #Find tag 040, any indicators values ??, and subfield $a starts with DLC
        #replace with tag 049 99 $9bbb (dummy data)
        
        sample_field = Field(tag="040", indicators=["?", "?"],
                    subfields=[Subfield(code="d", value="^DLC")])
                  
        replace_with_field = Field(tag="049", indicators=["9", "9"], 
                     subfields=[Subfield(code="9", value="BBB")]) 
                     
        output_file ='bibfiles/replace040dDLC_0499BBB.mrc'             
        
        rec = findit.find_and_replace(record, sample_field, 
                                      replace_with_field)
                                      
        if rec is not None:  
           print("Replaced record: ")
           print(rec)
           print ("========================")
           user_input = input("Save to MARC file? 'y' : ")
           if user_input == 'y':
               print ("")
               with open(output_file, 'ab') as out:
                    out.write(record.as_marc())

    print (f"Total extracted records : {extractednum} of {recnum}")
    
