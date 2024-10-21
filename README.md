# Simple CRUD (Django)

## 1. Setting up the Virtual Environment

The first step is to create and activate a Python virtual environment. This isolates the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then, all the necessary packages are installed as dependencies when drf-spectacular (for API schema generation) is installed:

```bash
pip install drf-spectacular
```

You can see all the packages installed with `pip freeze`.

## 2. Creating the Django Project

A new Django project named `root` is created using `django-admin startproject`. This command generates the basic structure of the Django project:

```bash
django-admin startproject root
cd root
```

The project structure includes essential files like `manage.py`, settings, URLs, and WSGI configuration.

## 3. Creating the 'cats' app

The `cats` app is created with the command:

```bash
./manage.py startapp cats
```

The `cats` folder contains the necessary files to handle models, views, migrations, etc.

At this moment, the project structure looks like this:

```ascii
├── cats
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── root
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

### 3.1. Defining Models for the 'cats' app

A `Cat` model is defined in `cats/models.py` with attributes like `name`, `age`, and `gender`. This is the blueprint of the data structure that the app will use:

```python
# cats/models.py
from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    gender = models.CharField(max_length=32)

```

### 3.2. Creating a Serializer

A `CatSerializer` serializer is created to convert the `Cat` model instances into a format that can be rendered into JSON for the API. This is placed in a new file `cats/serializers.py`:

```python
# cats/serializers.py
from rest_framework import serializers

from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    """
    Cat Serializers
    """

    class Meta:
        model = Cat
        fields = "__all__"

```

### 3.3. Setting Up Views for CRUD Operations

In `cats/views.py`, the `CatViewSet` is defined to handle CRUD operations for the `Cat` model. It uses `ModelViewSet` from Django Rest Framework (DRF), which automatically handles the logic for listing, creating, updating, and deleting entries:

```python
# cats/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cats.models import Cat
from cats.serializers import CatSerializer


class CatViewSet(ModelViewSet):
    """
    Cat ViewSet
    """

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

```

- `queryset = Cat.objects.all()`: Defines the queryset for the view, which retrieves all `Cat` objects from the database.
- `serializer_class = CatSerializer`: Specifies the serializer class to be used for converting `Cat` model instances to JSON and vice versa.
- `permission_classes = [IsAuthenticated]`: Restricts access to the view to authenticated users only.

### 3.4. Configuring URLs for the 'cats' app

A URL configuration is created for the `cats` app. A `SimpleRouter` is used to automatically route requests to the `CatViewSet`. This is placed in a new file `cats/urls.py`:

```python
# cats/urls.py
from rest_framework.routers import SimpleRouter

from cats.views import CatViewSet

router = SimpleRouter()
router.register("cats", CatViewSet)

urlpatterns = router.get_urls()

```

The generated URL patterns are then assigned to the `urlpatterns` variable. This variable is expected by Django's URL configuration system to define the routes for the application. When a request is made to the application, Django uses the urlpatterns list to match the request URL to the appropriate view. In this case, the views are part of the `CatViewSet`, which handles operations related to the `Cat` model.

## 4. Adding URLs to the Main Project

In `root/urls.py`, the URL paths for the admin interface, the DRF schema, and the `cats` app are included. This allows users to access the `cats` API through paths like `/apps/cats`:

```python
# root/urls.py
"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("apps/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "apps/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("apps", include("cats.urls")),
]

```

## 5. Modifying Settings

The `rest_framework`, `drf_spectacular`, and the new `cats` app are added to the `INSTALLED_APPS` list at the end of the file `root/settings.py`. This is necessary for Django to recognize and use them:

```python
# root/settings.py
...
INSTALLED_APPS += [
    'rest_framework',
    'drf_spectacular',
    'cats.apps.CatsConfig',
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

Additionally, we configure `REST_FRAMEWORK` to integrate `drf-spectacular` with Django REST Framework.

- `REST_FRAMEWORK`: This is a key in the Django settings dictionary that Django REST Framework looks for to configure its behavior.
- `"DEFAULT_SCHEMA_CLASS"`: This key within the `REST_FRAMEWORK` dictionary specifies the default schema class that DRF should use for generating API documentation.
- `"drf_spectacular.openapi.AutoSchema"`: This value indicates that the schema generation should be handled by the `AutoSchema` class from the `drf_spectacular.openapi` module. drf-spectacular is a library that provides OpenAPI 3.0 schema generation for DRF, which is useful for creating interactive API documentation.

## 6. Database Migrations

The commands `makemigrations` and `migrate` are run to create the necessary database tables and apply migrations for the `Cat` model:

```bash
./manage.py makemigrations
./manage.py migrate
```

## 7. Running the Application

Finally, the development server is started with:

```bash
./manage.py runserver
```

Then, you can access the Swagger-UI for the Cats API at http://localhost:8000/apps/schema/swagger-ui/. You can interact with this API using an admin user created with the command `./manage.py createsuperuser`. However, you first need to log in to the admin interface at http://localhost:8000/admin/.

## 8. Next Steps

This example is a complete first start to creating an API with Django Rest Framework. But don't stop here! Here are some suggestions for continuing your learning journey:

### 8.1 Database Access (QuerySet)

The reference framework is an SQL database and an ActiveRecord-type ORM. Understanding these two concepts provides an appropriate context for querying the database effectively.

Learning how to perform database queries is essential for any application. Django's ORM provides powerful tools to interact with the database. The key statements you should know are:

1. `filter` and `exclude`: Filter or exclude objects based on certain criteria.
1. `Q`: Allows building complex queries with logical operators.
1. `values` and `values_list`: Retrieve only the values of specific fields.
1. `annotate` and `aggregate`: Add annotations to objects and perform aggregate calculations.
1. `select_related`, `prefetch_related`, and `Prefetch`: Optimize queries to avoid the N+1 problem.

With these tools, you can build complex and efficient database queries. For more information, refer to the [official Django ORM documentation](https://docs.djangoproject.com/en/dev/topics/db/queries/).

### 8.2 Serializers

Serializers are a powerful tool for converting complex objects into data that can be sent over the network and vice versa. Django REST Framework provides a flexible and powerful API for creating serializers. You can learn more by consulting the [official Django REST Framework documentation](https://www.django-rest-framework.org/api-guide/serializers/).

### 8.3 Views

Views are the entry point for your application. Django REST Framework offers a wide range of generic views that you can use to quickly create RESTful APIs. You can also create your own custom views. For more information, consult the [official Django REST Framework documentation](https://www.django-rest-framework.org/api-guide/views/).

It's important to document your views. By doing so, you achieve two objectives: first, part of the documentation includes the routing of the API, and second, the documentation serves as a tool for developers to understand how your API works. To document your views, you can use [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/), a library that integrates with Django REST Framework to automatically generate the documentation for your API.

### 8.4 Security

Security has two separate yet interconnected aspects: Authentication and Permissions. Business logic allows you to combine these two aspects in the form of RBAC (Role-Based Access Control). To learn them, it is preferable to study them separately and then integrate them with business logic. A first approach to learning these two aspects separately is through the following extensions:

1. Authentication: [django-rest-framework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
2. Permissions: [django-rules](https://github.com/dfunckt/django-rules)
