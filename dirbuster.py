import requests
import sys
import time
import getopt

options, remainder = getopt.getopt(sys.argv[1:], 'u:e:w:t:o:h', ['url=', 'ext=', 'wordlist=', 'type=','outf=', 'help' ])

URL=""
ext = ""
wordfile = ""
type = ""
outfile=""

for opt, arg in options:
	if opt in ('-u', '--url'):
		URL = arg
	elif opt in ('-e', '--ext'):
		ext = arg
	elif opt in ('-w', '--wordlist'):
		wordfile = arg
	elif opt in ('-t', '--type'):
		type = arg
		if type == 'dir':
			ext = '/'
	elif opt in ('-h', '--help'):
		print("USAGE:",sys.argv[0],"[[--url | -u ] http url ] [[--ext | -e ] file extension or 'empty' ] " )
		print("[[--wordlist | -w ] wordlist ] [[--type | -t ] 'file' or 'dir' (directory) ] " )
		print("[[--outf | -o ] output file ] [[--help | -h ] view this help ]")
		exit(-1)
	elif opt in ('-o', '--outf'):
		outfile = arg


if URL=="" or ext=="" or wordfile=="" or type=="" or (type != 'dir' and type != 'file') :
	print("Not enough paramters or error(s) occured. Please view help.")
	exit(-1)

if ext == 'empty':
	ext = ""

outf = 0

if outfile != "":
	outf = open(outfile,"a")

words=open(wordfile,"rb").read()
wordarr=words.split(bytes((chr(10)).encode()))
print()
f = time.time()
counter = 0
tcounter = 0
outtemp=""

for i in wordarr:
	s = i.decode()
	if type=="file":
		temp = '/' + s + "." + ext
	elif type=="dir":
		temp = '/' + s + '/'
	resp = requests.get(url=URL + temp)
	if resp.status_code == 200:
		print(("\r\x1b[K"),end='',flush=True)
		print("\033[94m" + URL + "\033[96m" + temp)
		if outfile != "":
			outtemp = URL + temp + chr(13) + chr(10)
			outf.write(outtemp)
		continue
	if time.time() - f > 1.0:
		f = time.time()
		print('\x1b[K' + URL + temp.ljust(25) + ("\033[92m" + " " + str(counter) + " requests/sec").ljust(30),end='\r',flush=True)
		tcounter = counter
		counter = 0
		continue
	print('\x1b[K' + URL + temp.ljust(25) + ("\033[92m" + " " + str(tcounter) + " requests/sec").ljust(30),end='\r',flush=True)
	counter = counter + 1
print(("\r\x1b[K"),end='',flush=True)
print()
if outfile != "":
	outf.close()



