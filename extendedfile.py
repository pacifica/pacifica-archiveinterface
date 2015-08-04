class Extendedfile(file):
	def __init__(self,path,mode):
		file.__init__(self,path,mode)
		
	def status(self):
		return "disk"