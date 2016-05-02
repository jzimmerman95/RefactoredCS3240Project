import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES
from Crypto import Random
import ast

def login():
    print("Please enter your username: ")
    username = input()
    print("Please enter your password: ")
    password = input()
    s=requests.Session()
    rpost = s.post('http://safecollab18.herokuapp.com/auth_user_fda', data={'username': username, 'password': password})
    print(rpost.content.decode('utf-8'))
    if (rpost.content.decode('utf-8') == "Successful Login"):
        print("Type v to view reports, type e to encrypt a file, or type q to quit")
        ans = input()
        if ans == 'v':
            print("Your reports are displayed below. Type q at any point to quit.")
            menu(username)
        if ans == 'e':
            print("Please enter the name of the file that you would like to encrypt:")
            filename = input()
            encrypt_file(username, filename)
        if ans == 'q':
            print("Goodbye")
    else:
        print("Type t to try again, and type q to quit")
        user_input = input()
        if user_input == 't':
            login()
        else:
            print("Goodbye")

def menu(username):
    s=requests.Session()
    rpost = s.post('http://safecollab18.herokuapp.com/fda_reports', data={'username':username})
    #print(rpost.status_code)
    print(rpost.text)
    print("Type the ID of the report that you would like to view")
    idNo = input()
    if idNo == 'q':
        print("Goodbye")
        return
    else: 
        getReport(username, idNo)

def getReport(username, idNo):
    s=requests.Session()
    rpost = s.post('http://safecollab18.herokuapp.com/fda_view_files', data={'username':username, 'id': idNo})
    #print(rpost.status_code)
    print(rpost.text)
    print("Type the ID of the file that you would like to download")
    idNo = input()
    if idNo == 'q':
        print("Goodbye")
        return
    else:
        checkEncryption(username, idNo)
        return
        #downloadFile(username, idNo)

def checkEncryption(username, idNo):
    s=requests.Session()
    rpost = s.post('http://safecollab18.herokuapp.com/check_encryption', data={'id': idNo}) 
    if rpost.text == "False":
        downloadFile(username, idNo)
    else:
        # TODO: encryption stuff
        downloadEncryptedFile(username, idNo)
        pass

def downloadFile(username, idNo):
    s=requests.Session()
    response = s.post('http://safecollab18.herokuapp.com/download_files_fda', data={'id': idNo}, stream=True)
    print("What would you like to name the file?")
    filename=input()
    with open(filename, 'wb') as handle:
        if not response.ok:
            pass

        for block in response.iter_content(1024):
            handle.write(block)
    print("The file was downloaded to "+filename)
    menu(username)

def downloadEncryptedFile(username, idNo):
    s=requests.Session()
    response = s.post('http://safecollab18.herokuapp.com/download_files_fda', data={'id': idNo}, stream=True)
    print("What would you like to name the file?")
    filename=input()
    print("Please enter your private encryption key: ")
    privateKey = input()
    privateKey = privateKey.strip('-----BEGIN RSA PRIVATE KEY-----')
    privateKey = privateKey.strip('-----END RSA PRIVATE KEY-----')
    privateKey = privateKey.strip()
    privateKey = privateKey.replace(' ', '\r\n')
    privateKey = '-----BEGIN RSA PRIVATE KEY-----\r\n' + privateKey + '\r\n-----END RSA PRIVATE KEY-----'
    privateKey = ''.join(privateKey)
    privateKey = RSA.importKey(privateKey)
    text = ""
    for block in response.iter_content(1024):
        text = text+str(block) #write?
    # decrypt the text
    decrypted = privateKey.decrypt(ast.literal_eval(text))
    # write to a file
    with open(filename, 'wb') as wf:
        wf.write(decrypted)
    print("The file was decrypted and downloaded to "+filename)
    menu(username)

def encrypt_file(username, filename):  
    s=requests.Session()
    response = s.post('http://safecollab18.herokuapp.com/get_pub_key_fda', data={'username':username})
    pubKey = response.text
    pubKey = RSA.importKey(pubKey)
    
    text = ""
    with open(filename, 'rb') as f:
        text = f.read()
    cipher_text = pubKey.encrypt(text, 32)[0]

    write_filename = filename + ".enc"
    with open(write_filename, 'wb') as wf:
        wf.write(cipher_text)
    print("The file has been encrypted and saved as "+filename+".enc")
    print("Type v to view reports, type e to encrypt a file, or type q to quit")
    ans = input()
    if ans == 'v':
        print("Your reports are displayed below. Type q at any point to quit.")
        menu(username)
    if ans == 'e':
        print("Please enter the name of the file that you would like to encrypt:")
        filename = input()
        encrypt_file(username, filename)
    if ans == 'q':
        print("Goodbye")


if __name__=='__main__':
    login()