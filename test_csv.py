#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs

from pymarc import *
import export_csv

#Menu
print("=============")
print("What function would you like to test?")
print("1) Export Normalized Fields")
print("2) Export subfields")
print("3) DB Normalized Export ")
print("=============")
user_input = input("Enter item number: ")

#Create test records
#Create 1st test records
record1 = Record()
new_001 = Field(tag='001', data='fol05731351')
new_field1 = Field(
    tag='245',
    indicators=['0', '1'],
    subfields=[
        Subfield(code='a', value='TITLE1, "Sd":'),
        Subfield(code='b', value='from journeyman to master /'),
        Subfield(code='c', value='title1 Author I.')
    ]
)

new_field2 = Field(
    tag='100',
    indicators=['0', '1'],
    subfields=[
        Subfield(code='a', value='Author I '),
    ]
)
record1.add_ordered_field(new_001)
record1.add_ordered_field(new_field1)
record1.add_ordered_field(new_field2)

#Create 2nd test record
record2 = Record()
new_001 = Field(tag='001', data='fo0123456789')
new_field3 = Field(
    tag='245',
    indicators=['0', '1'],
    subfields=[
        Subfield(code='a', value="TITLE'2 :"),
        Subfield(code='b', value='from journeyman to master /'),
        Subfield(code='c', value='title2 Author II.')
    ]
)

new_field4 = Field(
    tag='300',
    indicators=['', ''],
    subfields=[
        Subfield(code='a', value='Physical, 2a '),
        Subfield(code='b', value='Physical 2b ')
    ]
)
new_field5 = Field(
    tag='300',
    indicators=['', ''],
    subfields=[
        Subfield(code='a', value='Physical 2aa '),
        Subfield(code='a', value='Physical 2aaa '),
    ]
)
record2.add_ordered_field(new_001)
record2.add_ordered_field(new_field3)
record2.add_ordered_field(new_field4)
record2.add_ordered_field(new_field5)


#Assuming you have a list of records (you can modify this as needed)
records = []
records.append(record1)
records.append(record2)


#1) Fields (join subfields) 
if user_input == '1':
  #CVS class calling
  fieldsto_csv = export_csv.EXPORT_CSV('0normarlized.csv')
  print(fieldsto_csv.csv_filename)
   
  #normalized_fields_to_csv (records_list, tags_list)
  fieldsto_csv.normalized_fields_to_csv(records,['100','245','650'])
   
   
#2) Fields and subfields 
if user_input == '2':
 #Create 2d list
 thislist = [["245","a","b","z"], ["300","a"], ["264","a","c"]]
 #CVS class calling
 fieldsto_csv = export_csv.EXPORT_CSV('0subfields.csv')
   
 #subfields_to_csv
 fieldsto_csv.subfields_to_csv(records,thislist)
        

if user_input == '3':
 #Recods list
 recs_list = []
 #CVS class calling
 fieldsto_csv = export_csv.EXPORT_CSV('00DB_Normalized.csv')
 with open("bibfiles/KSA.mrc", 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader: 
      recs_list.append(record)
 #subfields_to_csv
 print(f"Number of records: {len(recs_list)}")
 
 fieldsto_csv. db_normalized_to_csv(recs_list)
 
               
        
        
        
