import re

file = open('messages(10.26-11.2)', 'rb+')
lines = file.readlines()
for line in lines:
	time_regex = ur"[A-z]* \s?\d+ \d+\:\d+\:\d+"
	node_n_regex = ur" [c][A-z]*\-?\d?\d?\-?\d?\d?\.?[A-z]*"
	app_regex = ur"[a-z]+\[?\["
	pro_id_regex = ur"\d*\]"
	msg_regex = ur"[A-Z][A-z]*\:.+"
	timestamp = re.findall(time_regex, line)
	node_name = re.findall(node_n_regex, line)
	application = re.findall(app_regex, line)
	process_id = re.findall(pro_id_regex, line)
	message = re.findall(msg_regex, line)
	if application and process_id and message:
		print timestamp[0]
		print node_name[0][1:]
		print application[0][:-1]
		print process_id[0][:-1]
		print message[0][:-1]
file.close()
