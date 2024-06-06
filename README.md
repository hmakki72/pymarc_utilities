<H1>Pymarc Utilities</H1>
<p>Pymarc Utilities offer a suite of functions designed to facilitate the handling and manipulation of MARC (Machine-Readable Cataloging) records, which are the international standard for bibliographic and related information. These utilities require <a href="https://pypi.org/project/pymarc/" target="_blank">Pymarc 5.1.2 </a>, a Python library, as a prerequisite for their operation. </p>
<p>The utilities include features for finding and replacing data within MARC records, such as specific tags, indicators, or subfields, and can even utilize regular expressions for more complex search patterns. Additionally, they provide the ability to swap linked fields, particularly useful for managing vernacular and Romanized fields in bibliographic records. Another notable function is the uncombining of diacritics, which separates combined UTF-8 characters into their base characters and diacritic marks, aiding in the normalization of text. Lastly, the utilities can count the number of records in a raw MARC file, providing a quick overview of the dataset size. These tools are essential for librarians, archivists, and anyone working with large volumes of bibliographic data, streamlining the process of cataloging and data management.</p>
<p><h1>1- PyMARC_Utilites:</h1></p>
<p><h2>Class FIND_AND_REPLACE</h2></p>
<p>the FIND_AND_REPLACE class provides methods to locate specific data within records, such as tags, indicators, or subfields, and replace them as needed. This can be particularly useful for correcting or updating information across multiple entries. The find function, for example, can locate records with a specific tag, such as Tag 100, and can be refined further to search for records where the first indicator is 1 and the subfield $a contains a certain value, like 'James'. Regular expressions can also be employed for more complex queries, enhancing the precision of searches.</p>
<h2>1.1)	Find: </h2>
<p>
- Find functions allows you to search for target field, indicators, or subfields.</p>
<p>-	Finds MARC records that have Tag 100</p>
<p>-	Finds MARC records that have Tag 100 and first indicator equals 1</p>
<p>-	Finds MARC records where Tag is 100, first indicator equals 1, and subfield $a equals James. You can use regex pattern to find subfield values, for example ^James finds subfield value starts with James.
<p>-	You can find data in a control field as well.
  </p>
	<p ><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;find(record, sample_field)</h3></p>
<p></p>
<h2>1.2)	Find and Replace:</h2>
<p>
Find and Replace functions allows you to search for target field, indicators, or subfields, and replace it with something else.
	<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;find_and_replace(record, find_field, replace_with_field)</h3>
</p>
<p></p>
<h2>1.3)	Swap linked fields:</h2>
<p>
The swap function makes the 880 fields the main fields and converts the main fields into linked fields 880.  Use this function if you want to make the vernacular field the main fields, and make the Romanized fields the linked fields.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;swap_bib_linked_fields(record)</h3></p>
</p>
<p>It converts this:<BR>
      	<br>=100  1\$6880-01$aMuṣṭafá, ʻAbd al-ʻAzīz.
      	<br>=880  1\$6100-01/(3/r‏$a‏مصطفى، عبد العزيز. 
      	<br>To:
     	 <br>=100  1\$6880-01$a‏مصطفى، عبد العزيز.
     	<br>=880  1\$6100-01$aMuṣṭafá, ʻAbd al-ʻAzīz.
</p>
 <p></p>
<p><h1>2- PyMARC Utilities:</h1></p>
<p><h2>Class ENCODING</h2></p> 
<h2>2.1)	Uncombine diacritics:</h2>
<p>Replace combined UTF-8 characters to uncombined characters (characters+diacritics)</p>
<p>For example: change combine a macron ā to two characters (a+macron) ā </p> 
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uncombine_diacritics(record, skip_subfield_code)</h3></p>
<p>Use '?' in skip_subfield_code if you want to uncombine all subfields data</p>
<p></p>
<p><h1>3- PyMARC Utilities:</h1></p>
<p><h2>Class File</h2></p> 
<h2>3.1)	Count number of records in a raw MARC file:</h2>
Retrieves the total number of MARC records in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records_count()</h3></p>
<p></p>
<p><h2>3.2)	Get MARC records:</h2></p>
This Function retrieves a dataset of MARC records that starts from a record number in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records(5000,5009)</h3></p>
<p>Returns a list of 10 records starting from record number 5000 in a file, and ends with records number 5009.</p>
<p></p>

<p><h1>4- Export MARC fields to CSV file:</h1></p>
<p><h2>Class EXPORT_CSV</h2></p>
<p><h2>4.1)	Export Normalized Fields:</h2></p>
 This function removes all subfield codes and delimters from a field,  
 and saves the field into one row of a csv file.
 The csv is column headers are the tags in tags_list
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;normalized_fields_to_csv(records list of PyMARC records, list of tags)</h3></p>
<code> #CVS class calling
  fieldsto_csv = export_csv.EXPORT_CSV('normarlized.csv')
  #normalized_fields_to_csv (records_list, tags_list)
  fieldsto_csv.normalized_fields_to_csv(records_list,['100','245','650'])</code>
  <p></p>
<p>Creates a CSV file with the following headers<br><code>100,245,650</code></p>
<p><h2>4.2)	Export subfields:</h2></p>
It takes 2d list of tags and subfields like this [["245","a","b","z"], ["300","a"], ["264","a","c"]], and exports subfields values in one CSV row. This function retrieves only the first occurrence of the repeated fields and subfields.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;subfields_to_csv(records list of PyMARC records, 2D list if tags and subfields codes)</h3></p>
<code> #Create 2d list
 thislist = [["245","a","b","h"], ["300","a"], ["264","a","c"]]
 #CVS class calling
 fieldsto_csv = export_csv.EXPORT_CSV('subfields.csv')
 #subfields_to_csv
 fieldsto_csv.subfields_to_csv(records_list,thislist)</code>
<p></p>
<p>Creates a CSV file with the following headers<br><code>245a,245b,245h,300a,264a,264c</code></p>
<p><h2>4.3)	DB Normalized Export:</h2></p>
    It extracts records into a sinlge csv file.
    Each record is extracted in rows.
    All rows of a record can be link with a primary key
    and control number in 001.
    Also, this function retains the squence of tags and subfields. .
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;db_normalized_to_csv(records list of PyMARC records)</h3></p>
<p></p>
<code> #CVS class calling
 fieldsto_csv = export_csv.EXPORT_CSV('DB_Normalized.csv')
 #subfields_to_csv
 fieldsto_csv.db_normalized_to_csv(records_list)</code>
<p></p>
<p>Creates a CSV file with the following headers<br><code>PK,001,Tag_Sequence,Tag,Ind1,Ind2,Subfield_Squence,Subfield_code,Field_Value</code></p>
