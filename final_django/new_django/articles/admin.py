from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .forms import ArticleForm
from .forms import UserForm




#--------------------User Active Action---------------------------
def change_active(ModelAdmin,request,queryset):
	queryset.update(is_active = 1)
	change_active.short_description = "Change to active"	


#--------------------User Deactive Action---------------------------	
def change_deactive(ModelAdmin,request,queryset):
	queryset.update(is_active = 0)
	change_deactive.short_description = "Change to deactive"


#--------------------Article Publish Action-------------------------------
def make_published(ModelAdmin, request, queryset):
	queryset.update(art_status='p')
	make_published.short_description = "Mark selected articles as published"


#-------------------Article Approve Action--------------------------------
def make_approved(ModelAdmin, request, queryset):
	queryset.update(art_status='a')
	make_approved.short_description = "Mark selected articles as approved"


#-------------------Comment Approve Action--------------------------------
def make_comment_approved(ModelAdmin, request, queryset):
	queryset.update(Comment_status=True)
	make_comment_approved.short_description = "Mark selected Comment as approved"


#-------------------Lock System Action--------------------------------
def lock_system(ModelAdmin, request, queryset):
	queryset.update(is_locked=True)
	lock_system.short_description = "Lock the System"


#-------------------Unlock System Action--------------------------------
def unlock_system(ModelAdmin, request, queryset):
	queryset.update(is_locked=False)
	lock_system.short_description = "Unlock the System"




# -----------Define an inline admin descriptor for UserProfile model----------

class User_profileInline(admin.StackedInline):
    model = User_profile
    can_delete = False
    verbose_name_plural = 'user_profile'



# ------------------Define a new User admin---------------------------
class UserAdmin(BaseUserAdmin):
    inlines = (User_profileInline, )
    list_display =["username","is_active","first_name","last_name","email","is_superuser","is_staff"]
    actions = [change_active,change_deactive]
    form = UserForm
    readonly_fields = ('password','first_name','last_name','email')
    def get_readonly_fields(self, request, obj=None):
        if obj: # Editing
			return self.readonly_fields
        return ()


# ------------------Define a new Article admin---------------------------
class ArticleAdmin(admin.ModelAdmin):
	list_display = ["art_title","art_publish_date","art_status",
					"art_number_views","comments_count"]
	form = ArticleForm
	actions = [make_published,make_approved]
	list_filter = ('art_status','art_publish_date')
	readonly_fields = ('art_user_id','art_title','art_content','art_img')
	def get_readonly_fields(self, request, obj=None):
		if obj: # Editing
			return self.readonly_fields
		return ()


# ------------------Define a new Comment admin---------------------------
class CommentAdmin(admin.ModelAdmin):
	list_display = ["Comment_content","Comment_status"]
	actions = [make_comment_approved]
	list_filter = ('Comment_status',)
	readonly_fields = ('Comment_content','Comment_parent_id','Comment_user_like','Comment_art_id')
	def get_readonly_fields(self, request, obj=None):
		if obj: # Editing
			return self.readonly_fields
		return ()



# ------------------Define a new Lock_System admin---------------------------
class LockSystemAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False
	actions = [lock_system,unlock_system]


   

#--------------------Register Models------------------------------
admin.site.register(lockSystem,LockSystemAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Banwords)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(keywords)
