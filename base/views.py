from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from base.forms import UserRegisterForm, ClassroomForm, UpdateUserForm
from base.models import Subject, Classroom, Comment, Users


def RegisterPage(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = user.name.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/register_page.html', {'form': form})


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        name = request.POST.get('name').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, name=name, password=password)
            login(request, user)
            return redirect('base:home')
        except:
            messages.error(request, 'Name or password does not exist')

    return render(request, 'base/login_page.html')


def LogoutUser(request):
    logout(request)
    return redirect('base:home')


# you can find classroom by its name,subject
@cache_page(15)
def HomePage(request):
    s_s = request.GET.get('s_s') if request.GET.get('s_s') != None else ''

    subclass_search = Classroom.objects.filter(
        Q(name__icontains=s_s) |
        Q(description__icontains=s_s) |
        Q(subject__name__icontains=s_s))

    # subjects from subject_tags
    subclass_count = subclass_search.count()

    return render(request, 'templates/home_page.html', {'name_search': subclass_search,
                                                        'name_count': subclass_count, })


# You can create your own subject or pick one that already exists
@login_required(login_url='login')
def CreateClassroom(request):
    # subjects from subject_tags
    subject_name = request.POST.get('subject')
    subject, created = Subject.objects.get_or_create(name=subject_name)

    if request.method == 'POST':
        Classroom.objects.create(name=request.POST.get('name'),
                                 teacher=request.user,
                                 subject=subject,
                                 description=request.POST.get('description'))
        return redirect('base:home')

    return render(request, 'templates/create_classroom.html')


# will show 3 classrooms that a user visited lately, users can leave comments
@login_required(login_url='login')
def PageClassroom(request, slug):
    classroom = Classroom.objects.get(slug=slug)
    classroom.entries = F('entries') + 1
    classroom.save()

    recently_viewed_classrooms = None

    if 'recently_viewed' in request.session:
        r_v=request.session['recently_viewed']
        if slug in r_v:
            r_v.remove(slug)

        classrooms = Classroom.objects.filter(pk__in=r_v)
        recently_viewed_classrooms = sorted(classrooms,
                                         key=lambda x: r_v.index(x.slug))
        r_v.insert(0, slug)
        if len(r_v) > 3:
            r_v.pop()
    else:
        r_v = [slug]
    request.session.modified = True

    students = classroom.students.all()
    comments = classroom.comment_set.all()
    teacher = classroom.teacher
    current_user = request.user

    if request.method == 'POST':
        comment = Comment.objects.create(
            sender=current_user,
            classroom=classroom,
            text=request.POST.get('text')
        )
        classroom.students.add(current_user)

    context = {'classroom': classroom, 'students': students, 'comments': comments,
               'teacher': teacher, 'recently_viewed_classrooms': recently_viewed_classrooms}

    return render(request, 'templates/page_classroom.html', context)


@login_required(login_url='login')
def UserProfile(request, id):
    user = get_object_or_404(Users, id=id)

    # classrooms don't get often updated so we can cache them
    classrooms = cache.get('classrooms')
    if not classrooms:
        classrooms = user.classroom_set.all()
        cache.set('classrooms', classrooms, 60 * 10)

    comments = Comment.objects.filter(sender=user)

    context = {'user': user, 'classrooms': classrooms,
               'comments': comments}
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='login')
def UpdateClassroom(request, slug):
    try:
        classroom = Classroom.objects.get(slug=slug, teacher=request.user)
    except:
        return HttpResponse(f'Classrom with the slug "{slug}" does not exist')

    form = ClassroomForm(instance=classroom)
    # subjects from subject_tags

    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        subject, created = Subject.objects.get_or_create(name=subject_name)

        classroom.name = request.POST.get('name')
        classroom.subject = subject
        classroom.save()
        return redirect('home')

    return render(request, 'base/update_classroom.html', {'form': form,
                                                          'classroom': classroom})


@login_required(login_url='login')
def UpdateUser(request):
    curent_user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=curent_user)
        if form.is_valid():
            form.save()
            return redirect('user', id=curent_user.id)
        else:
            messages.error(request, 'Smt went wrong')
    else:
        form = UpdateUserForm(instance=curent_user)

    return render(request, 'base/update_user.html', {'form': form})


@login_required(login_url='login')
def DeleteUser(request):
    user = Users.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        return redirect('base:home')
    return render(request, 'base/delete_user.html', {'user': user})


@login_required(login_url='login')
def DeleteClassroom(request, slug):
    try:
        classroom = Classroom.objects.get(slug=slug, teacher=request.user)
    except:
        return HttpResponse(f'Classroom with the slug "{slug}" does not exist')

    if request.method == 'POST':
        classroom.delete()
        return redirect('base:home')
    return render(request, 'base/delete_classroom.html', {'classroom': classroom})


@login_required(login_url='login')
def DeleteMessage(request, id):
    comment = Comment.objects.get(id=id, sender=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('base:home')
    return render(request, 'base/delete_comment.html', {'comment': comment})
