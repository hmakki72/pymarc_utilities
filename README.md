<H1>Pymarc Utilities</H1>
<p>Pymarc Utilities is a set of functions developed to ease the manipulation of large raw MARC files. These functions are:</p>
<p>Pymarc is required. More information on Pymarc can be found on <a href="https://pypi.org/project/pymarc/" target="_blank">Pymarc 5.1.2 Project page</a>.</p>
<h2>1)	Find: </h2>
<p>
- Find functions allows you to search for target field, indicators, or subfields.</p>
<p>-	Finds MARC records that have Tag 100</p>
<p>-	Finds MARC records that have Tag 100 and first indicator equals 1</p>
<p>-	Finds MARC records where Tag is 100, first indicator equals 1, and subfield $a equals James. You can use regex pattern to find subfield values, for example ^James finds subfield value starts with James.
<p>-	You can find data in a control field as well.
  </p>
	<p ><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;find(record, sample_field)</h3></p>
<p></p>
<h2>2)	Find and Replace:</h2>
<p>
Find and Replace functions allows you to search for target field, indicators, or subfields, and replace it with something else.
	<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;find_and_replace(record, find_field, replace_with_field)</h3>
</p>
<p></p>
<h2>3)	Swap linked fields:</h2>
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
<h2>4)	Uncombine diacritics:</h2>
<p>Replace combined UTF-8 characters to uncombined characters (characters+diacritics)</p>
<p>For example: change combine a macron ā to two characters (a+macron) ā </p> 
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uncombine_diacritics(record, skip_subfield_code)</h3></p>
<p>Use '?' in skip_subfield_code if you want to uncombine all subfields data</p>
<p></p>
<h2>5)	Count number of records in a raw MARC file:</h2>
Retrieves the total number of MARC records in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records_count()</h3></p>
<p></p>
<p><h2>6)	Get MARC records:</h2></p>
This Function retrieves a dataset of MARC records that starts from a record number in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records(5000,5009)</h3></p>
<p>Returns a list of 10 records starting from record number 5000 in a file, and ends with records number 5009.</p>
<p></p>
<p><h1>Export MARC fields to CSV file:</h1></p>
<p><h2>7)	Export Normalized Fields:</h2></p>
This Function retrieves a dataset of MARC records that starts from a record number in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records(5000,5009)</h3></p>
<p>Returns a list of 10 records starting from record number 5000 in a file, and ends with records number 5009.</p>
<p><h2>8)	Export subfields:</h2></p>
This Function retrieves a dataset of MARC records that starts from a record number in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records(5000,5009)</h3></p>
<p>Returns a list of 10 records starting from record number 5000 in a file, and ends with records number 5009.</p>
<p><h2>9)	DB Normalized Export:</h2></p>
This Function retrieves a dataset of MARC records that starts from a record number in a file.
<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;get_records(5000,5009)</h3></p>
<p>Returns a list of 10 records starting from record number 5000 in a file, and ends with records number 5009.</p>
