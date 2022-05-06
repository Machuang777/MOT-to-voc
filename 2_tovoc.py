import os
import cv2
import codecs
import time
 
classes = ['Pedestrain', 'Person on vehicle','Car','Bicyle','Motorbike','Non motorized vehicle','Static person','Distractor','Occluder','Occluder on the ground','Occluder full','Reflection']
ori_gt_lists = ['D:/data/MOT_data/MOT16/train/MOT16-02/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-04/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-05/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-09/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-10/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-11/gt/gt.txt',
               'D:/data/MOT_data/MOT16/train/MOT16-13/gt/gt.txt']
 
img_dir = 'D:/data/MOT_data/MOT16_xml/JPEGImages/'
annotation_dir = 'D:/data/MOT_data/MOT16_xml/Annotations/'

if not os.path.exists(annotation_dir):
    os.makedirs(annotation_dir)

for each_dir in ori_gt_lists:

    start_time = time.time()

    fp = open(each_dir, 'r')
    userlines = fp.readlines()
    fp.close()

    # 寻找gt中的对应的最大frame
    # max_indx = 0
    # for line in userlines:
    #     e_fram = int(line.split(',')[0])
    #     if e_fram > max_index:
    #         max_index = e_fram
    # print(max_index)
    # 寻找gt中的对应的最大frame并存储fram索引列表
    fram_list = []
    for line in userlines:
        e_fram = int(line.split(',')[0])
        fram_list.append(e_fram)
    max_index = max(fram_list)
    print(each_dir + 'max_index：', max_index)

    for i in range(1, max_index):
        clear_name = each_dir[-12:-10] + format(str(i), '0>6s')
        format_name = clear_name + '.jpg'
        detail_dir = img_dir + format_name
        img = cv2.imread(detail_dir)
        shape_img = img.shape
        height = shape_img[0]
        width = shape_img[1]
        depth = shape_img[2]
        #如果采用index的方法去获取索引只会找到想匹配的第一个数据的索引，后面的索引信息无法获取，所以这里
        #采用enumerate方式来获取所有匹配的索引
        each_index = [num for num,x in enumerate(fram_list) if x == (i)]

        with codecs.open(annotation_dir + clear_name + '.xml', 'w') as xml:
            xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'voc' + '</folder>\n')
            xml.write('\t<filename>' + format_name + '</filename>\n')
            # xml.write('\t<path>' + path + "/" + info1 + '</path>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database> The MOT16 </database>\n')
            xml.write('\t</source>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>' + str(width) + '</width>\n')
            xml.write('\t\t<height>' + str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            for j in range(len(each_index)):
                num = each_index[j]

                x1 = int(userlines[num].split(',')[2])
                y1 = int(userlines[num].split(',')[3])
                x2 = int(userlines[num].split(',')[4])
                y2 = int(userlines[num].split(',')[5])

                # 调整边框，不至于出界
                if x1 <= 0:
                    x1 = 1
                if y1 <= 0:
                    y1 = 1

                xml.write('\t<object>\n')
                xml.write('\t\t<name>' + classes[int(userlines[num].split(',')[7]) - 1] + '</name>\n')
                xml.write('\t\t<pose>Unspecified</pose>\n')
                xml.write('\t\t<truncated>0</truncated>\n')
                xml.write('\t\t<difficult>0</difficult>\n')
                xml.write('\t\t<bndbox>\n')
                xml.write('\t\t\t<xmin>' + str(x1) + '</xmin>\n')
                xml.write('\t\t\t<ymin>' + str(y1) + '</ymin>\n')
                if x1 + x2 >= width:
                    xml.write('\t\t\t<xmax>' + str(width - 1) + '</xmax>\n')
                else:
                    xml.write('\t\t\t<xmax>' + str(x1 + x2) + '</xmax>\n')
                if y1 + y2 >= height:
                    xml.write('\t\t\t<ymax>' + str(height - 1) + '</ymax>\n')
                else:
                    xml.write('\t\t\t<ymax>' + str(y1 + y2) + '</ymax>\n')
                xml.write('\t\t</bndbox>\n')
                xml.write('\t</object>\n')

            xml.write('</annotation>')

    end_time = time.time()
    print('process {} cost time:{}s'.format(each_dir,(end_time-start_time)))

print('succeed in processing all gt files')