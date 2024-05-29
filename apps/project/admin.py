from django.contrib import admin
from apps.project.models import *



class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name',
    )
admin.site.register(Project,ProjectsAdmin)


class TudoAdmin(admin.ModelAdmin):
    list_display = ('id','project','description','status')
admin.site.register(Tudo,TudoAdmin)


