from django.contrib import admin
from .models import Dictionary

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    # Ro'yxatda ko'rinadigan ustunlar
    list_display = ('word', 'has_definition')
    # Qidiruv maydoni (so'z bo'yicha qidirish)
    search_fields = ('word',)
    # So'zlarni alifbo bo'yicha tartiblash
    ordering = ('word',)

    # Izoh bor yoki yo'qligini ko'rsatuvchi rangli belgi
    def has_definition(self, obj):
        return bool(obj.definition)
    has_definition.boolean = True
    has_definition.short_description = "Izoh mavjud"