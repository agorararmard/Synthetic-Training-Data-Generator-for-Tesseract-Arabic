from PIL import Image
import os
import sys

dir = sys.argv[1]

files_names = []
# r=root, d=directories, f = files
for r, d, f in os.walk(dir):
    for file in f:
        if '.jpg' in file:
            # print(file, ' ', r, d, f, '\n\n\n\n')
            file_name = file.split('.')[0]
            files_names.append(file_name)

for file in files_names:
    print(file)
    img_path = dir+'/' + ('%s.jpg' % file)

    im = Image.open(img_path)
    im.save(dir +'/'+ file +".tif",dpi=(300,300))
    im.close
    #width, height = im.size
