#!/usr/bin/python


# checkDuplicates.py
# Python 2.7.6

"""
Given a folder, walk through all files within the folder and subfolders
and get list of all files that are duplicates
The md5 checcksum for each file will determine the duplicates.

Then display dupes and give options to delete specified files.
"""

import os
import hashlib
from collections import defaultdict
import csv

src_folder = "/Users/benc/Documents/VIDEO_DUMP/TEST_DUPES"


class DeleteDuplicates:

	def __init__(self, src_folder):
		self.src_folder = src_folder
		self.duplicate_files = None
		self.deleted_dupes = None


	def generate_md5(self, fname, chunk_size=1024):
		"""
		Function which takes a file name and returns md5 checksum of the file
		"""
		print fname
		hash = hashlib.md5()
		with open(fname, "rb") as f:
			# Read the 1st block of the file
			chunk = f.read(chunk_size)
			# Keep reading the file until the end and update hash
			while chunk:
				hash.update(chunk)
				chunk = f.read(chunk_size)

		# Return the hex checksum
		return hash.hexdigest()


	def find_dupes(self):

		# The dict will have a list as values
		md5_dict = defaultdict(list)

		file_types_inscope = ["ppt", "pptx", "pdf", "txt", "html",
							  "mp4", "jpg", "png", "xls", "xlsx", "xml",
							  "vsd", "py", "json", "ari", "ale"]

		# Walk through all files and folders within directory
		for path, dirs, files in os.walk(self.src_folder):
			print("Analyzing {}".format(path))
			for each_file in files:
				if each_file.rsplit(".", 1)[-1].lower() in file_types_inscope:
					# The path variable gets updated for each subfolder
					file_path = os.path.join(os.path.abspath(path), each_file)
					print file_path
					# If there are more files with same checksum append to list
					md5_dict[self.generate_md5(file_path)].append(file_path)

		# Identify keys (checksum) having more than one values (file names)
		self.duplicate_files = [
			val for key, val in md5_dict.items() if len(val) > 1]

		return self.duplicate_files
		

	def delete_dupes_ui(self):
		#. THIS IS THE USER INTERFACE TO DISPLAY & DELETE DUPES
		self.deleted_dupes = []
		os.system('clear')
		if self.duplicate_files:
			print "\nThe following files are duplicates:\n"
			for dup in self.duplicate_files:
				print dup[0][str(dup[0]).rfind("/")+1:]
				
			## Print each duplicate and ask which copies to delete
			for dup in self.duplicate_files:
				print "\n\n" + "*" * 50 + "\n\nFILE: " + (dup[0])[str(dup[0]).rfind("/")+1:]
				c = 1
				tmp_dupes = {}
				for i in dup:
					print str(c) + " - " + i
					tmp_dupes[str(c)] = i
					c += 1
				
				print "\n"	

				ans = True	
				while ans and len(tmp_dupes) > 1:
					print "Which files would you like to delete?  Press ENTER to finish and move to next duplicate."
					resp = raw_input(": ")
					if resp == "":
						ans = False
						
					elif tmp_dupes[resp]:
						os.remove(tmp_dupes[resp])
						print "\nDeleting: " + tmp_dupes[resp] + "\n"
						self.deleted_dupes.append(tmp_dupes[resp])
						tmp_dupes.pop(resp)
					else:
						print "Invalid entry.  Please try again."


			## Print the files which have been deleted
			if self.deleted_dupes:
				print "*" * 50 + "\nDeleted Duplicates: \n"

				for i in self.deleted_dupes:
					print i
				print "\n"
			else: 
				print "No files deleted.\n\n"


		else:
			print "\nNo duplicates found.\n\n"


	def getValue(self, x):
		a,_,b = x.partition(" ")
		if not b.isdigit():
			return (float("inf"), x)
		return (a, int(b))


		

	def make_dupes_csv(self):

		# Write the list of duplicate files to csv file
		with open("duplicates.csv", "w") as log:
			# Lineterminator added for windows as it inserts blank rows otherwise
			csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",",
									lineterminator="\n")
			header = ["File Names"]
			csv_writer.writerow(header)

			for file_name in duplicate_files:
				csv_writer.writerow(file_name)





	def check_duplicates(self):
		self.find_dupes()
		self.delete_dupes_ui()
		# print "\nThe following duplicates were deleted: "
		# for i in self.delete_dupes:
		# 	print self.delete_dupes[i]

if __name__ == "__main__":

	DeleteDuplicates(src_folder).check_duplicates()
