from django.contrib import admin
from .models import Part, PointFile, Point


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PointFile)
class PointFileAdmin(admin.ModelAdmin):
    list_display = ('file_name',)
    search_fields = ('file_name',)


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('name', 'x', 'y', 'z', 'part',
                    'point_file', 'row_number')
    list_filter = ('part', 'point_file')
    search_fields = ('name', 'x', 'y', 'z')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'x', 'y', 'z', 'part',
                       'point_file', 'row_number')
        }),
    )

    def coordinates(self, obj):
        return f"({obj.x}, {obj.y}, {obj.z})"

    coordinates.short_description = 'Coordinates'
