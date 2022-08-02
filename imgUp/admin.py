from django.contrib import admin
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import TextInput, Textarea
# Register your models here.
from .models import Img, Detection, Feedback
# from .forms import Feedbacks

class ImgAdmin(admin.ModelAdmin):
    list_display = ('img_id','date','image_preview')
    readonly_fields = ('image_preview',)
    
    search_fields = ('img_id', )

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True



admin.site.register(Img, ImgAdmin)


class DetAdmin(admin.ModelAdmin):
    list_display = ('pred_id','link_to_Img')
    
    def link_to_Img(self, obj):
        url = reverse("admin:imgUp_img_change", args=[obj.img_data.id]) #model name has to be lowercase
        link = '<a href="%s">%s</a>' % (url, obj.img_data.img_id)
        return mark_safe(link)
    link_to_Img.allow_tags=True
    link_to_Img.short_description = 'Image'




admin.site.register(Detection, DetAdmin)
# admin.site.register(Prediction)
# admin.site.register(Feedback)
# admin.site.register(Feedbacks)

class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('finishCheck',)
    def del_selected(modeladmin, request, queryset):
        queryset.delete()
    del_selected.short_description = "Delete selected without check"

    def check_selected(modeladmin, request, queryset):
        
        for fb in queryset:
            fb.finishCheck = True
            fb.save()
            
    check_selected.short_description = '將選取項目設為已完成'
    
    readonly_fields = ('pred', 'date', 'image_preview', 'link_to_Img')
    
    # list_display = ('feedbackID', 'feedback', 'review', 'date', 'finishCheck')
    list_display = ('pred', 'issue', 'review', 'date', 'finishCheck')
    actions = [del_selected, check_selected]
    
    list_filter = ('finishCheck',)

    def link_to_Img(self, obj):
        url = obj.image_link
        home = reverse("home") #model name has to be lowercase
        link = '<a href="%s" target="_blank">%s</a>' % (url, '點我看大圖')
        return mark_safe(link)

    link_to_Img.allow_tags=True
    link_to_Img.short_description = 'Image'
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'10'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    fieldsets = [(None, {'fields': (('pred', 'date'),)}),
                ('結果圖預覽', { 'classes': ('collapse', 'open'),
                              'fields': (('image_preview','link_to_Img'),) }),
                 ('使用者回報', {'fields': (('issue', 'feedback'),('contact'))}),
                 ('茶改場檢閱', {'fields': (('true_label', 'review'),)}),
                 (None, {'fields': ('finishCheck',)})
                 ]
    # inlines = [,]

admin.site.register(Feedback, FeedbackAdmin)

