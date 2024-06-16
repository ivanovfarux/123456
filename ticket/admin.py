from django.contrib import admin
from django.contrib.auth.models import User

from .models import Problem, Compleks, Company, Partnyor, Duty, Education, Ticket, Events

admin.site.register(Education)
admin.site.register(Compleks)
admin.site.register(Duty)
admin.site.register(Events)
# admin.site.register(User)


@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['name', 'note', 'status', 'createDate', 'file',
                    'problem', 'compleks', 'partnyor', 'company', 'updatedDate']
    # list_filter = ["__all__"]
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'createDate'
    search_fields = ['name', 'note']
    ordering = ['status', 'createDate']


# class CompleksAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created', 'status', 'schema_net', 'documents', 'creatorId']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['name']
#     ordering = ['status', 'created']

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['name', 'createDate', 'status', 'author']
    list_filter = ['status', 'createDate', 'author']
    date_hierarchy = 'createDate'
    # search_fields = ['name']
    ordering = ['status', 'createDate']
    readonly_fields = ['createDate']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'createDate', 'status', 'author']
    list_filter = ['status', 'createDate', 'author']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'createDate'
    search_fields = ['name']
    ordering = ['status', 'createDate']
#
@admin.register(Partnyor)
class PartnyorAdmin(admin.ModelAdmin):
    list_display = ['fio', 'login', 'createDate', 'status', 'author', 'image', 'contacts', 'companyId', 'age']
    list_filter = ['status', 'createDate', 'author']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'createDate'
    search_fields = ['fio']
    ordering = ['status', 'createDate']
#
#
#
# @admin.register(Navbatchilik)
# class NavbatchiAdmin(admin.ModelAdmin):
#     list_display = ['kun', 'oy', 'yil',  'createDate', 'status', 'author', 'ticket']
#     list_filter = ['status', 'createDate', 'author']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'createDate'
#     search_fields = ['fio']
#     ordering = ['status', 'createDate']
#
# @admin.register(Education)
# class EducationAdmin(admin.ModelAdmin):
#     list_display = ['name', 'info', 'date', 'createDate', 'status', 'author', 'file', 'read', 'toDate', 'endDate']
#     list_filter = ['status', 'createDate', 'author']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'createDate'
#     search_fields = ['name']
#     ordering = ['status', 'createDate']
