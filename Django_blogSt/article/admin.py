from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','autor','created_time','last_updated_time','is_deleted','read_num')
    ordering = ('id',)



# admin.site.register(Article,ArticleAdmin)
