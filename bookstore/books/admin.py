from django.contrib import admin
from .models import Book, Purchase
from leaflet.admin import LeafletGeoAdmin # ino baraye admin gozashteh bodam
from .models import County

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'available')
    search_fields = ('title', 'author')
    list_filter = ('available',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')
    search_fields = ('user__username', 'book__title')


admin.site.register(Book, BookAdmin)
admin.site.register(Purchase, PurchaseAdmin)
