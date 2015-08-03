import os
import errno
import os.path


def id2dirandfilename(id):
	s = "%x" %(id)
	d = ""
	while len(s) > 2:
		d = "%s/%s" %(d, s[-2:])
		s = s[:-2]
	if d == "":
		f = "file.%s" %(s)
		ff = "/%s" %(f)
		d = "/"
	else:
		f = "%x" %(id)
		ff = "%s/%s" %(d, f)
	return ff

def id2filename(id):
	return id2dirandfilename(id)

if __name__ == '__main__':
	import sys
	#print id2filename(int(sys.argv[1]))