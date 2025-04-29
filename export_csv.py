# This file is part of pymarc. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution and at
# https://opensource.org/licenses/BSD-2-Clause. pymarc may be copied, modified,
# propagated, or distributed according to the terms contained in the LICENSE
# file.
#Must install PyMARC 
#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs
#

import csv
import uuid
import os


from pymarc import *

class EXPORT_CSV:
 def __init__(self, value: str) -> None:
    """ """
    self._csv_filename = value
           
 @property
 def csv_filename(self) -> str:
    """ """
    return self._csv_filename

 @csv_filename.setter
 def csv_filename(self, value: str) -> None:
    """ """
    if self.is_file_found (value):
           self._csv_filename = value
 
 #Functions
 def is_file_found(self, value: str) -> bool:
    if os.path.exists(value):
        return (True)
    else:
        return (False)

 def normalized_fields_to_csv (self, records_list, tags_list):
  
  '''This function removes all subfield codes and delimters from a field,  
     and saves the field into a csv file.
     The csv's column headers are the tags in tags_list
  '''
  fieldnames=[]
  with open(self._csv_filename, 'w', newline='') as csvfile:
    d = {} #Empty dictionary

    #Create CSV column headers
    for header in tags_list:
     fieldnames.append (header)
     
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    #loop on records and fields
    for rec in records_list:
     for fld in rec:
      #Check if the tag is in the list of tags
      if fld.tag in tags_list:
       #format_field() strips all subfield codes
       if fld.tag in d:
        #update value if the key exists
        d.update({fld.tag:fld.format_field()}) 
        #format_field() is a pymarc function that strips all subfield codes
       else:
        #add dictionary key and value 
        d[fld.tag] = fld.format_field()
     #print (d)
     writer.writerow(d)
      
 def subfields_to_csv (self, records_list, tags_subfields_list):
  
  '''Exports subfields' values in one row.
     It takes 2d list of tags and subfields like this [["245","a","b","z"], ["300","a"], ["264","a","c"]]
  '''
  fieldnames=[]
  with open(self._csv_filename, 'w', newline='') as csvfile:
    d = {} #Empty dictionary
    
    #Create CSV column headers
    for tag in tags_subfields_list:
     for subfld_code in tag:
      if subfld_code!=tag[0]:
       fieldnames.append (tag[0]+subfld_code)
    #    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    
    #Create CSV data
    #loop on records
    for rec in records_list:
     #Loop on tags
     for tag in tags_subfields_list:     
       
       for fld in rec.get_fields(tag[0]):
         #loop on subfields
         for subfld_code in tag:
         #
             
           if subfld_code!=tag[0]:
            for sbfld in fld.get_subfields(subfld_code):
              #print (f"header: {tag[0]+subfld_code} - value: {sbfld}") 
              d[tag[0]+subfld_code] = rec[tag[0]][subfld_code]
     #print (d)  
     writer.writerow(d)
        
 def db_normalized_to_csv (self, records_list):
  
  '''
    It extracts records into a single csv file.
    Each record is extracted in rows.
    All rows of a record can be link with a primary key
    and control number in 001.
    Also, this function retains the sequence of tags and subfields.    
  '''
  fieldnames=[]
  with open(self._csv_filename, 'w', newline='') as csvfile:
    d = {} #Empty dictionary
    
    #Create CSV column headers
    fieldnames=["PK","001","Tag_Sequence","Tag",
                "Ind1","Ind2", "Subfield_Squence",
                "Subfield_code","Field_Value"] 
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    
    #Loop on records in records list
    for rec in records_list:
     PK = uuid.uuid4().hex #Create a unique PK for the record
     tag001=rec['001'].data #Get record control number
    
     tag =""
     tag_Sequence=0
     ind1=""
     ind2=""
     subfield_code=""
     subfield_Squence=0
     field_Value=""
       
     #add record leader to dictionary key and value
     d['PK']=PK
     d['001']= tag001    
     d['Tag_Sequence'] = tag_Sequence
     d['Tag'] = "LDR"
     d['Field_Value']=str(rec.leader)
     writer.writerow(d) #Write row to the csv file
     #Loop on fields in a record
     for fld in rec:
      tag = fld.tag
      
      if fld.tag !='001': #Do not add a row for 001 field
        tag_Sequence += 1
        subfield_Squence=0
        #add dictionary key and value
        d['PK']=PK
        d['001']= tag001  
        d['Tag'] = fld.tag       
        d['Tag_Sequence'] = tag_Sequence
        if fld.is_control_field():
           field_Value= rec[fld.tag].data 
           #
           d['Field_Value']=field_Value
           writer.writerow(d)
        else: #Not a control field 00X
           #Add subfields           
           for subfld in fld:
               subfield_Squence +=1
               subfield_code = subfld[0]
               field_Value = subfld[1]
               #
               d['Ind1'] = fld.indicators[0]
               d['Ind2'] = fld.indicators[1]
               d['Subfield_code']= subfld[0]
               d['Field_Value']= subfld[1]
               d['Subfield_Squence']= subfield_Squence
               writer.writerow(d)     
 

