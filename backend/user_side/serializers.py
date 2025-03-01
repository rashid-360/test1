from decimal import Decimal
from datetime import date
from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id', 'user', 'name', 'amount', 'tenure', 'interest_rate', 
            'monthly_payment', 'start_date', 'status', 'total_interest', 
            'total_amount', 'foreclosure_amount', 'foreclosure_date'
        ]
        extra_kwargs = {
            'user': {'required': False},  # User will be set automatically
            'monthly_payment': {'required': False},  
            'start_date': {'required': False},
            'status': {'required': False},
            'total_interest': {'required': False},
            'total_amount': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user  # Get logged-in user
        start_date = date.today()
        status = 'active'
        
        amount = validated_data['amount']
        tenure = validated_data['tenure']
        interest_rate = Decimal(validated_data['interest_rate'])  # Convert to Decimal

        # Calculate total interest & total amount
        total_interest = (amount * (interest_rate / Decimal(100)) * (tenure / Decimal(12)))
        total_amount = amount + total_interest

        # Calculate monthly payment
        monthly_payment = total_amount / tenure if tenure > 0 else Decimal(0)

        # Create Loan instance
        return Loan.objects.create(
            user=user,
            name=validated_data['name'],
            amount=amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_payment=monthly_payment,
            start_date=start_date,
            status=status,
            total_interest=total_interest,
            total_amount=total_amount
        )
