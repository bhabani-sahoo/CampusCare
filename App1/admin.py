from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StudentProfile,Complains
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.
class StudentProfileInline(admin.StackedInline): 
        model = StudentProfile
        can_delete = False
class CustomUserAdmin(UserAdmin):
    inlines = [StudentProfileInline]
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class ComplainsAdmin(admin.ModelAdmin):
      def download_pdf(self,obj):
          url=reverse(
              'download-pdf',
              args=[obj.id]
          )
          return format_html(
              '<a href="{}" target="_blank">Download PDF</a>',
              url
          )
      def image_link(self,obj):
       if obj.image:
            return format_html(
                  '<a href="{}" target="_blank"> View Image</a>',
                  obj.image.url
            )
       return "No Image"
      def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">View File</a>',
                obj.file.url
            )
        return "No File"
      list_display=('complaint_id','student','complaint_catagory','description','created_at','updated_at','status','remark','satisfaction','file_link','image_link','branch','batch','download_pdf','Gender')
      readonly_fields=['complaint_id','student','complaint_catagory','description','created_at','updated_at','satisfaction','image','file','branch','batch']
      fields=['complaint_id','student','complaint_catagory','description','created_at','updated_at',"status",'remark','satisfaction','file','image','branch','batch','Gender']
      list_filter = (
      'status',
      'branch',
      'batch',
      'created_at',
      'complaint_catagory',
      'Gender'
      )
      search_fields = (
        'complaint_id', 
     )
admin.site.register(Complains,ComplainsAdmin)
