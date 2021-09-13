import getpass
from pathlib import Path
from termcolor import colored
import ketanEnc as ketan

def getPassword():
    pwd1 = getpass.getpass(prompt='Password: ', stream=None)
    pwd2 = getpass.getpass(prompt='Retype password: ', stream=None)
    if (pwd1==pwd2):
        print colored("Passwords match","green")
        return pwd1
    else:
        print colored("Passwords don't match. Try again.","red")
        return getPassword()


print "Hello. Welcome to Ketan's encryption service."
print "1. Encrypt something \n2. Decrypt something"
option = int(input())
if option==1:
    print colored("\nEncryption process","cyan",attrs=['bold','blink'])
    file=raw_input(colored("Filename? ","yellow")).rstrip()
    password=getPassword()
    if Path(file).is_file():
        print "Okay yes"
        ketan.encrypt(password,file)
        print colored("\nEncryption completed","green",attrs=['bold'])
    else:
        print file+" file doesn't exist"
elif option==2:
    print colored("\nDecryption process","cyan",attrs=['bold','blink'])
    file=raw_input(colored("Filename? ","yellow")).rstrip()
    password=getPassword()
    if Path(file).is_file():
        print "Okay yes"
        ketan.decrypt(password,file)
        print colored("\nDecryption completed","green",attrs=['bold'])
    else:
        print file+" file doesn't exist"
else:
    print "Something is wrong with your choice option"
