# Django Auto Router

**Fast Django Routing.**

DAR (Django Auto Router) is a simple library for easy routing DRF (Django REST Framework) views and viewsets.

## Requirements

DAR requires:
* Python 3.6+
* Django 3.0+
* Django REST Framework 

## Installation
Install using pip.
```
pip install djangoautorouter
```

Add `'auto_router'` to your `INSTALLED APPS`.
```python
INSTALLED_APPS = [
    ...
    'auto_router'
]
```

## Usage
1. You should create a `routers.py` in your main app:
```python
from auto_router import Router

router_v2 = AutoRouter("api/v2/", namespace="api-v2")
router_v1 = AutoRouter("api/v1/", namespace="api-v1")
```

2. Add it to your `urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

from .routers import main_router, router

urlpatterns = [
    path("admin/", admin.site.urls),
    main_router.path,
    router.path,
]
```

3. Then, from your `views.py` in any of your apps, you can route it by using:
```python
from rest_framework import generics, mixins, viewsets

from main.routers import router_v1

from . import models, serializers

@router_v1.route_view("cinema/list-movies/", "movie-list")
class ListMovies(generics.ListAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer

@router_v1.route_viewset("cinema/movies", "movies")
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MovieSerializer
    queryset = models.Movie.objects.all()
```

4. Call it:
```bash
GET http://localhost:8000/api/v1/cinema/list-movies/
```
```bash
POST http://localhost:8000/api/v1/cinema/movies/
```
