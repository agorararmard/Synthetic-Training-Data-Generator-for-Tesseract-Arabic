import random
import sys

f = open(str(sys.argv[1]), "r")
if f.mode == 'r':
    cont = f.read()
    target = random.randint(1,6)
    cnt = 0
    for i in range(len(cont)):
        if(cont[i] == ' '):
            cnt+=1
            if(cnt == target):
                cont = cont[:i]+'\n'+cont[i+1:]
                cnt = 0
                target = random.randint(1,6)
f.close()

f1 = open(str(sys.argv[2]), "w+")
f1.write(cont)
f1.close()
