
## Reservation

The app-Reservation offers a convenient tool for a workforce leasing company to provide short-time work opportunities (Gig work) for healthcare professionals. Currently, there is no signup function available, and only allowed users can use the app. At the moment, there are four user groups:

A. Employer

An employer can publish, update shifts via the user interface. An employer can also delete a shift if it hasn't been reserved (by nurses, agency staff, or admin) yet. Otherwise, only job agency staff can delete it.

With the employee's pre-approval, an employer can assign a specific shift to that employee (reserve a shift).

An employer can view all of their own shifts (open, reserved, unpublished, unfilled, done). The employer cannot view other employers' published shifts.

B. Nurse

There are three types of nurses: registered nurse (RN), practical nurse (PN), and assistant (ASST). RNs have the right to access and reserve all available shifts (RN, PN, and ASST). Practical nurses can only view shifts that are open to PN and ASST. Assistants are restricted to working on ASST shifts. A nurse can view and reserve all **OPEN** shifts offered by all employers.

Employers and nurses are treated as customers. A customer user can update their own profile and reset their password.

C. Agency staff

Agency staff can access all open shifts offered by different employers. Agency staff can assign a shift to a nurse under mutual agreement. Agency staff can publish, update, and delete shifts.

D. Admin (Superuser)

An admin has all the rights mentioned above. Admins also create, update, and delete users. Admins issue initial passwords to users.

### Built on top of:

1. [django framework](https://www.djangoproject.com/)
2. [bootstrap](https://getbootstrap.com/)
3. [crispy forms](https://django-crispy-forms.readthedocs.io/en/latest/)
4. [bootstrap_datepicker_plus](https://pypi.org/project/django-bootstrap-datepicker-plus/))

## Quick start

For Mac users:

```
$ mkdir reservation
$ cd reservation
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

## install django before that make sure pip is update
```
~$ python3 -m pip install --upgrade pip
(myvenv) ~$ pip3 install -r requirements.txt
~$ git init
~$ django-admin startproject reservation .
~$ pip3 install python-decouple
~$ pip3 install python_extensions
~$ python3 manage.py runserver
~$ python3 manage.py migrate
~$ pip3 freeze > requirements.txt
~$ python manage.py startapp core
~$ deactivate
```
# restart 

```
$ source myvenv/bin/activate
````
