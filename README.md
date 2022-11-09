
## Reservation



This app-Reservation offers workforce leasing company a convienent tool to provide short-time work opportunities (Gag work) in healthcare sectors. There is no signup function available, only allowed users are able to use the app.  At the moment there are four user groups:

A. Employer

An employer could publish, update shifts via user interface. An employer can also delete a shift if it's not been reserved (by nurses, agency staff, admin) yet. Otherwise only job agency staff can delete it. 

With the pre-approval of the employee, an employer can assign certain shift to that employee. (Reserve a shift). 

An employer could view all its own shifts (open,reserved,unpublished, unfilled, done). The employer could not view other employers published shifts. 


B. Nurse 

There are three types of nurses: registered nurse (RN), pratical nurse (PN) and assistant (ASST). RN has the right to access and reserve all avaible shifts (RN, PN and ASST). Practical nurse could only view shifts that opens to PN and ASST. Then an assistant is restricted to work on ASST shifts. A nurse could view and reserve all **OPEN** shifts offered by all employers. 

Employer and Nurse are treated as customers.  A customer user can update own profile and reset password. 

C. Agency staff

An agency staff could access all open shifts offered by different employers. Agency staff can assign a shift to a nurse under mutual agreement. Agency staff can publish, update and delete shifts. 

D. Admin (Superuser)

An admin has all rights mentioned above. Admin also creates, updates and deletes users. Admin issues initial password to a user. 


### Build on top of 

1. [django framework](https://www.djangoproject.com/)
2. [bootstrap](https://getbootstrap.com/)
3. [crispy forms](https://django-crispy-forms.readthedocs.io/en/latest/)
4. [bootstrap_datepicker_plus](https://aerabi.medium.com/](https://pypi.org/project/django-bootstrap-datepicker-plus/))



## Quick start (rewrite)

$ mkdir reservation
$ cd reservation
$ python3 -m venv myvenv
$ source myvenv/bin/activate

##install django before that make sure pip is update

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

# restart 

$ source myvenv/bin/activate
