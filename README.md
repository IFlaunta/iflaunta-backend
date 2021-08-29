# **IFlaunta-Backend**

This repository contains the backend and AI related stuff.

---

## **Technologies**

* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Rest APIs with [Django](https://www.djangoproject.com/)
* Database used: [SQLite](https://www.sqlite.org/index.html) (for development)

---

## **Local Setup**

* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python [here](https://www.python.org/downloads/).

* Download [pip](https://pip.pypa.io/en/stable/installing/) and add it to the path

* Make a working directory `IFlaunta`, to setup virtual environment.

* Change your working directory to `IFlaunta`

    ```bash
    cd path/to/IFlaunta
    ```

* Create a new virtual environment inside `IFlaunta` directory and activate that

    ```bash
    python -m venv env
    ```

    > ***NOTE***  
    > By default, this will **not** include any of your existing site packages.

    For activating or deactivating virtual env, take [this](https://github.com/orgs/IFlaunta/teams/iflaunta-team/discussions/1) for reference.

* Clone the repository

  * Using HTTPS

    ```sh
    git clone https://github.com/IFlaunta/IFlaunta-Backend.git
    ```
  
  * Using SSH

    ```sh
    git clone git@github.com:IFlaunta/IFlaunta-Backend.git
    ```

* Change your working directory to the cloned folder `IFlaunta-Backend`

    ```bash
    cd path/to/IFlaunta-Backend
    ```

* Download all the dependencies

    ```bash
    pip install -r requirements.txt
    ```

    Use `pip3` if `pip` not working

* Make a `.env` file in this directory only and put the following

    ```bash
    DJANGO_SECRET_KEY = django-insecure-3a65@ycam887r2c69p=3st-_#s8k26t(-*h8@4ic_f1qo1*ow6
    DJANGO_DEBUG = True
    ```

<!--
  * While putting `DEBUG = False`, remember to modify `ALLOWED_HOSTS` (for just quick reference, modify as `ALLOWED_HOSTS = ['*']`)

  * For generating a Django ***SECRET_KEY***, many different sites are there. This [site](https://miniwebtool.com/django-secret-key-generator/) can be used for quick reference.
-->

### Before proceeding further, make sure ```Directory``` looks like

```
IFlaunta
├── env
└── IFlaunta-Backend
    ├── iflaunta
    |   ├── __init__.py
    |   ├── settings.py
    |   ├── asgi.py
    |   ├── wsgi.py
    |   └── urls.py
    ├── .env
    ├── .gitignore
    ├── manage.py
    ├── README.md
    └── requirements.txt
```

### For running Django Server

* Migrate to the database

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    Use `python3` if `python` not working

    After this, you would see a new file named `db.sqlite3` in your parent folder

* Run server

    ```sh
    python manage.py runserver
    ```

---
