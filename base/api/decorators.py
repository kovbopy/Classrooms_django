from rest_framework import status
from rest_framework.response import Response
from base.models import Classroom, Users


def user_exists(view):
    def user_view(request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            Users.objects.get(id=id)
            return view(request, *args, **kwargs)
        except:
            return Response(f"User with id {id} does not exist",
                            status=status.HTTP_404_NOT_FOUND)
    return user_view


def change_user_permission(view):
    def not_allowed(request, *args, **kwargs):
        id = kwargs['id']
        user = Users.objects.get(id=id)
        if user != request.user and not request.user.is_staff:
            return Response("You are not authorized to perform this action",
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view(request, *args, **kwargs)

    return not_allowed


def classroom_exists(view):
    def classroom_view(request, *args, **kwargs):
        slug = kwargs.get('slug')
        classroom = Classroom.objects.filter(slug=slug)
        if classroom.exists():
            return view(request, *args, **kwargs)

        elif not classroom.exists():
            return Response(f"Classroom with slug {slug} does not exist",
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Smt went wrong",
                            status=status.HTTP_400_BAD_REQUEST)
    return classroom_view


def change_classroom_permission(view):
    def not_allowed(request, *args, **kwargs):
        slug = kwargs['slug']
        classroom = Classroom.objects.get(slug=slug)
        if classroom.teacher != request.user and not request.user.is_staff:
            return Response("You are not authorized to perform this action",
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view(request, *args, **kwargs)

    return not_allowed