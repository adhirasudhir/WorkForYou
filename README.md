jango-Login-Register-Form
```
3. Create Virtual Environment
```
virtualenv env
```
4. Active Virtual Environment
```
env\scripts\activate
```
5. Install Requirements File
```
pip install -r requirements.txt
```
6. Make Migrations
```
py manage.py makemigrations
```
7. Migrate Database
```
py manage.py migrate
```
8. Create Super User
```
py manage.py createsuperuser
```
9. Run Project
```
py manage.py runserver
```

Under settings.py, make changes to the Email Setup
```
#Email Setup
EMAIL_FROM_USER = 'Your Email Address'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'Your Email Host Provider'
EMAIL_PORT = 'Your Email Host Port Number'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'Your Email Addres'
EMAIL_HOST_PASSWORD = 'Your Email Password'
```

© 2021 Steve Njuguna

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
