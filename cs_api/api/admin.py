from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.utils import OperationalError

from api import models, constants


admin.site.register(models.Account)

admin.site.register(models.Transaction)

try:
    group, created = Group.objects.get_or_create(name=constants.GROUP_ADMIN)

    if created:
        print("Admin successfully created")
    else:
        print("Admin already existed, it was not created")

    group, created = Group.objects.get_or_create(name=constants.GROUP_USER)
    
    if created:
        print("User successfully created")
    else:
        print("User already existed, it was not created")
except OperationalError:
    print("Group database does not exist")
