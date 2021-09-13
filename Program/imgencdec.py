import numpy
import PIL
import math
import os
import hashlib
import time
import sys
from PIL import Image

m = hashlib.md5()
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'



def loadImg(filename):
    # Convert Image to array
    print "Loading image --- "+filename
    img = PIL.Image.open(filename)
    arr = numpy.array(img)
    # print "Done to array"
    print "Dimensions of the image " + str(arr.shape)
    convarr= arr.copy()
    return convarr

def pixelDiffuse(wx,wy,convarr):
    for i in range(0,numpy.size(convarr,0)):
        for j in range(0,numpy.size(convarr,1)):
            convarr[i,j,0]+= (wx*i+wy*j)*500
            convarr[i,j,1]+= (wx*i+wy*j)*300
            convarr[i,j,2]+= (wx*i+wy*2*j)*500

            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            print ("Diffusion process : " + str((numpy.size(convarr,1)*i+j)*100/(numpy.size(convarr,0)*numpy.size(convarr,1))) + "% done")
            # time.sleep(0.1)
            # print (numpy.size(convarr,1)*i+j)*100/(numpy.size(convarr,0)*numpy.size(convarr,1))
    print "Diffusion process :100% done"
    return convarr

def inversePixelDiffuse(wx,wy,convarr):
    for i in range(0,numpy.size(convarr,0)):
        for j in range(0,numpy.size(convarr,1)):
            convarr[i,j,0]-= (wx*i+wy*j)*500
            convarr[i,j,1]-= (wx*i+wy*j)*300
            convarr[i,j,2]-= (wx*i+wy*2*j)*500

            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            print ("Inverse Diffusion process : " + str((numpy.size(convarr,1)*i+j)*100/(numpy.size(convarr,0)*numpy.size(convarr,1))) + "% done")

    print "Inverse Diffusion process :100% done"
    return convarr

def bandPermute(filename,convarr):
    loop=0
    loop2=0
    width = 20
    hwidth = 20
    cipher = 2

    dummy = convarr[:,width-1:2*width-1,:].copy()
    for x in range(width,numpy.size(convarr,1)):
        loop+=1
        if loop%(cipher*width)==0:
            try:
                temp = convarr[:,x:x+width,:].copy()
                convarr[:,x:(x+hwidth),:] = dummy.copy()
                dummy = temp.copy()
            except Exception as e:
                # print "Loop break because of length problem"
                break

    convarr[:,width-1:2*width-1,:]=dummy.copy()
    # print "second breaking loop is "+str(loop)

    #horizontal
    dummy = convarr[hwidth-1:2*hwidth-1,:,:].copy()
    for x in range(hwidth,numpy.size(convarr,0)):
        loop2+=1
        if loop2%(cipher*hwidth)==0:
            try:
                temp = convarr[x:x+hwidth,:,:].copy()
                convarr[x:(x+hwidth),:,:] = dummy.copy()
                dummy = temp.copy()
            except Exception as e:
                # print "Loop break because of length problem"
                break

    convarr[hwidth-1:2*hwidth-1,:,:]=dummy.copy()
    # print "second breaking loop is "+str(loop2)

    print "Permute done"

    return convarr

def inverseBandPermute(filename,convarr):
    loop=0
    loop2=0
    width = 20
    hwidth = 20
    cipher = 2

    #inverse_permutation_process
    #horizontal

    first = True;
    dummy = convarr[hwidth-1:2*hwidth-1,:,:].copy()
    firstBand = convarr[hwidth-1:2*hwidth-1,:,:].copy()
    thirdBand = convarr[3*hwidth-1:4*hwidth-1,:,:].copy()

    for x in range(hwidth,numpy.size(convarr,0)):
        loop2+=1
        if loop2%(cipher*hwidth)==0:
            try:
                temp = convarr[x:x+hwidth,:,:].copy()
                convarr[(x-2*hwidth):(x-hwidth),:,:] = temp.copy()
                if(numpy.size(convarr,0)-x<cipher*hwidth):
                    #print "I think this is last one at "+str(x)
                    convarr[x:x+hwidth,:,:] = firstBand.copy()
            except Exception as e:
                convarr[x-2*hwidth:x-hwidth,:,:] = firstBand.copy()
                #print "Loop break because of length problem"
                break

    convarr[hwidth-1:2*hwidth-1,:,:]=thirdBand.copy()
    #print "second breaking loop is "+str(loop2)

    #till here

    #vertical

    first = True;
    dummy = convarr[:,width-1:2*width-1,:].copy()
    firstBand = convarr[:,width-1:2*width-1,:].copy()
    thirdBand = convarr[:,3*width-1:4*width-1,:].copy()

    for x in range(width,numpy.size(convarr,1)):
        loop+=1
        if loop%(cipher*width)==0:
            try:
                temp = convarr[:,x:x+width,:].copy()
                convarr[:,(x-2*width):(x-width),:] = temp.copy()
                if(numpy.size(convarr,1)-x<cipher*width):
                    # print "I think this is last one at "+str(x)
                    convarr[:,x:x+width,:] = firstBand.copy()
            except Exception as e:
                convarr[:,x-2*width:x-width,:] = firstBand.copy()
                # print "Loop break because of length problem"
                break

    convarr[:,width-1:2*width-1,:]=thirdBand.copy()
    #print "second breaking loop is "+str(loop2)

    #till here vertical

    print "Inverse Permute done"

    return convarr


def encrypt(password, filename): #password cipher, Filename to encrypt
    imgarray = loadImg(filename)
    lolstring=0;
    # OLD algorithm (ASCII FAIL)
    # for c in password:
    #     lolstring+=ord(c)
    # print "my ord gives "+str(lolstring)

    # if lolstring<300:
    #     lolstring*=31
    # elif lolstring<150:
    #     lolstring*=39
    #
    # print "My lol string here is "+str(lolstring)
    #
    # weightx=lolstring*17
    # weighty=lolstring*23

    m.update(password)
    m.hexdigest()

    # print "my m is "+str(m.hexdigest())

    for c in str(m.hexdigest())[2:30]:
        lolstring+=ord(c)
    # print "my ord gives "+str(lolstring)

    weightx=lolstring*23
    weighty=lolstring*31


    # print "image array first" +str(imgarray[350,350,:])

    imgarray = pixelDiffuse(weightx,weighty,imgarray)

    # print "image array after diffuse is "+str(imgarray[350,350,:])

    imgarray = bandPermute(filename,imgarray)

    img = PIL.Image.fromarray(imgarray)
    print "Done to image"

    saveFileName = os.path.splitext(filename)[0]+"_enc.png"
    img.save(saveFileName, "PNG", subsampling=0, quality=100 )
    print "Saved"
    print filename+" ----> "+saveFileName

def decrypt(password, filename): #password cipher, Filename to encrypt
    imgarray = loadImg(filename)
    lolstring=0;
    # OLD ALGORITHM
    # for c in password:
    #     lolstring+=ord(c)
    # print "my ord gives "+str(lolstring)
    #
    # if lolstring<300:
    #     lolstring*=31
    # elif lolstring<150:
    #     lolstring*=39
    #
    # print "My lol string here is "+str(lolstring)
    #
    # weightx=lolstring*17
    # weighty=lolstring*23

    m.update(password)
    m.hexdigest()

    # print "my m is "+str(m.hexdigest())

    for c in str(m.hexdigest())[2:30]:
        lolstring+=ord(c)
    # print "my ord gives "+str(lolstring)

    weightx=lolstring*23
    weighty=lolstring*31

    imgarray = inverseBandPermute(filename,imgarray)

    # print "image array first is" + str(imgarray[350,350,:])

    imgarray = inversePixelDiffuse(weightx,weighty,imgarray)

    # print "image array after inverse is "+str(imgarray[350,350,:])

    img = PIL.Image.fromarray(imgarray)
    print "Done to image"

    saveFileName = (os.path.splitext(filename)[0])[:-4]+"_dec.png"
    img.save(saveFileName, "PNG", subsampling=0)
    print "Saved"
    print filename+" ----> "+saveFileName

if __name__== "__main__":
  # encrypt("eiffeltower","v1-eiffel-tower-summit-priority.jpg")
  # decrypt("eiffeltower","v1-eiffel-tower-summit-priority_enc.png")

  encrypt("123","LasheetaSahay.jpg")
  decrypt("123","LasheetaSahay_enc.png")
