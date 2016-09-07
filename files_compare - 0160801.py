from see import *; #log_on(__file__)  # \s*?(# )*?(log|st)\(.*\)` @RFVenter` http://www.rfv.io
import os, datetime, hashlib, argparse, sys, csv, time
from send2trash import send2trash

platform = sys.platform


def calculate_file_properties(file_name):
	# create new list for all files + details
	name = os.path.split(os.path.abspath(file_name))[1]  # get only the name
	if not os.path.isfile(file_name): return {'file_name': file_name, 'name': None}
	stats = os.stat(file_name)
	# get the timestamp in standard python datetime
	if platform == 'win32':
		timestamp = datetime.datetime.fromtimestamp(stats.st_ctime)
	elif platform == 'darwin':
		timestamp = datetime.datetime.fromtimestamp(stats.st_birthtime)
	modified = os.path.getmtime(file_name)  # time of last modification
	file_size = os.path.getsize(file_name)  # file size

	block_size = 65536
	hasher = hashlib.md5()
	with open(file_name, 'rb') as afile:
		buf = afile.read(block_size)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(block_size)
	md5_hash = hasher.hexdigest()
	return {'file_name': file_name,
			'name': name,
			'timestamp': timestamp,
			'modified': modified,
			'file_size': file_size,
			'md5_hash': md5_hash}


def compare_files(left_files, right_files, name=True, timestamp=True, file_size=True, md5_hash=True, modified=True):
	'''
	see if the sources are found anywhere in the target location, may be found in more than one target file location.
	output a list with tab separated fields as follows: source file location, target file location, match type
	'''
	#log('right_files\n' + str(right_files))
	# setup the search list for which properties to be searched
	search_list = []
	if name:
		search_list.append('name')
	if timestamp:
		search_list.append('timestamp')
	if file_size:
		search_list.append('file_size')
	if md5_hash:
		search_list.append('md5_hash')
	if modified:
		search_list.append('modified')
	file_matches = []
	for left in [calculate_file_properties(file) for file in left_files]:
		left_found = False
		if left['name']:
			for right in [calculate_file_properties(file) for file in right_files]:
				property_matches = []
				if right['name'] and left['file_name'] != right['file_name']:
					full_match = True
					for property in search_list:
						if left[property] == right[property]:
							property_matches.append(property)
							left_found = True
						else:
							full_match = False
					if property_matches:
						file_matches.append((left['file_name'], right['file_name'], property_matches, full_match))
		# if the source file is not found in any target file location
		if not left_found:
			file_matches.append((left['file_name'], "", ["not found"], False))
	return file_matches


def main():
	start_time = time.time()
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', required=False, nargs='+', help="List1 (input) file/folder name")
	ap.add_argument('-if', required=False, help="List1 (input) filelist")
	ap.add_argument('-o', required=False, nargs='+', help="List2 (output) file/folder name")
	ap.add_argument('-of', required=False, help="List2 (output) filelist")
	ap.add_argument('-trash', required=False, action="store_true", help="Sent to Trash?")
	ap.add_argument('-noempty', required=False, action="store_true", help="Don't leave folder empty after delete")
	ap.add_argument('-noname', required=False, action="store_true", help="No name search")
	ap.add_argument('-nosize', required=False, action="store_true", help="No file size search")
	ap.add_argument('-nohash', required=False, action="store_true", help="No hash search")
	ap.add_argument('-nocreation', required=False, action="store_true", help="No creation timestamp search")
	ap.add_argument('-nomodified', required=False, action="store_true", help="No modified timestamp search")

	args = vars(ap.parse_args())

	left_list = []
	right_list = []
	if args['if']:
		with open(args['if'], 'r') as left_list_file:
			left_list = left_list_file.read().splitlines()
	if args['i']: left_list += args['i']

	if args['of']:
		with open(args['of'], 'r') as right_list_file:
			right_list = right_list_file.read().splitlines()
	if args['o']: right_list += args['o']

	left_list_exp = []
	right_list_exp = []
	for entry in left_list:
		if os.path.isdir(entry):
			for path, subdirs, files in os.walk(entry):
				for file in files:
					left_list_exp.append(path + '\\' + file)
		else:
			left_list_exp.append(entry)
	for entry in right_list:
		if os.path.isdir(entry):
			for path, subdirs, files in os.walk(entry):
				for file in files:
					right_list_exp.append(path + '\\' + file)
		else:
			right_list_exp.append(entry)

	if args['noname']: name = False
	else: name = True
	if args['nosize']: file_size = False
	else: file_size = True
	if args['nohash']: md5_hash = False
	else: md5_hash = True
	if args['nocreation']: timestamp = False
	else: timestamp = True
	if args['nomodified']: modified = False
	else: modified = True

	compared = compare_files(left_list_exp, right_list_exp, name=name, file_size=file_size, md5_hash=md5_hash,
							 timestamp=timestamp, modified=modified)
	matches = 0
	with open('output.csv', 'wb') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(['input files', 'output files', 'matched attributes', 'all attributes found (trash option)'])
		for result in compared:
			if result[3]:  # if its a full match and trash option selected
				matches += 1
				if args['trash']:
					try:
						send2trash(result[0])
						if args['noempty']: #now check if that folder is empty or contains the .DS_Store file
							folder = os.path.dirname(result[0])
							files = os.listdir(folder)
							if not files or files[0] == ".DS_Store":
								os.rmdir(folder)
					except OSError:
						pass  # file has already been removed from another operation
			csvwriter.writerow([result[0], result[1], ", ".join(result[2]), result[3]])

	print "Time from start to finish: %s seconds" % str(time.time() - start_time)
	print "Total number of source files checked: %d" % len(left_list_exp)
	print "Total number of target locations checked: %d" % len(right_list_exp)
	print "Total number of matches: %d" % matches
	print 'Total number of unique matches: %d' % (len(left_list_exp) - (len(compared) - matches))
	print "Total number of non-matches: %d" % (len(compared) - matches)

if __name__ == '__main__':
	main()
