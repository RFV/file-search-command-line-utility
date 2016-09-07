#@RFVenter` rfv.io
from see import *; log_on(__file__) #\s*(log|st)\(.*\)
import os, datetime, hashlib, argparse, send2trash

def compare_files(left_files, right_files):
	'''
	see if the sources are found anywhere in the target location, may be found in more than one target file location.
	output a list with tab separated fields as follows: 
		source file location, target file location, match type
	'''
	def calculate_file_properties(file_name):
		'''
		?????file attributes
		'''
		def get_file_hash(file_name): #returns a md5 hash of file, and put into another function because its only used here in this function
			BLOCKSIZE = 65536
			hasher = hashlib.md5()
			with open(file_name, 'rb') as afile:
				buf = afile.read(BLOCKSIZE)
				while len(buf) > 0:
					hasher.update(buf)
					buf = afile.read(BLOCKSIZE)
			return hasher.hexdigest()
		#create new list for all files + details
		name = os.path.split(os.path.abspath(file_name))[1]								#get only the name
		timestamp = datetime.datetime.fromtimestamp(os.stat(file_name).st_birthtime)	#get the timestamp in standard python datetime
		modified = os.path.getmtime(file_name) 											#time of last modification
		file_size = os.path.getsize(file_name)											#file size
		md5_hash = get_file_hash(file_name)												#hash of file to see if its the same
		return (name, timestamp, modified, file_size, md5_hash)
	
	left_calculated = [calculate_file_properties(file) for file in left_files]
	right_calculated = [calculate_file_properties(file) for file in right_files]
	file_matches = []
	for left in left_calculated:
		for right in right_calculated:
			property_matches = []
			for property in ('name', 'timestamp', 'modified', 'file_size', 'md5_hash'):
				if left[property] == right[property]: property_matches.append(property)
				if property_matches: file_matches.append((left, right, property_matches))
			#if the source file is not found in any target file location
			if not property_matches: file_matches.append((left, left, "not found"))
	return file_matches

def main():
	'''
	take as input a list of files and/or folders, or a file containing same
	search another list of files and/or folders, or a file containing same
	Sample arguments:
		utilityname -i filename1 filename2 -o location1 location2 
		utilityname -if filelist_i -o location1 location2
		utilityname -i filename1 -of filelist_o
		utilityname -if filelist_i -of filelist_o
		utilityname -if filelist_i -of filelist_o -trash
		-trash	  indicates that matching source filename and/or directories should be moved to Finder Trash
		-noempty  indicates that directories left empty as a result of -trash (ignoring the .DS_Store file) should also be  moved to the Finder Trash
		An optional argument to the utility will move source file(s) to the Finder Trash (not delete). Source file(s) and target location(s) may be on remotely mounted drives, so the optional "move to trash" feature will need to determine if this is the case, and, if so, "move to trash" on the remote volume and not "move to trash" on the target volume which would force a cross-volume move.
	'''
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', nargs='+', help = "List1 file/folder name")
	ap.add_argument('-if', help = "List1 filelist")
	ap.add_argument('-o', nargs='+', help = "List2 file/folder name")
	ap.add_argument('-of', help = "List2 filelist")
	ap.add_argument('-trash', help = "Sent to Trash?")
	args = vars(ap.parse_args())
	# st()
	left_list = []; right_list = []
	if args['if']:
		with open(args['if'], 'r') as left_list_file:
			left_list = [file for file in left_list_file.read()]
	if args['of']:
		with open(args['of'], 'r') as right_list_file:
			right_list = [file for file in right_list_file.read()]

	for entry in args['i']:
		if os.path.isdir(entry): left_list += os.listdir(entry)
		else: left_list.append(entry)
	for entry in args['o']:
		if os.path.isdir(entry): rigth_list += os.listdir(entry)
		else: rigth_list.append(entry)

	st()


if __name__ == '__main__':
	main()

