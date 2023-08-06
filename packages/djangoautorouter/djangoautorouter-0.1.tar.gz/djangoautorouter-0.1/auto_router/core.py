import importlib
from inspect import isclass

from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django.conf import settings


class AutoRouter:
    def __init__(self, endpoint: str, namespace: str, module: str = None) -> None:
        self.endpoint: str = endpoint
        self.namespace: str = namespace
        self.module: str = module
        self._router = DefaultRouter()
        self._urls = []
        self.DEBUG = settings.DEBUG

    def route_viewset(self, route: str, basename: str = ""):
        def inner(viewset):
            self._log(
                "Routing viewset " + str(viewset) + " to " + self.endpoint + route
            )
            self._router.register(route, viewset, basename=basename)
            return viewset

        return inner

    def route_view(self, route: str, name: str = ""):
        def inner(view):
            self._log("Routing view " + str(view) + " to " + self.endpoint + route)
            self._urls.append(path(route, view.as_view(), name=name))
            return view

        return inner

    def _log(self, message: str):
        if self.DEBUG:
            print("Auto Router - " + message)

    def _load_all_modules(self):
        for module in settings.INSTALLED_APPS:
            try:
                module = importlib.import_module(module + ".views")
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)

                    if isclass(attribute):
                        # Add the class to this package's variables
                        globals()[attribute_name] = attribute
            except:
                pass

    @property
    def urls(self):
        return [*self._urls, *self._router.urls]

    @property
    def path(self):
        if self.module:
            importlib.import_module(self.module)
        else:
            self._load_all_modules()

        self._log("Done loading views")

        return path(
            self.endpoint,
            include((self.urls, "main"), namespace=self.namespace),
        )
