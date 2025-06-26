from django.contrib import admin
from .models import Problem, Compleks, Company, Partnyor, Ticket, Education, ToDo, UserProfile, LoginHistory, Events

admin.site.register(Company)
admin.site.register(Ticket)
admin.site.register(Events)
admin.site.register(Partnyor)
admin.site.register(LoginHistory)
admin.site.register(Compleks)
admin.site.register(Problem)
admin.site.register(Education)
admin.site.register(ToDo)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_last_name', 'get_first_name', 'get_username', 'get_password', 'birth_date', 'photo']

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def get_password(self, obj):
        return obj.user.password
    get_password.short_description = 'Password'
    get_password.admin_order_field = 'user__password'

#                     'endDate', 'problem', 'compleks', 'partnyor', 'company', 'update_Time']
#     list_filter = ['status', 'createDate','problem','partnyor', 'company', 'update_Time']
# @admin.register(Ticket)
# class TicketsAdmin(admin.ModelAdmin):
#     list_display = ['name', 'note', 'status', 'createDate', 'file',
#                     'endDate', 'problem', 'compleks', 'partnyor', 'company', 'update_Time']
#     list_filter = ['status', 'createDate','problem','partnyor', 'company', 'update_Time']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'createDate'
#     search_fields = ['name', 'note']
#     ordering = ['status', 'createDate']
#
# @admin.register(Compleks)
# class CompleksAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created', 'status', 'schema_net', 'documents', 'creatorId']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['name']
#     ordering = ['status', 'created']
#
# @admin.register(Problem)
# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created', 'status', 'creatorId']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     # search_fields = ['name']
#     ordering = ['status', 'created']
#     readonly_fields = ['created']
#
# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created', 'status', 'creatorId']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['name']
#     ordering = ['status', 'created']

# @admin.register(Partnyor)
# class PartnyorAdmin(admin.ModelAdmin):
#     list_display = ['fio', 'login', 'created', 'status', 'creatorId', 'image', 'contacts', 'companyId']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['fio']
#     ordering = ['status', 'created']



# @admin.register(Navbatchilik)
# class NavbatchiAdmin(admin.ModelAdmin):
#     list_display = ['kun', 'oy', 'yil',  'created', 'status', 'creatorId', 'ticket']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['fio']
#     ordering = ['status', 'created']

# @admin.register(Education)
# class EducationAdmin(admin.ModelAdmin):
#     list_display = ['name', 'info', 'date', 'created', 'status', 'creatorId', 'file', 'read', 'toDate', 'endDate']
#     list_filter = ['status', 'created', 'creatorId']
#     # prepopulated_fields = {"slug": ('title',)}
#     date_hierarchy = 'created'
#     search_fields = ['fio']
#     ordering = ['status', 'created']
