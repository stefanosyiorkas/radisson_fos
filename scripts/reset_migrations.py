import os
consent = input("Would you like to reset migrations? (y/n) ")
if consent.upper() == "Y":
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc"  -delete')
    os.system('find . -path "*.sqlite3"  -delete')

    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin\')" | python manage.py shell')
