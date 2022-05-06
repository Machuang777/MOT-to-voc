主要功能是将MOT数据集中的gt.txt转换成对应每帧图片的xml文件，在转换成xml文件后在生成对应的txt文件，便于在YOLO中进行训练。 

一、两种数据格式介绍
1、MOT数据集格式
   --test
   ----MOT16-01
   ------img1（存储数据集照片）
   ------seqinfo.ini（初始化信息）
   ----MOT16-03
   ----MOT16-06
   ----......
   --train
   ----MOT16-02
   ------gt
   --------gt.txt(以txt文件格式存储的ground truth)
   --------img1（存储数据集照片）
   --------seqinfo.ini（初始化信息）
   ----MOT16-04
   ----MOT16-05
   ----......

 
MOT数据中test数据集是没有标注信息的，只有train数据集有标注信息。
有一个比较坑的地方，在train中的gt.txt有的标注信息超出图片范围内，使得在转化后在YOLO中进行训练会报错，需要将其限制在图片大小内。

gt.txt
1,1,912,484,97,109,0,7,1
2,1,912,484,97,109,0,7,1
3,1,912,484,97,109,0,7,1
4,1,912,484,97,109,0,7,1
5,1,912,484,97,109,0,7,1
6,1,912,484,97,109,0,7,1

<frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <>, <classes>, <visibility ratio>
第一个值代表第几帧，第二个代表轨迹编号，bb开头的4个数代表物体框的左上角坐标及长宽
第七个值为目标轨迹是否进入考虑范围内的标志，0表示忽略，1表示active；第八个值为该轨迹对应的目标种类，第九个值为box的visibility ratio，表示目标运动时被其他目标box包含/覆盖或者目标之间box边缘裁剪情况。 
classes = ['Pedestrain', 'Person on vehicle','Car','Bicyle','Motorbike','Non motorized vehicle','Static person','Distractor','Occluder','Occluder on the ground','Occluder full','Reflection']


det.txt
1,-1,1359.1,413.27,120.26,362.77,2.3092,-1,-1,-1
1,-1,571.03,402.13,104.56,315.68,1.5028,-1,-1,-1
1,-1,650.8,455.86,63.98,193.94,0.33276,-1,-1,-1
1,-1,721.23,446.86,41.871,127.61,0.27401,-1,-1,-1
1,-1,454.06,434.36,97.492,294.47,0.20818,-1,-1,-1
1,-1,1254.6,446.72,33.822,103.47,0.14776,-1,-1,-1

<frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z> 
每行10个数字，第一个代表第几帧，第二个代表轨迹编号,
bb开头的4个数代表物体框的左上角坐标及长宽，conf代表置信度，最后3个是MOT3D用到的内容，2D检测总是为-1.

seqinfo.ini文件
主要介绍视频的帧率、分辨率等基本信息。


2、Pascal VOC数据集格式

--VOCdevkit2007
   --VOC2007
      --Annotations (xml格式的文件)
         --000001.xml
      --ImageSets
         --Layout
         --Main
            --train.txt
            --test.txt
            --val.txt
            --trainval.txt
      --Segmentation
      --JPEGImages (训练集和测试集图片)
         --000001.jpg
      --results  

VOC数据集的所有的图片均放在JPEGImages文件夹中，通过在ImageSets中的train.txt和test.txt中来进行训练集和测试集图片的选取

VOC的数据集标注格式为xml文件进行标注，每个xml对应JPEGImage中的一张图片，其中包含了照片的基本信息以及标注的信息

<annotation>
	<folder>photo</folder>
	<filename>00001.jpg</filename>
	<path>E:\MYSELF\make_dataset\photo\00001.jpg</path>
	<source>                      //图像来源（不重要）
		<database>Unknown</database>
	</source>
	<size>                        //图像尺寸（长宽以及通道数） 
		<width>1320</width>
		<height>1080</height>
		<depth>1</depth>
	</size>
	<segmented>0</segmented>      //是否用于分割（在图像物体识别中01无所谓） 
	<object>                      //检测到多个物体 
		<name>surface</name>       //物体类别
		<pose>Unspecified</pose>   //拍摄角度
		<truncated>0</truncated>   //是否被截断（0表示完整）
		<difficult>0</difficult>   //目标是否难以识别（0表示容易识别） 
		<bndbox>                   //bounding-box（包含左下角和右上角xy坐标）
			<xmin>520</xmin>
			<ymin>529</ymin>
			<xmax>601</xmax>
			<ymax>602</ymax>
		</bndbox>
	</object>
	<object>                      //检测到多个物体 
		<name>surface</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>734</xmin>
			<ymin>528</ymin>
			<xmax>901</xmax>
			<ymax>598</ymax>
		</bndbox>
	</object>
</annotation>


二、将MOT数据转换成VOC格式
# 为了避免将MOT数据中多个数据合并在一处时名字重复，需要先将其重命名再合并
1_rename.py

# 对于MOT的标注以fram为主索引，对应图片文件夹中的每一帧，然后需要对每一帧进行归类，将所有的标注信息都获取出来存储到每个图片文件的标注中
2_tovoc.py

# 需要对train.txt进行分割，将其拆分成train,test,val,train_val，可以设置中间的随机参数的阈值来实现各数据集的体量的划分
3_devied.py

# 主要是可视化标注在原图上，用以检验是否标注正确，MOT数据集有些标注超出图片大小
4_show_labels_img.py

# 将xml转换成txt文件，在YOLO训练中需要文件夹labels存放每个图片的标注信息,xml中框的左上角坐标和右下角坐标(x1,y1,x2,y2)，txt中的中心点坐标和宽和高(x,y,w,h)，并且归一化
5_xml2txt.py

02000004.txt
6 0.500260 0.498611 0.050521 0.100926
0 0.748177 0.562500 0.089063 0.352778
0 0.327344 0.535185 0.044271 0.244444
8 0.912500 0.268519 0.173958 0.535185
7 0.614323 0.449537 0.017188 0.082407
7 0.690104 0.453704 0.017708 0.109259

<classes>, <x>, <y>, <w>, <h>

# 还涉及一个问题，需要将train.txt，test.txt，val.txt改成以下格式，可以自己手动调节

val.txt
train_data_MOT16/images/02000004.jpg
train_data_MOT16/images/02000005.jpg
train_data_MOT16/images/02000009.jpg
train_data_MOT16/images/02000010.jpg
train_data_MOT16/images/02000023.jpg
train_data_MOT16/images/02000024.jpg
train_data_MOT16/images/02000036.jpg