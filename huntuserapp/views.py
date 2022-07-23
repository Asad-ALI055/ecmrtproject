from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os

from AnalysisModule.SalesAnalysis import preprocess,myanalysis
from AnalysisModule.DFSA import daraz_analysis_function
from SeoKeywordRecommend.SeoKeyword import seokeyword
from PlatformRecommend.recommendplatform import Platform_Recommendation
from SalesPrediction.SalesPrediction import linear_prediction
from SalesPrediction.getcolumns import get_columns

act_url=settings.MEDIA_URL
act_root=settings.MEDIA_ROOT
# Create your views here.

def login(request):
    if request.method=='POST':
        username = request.POST.get('username1')
        password = request.POST.get('password1')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'userapp/dashboard.html')
        else:
            return redirect('/')



def users(request):
    if request.method=='POST':
        f_name=request.POST.get('first_name')
        l_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        conf_password = request.POST.get('confirm_password')
        l1=[f_name,l_name,username,email,password]

        if password==conf_password:
            if User.objects.filter(username=username).exists():
                print('Username Taken')
                messages.error(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                print('Email Taken')
                messages.error(request,'Email Taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password,first_name=f_name,last_name=l_name)
                user.save()
                print("User Sign Up Successfully!!")
                messages.error(request,'Sign Up Successfully!!')
                # return render(request,'hello.html',{'signup_data':l1})
                return redirect('signup')
        return redirect('signup')
    else:
        return HttpResponse("Error User Not Sign Up Try Again!!!")




def analysis(path):
    # _,dict1=preprocess()
    dict1=myanalysis(path)
    print(dict1)
    return dict1

def dashboard(request):
    return render(request,'userapp/dashboard.html')

def savefile(request,folder):
    settings.MEDIA_URL=act_url
    settings.MEDIA_ROOT=act_root
    if request.FILES['myfile']:
        myfile = request.FILES['myfile']
        settings.MEDIA_URL = settings.MEDIA_URL + folder+'/'
        settings.MEDIA_ROOT = settings.MEDIA_ROOT + '/'+folder
        print(settings.MEDIA_ROOT)
        fs = FileSystemStorage()
        print(settings.MEDIA_URL)
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        uploaded_file_url=settings.MEDIA_ROOT+'/'+filename
        print(uploaded_file_url)
        return uploaded_file_url

def sales_analysis(request):
    try:
        if request.method=='POST':
            uploaded_file_url=savefile(request,'Userinput_analysis_dataset')
            dict1=analysis(uploaded_file_url)
            return render(request,'userapp/salesanalysis.html',{'dict':dict1,'city2':dict1['city2'],'product4':dict1['product4']})
        else:
            return render(request, 'userapp/salesanalysis_front.html')
    except:
        if uploaded_file_url is not None:
            os.remove(uploaded_file_url)
        messages.error(request, 'Invalid Dataset!')
        return redirect('sales-analysis')


def platform_recommend(request):
    settings.MEDIA_ROOT=act_root
    settings.MEDIA_URL=act_url
    try:
        val1 = request.GET.get('platform')
        if val1 is not None:
            group_dict = Platform_Recommendation(val1, settings.MEDIA_ROOT + '/platform_data/')
            return render(request, 'userapp/platformrecommendation.html', {'group_dict': group_dict})

        return render(request,'userapp/platformrecommendation.html')
    except:
        messages.error(request, 'This Keyword Not Exist!')
        return redirect('platform-recommendation')


def sales_predication(request):
    settings.MEDIA_ROOT=act_root
    settings.MEDIA_URL=act_url
    try:
        if request.method=='POST':
            uploaded_file_url=savefile(request,'Userinput_predictiondataset')
            columns=get_columns(uploaded_file_url)
            return render(request,'userapp/salespredication_column.html',{'file_name':uploaded_file_url,'columns':columns})
        else:
            return render(request, 'userapp/salespredication_front.html')
    except:
        if uploaded_file_url is not None:
            os.remove(uploaded_file_url)
        messages.error(request, 'Invalid Dataset!')
        return redirect('sales-predication')

def actual_prediction(request):
    try:
        uploaded_file_url=request.GET.get('path_data')
        target_column=request.GET.get('target')
        x_column=request.GET.get('Independent_column')
        dict_predict = linear_prediction(uploaded_file_url, target_column, x_column)
        return render(request,'userapp/salespredication.html',{'dict_predict':dict_predict})
    except:
        if uploaded_file_url is not None:
            os.remove(uploaded_file_url)
        messages.error(request, 'Invalid Dataset!')
        return redirect('sales-predication')



def seo_keyword(request):
    settings.MEDIA_ROOT=act_root
    settings.MEDIA_URL=act_url
    try:
        val1=request.GET.get('seo_keyword')
        print(val1)
        print(settings.MEDIA_ROOT)
        if val1 is not None:
            seo_dict = seokeyword(val1,settings.MEDIA_ROOT+'/seo_keyworddata/')
            return render(request, 'userapp/SEOkeyword.html',{'seo_dict':seo_dict})

        return render(request,'userapp/SEOkeyword.html')
    except:
        messages.error(request, 'This Keyword Not Exist!')
        return redirect('seo-keyword')


def daraz_analysis(request):
    settings.MEDIA_ROOT=act_root
    settings.MEDIA_URL=act_url
    daraz_dict=daraz_analysis_function(settings.MEDIA_ROOT+'/darazdata/')
    print(daraz_dict)
    return render(request,'userapp/Darazflashsale.html',{'daraz_dict':daraz_dict})



# dashboard sub function

def all_item_detail(request):
    settings.MEDIA_ROOT = act_root
    settings.MEDIA_URL = act_url
    daraz_dict = daraz_analysis_function(settings.MEDIA_ROOT + '/darazdata/')
    return render(request,'userapp/DarazAllProductlist.html',{'daraz_dict':daraz_dict})

# in term of sales amount
def all_item_detail_revenue(request):
    settings.MEDIA_ROOT = act_root
    settings.MEDIA_URL = act_url
    daraz_dict = daraz_analysis_function(settings.MEDIA_ROOT + '/darazdata/')
    daraz_dict['all_product_detail_date']=daraz_dict['all_product_sale_detail_date']
    daraz_dict['all_product_detail_title']=daraz_dict['all_product_sale_detail_title']
    daraz_dict['all_product_detail_amount']=daraz_dict['all_product_sale_detail_amount']
    daraz_dict['all_product_detail_sales']=daraz_dict['all_product_sale_detail_sales']

    return render(request,'userapp/DarazAllProductlist.html',{'daraz_dict':daraz_dict})

# Daraz Market Share
def all_item_market_revenue(request):
    settings.MEDIA_ROOT = act_root
    settings.MEDIA_URL = act_url
    daraz_dict = daraz_analysis_function(settings.MEDIA_ROOT + '/darazdata/')
    daraz_dict['all_product_detail_date']=daraz_dict['mrk_date']
    daraz_dict['all_product_detail_title']=daraz_dict['mrk_name']
    daraz_dict['all_product_detail_amount']=daraz_dict['mrk_amount']
    daraz_dict['all_product_detail_sales']=daraz_dict['mrk_sales']

    return render(request,'userapp/DarazAllProductlist.html',{'daraz_dict':daraz_dict})

# Daraz Repeated Product in term of sold products
def repeated_sold(request):
    settings.MEDIA_ROOT = act_root
    settings.MEDIA_URL = act_url
    daraz_dict = daraz_analysis_function(settings.MEDIA_ROOT + '/darazdata/')
    return render(request, 'userapp/DarazRepeatProductlist.html', {'daraz_dict': daraz_dict})

# Daraz Repeated Product in term of sales
def repeated_sales(request):
    settings.MEDIA_ROOT = act_root
    settings.MEDIA_URL = act_url
    daraz_dict = daraz_analysis_function(settings.MEDIA_ROOT + '/darazdata/')
    daraz_dict['top15_repeat_name1'] =daraz_dict['top15_repeat_name2']
    daraz_dict['top15_repeat_rep1']=daraz_dict['top15_repeat_rep2']
    daraz_dict['top15_repeat_sold1']=daraz_dict['top15_repeat_sold2']
    daraz_dict['top15_repeat_sales1']=daraz_dict['top15_repeat_sales2']
    return render(request, 'userapp/DarazRepeatProductlist.html', {'daraz_dict': daraz_dict})
