from django.contrib import admin

from .models import StaticPage, Problem, Member, Group


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time')
    list_display_links = ('id', 'title')
    list_per_page = 20
    # fields = ('id', 'title', 'create_time', 'desc',
    #           'mem_limit', 'time_limit', 'test_input', 'test_output')
    readonly_fields = ('id', 'create_time')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'group_name')
    list_display_links = ('id', 'user_name')
    list_per_page = 20


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 20


admin.site.register(StaticPage)
admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Problem, ProblemAdmin)


admin.site.site_header = 'YAOJ Administration'
admin.site.site_title = 'YAOJ Admin'
admin.site.index_title = 'Index'
