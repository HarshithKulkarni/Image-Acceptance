import subprocess

class count_and_fetch:
	
	def __init__(self):
		file = open("count.txt","r")
		self.count = file.read()
		self.count = int(self.count)
		print("The Saved Count is {}".format(self.count))
		#self.get_directories_count_from_disk()

	def get_directories_count_from_disk(self):
		self.dcd = subprocess.check_output('./count_directories.sh')
		self.dcd = str(self.dcd)
		self.dcd = self.dcd.strip("b'\\n")
		self.dcd = int(self.dcd)
		print("Live Directories Count is {}".format(self.dcd))
		return self.dcd
		#self.check_for_update()

	def check_for_update(self):
		if(self.count == self.dcd):
			print("No New Uploads!!!")
			return 0
		else:
			#Check for the recently created directory.
			self.recent_dir = subprocess.check_output('./recent_directory.sh')
			self.recent_dir = str(self.recent_dir)
			self.recent_dir = self.recent_dir.strip("b'\\n")
			print("The recently generated directory is {}".format(self.recent_dir))
			self.change_directory_to_recent_dir()
	
	def change_directory_to_recent_dir(self):
		self.cd = subprocess.check_output('./cd_to_recent_directory.sh',shell = True)
		self.cd = str(self.cd)
		self.cd = self.cd.strip("b'\\n")
		return self.cd
		self.fetch_images_from_recent_directory()

	def fetch_images_from_recent_directory(self):
		export = open("fetch_files.sh","w")
		export.write("#!/bin/bash\n")
		export.write("var="+self.cd+"\n")
		export.write("cd /home/hk/Desktop/tst/$var\n")
		export.write("/bin/ls -1U | wc -l\n")
		export.close()
		subprocess.call('chmod +x fetch_files.sh',shell = True)
		number_of_files = subprocess.check_output('./fetch_files.sh',shell = True)
		number_of_files = str(number_of_files)
		number_of_files = number_of_files.strip("b'\\n")
		#print("The number of Images in {} is {}".format(self.recent_dir,number_of_files))
		return number_of_files

if(__name__ == "__main__"):
	counter_obj = count_and_fetch()
	dcd = counter_obj.get_directories_count_from_disk()
	var = counter_obj.check_for_update()
	if(var is not 0):
		chng_dir = counter_obj.change_directory_to_recent_dir()
		number_of_files = counter_obj.fetch_images_from_recent_directory()
