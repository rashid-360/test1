from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
# Create your views here.
from rest_framework import viewsets
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.permissions import IsAuthenticated
class ViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)  # Only return user's loans

    def perform_create(self, serializer):
        if self.request.user.user_type != "user":
            raise PermissionDenied("Only users with type 'user' can create loans.")
        serializer.save(user=self.request.user)  # Assign logged-in user