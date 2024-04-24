from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User  # Import your User model

admin.site.register(User)
from .models import Region, Zone, Sport, Championship
from .models import Sport
from football.models import Season
from athletes.models import Age, Classroom, Athlete

admin.site.register(Region)
admin.site.register(Zone)  # Register your User model
admin.site.register(Sport)  # Register your User model
admin.site.register(Age)  # Register your User model
admin.site.register(Classroom)  # Register your User model
admin.site.register(Athlete)  # Register your User model
admin.site.register(Championship)  # Register your User model
admin.site.register(Season)  # Register your User model

# Register your models here.
