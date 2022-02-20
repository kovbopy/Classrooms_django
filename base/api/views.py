from django.db.models import Count, Q, F
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from base.models import Classroom,Users
from .decorators import classroom_exists, user_exists, change_user_permission, change_classroom_permission
from .serializers import ClassroomSerializer, UserSerializer


@api_view(['GET',"POST"])
@permission_classes([IsAuthenticated])
def gp_users(request):
    if request.method=="GET":
       user = Users.objects.all()
       serializer = UserSerializer(user,many=True)
       return Response(serializer.data)

    if request.method=="POST":
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET",'PUT',"PATCH","DELETE"])
@permission_classes([IsAuthenticated])
@user_exists
@change_user_permission
def crud_user(request, id):
    user = Users.objects.get(pk=id)
    user_name=user.username

    if request.method=="GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method in ("PUT","PATCH"):
       serializer = UserSerializer(instance=user, data=request.data,
                                   partial=True)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method=="DELETE":
         try:
             user.delete()
         except:
             return Response(f'Error while deleting {user_name}')
         return Response(f'{user_name} deleted', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_classrooms(request):
    classrooms = Classroom.objects.annotate(students_count=Count("students"))
    serializer = ClassroomSerializer(classrooms, many=True)
    return Response(serializer.data)

@api_view(["GET",'PUT',"PATCH","DELETE"])
@classroom_exists
@change_classroom_permission
@permission_classes([IsAuthenticated])
def crud_classroom(request, slug):
    cl=Classroom.objects.get(slug=slug)
    cl.entries=F('entries') + 1
    cl.save()

    classroom = Classroom.objects.annotate(students_count=Count("students")).\
                                           get(slug=slug)
    classroom_name=classroom.name

    if request.method=="GET":
       serializer = ClassroomSerializer(classroom)
       return Response(serializer.data)

    elif request.method in ("PUT","PATCH"):
       serializer = ClassroomSerializer(instance=classroom, data=request.data,
                                        partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)

       elif request.method == "DELETE":
           try:
               classroom.delete()
           except:
               return Response(f'Error while deleting {classroom_name}')
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def classroom_search(request,subject,teacher):
    classrooms = Classroom.objects.filter(Q(subject__name__icontains=subject) &
                                          Q(teacher__username__icontains=teacher)). \
                                          annotate(students_count=Count("students"))
    classrooms.update(entries=F('entries') + 1)
    serializer = ClassroomSerializer(classrooms, many=True)
    return Response(serializer.data)
