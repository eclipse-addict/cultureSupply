from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import PointHistorySerializer, PointSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Point, PointHistory
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status


'''
In case of bad request occurs, functions within this view can only be called within BE Server
'''
class PointError(Exception):
    def __str__(self):
            return "User_pk error, already exists"
    


User = get_user_model()

# when new user is added, create a new row for point record. 
# initally new user will be get 1,000 points which is minimum rate of points for raffle entry  
def new_user_point(user_id):
    user = User.objects.get(pk=user_id)
    
    # 이미 존재하는 row 가 있는지 확인 
    if Point.objects.filter(user=user).exists():
        raise PointError()
    else:
        # 없으면 새로운 로우 생성. 
        new_point_row = Point(user = user, current_points = 1000)
        new_point_row.save()
        create_point_history(1000, user, '회원가입', 'add')     
        


'''
according to user's activity within app, will provide points
this methods will be called everytime user activity method been callded
for instance : 
    - regist: 1,000p
    - login: 10p
    - info regist: 100p
    - community post(3 a day) : 50p
    - any comments(no limitation at the moment) : 10p   

'''
def add_use_point(point, user_id, activity, kind):
    user = User.objects.get(pk=user_id)
    point_row = Point.objects.filter(user=user)
    
    if kind =='add':
        point_row.current_point += point
    else:
        point_row.current_point -= point
        
    point_row.save()
    create_point_history(point, user, activity, kind)     

api_view(['GET',])



def create_point_history(point, user, activity, kind):
    point_history = PointHistory(user=user, description=activity, point_amount=point, point_type=kind)
    point_history.save()


class PointHistoryPagination(PageNumberPagination):
    page_size = 2

class PointHistoryViewSet(ModelViewSet):
    queryset = PointHistory.objects.all()
    serializer_class = PointHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PointHistoryPagination

    def get_queryset(self):
        user = self.request.user
        return PointHistory.objects.filter(user=user)
    #
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     serializer.save(user=user)
    #
    # def perform_update(self, serializer):
    #     user = self.request.user
    #     serializer.save(user=user)
    #
    # def perform_destroy(self, instance):
    #     instance.delete()




@permission_classes([IsAuthenticated])
def get_point_history(request, id):
    user = User.objects.get(pk=id)
    point_history = PointHistory.objects.filter(user=user)
    serializer = PointSerializer(point_history, many=True)

    return HttpResponse(serializer.data, status=status.HTTP_200_OK)


