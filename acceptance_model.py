from counter import count_and_fetch
import subprocess
import sqlite3

class model:
	def __init__(self):
		pass
	def accept(self):
		
		obj = count_and_fetch()
		chng_dir = obj.change_directory_to_recent_dir()
		number_of_files = obj.fetch_images_from_recent_directory()
		number_of_files = str(number_of_files)
		number_of_files = number_of_files.strip("b'\\n")
		number_of_files = int(number_of_files)
		dir_count = obj.get_directories_count_from_disk()
		acc = open("image_accept.sh","w")
		acc.write("#!/bin/bash\n")
		acc.write("cd /home/hk/Desktop/tst/{}\n".format(chng_dir))
		acc.write("ls | sort\n")
		acc.write("for i in {1..%d}\n"%(number_of_files))
		acc.write("do\n")
		acc.write("		")
		acc.write("	ls | sort | awk 'NR==$i{print $1}'\n")
		acc.write("done\n")
		acc.close()
		subprocess.call('chmod +x image_accept.sh',shell = True)
		subprocess.call('./image_accept.sh',shell = True)
		print("\n")
		print("There are {} Images in {} directory, Do you want to save them (Y 'or' N)?".format(number_of_files,chng_dir))
		n = input()
		if(n=='Y'):
			conn = sqlite3.connect("Images.db")
			c = conn.cursor()
			for i in range(dir_count):
				c.execute('''CREATE TABLE `{}/` (`Front`	REAL,`Side`	REAL)'''.format(i+1))
				#for j in range(number_of_files):
				#	c.execute('''INSERT INTO `{}/` VALUES(?,?)''',().format(i+1))
				#	conn.commit()
			print("Saved to Database Successfully!!!!")
			update_dir_count = open("count.txt","w")
			update_dir_count.write(dir_count)
			update_dir_count.close()
		
		elif(n=='N'):
			update_dir_count = open("count.txt","w")
			update_dir_count.write(dir_count)
			update_dir_count.close()
			print("Discarded!!")

if(__name__ == "__main__"):
	model_obj = model()
	model_obj.accept()