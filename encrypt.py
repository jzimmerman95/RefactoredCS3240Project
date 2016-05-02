
text = ""
with open(file_name, 'rb') as f:
	text = f.read()
cipher_text = des1.encrypt(text)
write_filename = file_name + ".enc"
with open(write_filename, 'wb') as wf:
	wf.write(cipher_text)
return True
