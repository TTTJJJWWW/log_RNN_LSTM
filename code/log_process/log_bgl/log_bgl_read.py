import re

def read_write(path_s, path_t):
	with open(path_s, 'r+') as rf:
		for i in range(500):
			print rf.readline(),
			
		'''	msg = re.sub(r'RAS (.*)', '', line)
			with open(path_t, 'w+') as wf:
				if msg != '':				
				f.write(msg+'\n')
		'''		
if __name__ == '__main__':
	path_s = '/home/sc/bgl'
	path_t = '/home/sc'
	read_write(path_s, path_t)