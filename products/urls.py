from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path, include, re_path
from . import views
from .Crawling import views as crawling_views
from .views import ProductListViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='My API',
        default_version='v1',
        description="KICKI BE.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kickin@kickin.kr"),
        license=openapi.License(name="KICKIN License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)



urlpatterns = [
    path('sneaker/<int:prd_id>/', views.get_detail),
    path('sneaker/like/<int:product_id>/<int:user_id>/', views.product_like),
    path('sneaker/list/', ProductListViewSet.as_view()),
    path('recent/', views.recent_releases),
    
    # data crwaling activated request
    path('goat/collections/', crawling_views.goat_collections), # goat collections 데이터 크롤링 USING
    
    path('swagger/', schema_view.with_ui('swagger')),
    #Achive request
    # path('sneaker/', views.get_sneaker),
    # path('new/', views.new_release_paser),
    # path('brand/', views.sneaker_data_by_brand_paser),
    # path('test/', views.google_img_download),
    # path('img/pasing/', views.sneaker_img_paser), # 이미지 다운로더 
    # path('goat/', views.get_goat),
    # path('dup/', views.duplicate_check),
    # path('imgmodel/', views.temp_img_fix),
    # path('imgmodeladd/', views.select_all_and_add_img_model),
    # path('imgupdator/', views.img_url_updator), # 이미지 Url Localhost -> https://www.kickin.co.kr/ 로 변경
    # path('test/', views.select_all_test),
] 
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]