from django.contrib import admin
from .models import Problem, Compleks, Company, Partnyor, Tickets, Navbatchilik, Education


# admin.site.register(Problem)
# admin.site.register(Company)
# admin.site.register(Compleks)
# admin.site.register(Partnyor)
# admin.site.register(Tickets)

@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['name', 'note', 'status', 'createDate', 'file',
                    'endDate', 'problem', 'compleks', 'partnyor', 'company', 'update_Time']
    list_filter = ['status', 'createDate','problem','partnyor', 'company', 'update_Time']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'createDate'
    search_fields = ['name', 'note']
    ordering = ['status', 'createDate']

@admin.register(Compleks)
class CompleksAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'status', 'schema_net', 'documents', 'creatorId']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['name']
    ordering = ['status', 'created']

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'status', 'creatorId']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['name']
    ordering = ['status', 'created']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'status', 'creatorId']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['name']
    ordering = ['status', 'created']

@admin.register(Partnyor)
class PartnyorAdmin(admin.ModelAdmin):
    list_display = ['fio', 'login', 'created', 'status', 'creatorId', 'image', 'contacts', 'companyId']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['fio']
    ordering = ['status', 'created']



@admin.register(Navbatchilik)
class NavbatchiAdmin(admin.ModelAdmin):
    list_display = ['kun', 'oy', 'yil',  'created', 'status', 'creatorId', 'ticket']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['fio']
    ordering = ['status', 'created']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['name', 'info', 'date', 'created', 'status', 'creatorId', 'file', 'read', 'toDate', 'endDate']
    list_filter = ['status', 'created', 'creatorId']
    # prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'created'
    search_fields = ['fio']
    ordering = ['status', 'created']
