import torch
import os
import cv2
from yolo.utils.utils import *
from predictors.YOLOv3 import YOLOv3Predictor
#from predictors.DetectronModels import Predictor
import glob
from tqdm import tqdm
import sys
import argparse



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()


#YOLO PARAMS
yolo_df2_params = {   "model_def" : "yolo/df2cfg/yolov3-df2.cfg",
"weights_path" : "yolo/weights/yolov3-df2_15000.weights",
"class_path":"yolo/df2cfg/df2.names",
"conf_thres" : 0.5,
"nms_thres" :0.4,
"img_size" : 416,
"device" : device}

yolo_modanet_params = {   "model_def" : "yolo/modanetcfg/yolov3-modanet.cfg",
"weights_path" : "/Users/MaryamForootaninia/Desktop/Clothing-Detection-master/yolomodels/yolov3-modanet_last.weights",
"class_path":"yolo/modanetcfg/modanet.names",
"conf_thres" : 0.5,
"nms_thres" :0.4,
"img_size" : 416,
"device" : device}


#DATASET
dataset = 'modanet'


if dataset == 'df2': #deepfashion2
    yolo_params = yolo_df2_params

if dataset == 'modanet':
    yolo_params = yolo_modanet_params


#Classes
classes = load_classes(yolo_params["class_path"])

#Colors
cmap = plt.get_cmap("rainbow")
colors = np.array([cmap(i) for i in np.linspace(0, 1, 13)])
#np.random.shuffle(colors)



#


model = 'yolo'

if model == 'yolo':
    print("yolo")
    detectron = YOLOv3Predictor(params=yolo_params)
#else:
    #detectron = Predictor(model=model,dataset= dataset, CATEGORIES = classes)

#Faster RCNN / RetinaNet / Mask RCNN

def getListOfFiles(_directory):
    listOfFiles = os.listdir(_directory)
    allFiles = []
    for entry in listOfFiles:
        fullpath = os.path.join(_directory,entry)

        if os.path.isdir(fullpath):
            allFiles = allFiles + getListOfFiles(fullpath)
        else:
            allFiles.append(fullpath)
    return allFiles
        
 

def filter(_directory):
    #files = getListOfFiles(_directory)
    with open('detection.txt', 'a') as fp:
        with open(product_images_file, 'r') as f1, open(product_ids_file, 'r') as f2:
            pImages = f1.readlines()
            PIds = f2.readlines()

            ##print(pImages)
            ##print(PIds)

            for _id in PIds:
                for image in pImages:
                    if image.find(str(_id)):
                        '''if not os.path.exists(_file):
                            print('Img does not exists..')
                            #continue'''
                        print(image)

                        img = cv2.imread(image)
                        detections = detectron.get_detections(img)
                        if len(detections) != 0:
                            detections.sort(reverse=False ,key = lambda x:x[4])
                            for x1, y1, x2, y2, cls_conf, cls_pred in detections:

                                    #feat_vec =detectron.compute_features_from_bbox(img,[(x1, y1, x2, y2)])
                                    #feat_vec = detectron.extract_encoding_features(img)
                                    #print(feat_vec)
                                    #print(a.get_field('features')[0].shape)
                                    print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf))


                                    #color = bbox_colors[np.where(unique_labels == cls_pred)[0]][0]
                                    color = colors[int(cls_pred)]

                                    color = tuple(c*255 for c in color)
                                    color = (.7*color[2],.7*color[1],.7*color[0])

                                    font = cv2.FONT_HERSHEY_SIMPLEX


                                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                                    text =  "%s conf: %.3f" % (classes[int(cls_pred)] ,cls_conf)
                                    fp.write(_id + "\t" + image + "\t" + x1 + "\t" + y1 + "\t" + x2 + "\t" + y2 + "\t" + int(cls_pred) + "\t" + cls_conf + "\n")
                                    '''cv2.rectangle(img,(x1,y1) , (x2,y2) , color,3)
                                    y1 = 0 if y1<0 else y1
                                    y1_rect = y1-25
                                    y1_text = y1-5

                                    if y1_rect<0:
                                        y1_rect = y1+27
                                        y1_text = y1+20
                                    cv2.rectangle(img,(x1-2,y1_rect) , (x1 + int(8.5*len(text)),y1) , color,-1)
                                    cv2.putText(img,text,(x1,y1_text), font, 0.5,(255,255,255),1,cv2.LINE_AA)

                                    img_id = _file.split(jpeg_product_directory)[-1]
                                    tokens = []
                                    for token in img_id.split('/'):
                                        tokens.append(token)
                                    output_directory = ""
                                    if len(tokens) == 3:
                                        if not os.path.isdir(home + '/' + jpeg_product_directory + tokens[0] + '/' + tokens[1] + '/'):
                                            os.makedirs(home + '/' + jpeg_product_directory + tokens[0] + '/' + tokens[1] + '/')
                                        output_directory = home + '/' + jpeg_product_directory + tokens[0] + '/' + tokens[1] + '/'
                                    else:
                                        if not os.path.isdir(home + '/' + jpeg_product_directory + tokens[0] + '/'):
                                            os.makedirs(home + '/' + jpeg_product_directory + tokens[0] + '/')
                                        output_directory = home + '/' + jpeg_product_directory + tokens[0] + '/'

                                    img_id = img_id.split('/')[-1]
                                    cv2.imwrite(output_directory+ '{}'.format(img_id),img)'''
                        '''else:
                            with open(ignored_file, 'a') as fp:
                                fp.write(_file )'''


def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments for cleaning jpeg data')
    parser.add_argument('--input', type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    jpeg_product_directory = "JPEG/Product/"
    product_images_file = "product_images.txt"
    product_ids_file = "product_ids.txt"

    #if not os.path.exists('detection.txt'):
        #os.mknod('detection.txt')

    home = os.path.expanduser('~')
    ignored_file = os.path.join(home + '/ignored.txt')
    filter(args.input)
