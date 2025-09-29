from django.contrib import admin
from django.urls import path, include
from colegio.views import graphiql_interface, graphql_endpoint, debug_schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('colegio.urls')),
    path('debug-schema/', debug_schema, name='debug-schema'),
    path('graphql/', graphql_endpoint, name='graphql-endpoint'),
    path('graphiql/', graphiql_interface, name='graphiql'),
]