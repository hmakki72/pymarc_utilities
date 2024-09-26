#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs

import re
import codecs
import os
from pymarc import *

class ENCODING:

 def __init__(self):
     self.default_encoding = "UTF-8"
     self.is_uncombine_diacritics = True
 

     
#replace combined UTF-8 characters+diacritics to uncombined characters
#For example: change ā (U+0101) to ā   ((U+0061 U+0304)
 def uncombine_diacritics(self, record, skip_subfield_code):
       
       try:
            #Vars
            extracted_rec = Record()  
            #Loop on MARC_record fields
            for field in record:
              #
              if int(field.tag) < 99:
                extracted_rec.add_field(field)
              else:
                #Create new field from current record.field data
                newfield = Field(
                      field.tag,
                      field.indicators
                      )
                #Loop on subfields
                for subfield in field:
                    #Skip $1 in authority files because it throws errors
                    #Subfields' values with slash or backslash may throw errors
                    if subfield[0] != skip_subfield_code:
                       val=subfield[1]
                       #normalized_record = unicodedata.normalize("NFD", subfield[1])
                       sfcode = subfield[0]
                       #Uncombine subfield values
                       newfield.add_subfield(subfield[0], unicodedata.normalize("NFD", subfield[1]))
                       #print (field.tag, normalized_record)
                    else:
                       #Add subfield to the newfield
                       newfield.add_subfield(subfield[0], subfield[1])
                #Add newfield to extracted_rec    
                extracted_rec.add_field(newfield)
            return extracted_rec
            #print (record)
            #print (extracted_rec)            
            #user_input = input("Save to MARC file? 'y' : ")            
  
       except:
              print ("Err in uncombine_diacritics")        
              
class FIND_AND_REPLACE:

 def __init__(self):
    self.default_encoding = "UTF-8"
    self.is_uncombine_diacritics = True

#Finds a field in a record
 @staticmethod
 def find(record, find_field):

    ''''
    Use regex to search a value
    regex Metacharacters, Special Sequences, or Sets
    must be part of find_field value

    Example: Check if the string starts with "Zalis" and ends with "Elayne":
    sample_field = Field(
               tag="100", indicators=["1", "?"], 
               subfields=[Subfield(code="d", value="^Zalis.*Elayne$")])
    Control Field Example:
    sample_field = Field(tag='001', data='^fol05731351')
    '''
    found = False
    #check if find_field is a fixed or variable length field 
    ##if find_field.subfields:
    if record.get_fields(find_field.tag):
       #Tag found in the record
       #Mark results as found
       found = True
       for field in record.get_fields(find_field.tag):
        '''
        Check if find_field is a MARC control field
        MARC control fields start with 00X (00*),
        and has no indicators or subfields
        '''
        if find_field.is_control_field() and find_field.data is not None:
         #Control field
         value_found = re.search(find_field.data, record[find_field.tag].data) 
         #print (f"CONTROL FOUND : {value_found}")
         
         return (value_found)
        else:
         #Not a control field
         if find_field.indicators:

          #Ignore if an indicator has ? in its value
          if find_field.indicators [0]!= '?':
            if find_field.indicators [0] != field.indicators [0]:
               found = False
               
          if find_field.indicators [1]!= '?':
            if find_field.indicators [1] != field.indicators [1]:
               found = False
          #Find Subfields
          for subfield in find_field.subfields:
            if field.get_subfields(subfield[0]):
               
                value_found = re.search(subfield[1], record[find_field.tag][subfield[0]]) 
                found = value_found
            else:
                #Subfield not found
                found = False            
    return (found)

 @classmethod
 #Finds and replace a field in a record
 def find_and_replace(self, record, find_field, replace_with_field):

    found = self.find(record, find_field)

    if found:
       
       for field in record.get_fields(find_field.tag):
          #Replace value using regex
          for subfield in replace_with_field.subfields:
              if field.get_subfields(subfield[0]):
                #Change subfield value not subfield code
                original_value = record[find_field.tag][subfield[0]]
                find_field_value = find_field.subfields[0][1]
                replace_field_value = subfield[1]
                modified_value = re.sub(find_field_value, replace_field_value , original_value)
                #Updadte value
                record[find_field.tag][subfield[0]]=modified_value
                
              else:
                #Change subfield code and value if the value is available
                #Deletes the first subfield with the specified ‘code’ and returns its value.
                
                original_value = field.delete_subfield('a')

                find_field_value = find_field.subfields[0][1]
                replace_field_value = subfield[1]
                modified_value = re.sub(find_field_value, replace_field_value , original_value)
                #Construct subfield
                
                new_subfieldcode = replace_with_field.subfields[0][0]
                add_newsubfield = field.add_subfield(new_subfieldcode, modified_value, 0)
                                  
          #Replace indicators
          if replace_with_field.indicators[0] !="?" or replace_with_field.indicators[0] is not None:
             field.indicators[0] = replace_with_field.indicators[0]
          if replace_with_field.indicators[1] !="?" or replace_with_field.indicators[1] is not None:
             field.indicators[1] = replace_with_field.indicators[1]
          #Replace Tag   
          if find_field.tag !=  replace_with_field.tag :        
             #Construct new field
             
             new_field = record[find_field.tag]
             add_newfield = Field(replace_with_field.tag, 
                          indicators=new_field.indicators, 
                          subfields=new_field.subfields
                          )
             #Modify record
             record.add_ordered_field(add_newfield)
             record.remove_field(record[find_field.tag])
             
             
          
       return (record)


 def swap_bib_linked_fields(record):
    '''
      Test swap linked fields
      The swap function makes the 880 fields the main fields
      and converts the main fields into linked fields 880
      Use this function if you want to make the vernacular field 
      the main fields, and the Romainzed fields are the linked fields
      It converts this:
      =100  1\$6880-01$aMuṣṭafá, ʻAbd al-ʻAzīz.
      =880  1\$6100-01/(3/r‏$a‏مصطفى، عبد العزيز.
      =245  10$6880-02$aQabla an yuhdama al-Aqṣá /$cʻAbd al-ʻAzīz Muṣṭafá.
      =880  10$6245-02/(3/r‏$a‏قبل ا يهدم الأقصى /‏$c‏عبد العزيز مصطفى.
      =260  \\$6880-03$a[Riyadh :$bs.n.],$c1989$e(al-Suwaydī, al-Riyāḍ :$fṬubiʻat bi-Maṭābiʻ Dār Ṭaybah)
      =880  \\$6260-03/(3/r‏$a[Riyadh :$b‏س.ن.]،‏$c1989‏$e‏(السويدي، الرياض :‏$f‏طبعة بمطابع دار طيبة)‬
      
      To this:
      =100  1\$6880-01$a‏مصطفى، عبد العزيز.
      =245  10$6880-02$a‏قبل ا يهدم الأقصى /‏$c‏عبد العزيز مصطفى.
      =260  \\$6880-03$a[Riyadh :$b‏س.ن.]،‏$c1989‏$e‏(السويدي، الرياض :‏$f‏طبعة بمطابع دار طيبة)‬
      =880  1\$6100-01$aMuṣṭafá, ʻAbd al-ʻAzīz.
      =880  10$6245-02$aQabla an yuhdama al-Aqṣá /$cʻAbd al-ʻAzīz Muṣṭafá.
      =880  \\$6260-03$a[Riyadh :$bs.n.],$c1989$e(al-Suwaydī, al-Riyāḍ :$fṬubiʻat bi-Maṭābiʻ Dār Ṭaybah)

      
      '''
    new_record = Record()
    
    for field in record.get_fields():
        #
        if int(field.tag)< 99 :
          #No need to work on fields (0XX)
          #Just add them to the new_record
          new_record.add_ordered_field(field)
        else:
          #Ignore 880 fields
          if int(field.tag)!= 880 : 
           #Only fields with $6 are linked to other fields
           if field.get_subfields('6'): 
            #Loop on linked fields 880
            for linked_field in record.get_linked_fields(record[field.tag]):
                #Create new linked field without subfields
                new_linked_field = Field('880', 
                          indicators=field.indicators
                          )
                #loop and add subfields and change reference field in $6
                for subfld in field:
                    if subfld[0] == '6':
                       #Change subfield $6 value 
                       new_linked_field.delete_subfield (subfld[0])
                       new_subfld_value = subfld[1].replace ('880', field.tag)
            
                       new_linked_field.add_subfield (subfld[0], new_subfld_value)
                    else:
                       #Add other subfields
                       new_linked_field.add_subfield (subfld[0], subfld[1])

                #Create new field that links to the above new_linked_field
                add_newfield = Field(field.tag, 
                          indicators=linked_field.indicators, 
                          subfields=linked_field.subfields
                          )
                
                #Modify $6 values in the swapped field
                add_newfield.delete_subfield ('6')
                add_newfield.add_subfield ('6', record[field.tag]['6'], 0)
                       
                #Add new field to the new record
                new_record.add_ordered_field(add_newfield)
                new_record.add_ordered_field(new_linked_field)
           else:
                #add field that are not linked
                new_record.add_ordered_field(field)
    #print (record)
    return (new_record)

class File :

    def __init__(self, value: str) -> None:
        """ """
        if self.is_file_found (value):
           self._marc_filename = value
           
    @property
    def marc_filename(self) -> str:
        """ """
        return self._marc_filename

    @marc_filename.setter
    def marc_filename(self, value: str) -> None:
        """ """
        if self.is_file_found (value):
           self._marc_filename = value
     
    @property
    def records_count(self) -> int:
        return self._records_count    
    @records_count.setter
    def records_count(self, value: int) -> None:
        if is_file_found(value) :
           self._records_count =value
    
    #Functions
    
    def get_records_count(self) -> int:
        with open(self._marc_filename, 'rb') as fh:
            recnum = 0
            reader = MARCReader(fh)
            for record in reader:
                recnum += 1 #record count
            self._records_count = recnum
     
    def is_file_found(self, value: str) -> bool:
       if os.path.exists(value):
            return (True)
       else:
            # Printing a message if the file does not exist
           raise BadLeaderValue(f"File {value} not found.")

    def get_records(self, start: int, end: int) :
        '''
        start value must not be negative
        end value must not be bigger than records_count
        '''
        with open(self._marc_filename, 'rb') as fh:
            recnum = 0
            records = [] 
            reader = MARCReader(fh)
            for record in reader:
                recnum += 1 #record count
                if recnum >= start and recnum <= end:
                   records.append(record)
                #Break loop
                if recnum == end:
                   break
        return (records)
                
                   
                
            
