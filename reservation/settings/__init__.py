from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)

"""

usful link https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings 
answered by Ahtisham

Then in manage.py file find

def main():
   
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation.settings.dev')
    #here the default settings to dev

    ?asgi default
    ?wsgi?


见下面设置 
os.environ.get("myprojectname") not app name

"""
if os.environ.get('reservation')== 'prod':
   from .prod import *
else:
   from .dev import *