from django.urls import path,include
from .import views
from .views import LoansGroupedByUser, LoanDetailView
urlpatterns = [
   
      path("admin/get/loans/", LoansGroupedByUser.as_view(), name="loans-grouped"),
    path("admin/loan/<int:loan_id>/", LoanDetailView.as_view(), name="loan-detail"),
]