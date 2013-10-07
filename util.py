#! util 

def loggin(log):
	logFile = open('final.log','a')

	logFile.write(log + "\n")

	logFile.close()

def parse_file(file_name):

	config_file = open(file_name,'r')

	result = config_file.readlines()

	result = [ i.replace('\n','') for i in result]

	maze = [ [1 if space  == "#" else 0 for space in i] for i in result ]

	target = [0,0]

	for y,row in enumerate(maze):
		for x,item in enumerate(row):
			if item == '2':
				target = [x,y]

	return maze,target
	
def getValues(context,nkeys):
	result = 0

	for key in nkeys:
		try:
			result = result + context[key]
		except Exception, e:
			pass

	return result