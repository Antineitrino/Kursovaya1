from django.contrib import admin
from .models import User, Tovar, Zakaz, ZakazItem

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'FIO', 'Number', 'Address', 'is_staff')
    list_display_links = ('id', 'username')
    search_fields = ('FIO', 'Number', 'username')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'FIO', 'Number', 'Address', 'email')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

class TovarAdmin(admin.ModelAdmin):
    list_display = ('id', 'Vid_tovara', 'Nomer_tovara', 'Prace', 'category')
    list_display_links = ('id', 'Vid_tovara')
    search_fields = ('Vid_tovara', 'Nomer_tovara')
    list_filter = ('category',)
    list_editable = ('Prace',)  # Можно редактировать цену прямо в списке

class ZakazItemInline(admin.TabularInline):
    model = ZakazItem
    extra = 1
    readonly_fields = ('price',)

class ZakazAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'Symma', 'Sposob_oplati', 'status', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('status', 'Sposob_oplati', 'created_at')
    search_fields = ('user__FIO', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ZakazItemInline]
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'Symma', 'Sposob_oplati', 'status')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ZakazItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz', 'tovar', 'quantity', 'price')
    list_filter = ('zakaz', 'tovar')
    search_fields = ('zakaz__id', 'tovar__Vid_tovara')

# Регистрируем модели в админке
admin.site.register(User, UserAdmin)
admin.site.register(Tovar, TovarAdmin)
admin.site.register(Zakaz, ZakazAdmin)
admin.site.register(ZakazItem, ZakazItemAdmin)

# Настройка заголовка админки
admin.site.site_header = 'Управление пиццерией'
admin.site.site_title = 'Админ-панель пиццерии'
admin.site.index_title = 'Добро пожаловать в систему управления'