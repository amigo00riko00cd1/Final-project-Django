from django.contrib import admin
from .models import Weapon, Module, AssembledWeapon


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "recoil", "bullet_speed", "accuracy", "mobility")
    list_filter = ("type",)
    search_fields = ("title",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type_module",
        "recoil_change",
        "bullet_speed_change",
        "accuracy_change",
        "mobility_change",
    )
    list_filter = ("type_module",)
    search_fields = ("title",)


@admin.register(AssembledWeapon)
class AssembledWeaponAdmin(admin.ModelAdmin):
    list_display = ("weapon", "created_by", "created_at", "display_final_stats")
    filter_horizontal = ("modules",)
    readonly_fields = ("created_at",)
    exclude = ("assemblies",)  # предотвращает рекурсию при отображении связанных объектов

    def display_final_stats(self, obj):
        stats = obj.final_stats
        return (
            f"Отдача: {stats['recoil']}, "
            f"Скорость пули: {stats['bullet_speed']}, "
            f"Точность: {stats['accuracy']}, "
            f"Манёвренность: {stats['mobility']}"
        )

    display_final_stats.short_description = "Итоговые характеристики"
