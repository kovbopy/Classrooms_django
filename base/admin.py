import django.apps
from django.contrib import admin
from .models import Subject, Users, Classroom,  Comment


class ClassroomAdmin(admin.ModelAdmin):
    fieldsets = (
        ('People Section',{'fields':(('name','slug'),'teacher','students'),
                      'description':'It is people section',
                      'classes':('collapse',)}),

        ('Non-people Section',{'fields':('subject','is_admin_only'),
                      'description':'It is non-people section',
                      'classes':('collapse',)})
    )
    list_display = ('name','teacher','subject','id','is_subject_tech')
    list_filter = ('subject__is_tech',)
    search_fields = ('name',)
    prepopulated_fields = {"slug":("name",)}
    ordering=('name',)
    filter_horizontal = ('students',)

    def is_subject_tech(self,obj):
        return obj.subject.is_tech

    def has_view_or_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='admins').exists():
            return False
        return True


# we can have different urls for different tables
# for example we can add Classrooms table to url 'admin/classroom/'
class ClassroomAdminArea(admin.AdminSite):
    pass

classroom_site=ClassroomAdminArea(name='ClassroomArea')


classroom_site.register(Classroom,ClassroomAdmin)
admin.site.register(Classroom,ClassroomAdmin)


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','behavior','pk','updated')
    list_display_links = ('pk',)
    search_fields = ('username',)
    list_editable = ('username',)


    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='staff').exists():
            return False
        return True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'pk','created')
    list_display_links = ('sender',)
    search_fields = ('sender',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name','is_tech', 'pk','created')
    list_display_links = ('name',)
    list_editable = ('is_tech',)
    list_filter = ('is_tech',)
    search_fields = ('name',)
    prepopulated_fields = {"slug":("name",)}

    # you can't change nor delete tech subject
    def has_change_permission(self, request, obj=None):
        return obj is None or obj.is_tech =="True"

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.is_tech == "True"


models=django.apps.apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
