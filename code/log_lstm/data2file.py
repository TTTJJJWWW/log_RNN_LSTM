
def write_file(filename, raw_text, text_list):
	with open(filename, 'a') as wf:
		for i in range(len(raw_text)):
			wf.write(raw_text[i] + ' --> ' + text_list[i] + '\n')
			
def write2file(filename, raw_text, text_list):
	with open(filename, 'a') as wf:
		wf.write(raw_text + ' --> ' + ', '.join(text_list[0]) + '\n')
		
def write4file(filename, raw_text, text_list):
	with open(filename, 'a') as wf:
		for i in range(len(raw_text)-4):
			wf.write(raw_text[i] + ', ' + raw_text[i+1] + ', ' + raw_text[i+2] + ', ' + raw_text[i+3] 
			+ ' --> ' + text_list[i] + '\n')

def write_eva(filename, eva_name, eva_value):
	with open(filename, 'w') as we:
		for i in range(len(eva_name)):
			we.write(eva_name[i] + ' = ' + eva_value[i] + '\n')	
	