#!/bin/python
# domain.py - ZmEu <zmeu@whitehat.ro>
# Changelog:
#	- first version v0.1. (Sun Sep 30 16:12:34 EEST 2018)
#	- added time.sleep() & fixed some lines. (Sun Sep 30 18:20:02 EEST 2018)

import subprocess, sys, time
from datetime import date
from random import randint

while True:
	with open(sys.argv[1]) as fp:
		for line in fp:
			print "+ we check \033[0;36m{}\033[0m".format(line.rstrip("\r\n"))
			today = date.today()
			t = "{:%Y-%m-%d}".format(today)
			cmd = "echo '{}\r\n' | nc whois.rotld.ro -s 1.2.3.{} 43".format(line.rstrip("\r\n"), randint(1, 254))
			ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			output = ps.communicate()[0]
			if t in output.split():
				print "- we found \033[0;31m{}\033[0m reserved.".format(line.rstrip("\r\n"))
				with open(sys.argv[1], "r") as infile:
					newlist = [i for i in infile.read().split() if i != line.rstrip("\r\n")]
				with open(sys.argv[1], "w") as outfile:
					outfile.write("\n".join(newlist))
			elif "entries" in output.split():
				print "+ we found \033[0;32m{}\033[0m free.".format(line.rstrip("\r\n"))
				cmd = "curl https://localhost/api.php -X POST -F 'domeniu={}' -F 'extensie=ro'".format(line.replace(".ro", "").rstrip("\r\n"))
				ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			time.sleep(0.05)
