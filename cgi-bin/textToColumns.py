#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import cgi
import re
import sys
import collections
import cPickle as cp

form = cgi.FieldStorage()
userinput = form.getvalue("userinput")
runtranslate = form.getvalue("runtranslate")
dltranslate = form.getvalue("dltranslate")

# Logging
#logging.basicConfig(
#    filename='errors.log',
#    level=getattr(logging, args.log_level.upper()),
#    filemode='w',
#    format='%(asctime)s %(message)s'
#)

pattern = re.compile(r'(\[.*?\])')

def printHtmlHeaders():
    print "Content-Type: text/html"
    print
    print """<!DOCTYPE html><html><head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="../cgi-bin/script.js"></script>
    <link rel="stylesheet" href="../css/style.css"></head><body>"""

def parseData(text):
    text = filter(None, text.replace('\r','').split('\n'))
    lines = []
    for line in text:
        values = []
        line = filter(None, re.split(pattern, line))
        for i in xrange(len(line)):
            if (line[i][0] != '['):
                line[i] = [x for x in line[i]]
                values += line[i]
            else:
                values.append(line[i])
        lines.append(values)
    return lines

def printFileHeaders(filename):
    print "Content-Disposition: attachment; filename=\""+filename+"\""
    print "Content-Type:application/octet-stream; name=\""+filename+"\""
    print
        
if (runtranslate is not None):
    printHtmlHeaders()
    results = parseData(userinput)
    print '<div class="container">'
    print '<table>'
    for line in results:
        print '<tr>'
        for char in line:
            print '<td>{}</td>'.format(char)
        print '</tr>'
    print '<tr>'
    for column in xrange(len(results[0])):
        print '<td>{}</td>'.format(collections.Counter([x[column] for x in results]))
    print '<tr>'
    print '</table>'
    print '</div>'

elif (dltranslate is not None):
    printFileHeaders('columns.csv')
    parsed = parseData(userinput)
    cp.dump(parsed, open('data','wb'))
    print ("\n").join([(",").join(line) for line in parsed])
    print (',').join([(' ').join(['{}:{}'.format(k,v) for k,v in collections.Counter([y[i] if i < len(y) else 'NAN' for y in parsed]).items()]) for i in xrange(len(parsed[0]))])
