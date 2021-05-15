from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="HEX API",
        default_version='v1',
        description="API version 1 for Test Services",
        contact=openapi.Contact(email="oliver.koyoc@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)
