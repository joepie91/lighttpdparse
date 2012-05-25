import re, argparse, os

def show_sorted(dictionary):
	for entry in sorted(dictionary, key=dictionary.get, reverse=True):
		if options.has_key('minimum') == False or dictionary[entry] > int(options['minimum']):
			print str(dictionary[entry]).rjust(total_digits), entry
	print ""

parser = argparse.ArgumentParser(description='Parse a lighttpd access log.')

parser.add_argument('logfiles', metavar='logfile', type=str, nargs='+',
                   help='path(s) of the logfile(s)')

parser.add_argument('-e', '--extensions', dest='extensions', action='store',
                   help='specify a comma-separated list of extensions to ignore during parsing')
                   
parser.add_argument('-m', '--minimum', dest='minimum', action='store',
                   help='the counting threshold that has to be exceeded to display the entry')

args = parser.parse_args()
options = vars(args)

referers = {}
days = {}
hosts = {}
files = {}
urls = {}
extensions = {}

total_digits = 10

try:
	ignore_extensions = options['extensions'].split(',')
except AttributeError:
	ignore_extensions = []

for logpath in options['logfiles']:
	try:
		log = open(logpath, 'r')
		
		for line in log:
			ip, hostname, dash, datetime, timezone, method, uri, version, status, size, referer, useragent = line.split(' ', 11)
			datetime = datetime[1:]
			date = datetime.split(':')[0]
			timezone = timezone[:-1]
			method = method[1:]
			version = version[:-1]
			useragent = useragent[1:-2]
			referer = referer[1:-1]
			filename = uri.split('?')[0]
			extension = os.path.splitext(filename)[1][1:]
			
			if extension not in ignore_extensions:
				if hostname not in hosts:
					hosts[hostname] = 0
				
				if referer not in referers:
					referers[referer] = 0
				
				if date not in days:
					days[date] = 0
				
				if filename not in files:
					files[filename] = 0
				
				if uri not in urls:
					urls[uri] = 0
					
				if extension not in extensions:
					extensions[extension] = 0
					
				hosts[hostname] += 1
				referers[referer] += 1
				days[date] += 1
				files[filename] += 1
				urls[uri] += 1
				extensions[extension] += 1
		
		print "Top days:"
		show_sorted(days)
		print ""
		
		print "Top requested hostnames:"
		show_sorted(hosts)
		print ""
		
		print "Top files:"
		show_sorted(files)
		print ""
		
		print "Top extensions:"
		show_sorted(extensions)
		print ""
		
		print "Top referers:"
		show_sorted(referers)
		print ""
		
		print "Top URLs:"
		show_sorted(urls)
		print ""
		
		
	except IOError:
		print "Could not find file %s, ignored entry." % logpath
