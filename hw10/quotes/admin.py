from django.contrib import admin
from .models import Author, Quote, Profile

admin.site.register(Profile)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'born_date', 'born_location', 'description')
    search_fields = ('fullname',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ('text', 'author__name')
