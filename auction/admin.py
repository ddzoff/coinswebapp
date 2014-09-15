from django.contrib import admin
from auction.models import Auctions, Category

class AuctionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'display_name')

# class BidAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         obj.save

admin.site.register(Auctions, AuctionsAdmin)
admin.site.register(Category, CategoryAdmin)


