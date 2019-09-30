# Tested on Python 3.6.1

import random
import subprocess
from PIL import ImageFont
from PIL import Image
import sys



cp = subprocess.run([
'mkdir', 'generated-data'],stdout = -1)
print(cp.stdout.decode())


State = int(sys.argv[2]);


print('Loading Font and Data...\n')
# loading dataset
f = open("./text-corpus/" + sys.argv[3], "r")
if f.mode == 'r':
    cont = f.read()
    if State & 2:
        # making sure there are no empty strings
        cont = cont.replace('\n', ' ')
        # splitting per item
        x = cont.split(" ")
    else:
        # making sure there are no empty strings
        cont = cont.replace('\n\n', '\n')
        # splitting per item
        x = cont.split("\n")
f.close()

# Directories and common prefix saving name
savedName = "Sample"
outputDir = "./generated-data/"
fontsDir = "./fonts"

# Loading fonts
f = open(fontsDir + "/fonts.txt", "r")
fontFiles = {}
if f.mode == 'r':
    cont1 = f.read()
    tmp = cont1.split("\n")
    for i in tmp:
        if ((i != "") & (i != "\n")):
            tmp2 = str(i).split("$%$")
            fontFiles[tmp2[1]] = tmp2[0]
f.close()

# Declaring variables; N is the number of samples per font.
N = int(sys.argv[1])
height = 400
width = 1200

print('There will be ', N, 'images per font\n', len(fontFiles), ' Fonts in this run\n')


# load the font and image
def testmaker(savedName, IDcnt):
    text = ""

    # Generating sample text; endline seperated;
    if State & 1:
        for i in range(random.randint(1, 4)):
            if (i):
                text = text + " "
            text = text + x[random.randint(0, len(x) - 1)]
    else:
        text = x[random.randint(0, len(x) - 1)]

    outname = savedName + str(IDcnt)
    f1 = open(outputDir + outname + ".gt.txt", "w+")
    f1.write(text)
    f1.close()


# Generating text samples
print('Generating Samples...')
for j in range(N):
    pri = N / 5
    testmaker(savedName, j)
    if (j % pri == 0):
        print((float(j) / N) * 100, '% Done out of ', N, 'Ground-Truths')

# Rendering images
print("Creating Images...")
# counter for display
jcnt = 0
# random ID of the image
ID = 1000
# Font Size
si = 0

for j,k in zip(fontFiles.keys(), fontFiles.values()):
    jcnt += 1
    for i in range(N):
        pri = N / 5
        if (i % pri == 0):
            print((float(i) / N) * 100, '% Done out of ', N, 'images from Patch ', jcnt, 'out of ', len(fontFiles),
                  'Patches')

        # Generating random ID for the sample
        ID = random.randint(10000, 999999999)
        # Choosing random font size
        si = random.randint(6, 9)

        # Reading Ground truth of the sample
        f3 = open(outputDir + str(savedName + str(i)) + ".gt.txt", "r")
        contX = f3.read()
        f3.close()

        # Rendering sample into the data folder using text2image command
        cp = subprocess.run([
            'text2image', '--text', outputDir + str(savedName + str(i)) + '.gt.txt',
            '--outputbase', outputDir + str(savedName + str(ID)), '--fonts_dir',
            fontsDir, '--font', j, '--ptsize', str(si), #'--degrade_image=true',
            '--xsize', str(width), '--ysize', str(height)], stdout=-1)
        print(cp.stdout.decode())

        # writing the sample specific ground-truth
        f4 = open(outputDir + str(savedName + str(ID)) + ".gt.txt", "w+")
        f4.write(contX)
        f4.close()

        #reading the box file to facilitate cropping the image
        f5 = open(outputDir + str(savedName + str(ID)) + ".box", "r")
        contZ = f5.read()
        f5.close()

        Lines = contZ.split('\n')
        minBot = 0x7fffffff
        maxTop = 0
        minLeft = 0x7fffffff
        maxRight = 0
        for line in Lines:
            if(line != ''):
                flag = 0
                if(line[0] == ' '):
                    flag = 1
                    line = line.replace('  ','z ')
                arr = line.split(' ')
                if(flag):
                    arr[0] = ' '
                    flag = 0
                minLeft = min(minLeft, int(arr[1]))
                minBot= min(minBot,int(arr[2]))
                maxRight = max(maxRight,int(arr[3]))
                maxTop = max(maxTop,int(arr[4]))


        #cropping the image to fit the textline
        img = Image.open(outputDir + str(savedName + str(ID))+".tif")
        border = (minLeft-10,height-(maxTop+10),maxRight + 10, height-(minBot-10))
        img2 =img.crop( border)
        img2.save(outputDir+ str(savedName + str(ID))+".tif",dpi=(300,300))

        #modifying the box file to adjust to the new image
        f5 = open(outputDir + str(savedName + str(ID)) + ".box", "r")
        f5.close()
        contZ = f5.read()
        f5 = open(outputDir + str(savedName + str(ID)) + ".box", "w+")

        lines = contZ.split('\n')
        for line in lines:
            if(line != ''):
                flag = 0
                if(line[0] == ' '):
                    flag = 1
                    line = line.replace('  ','z ')
                arr = line.split(' ')
                if(flag):
                    arr[0] = ' '
                    flag = 0
                arr[1] = str(int(arr[1]) - (minLeft-10))
                arr[2] = str(int(arr[2]) - (minBot-10))
                arr[3] = str(int(arr[3]) - (minLeft-10))
                arr[4] = str(int(arr[4]) - (minBot-10))
                for x in range(6):
                    if x:
                        f5.write(' ')
                    f5.write(arr[x])
                f5.write('\n')
        f5.close()




        # removing the general ground-truths files from the data folder
for i in range(N):
    cp = subprocess.run([
        'rm', outputDir + str(savedName + str(i)) + '.gt.txt'], stdout=-1)
    print(cp.stdout.decode())
