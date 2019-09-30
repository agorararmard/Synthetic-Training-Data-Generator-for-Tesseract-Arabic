from PIL import Image
import os
import sys

dir =  sys.argv[1]

classes = open(dir+'/classes.txt','r')
cont = classes.read()
list = cont.split('\n')
dict ={}
for i in range(len(list)):
    dict[i] = list[i]
#print (dict)
files_names = []
# r=root, d=directories, f = files
for r, d, f in os.walk(dir):
    for file in f:
        if '.txt' in file:
            # print(file, ' ', r, d, f, '\n\n\n\n')
            file_name = file.split('.')[0]
            files_names.append(file_name)

for file in files_names:
    if file != 'classes':
        print(file)
        img_path = dir + '/' + '%s.jpg' % file
        yollo_file_path = dir+'/' + ('%s.txt' % file)
        #gt_file_path = '%s_gt.txt' % file
        box_file_path = dir+'/' + ('%s.box' % file)

        yollo_file = open(yollo_file_path, 'r')
        #gt_file = open(gt_file_path, 'r')
        box_file = open(box_file_path, 'w+')

        #gt_str = gt_file.read()
        im = Image.open(dir + img_path)
        width, height = im.size
        #print(gt_str)
        yollo_data = yollo_file.read()
        yollo_data = yollo_data.split('\n')
        for i, line in enumerate(reversed(yollo_data)):
            if i:
                # print(line)
                line_arr = line.split()
                #print (line)
                x_center = float(line_arr[1]) * width
                y_center = float(line_arr[2]) * height
                box_w = float(line_arr[3]) * width
                box_h = float(line_arr[4]) * height
                l = x_center - box_w/2
                b = height - (y_center - box_h/2)
                r = x_center + box_w/2
                t = height - (y_center + box_h/2)
                if dict[int(line_arr[0])] == 'space':
                    box_file.write("%s %d %d %d %d 0\n" % (' ', l, b, r, t))
                else:
                    box_file.write("%s %d %d %d %d 0\n" % (dict[int(line_arr[0])], l, b, r, t))
                #print(i)

        yollo_file.close()
        #gt_file.close()
        box_file.close()
