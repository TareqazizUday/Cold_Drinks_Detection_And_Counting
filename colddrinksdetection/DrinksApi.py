from ultralytics import YOLO
import cv2
from collections import Counter


def counter(classes):
     counts = dict(Counter(classes))
     duplicates = {key:value for key, value in counts.items() if value > 1}
     return duplicates

def dict_to_str(dic):
    count_products = list(dic.items())
    print(count_products)
    products = []
    for item in count_products:
        x = ' : '.join(map(str, item))
        products.append(x)
    products = '\n'.join(products)
    return products



def drinksdetection(image_path):
    # image_path = '/home/tareq/Downloads/imas
    image = cv2.imread(image_path)
    drinks = ['7up bottel', '7up can', 'Red Bull bottel', 'Red Bull can', 'clemon bottel', 'clemon can', 'coca cola bottel', 'coca cola can', 'coke bottel', 'coke can', 'fanta bottel', 'fanta can', 'mirinda bottel', 'mirinda can', 'mojo bottel', 'mojo can', 'mountain dew bottel', 'mountain dew bottle', 'mountain dew can', 'pepsi bottel', 'pepsi can', 'speed bottel', 'speed can', 'sprite bottel', 'sprite can', 'tango bottel', 'tango can']
    ds = ['7upB', '7upC', 'RedBB', 'RedBC', 'CB', 'CC', 'CCB', 'CCC', 'CB', 'CC', 'FB', 'FC', 'MB', 'MC', 'MOB', 'MOC', 'MDB', 'MDC','PB', 'PC', 'SPB', 'SPC', 'STB', 'STC', 'TB', 'TC']
    cal = []

    try:
        model = YOLO('/home/tareq/colddrinksdetection/best.pt')  # model path
        results = model.predict(source = image_path, imgsz=640, conf=0.6)  # predict on an image
        tensor_list = results[0].boxes.data
        detection = tensor_list.tolist()
        total_product_count =  len(detection)
        print("Found Products:", total_product_count)
        if len(detection) == 0:
            print("Detected 0 Products")
            return "Unknow","Found 0"
        else:
            for det in detection:
                x,y,w,h = int(det[0]),int(det[1]),int(det[2]),int(det[3])
                confidence = det[4]
                cls = det[5]
                # print("box", x,y,w,h ,"confidence", confidence, "class", drinks[int(cls)])
                cal.append(str(drinks[int(cls)]))
                img = cv2.rectangle(image,(x,y),(w,h),(0,255,0),2)
                # cv2.putText(image, str(ds[int(cls)]), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                
            count_products = counter(cal)
            print(count_products)
            products = dict_to_str(count_products)
            cv2.imwrite(image_path, img)
            return products, total_product_count
    except Exception as e:
        print(e)
        return "ERORR","Unknown"