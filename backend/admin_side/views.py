from itertools import groupby
from operator import attrgetter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from user_side.models import Loan
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class LoansGroupedByUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != "admin":
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        loans = Loan.objects.select_related("user").order_by("user__username")  # Ensure proper sorting for groupby

        grouped_loans = {}
        for username, loan_list in groupby(loans, key=attrgetter("user.username")):
            grouped_loans[username] = [
                {
                    "id": loan.id,
                    "name": loan.name,
                    "amount": float(loan.amount),
                    "interest_rate": loan.interest_rate,
                    "monthly_payment": float(loan.monthly_payment),
                    "start_date": loan.start_date.strftime("%Y-%m-%d"),
                    "tenure": loan.tenure,
                    "status": loan.status,
                    "total_interest": float(loan.total_interest),
                    "total_amount": float(loan.total_amount),
                    "foreclosure_amount": float(loan.foreclosure_amount) if loan.foreclosure_amount else None,
                    "foreclosure_date": loan.foreclosure_date.strftime("%Y-%m-%d") if loan.foreclosure_date else None,
                }
                for loan in loan_list
            ]

        return Response(grouped_loans, status=status.HTTP_200_OK)  # Use DRF Response


@method_decorator(csrf_exempt, name="dispatch")
class LoanDetailView(APIView):
    """Retrieve or delete a loan by ID, only accessible to admins"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, loan_id):
        if request.user.user_type != "admin":
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        loan = get_object_or_404(Loan.objects.select_related("user"), id=loan_id)

        return Response({
            "id": loan.id,
            "user": loan.user.username,
            "name": loan.name,
            "amount": float(loan.amount),
            "interest_rate": loan.interest_rate,
            "monthly_payment": float(loan.monthly_payment),
            "start_date": loan.start_date.strftime("%Y-%m-%d"),
            "tenure": loan.tenure,
            "status": loan.status,
            "total_interest": float(loan.total_interest),
            "total_amount": float(loan.total_amount),
            "foreclosure_amount": float(loan.foreclosure_amount) if loan.foreclosure_amount else None,
            "foreclosure_date": loan.foreclosure_date.strftime("%Y-%m-%d") if loan.foreclosure_date else None,
        }, status=status.HTTP_200_OK)

    def delete(self, request, loan_id):
        if request.user.user_type != "admin":
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        loan = get_object_or_404(Loan.objects.select_related("user"), id=loan_id)
        loan.delete()
        return Response({"message": "Loan deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
