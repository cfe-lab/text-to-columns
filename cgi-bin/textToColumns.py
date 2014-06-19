#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import cgi

form = cgi.FieldStorage()
userinput = form.getvalue("userinput")
runtranslate = form.getvalue("runtranslate")
dltranslate = form.getvalue("dltranslate")

def printHtmlHeaders():
	print "Content-Type: text/html"
	print
	print """<!DOCTYPE html><html><head>
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script src="../cgi-bin/script.js"></script>
	<link rel="stylesheet" href="../css/style.css"></head><body>"""

def textToColumns(text):
	text = filter(None, text.replace('\r','').split('\n'))
	print '<table>'
	for line in text:
		print '<tr>'
		for char in line:
			print '<td>'
			print char
			print '</td>'
		print '</tr>'
	print '</table>'

def countColumns(text):
	text = filter(None, text.replace('\r','').split('\n'))
	dict = {}
	shortest = len(min(text, key=len))
	i = 0
	while i < shortest:
		column = [x[i] for x in text]
		dict['col'+str(i)] = {}
		for item in column:
			if (item not in dict['col'+str(i)]):
				dict['col'+str(i)][item] = 1
			else:
				dict['col'+str(i)][item] += 1
		i += 1
	return dict

def printFileHeaders(filename):
	print "Content-Disposition: attachment; filename=\""+filename+"\""
	print "Content-Type:application/octet-stream; name=\""+filename+"\""
	print
		
if (runtranslate is not None):
	printHtmlHeaders()
	textToColumns(userinput)
	info = countColumns(userinput)
	i = 0
	print '<table>'
	print '<tr>'
	while i < len(max(userinput.replace('\r','').split('\n'), key=len)):
		print '<td>'
		for column in info['col'+str(i)]:
			print "{}:{}".format(column,info['col'+str(i)][column])
		i += 1
		print '</td>'
	print '</tr>'
	print '</table>'

elif (dltranslate is not None):
	printFileHeaders('columns.csv')
	info = countColumns(userinput)
	text = filter(None, userinput.replace('\r','').split('\n'))
	for line in text:
		print (',').join([x for x in line])
	print (",").join([str((" ").join([y+':'+str(info[x][y]) for y in info[x]])) for x in sorted(info)])
