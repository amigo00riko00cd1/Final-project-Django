from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Weapon(models.Model):
    TYPE_CHOICES = [
        ("rifle", "Автомат"),
        ("pistol", "Пистолет"),
        ("sniper", "Снайперская винтовка"),
    ]

    title = models.CharField(max_length=100)
    image = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # базовые характеристики оружия
    recoil = models.IntegerField(default=0)
    bullet_speed = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)
    mobility = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class Module(models.Model):
    TYPE_CHOICES = [
        ("rifle", "Автомат"),
        ("pistol", "Пистолет"),
        ("sniper", "Снайперская винтовка"),
    ]

    title = models.CharField(max_length=100)
    type_module = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # параметры, которые модуль изменяет
    recoil_change = models.IntegerField(default=0)
    bullet_speed_change = models.IntegerField(default=0)
    accuracy_change = models.IntegerField(default=0)
    mobility_change = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} для {self.get_type_module_display()}"


class AssembledWeapon(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.pk:  # проверяем, что объект уже сохранён
            for module in self.modules.all():
                if module.type_module != self.weapon.type:
                    raise ValidationError(f"Модуль {module.title} не подходит для оружия {self.weapon.title}")
            if self.modules.count() > 5:
                raise ValidationError("Оружие не может иметь больше 5 модулей")

    def save(self, *args, **kwargs):
        """Сохраняем объект перед добавлением модулей"""
        super().save(*args, **kwargs)
        # После сохранения можно безопасно обращаться к self.modules

    @property
    def final_stats(self):
        recoil = self.weapon.recoil
        bullet_speed = self.weapon.bullet_speed
        accuracy = self.weapon.accuracy
        mobility = self.weapon.mobility

        for module in self.modules.all():
            recoil += module.recoil_change
            bullet_speed += module.bullet_speed_change
            accuracy += module.accuracy_change
            mobility += module.mobility_change

        return {
            "recoil": recoil,
            "bullet_speed": bullet_speed,
            "accuracy": accuracy,
            "mobility": mobility,
        }

    def __str__(self):
        return f"Сборка {self.weapon.title}"
