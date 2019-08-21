# Checked for 3.7?

import cgi, re, sys, os
import collections
#import pickle as cp


def run(userinput, button):
    
	# this holds html file data to be rendered as output.
	output_str = "" 
	pattern = re.compile(r'(\[.*?\])')


	##### Function Definitions


	def printHtmlHeaders():
		return '''{% load static %}<!DOCTYPE html><html><head> <title>Text to Columns - Results</title>
			  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
			  <script src="{% static "ttc_script.js" %}"></script>
			  <link rel="stylesheet" href="{% static "ttc_css/style.css" %}"></head><body>'''

	def parseData(text):
		text = [_f for _f in text.replace('\r','').split('\n') if _f]
		lines = []
		for line in text:
			values = []
			line = [_f for _f in re.split(pattern, line) if _f]
			for i in range(len(line)):
				if (line[i][0] != '['):
					line[i] = [x for x in line[i]]
					values += line[i]
				else:
					values.append(line[i])
			lines.append(values)
		return lines
    

	##### Run Analyis


	#try:   
	if True: 
		if button == "run":
			output_str += printHtmlHeaders()
			results = parseData(userinput)
			output_str += ('<div class="container">\n')
			output_str += ('<table>\n')
			for line in results:
				output_str += ('<tr>\n')
				for char in line:
					output_str += ('<td>{}</td>\n'.format(char))
				output_str += ('</tr>\n')
			output_str += ('<tr>\n')
			for column in range(len(results[0])):
				inner = collections.Counter([x[column] for x in results])
				output_str += ('<td>{}</td>\n'.format( inner ))
			output_str += ('<tr>\n')
			output_str += ('</table>\n')
			output_str += ('</div>\n')
			return (False, output_str)	
		
		elif button == "dl":
			parsed = parseData(userinput)
			#cp.dump(parsed, open('data','wb'))  # Is this a backup file?  TODO: will this get too big? it's 1.6MB already...
			# We don't want any data to be stored on the webserver.
			output_str += (("\n").join([(",").join(line) for line in parsed])) + "\r\n"
			output_str += ((',').join([(' ').join(['{}:{}'.format(k,v) for k,v in list(collections.Counter([y[i] if i < len(y) else 'NAN' for y in parsed]).items())]) for i in range(len(parsed[0]))])) + "\r\n"
			return (True, output_str, 'columns.csv')
	#except Exception:
		#return "<b>Error running analysis,</b> is your data formatted properly?"
