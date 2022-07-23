from django.urls import path
from . import views
from huntuserapp import views as v

urlpatterns=[
    path('',views.index,name='index'),
    path('solutions',views.solutions,name='solutions'),
    path('signup',views.signup,name='signup'),
    path('producttrend',views.producttrend,name='producttrend'),
    path('eachtrend',views.eachtrend,name='eachtrend'),
    path('keyword_search',views.keyword_search,name='keyword_search'),
    path('users',v.users,name='users'),
    path('login',v.login,name='login'),

    # dashoard urls
    path('dashboard', v.dashboard, name='dashboard'),
    path('platform-recommendation',v.platform_recommend,name='platform-recommendation'),
    path('sales-predication',v.sales_predication,name='sales-predication'),
    path('sales-analysis',v.sales_analysis,name='sales-analysis'),
    path('seo-keyword',v.seo_keyword,name='seo-keyword'),
    path('daraz-analysis',v.daraz_analysis,name='daraz-analysis'),

    # dashboard Sub urls
    path('all-item-detail',v.all_item_detail,name='all-item-detail'),
    path('all-item-detail-revenue', v.all_item_detail_revenue, name='all-item-detail-revenue'),
    path('all-item-market-revenue',v.all_item_market_revenue,name='all-item-market-revenue'),
    path('repeat-product-sold', v.repeated_sold, name='repeat-product-sold'),
    path('repeat-product-sales', v.repeated_sales, name='repeat-product-sales'),
    path('platform-recommend',v.platform_recommend,name='platform-recommend'),
    path('actual-prediction', v.actual_prediction, name='actual-prediction')

]

