import os
import random
 
root = 'D:/data/MOT_data/MOT16_xml/ImageSets/Main/labels/'
 
fp = open(root + 'train_list.txt')
fp_train = open(root + 'train.txt','w')
fp_test = open(root + 'test.txt','w')
fp_val = open(root + 'val.txt','w')
fp_trainval = open(root + 'trainval.txt' , 'w')
 
 
filenames = fp.readlines()
for i in range(len(filenames)):
    pic_name = filenames[i]
    pic_name = pic_name.strip()
    x = random.uniform(0, 1)
 
    if x >= 0.2:
        fp_trainval.writelines(pic_name + '\n')
    else:
        fp_test.writelines(pic_name + '\n')
 
fp_trainval.close()
fp_test.close()
fp.close()
 
fp = open(root + 'trainval.txt')
filenames = fp.readlines()
for i in range(len(filenames)):
    pic_name = filenames[i]
    pic_name = pic_name.strip()
    x = random.uniform(0, 1)
 
    if x >= 0.4:
        fp_train.writelines(pic_name + '\n')
    else:
        fp_val.writelines(pic_name + '\n')
fp_train.close()
fp_val.close()
fp.close()