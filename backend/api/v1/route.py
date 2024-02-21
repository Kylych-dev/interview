from django.urls import path
from rest_framework.routers import DefaultRouter

from api.auth.views import RegisterView, UserAuthenticationView
from api.v1.accounts.views import CustomUserViewSet, UserRoleViewSet
from api.v1.sewing_workshop.views import SewingWorkshopViewSet
from api.v1.wallet.views import EmployeeWalletViewSet
from api.v1.warehouse.views import ProductViewSet
from api.v1.warehouse.material_template_views import MaterialTemplateViewSet
from api.v1.warehouse.warehousematerial_views import WarehouseMaterialViewSet
from api.v1.warehouse.warehouse_views import WarehouseViewSet
from api.v1.workorder.views import FabricationViewSet
from api.v1.order.views import OrderModelViewSet
from api.v1.client.views import ClientModelViewSet
from api.v1.cut.views import CutModelViewSet
from api.v1.location.views import UserEntryCheckModelViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # registration
        path("register/", RegisterView.as_view({"post": "register"}), name="register"),

        # verify
        path("verify-code/", RegisterView.as_view({"post": "verify"}), name="verify"),
        path("resend/verify-code/", RegisterView.as_view({"post": "resend_verify"}), name="resend-verify"),
        
        # login
        path("login/", UserAuthenticationView.as_view({"post": "login"}), name="login"),
        path("logout/", UserAuthenticationView.as_view({"post": "logout"}), name="logout"),
        
        # user
        path("users/", CustomUserViewSet.as_view({"get": "list"}), name="user-list"),
        path("users/profile/", CustomUserViewSet.as_view({"get": "user_profile"}), name="user-profile"),
        path("users/<slug:slug>/", CustomUserViewSet.as_view({"get": "user_detail"}), name="user-detail"),
        path("users/<slug:slug>/", CustomUserViewSet.as_view({"put": "update_detail"}), name="update-detail"),

        # role
        path("roles/", UserRoleViewSet.as_view({"get": "list"}), name='user-roles'),

        # location
        path("users/entry-check/", UserEntryCheckModelViewSet.as_view({"get": "list"}), name="entry-chick-list"),
        path("users/entry-check/create/", UserEntryCheckModelViewSet.as_view({"post": "create"}), name="entry-check-create"),
        
        # workshop
        path("workshop/", SewingWorkshopViewSet.as_view({"get": "list"}), name="workshop-list"),
        path("workshop/<int:pk>/",SewingWorkshopViewSet.as_view({"put": "update"}), name="workshop-update"),
        path("workshop/<int:pk>/", SewingWorkshopViewSet.as_view({"delete": "delete"}), name="workshop-delete"),
        
        # wallet
        path("wallet/", EmployeeWalletViewSet.as_view({"get": "employee_wallet"}), name="employee-wallet"),
        path("wallet/transaction/", EmployeeWalletViewSet.as_view({"post": "subtract_balance"}), name="subtract-balance"),
        
        # product
        path("product/", ProductViewSet.as_view({"get": "list"}), name="product-list"),
        path("product/create/", ProductViewSet.as_view({"post": "create"}), name="product-create"),
        path("product/<int:pk>/", ProductViewSet.as_view({"put": "update"}), name="product-update"),
        path("product/<int:pk>/",ProductViewSet.as_view({"delete": "delete"}), name="product-delete"),

        
        # fabrication
        path("fabric/", FabricationViewSet.as_view({"get": "list"}), name="fabrica-list"),
        path("fabric/create/", FabricationViewSet.as_view({"post": "create"}), name="fabrica-create"),
        path("fabric/<slug:slug>/", FabricationViewSet.as_view({"put": "update"}), name="fabrica-update"),
        path("fabric/<slug:slug>/", FabricationViewSet.as_view({"delete": "delete"}), name="fabrica-delete"),
        
        # item
        # path("product-template/", ProductTemplateViewSet.as_view({"get": "list"}), name="product-template-list"),
        # path("product-template/create/", ProductTemplateViewSet.as_view({"post": "create"}), name="product-template-create"),
        # path("product-template/<int:pk>/", ProductTemplateViewSet.as_view({"put": "update"}), name="product-template-update"),
        # path("product-template/<int:pk>/", ProductTemplateViewSet.as_view({"delete": "delete"}), name="product-template-delete"),
        
        # Order
        path("order/", OrderModelViewSet.as_view({"get": "list"}), name="order-list"),
        path("order/create/", OrderModelViewSet.as_view({"post": "create"}), name="order-create"),

        path("order/create/", OrderModelViewSet.as_view({"delete": "delete"}), name="order-delete"),
        path("order/<int:pk>/", OrderModelViewSet.as_view({"put": "update"}), name="order-update"),
        
        # material
        path("material-template/", MaterialTemplateViewSet.as_view({"get": "list"}), name="material-list"),
        path("material-template/create/", MaterialTemplateViewSet.as_view({"post": "create"}), name="material-create"),
        path("material-template/<int:pk>/", MaterialTemplateViewSet.as_view({"put": "update"}), name="material-update"),
        path("material-template/<int:pk>/", MaterialTemplateViewSet.as_view({"delete": "delete"}), name="material-delete"),
        
        # warehousematerial
        path("warehousematerial/", WarehouseMaterialViewSet.as_view({"get": "list"}), name="warehousematerial-list"),
        path("warehousematerial/create/", WarehouseMaterialViewSet.as_view({"post": "create"}), name="warehousematerial-create"),
        path("warehousematerial/<int:pk>/", WarehouseMaterialViewSet.as_view({"put": "update"}),name="warehousematerial-update"),
        path("warehousematerial/<int:pk>/", WarehouseMaterialViewSet.as_view({"delete": "delete"}), name="warehousematerial-delete"),
        
        # client
        path("client/", ClientModelViewSet.as_view({"get": "list"}), name="client-list"),
        path("client/create/", ClientModelViewSet.as_view({"post": "create"}), name="client-create"),
        path("client/<int:pk>/", ClientModelViewSet.as_view({"put": "update"}), name="client-update"),
        path("client/<int:pk>/", ClientModelViewSet.as_view({"delete": "delete"}), name="client-delete"),

        # Cut
        path("cut/", CutModelViewSet.as_view({"get": "list"}), name="cut-list"),
        path("cut/create/",CutModelViewSet.as_view({"post": "create"}), name="cut-create"),
        path("cut/<int:pk>/",CutModelViewSet.as_view({"put": "update"}), name="cut-update"),
        path("cut/<int:pk>/",CutModelViewSet.as_view({"delete": "delete"}), name="cut-delete"),

        # warehouse
        path("warehouse/<int:pk>", WarehouseViewSet.as_view({"get": "retrieve"}), name="warehouse-list"),
        path("warehouse/<int:pk>", WarehouseViewSet.as_view({"delete": "delete"}), name="warehouse-delete"),
    ]
)