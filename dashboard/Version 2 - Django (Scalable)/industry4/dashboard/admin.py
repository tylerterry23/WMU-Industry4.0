from django.contrib import admin
from .models import Process, Product, ProductTime, StationHistory, Stations, Steps
import datetime


admin.site.register(Process)
# admin.site.register(Product)
admin.site.register(ProductTime)
admin.site.register(StationHistory)
admin.site.register(Stations)
admin.site.register(Steps)

# for product show product id, total time, completed, accepted
class ProductAdmin(admin.ModelAdmin):

    def format_time(self, obj):
        return obj.TotalTime.strftime('%M:%S')

    format_time.short_description = 'Total Time'
    
    list_display = ('ProductID', 'format_time', 'Completed', 'Accepted')

admin.site.register(Product, ProductAdmin)


# Input users and faculty a