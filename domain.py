#!/usr/bin/python

# domain.py - ZmEu <zmeu@whitehat.ro>
#	- Don't hate me, hate the code.

# Changelog:
#	- first version v0.1 (Sun Sep 30 16:12:34 EEST 2018)
#	- added: time.sleep [slow/fast] check & fixed some lines. (Sun Sep 30 18:20:02 EEST 2018)
#	- added: save domains [registered/reserved]. (Sun Sep 30 10:29:29 CDT 2018)
#	- added: functions [whois/api]. (Sun Sep 30 11:00:25 CDT 2018)

import subprocess, sys, time
from datetime import date
from random import randint

def save(argument1, argument2):
	with open(argument1, "a+") as outfile:
		outfile.write(argument2+"\n")

def whois(argument):
	cmd = "echo '{}\r\n' | nc whois.rotld.ro -s 1.2.3.{} 43".format(argument.rstrip("\r\n"), randint(1, 254))
	ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return ps.communicate()[0]

def api(argument):
	cmd = "curl htts://localhost/api --interface ethX -X POST -F 'domeniu={}' -F 'extensie=ro'".format(argument.replace(".ro", "").rstrip("\r\n"))
	ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

while True:
	with open(sys.argv[1]) as fp:
		for line in fp:
			print "+ we check \033[0;36m{}\033[0m".format(line.rstrip("\r\n"))

			today = date.today()
			t = "{:%Y-%m-%d}".format(today)
			output = whois(line.rstrip("\r\n"))

			if "entries" in output.split():
				api(line.rstrip("\r\n"))
				print "+ we found \033[0;32m{}\033[0m free.".format(line.rstrip("\r\n"))
				save("registered.txt", "{}".format(line.rstrip("\r\n")))

			elif t in output.split():
				print "- we found \033[0;31m{}\033[0m reserved.".format(line.rstrip("\r\n"))
				with open(sys.argv[1], "r") as infile:
					newlist = [i for i in infile.read().split() if i != line.rstrip("\r\n")]
				with open(sys.argv[1], "w") as outfile:
					outfile.write("\n".join(newlist))
				save("deleted.txt", "{}".format(line.rstrip("\r\n")))

			time.sleep(0.03)

# - END OF LINE -
