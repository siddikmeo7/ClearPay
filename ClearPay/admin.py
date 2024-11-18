from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","phone_number",]
    list_filter = ["username","age","email",]
    search_field = ["username","age","email",]


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","balance","created_at",]


@admin.register(Loan)
class UserAdmin(admin.ModelAdmin):
    list_display = ["client","amount","issue_date","repayment_date",]


@admin.register(Transaction)
class UserAdmin(admin.ModelAdmin):
    list_display = ["client","transaction_date","description",]
