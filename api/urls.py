from django.urls import path
from . import views

urlpatterns = [
    path("api/contract/", views.contract_status, name="contract_status"),
    path("api/contract/balance/", views.get_balance, name="contract_balance"),
    path("api/contract/listing/<int:nft_id>/", views.get_listing, name="contract_listing"),
    # YOU WOULD ADD MORE API ENDPOITNS HERE ...
]