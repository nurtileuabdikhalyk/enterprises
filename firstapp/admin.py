from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'count', 'total')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'created')
    list_display_links = ('id', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email',)
    # list_filter = ('staff',)
    # prepopulated_fields = {'slug': ('name',), }


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'created')
    list_display_links = ('id', 'fullname',)
    search_fields = ('fullname',)


@admin.register(Dogovor)
class DogovorAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'description')
    list_display_links = ("id", 'name', 'description')
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", 'name',)
    list_display_links = ("id", 'name',)
    search_fields = ("name",)


@admin.register(Platej)
class PlatejAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'dogovor', 'product', 'sum')
    list_display_links = ("id", 'organization', 'dogovor', 'product',)
    search_fields = ("organization", 'dogovor', 'product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'platej', 'courier', 'data')
    list_display_links = ("id", 'organization', 'platej', 'courier',)
    search_fields = ("organization", 'dogovor', 'project',)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone')
    list_display_links = ('id', 'first_name', 'last_name', 'phone')
