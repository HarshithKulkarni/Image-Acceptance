from Counter import count_and_fetch
import subprocess
from PIL import Image
from sqlite3 import dbapi2 as sqlite

class model:
	def __init__(self):
		pass
	def accept(self):
		
		lst = []
		idata = []
		obj = count_and_fetch()
		chng_dir = obj.change_directory_to_recent_dir()
		number_of_files = obj.fetch_images_from_recent_directory()
		number_of_files = int(number_of_files)
		dir_count = obj.get_directories_count_from_disk()
		acc = open("image_accept.sh","w")
		acc.write("#!/bin/bash\n")
		acc.write("cd /home/hk/Desktop/tst/{}\n".format(chng_dir))
		acc.write("ls | sort > /media/hk/HK/DERBI/Tech-Tailor/SSHD/list.txt\n")
		acc.close()
		subprocess.call('chmod +x image_accept.sh',shell = True)
		subprocess.call('./image_accept.sh',shell = True)
		
		var = '/home/hk/Desktop/tst/list1.txt'
		with open("/media/hk/HK/DERBI/Tech-Tailor/SSHD/list.txt") as f1, open(var,"w") as f2:
			for i in f1:
				f2.write('/home/hk/Desktop/tst/{}'.format(chng_dir)+i)
				
		with open(var) as q:
			for each_line in q:
				lst.append(each_line)
		
		#for i in lst:
		#	print(i)
		
		print("There are {} Images in {} directory, Do you want to save them (Y 'or' N)?".format(number_of_files,chng_dir))
		n = input()
		if(n=='Y'):
			con = sqlite.connect('blob.db')
			cur = con.cursor()
			cur.execute('''CREATE TABLE `chng_dir` (`Names`	REAL ,Images 	REAL)''')
			for ind,j in enumerate(lst):
				j = j.rstrip()
				file = open(j, 'rb')
				idata.append(file.read())
				temp = idata[ind]
				file.close()
				cur.execute('''INSERT INTO `chng_dir` values (?, ?)''',(file.name, sqlite.Binary(temp)))
				con.commit()
			print("Saved to Database Successfully!!!!")
			
			update_dir_count = open("count.txt","w")
			dir_count = str(dir_count)			
			update_dir_count.write(dir_count)
			update_dir_count.close()
		
		elif(n=='N'):
			
			print("Discarded!!")

if(__name__ == "__main__"):
	model_obj = model()
	model_obj.accept()
