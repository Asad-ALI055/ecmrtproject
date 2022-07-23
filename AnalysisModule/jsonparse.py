import json
import pandas as pd
import os

def get_dirfiles():
    files=os.listdir('darazdata/input')
    filepath=[]
    for file in files:
        print('darazdata/'+file)
        filepath.append('darazdata/input/'+file)

    return filepath


def json_parsing(filepath):
    f=open(filepath, encoding="utf8")
    data1=json.load(f)

    # print(data1['data']['resultValue']['101102']['data'][0]['items'])
    # print(data1['data']['resultValue']['101102']['data'][0]['items'][0]['itemRatingScore'])

    items=data1['data']['resultValue']['101102']['data'][0]['items']
    print(len(items))
    title,rating,price,review,sold,img_link,date=[],[],[],[],[],[],[]
    for c in range(len(items)):
        # print('Ratings :',items[c]['itemRatingScore'])
        # print('Product Title :',items[c]['itemTitle'])
        # print('Price :',items[c]['itemDiscountPrice'])
        # print('Reviews :',items[c]['itemReviews'])

        title.append(items[c]['itemTitle'])
        pri=str(items[c]['itemDiscountPrice']).replace(",","")
        price.append(int(pri))
        rating.append(float(items[c]['itemRatingScore']))
        review.append(int(items[c]['itemReviews']))
        sold.append(int(items[c]['itemSoldCnt']))
        img_link.append(items[c]['itemImg'])

        dt = str(items[c]['__startDate'])
        dt = dt.split("T")
        date.append(dt[0])


    flash_sale_data={
        'Date':date,
        'Product Title':title,
        'Price':price,
        'Rating':rating,
        'Review':review,
        'Sold Products':sold,
        'Image Link':img_link
    }

    # daraz_data=pd.DataFrame(flash_sale_data)
    # daraz_data.to_csv('Daraz_flash_sale.csv',index=False)
    return flash_sale_data

def json_to_csv():
    filepath=get_dirfiles()
    ds=[]
    for file in filepath:
        ds.append(json_parsing(file))

    allfiles = pd.concat(map(pd.DataFrame, ds))
    print(allfiles)
    allfiles.to_csv('darazdata/output/Daraz_alldata.csv',index=False)


# json_to_csv()








# json_parsing('')
# get_dirfiles('')

json_to_csv()