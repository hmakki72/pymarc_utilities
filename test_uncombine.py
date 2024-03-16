

#PyMARC API documentation https://pymarc.readthedocs.io/en/latest/#api-docs


'''
 Combine characters examples : ḥ ḍ ā ī á
Uncombine characters examples: Ḥ ḍ ā ī
'''

import unicodedata
import codecs
import pymarc_utilities
import control_bib008
from pymarc import *


modf = pymarc_utilities.ENCODING()
findit = pymarc_utilities.FIND_AND_REPLACE

uncombine_all = False
input_marcfile='authfiles/FASTPersonal_9.mrc'
output_marcfile='authfiles/FASTPersonal_9.uncomb.mrc'

extracted_rec = Record()


#Uncombine MARC file 
with open(input_marcfile, 'rb') as fh:
    recnum = 0
    extractednum = 0
    reader = MARCReader(fh)
    for record in reader:
      recnum += 1 #Records count
      if uncombine_all:
      #Uncombaine all records in the file
        
        try:
          '''
           uncombine_diacritics(record, skip_subfield_code)
           Use '?' in skip_subfield_codeif you want to 
           uncombine all subfields data
          '''   
          extracted_rec = modf.uncombine_diacritics(record, '?')
          if extracted_rec is not None: 
            extractednum += 1
            print (extracted_rec)
            user_input = input("Save to MARC file? 'y' : ")
            if user_input == 'y':
              with codecs.open(output_marcfile, "ab") as out:
                   out.write(extracted_rec.as_marc21())
          else:
            print ("Extracted Record Returned None")
        except:
        #Dummy line
        #Add your own except code
          a = 0
        
      else:
        '''Perfom the function only if certain criteria is found in the record
           Uncombine the record only if 100$a has any
           of the following combine characters āūīḥḍ
        '''
        sample_field = Field(tag="100", indicators=["?", "?"],
                    subfields=[Subfield(code="a", value="[āūīḥḍ]")])
        is_found = findit.find(record, sample_field)
        if is_found:
            extracted_rec = modf.uncombine_diacritics(record, '?')
            print(extracted_rec)   
            user_input = input("Save to MARC file? 'y' : ")
            if user_input == 'y':
               extractednum += 1
               with open('exrt377aARA_Diac.mrc', 'ab') as out:
                    out.write(extracted_rec.as_marc())

    print (f"Total processed records : {extractednum} of {recnum}")
    
