from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage


import json
import os
import pandas as pd
import cv2
import numpy as np
import statistics


act_url=settings.MEDIA_URL
act_root=settings.MEDIA_ROOT


# Create your views here.

def verif(image_name):

    modelconfiguration = 'C:/Users/Muhammad Umair/PycharmProjects/ProductHunt/producthuntproject/huntapp/yolo configuration files\yolov3.cfg'
    modelweights = 'C:/Users/Muhammad Umair/PycharmProjects/ProductHunt/producthuntproject/huntapp/yolo configuration files\yolov3.weights'
    classesfile_add = 'C:/Users/Muhammad Umair/PycharmProjects/ProductHunt/producthuntproject/huntapp/coco.names'
    classNames = []
    wht = 320
    confidencethreshold = 0.5
    nmsthreshold = 0.3  # lower this more aggressive and less no. of boxes

    with open(classesfile_add, 'rt') as f1:
        classNames = f1.read().rstrip('\n').split('\n')

    print(classNames)
    print(len(classNames))


    # create network
    net = cv2.dnn.readNetFromDarknet(modelconfiguration, modelweights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # find objects
    def findobj(outputs, img):
        ht, wt, chanel = img.shape  # height, width, chanel of image
        bbox = []  # it contain x, y, height, width
        classids = []  # it contain class ids
        confs = []  # confidence value

        for output in outputs:
            for det in output:
                scores = det[5:]  # remove first 5 values
                classid = np.argmax(scores)  # find index of max value
                confidence = scores[classid]  # find confidence value

                # check Confidence threshold to check good or bad detection
                if confidence > confidencethreshold:
                    w, h = int(det[2] * wt), int(det[
                                                     3] * ht)  # output store percentage of width and height we need to multiply by image width & hight to get actual value
                    x, y = int((det[0] * wt) - w / 2), int((det[1] * ht) - h / 2)
                    bbox.append([x, y, w, h])
                    classids.append(classid)
                    confs.append(float(confidence))

        print(len(bbox))
        indices = cv2.dnn.NMSBoxes(bbox, confs, confidencethreshold,
                                   nms_threshold=nmsthreshold)  # it remove the overlaping bounding boxs
        print(indices)
        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(img, f'{classNames[classids[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 255), 2)

            return classNames[classids[i]]

    img =cv2.imread(image_name)

    # convert input into blob image
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (wht, wht), [0, 0, 0], 1, crop=False)

    # give input to network
    net.setInput(blob)

    # get All layers names
    layernames = net.getLayerNames()
    # print(layernames)
    # print(len(layernames))

    # get only output layers (in yolo 3 output layers)
    # in which we get indexes of these layers
    outlayers = net.getUnconnectedOutLayers()
    # print(outlayers)

    # they don't use 0 so need to minus 1 from indexes
    # then display name of outputs
    outlayersnames = [layernames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # print(outlayersnames)

    # get output of output layers



    outputs = net.forward(outlayersnames)
    # print(len(outputs))
    # print(type(outputs))

    # in tuple scond value 85 (0-1 is center x & y points ,width & height,confidence value,object ids)
    #     print(outputs[0].shape)
    #     print(outputs[1].shape)
    #     print(outputs[2].shape)

    # values of output
    print(outputs[0][0])

    # objct detect
    obj_name=findobj(outputs, img)

    print("Object name is ",obj_name)
    return str(obj_name)



def savefile(request,folder):
    settings.MEDIA_URL=act_url
    settings.MEDIA_ROOT=act_root
    if request.FILES['sentFile']:
        myfile = request.FILES['sentFile']
        settings.MEDIA_URL = settings.MEDIA_URL + folder+'/'
        settings.MEDIA_ROOT = settings.MEDIA_ROOT + '/'+folder
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        uploaded_file_url=settings.MEDIA_ROOT+'/'+filename
        return uploaded_file_url




def index(request):
    try:
        if request.method=='POST':
            image_url=savefile(request,'img')
            val='None'
            # val=verif(image_url)

            all_prod_data = product_trend_analysis(val)
            each_web, len_price, p_web = eachproduct_trend(val)
            print(len_price)
            t2 = json.dumps(p_web)
            return render(request, 'producttrend.html',{'len1': len(all_prod_data),'list_values': all_prod_data, 'acc_length': len(each_web),'len_price': len_price, "p_web": t2, 'search_pro_name': val.upper()})
        else:
            return render(request,'index.html')
    except:
        return render(request, 'index.html')

def keyword_search(request):
    val=request.GET['search']
    print(val)
    all_prod_data=product_trend_analysis(val)
    each_web,len_price,p_web=eachproduct_trend(val)
    print(len_price)
    t2=json.dumps(p_web)
    return render(request,'producttrend.html',{'len1':len(all_prod_data),'list_values':all_prod_data,'acc_length':len(each_web),'len_price':len_price,"p_web":t2,'search_pro_name':val.upper()})

def solutions(request):
    return render(request,'solutions.html')

def signup(request):
    return render(request,'signup.html')
def myview(request):
    f = request.FILES['sentFile'] # here you get the files needed
    print(f.name)

def producttrend(request):
    return render(request,'producttrend.html')

def eachtrend(request):
    data=request.GET.get('website1')
    # print("Website Name ",data)   # in data we have website name +product name
    web=data.split(',')[0]
    product=data.split(',')[1].lower()
    # print(web,product)
    p_items_list=['Voltage stabilizer','Vacuum cleaner','Sandwich maker','Electric Kettle','Electric heater','Coffee maker','Microwave oven','Water dispenser','Washing machine','Air conditioner','Hair dryer','Electric shaver','Water geyser']
    for p1 in p_items_list:
        if product in p1.lower():
            product=p1.lower()
            break

    df,_,_=eachproduct_trend(product)
    len_point,product_detail=get_eachproduct_data(df,web)
    max_min_mean=[max(len_point[1]),min(len_point[1]),int(statistics.mean(len_point[1]))]
    # product_detail=json.dumps(product_detail)
    # product_detail=['df','dsf','sde']
    product_detail=json.dumps(product_detail)
    return render(request,'Eachproducttrend.html',{'len_point':len_point,'max_min_mean':max_min_mean,'p_name':product.upper(),'p_web':web,'product_detail':product_detail})


# for products amount vs prices Analysis
def product_trend_analysis(name):

    filenames=os.listdir(os.getcwd()+'/huntapp/FYP Data')
    path=os.getcwd()+'/huntapp/FYP Data/'
    print(filenames)
    combined_csv = pd.concat([pd.read_csv(path+f) for f in filenames])
    print(len(combined_csv['Price']))
    def rep(x):
        x=x.replace('Rs.','')
        return x.replace(',','')
    combined_csv=combined_csv[combined_csv['Product_category'].str.lower()==name.lower()]
    print(len(combined_csv))
    df=combined_csv['Price'].apply(rep).apply(pd.to_numeric)
    all_prod_data=list(df)
    for i in all_prod_data:
        if i > 1000000:
            all_prod_data.remove(i)
    return all_prod_data


def eachproduct_trend(name):
    filenames = os.listdir(os.getcwd() + '/huntapp/FYP Data')
    path = os.getcwd() + '/huntapp/FYP Data/'
    web_list_products=[]
    for i in filenames:
        df=pd.read_csv(path+i)
        df['website']=[i.replace('_data.csv','') for k in range(len(df))]
        web_list_products.append(df)

    combine_csv_web = pd.concat(web_list_products)
    combine_csv_web=combine_csv_web[combine_csv_web['Product_category'].str.lower()==name.lower()]
    print(combine_csv_web)
    print(combine_csv_web['website'].unique())

    df=combine_csv_web.groupby(combine_csv_web['website'])

    p_len,p_price=[],[]
    p_website = list(combine_csv_web['website'].unique())

    for k in df:
        print(k[0])
        print(k[1]['Price'].str.replace(',','').apply(pd.to_numeric))
        p_len.append(len(k[1]['Price']))
        p_price.append(list(k[1]['Price'].str.replace(',','').apply(pd.to_numeric)))

    len_web_price=[p_len,p_price]
    return df,len_web_price,p_website


def get_eachproduct_data(df,web):
    data_p=pd.DataFrame()
    for k in df:
        if k[0]==web:
            data_p=k[1]

    print(data_p)
    len_point = [len(data_p['Price']), list(data_p['Price'].str.replace(',', '').apply(pd.to_numeric))]
    product_detail = [list(data_p['Product_category']), list(data_p['Description']), list(data_p['Image']),list(data_p['Price'])]
    return len_point,product_detail

