from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.utils.timezone import now
from .models import CustomUser, OtpCode
import requests
import os
from dotenv import load_dotenv
load_dotenv()
@csrf_exempt
def send_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        phone = data.get("phone")
        name=data.get("name")
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error':'user already exists'},status=403)
        if not email or not phone:
            return JsonResponse({"error": "Email and phone are required"}, status=400)

        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)

        # Save or update OTP
        otp_instance, created = OtpCode.objects.update_or_create(
            email=email,
            defaults={"otp": otp, "created_at": now()}
        )
        
        # Simulate sending OTP (Replace with actual email/SMS API)
        print(f"OTP for {email}: {otp}")
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": os.getenv('API_key'),
            "content-type": "application/json"
        }

        data = {
            "sender": {
                "name": "Loanapp",
                "email": "iamhop192@gmail.com"
            },
            "to": [
                {
                    "email": email,
                    "name": name
                }
            ],
            "subject": "OTP Verification",
            "htmlContent": f"<html><head></head><body><h1>Hello {name}!</h1><p>Here is your OTP: <strong>{otp}</strong></p></body></html>"
        }

        response = requests.post(url, headers=headers, json=data)

        return JsonResponse({"message": "OTP sent successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
@csrf_exempt
def verify_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        phone = data.get("phone")
        pin = data.get("pin")

        if not all([email, phone, pin]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        otp_instance = OtpCode.objects.filter(email=email).first()
        if not otp_instance:
            return JsonResponse({"error": "Invalid OTP request"}, status=400)

        if otp_instance.is_expired():
            return JsonResponse({"error": "OTP expired"}, status=400)

        if str(otp_instance.otp) != str(pin):
            return JsonResponse({"error": "Invalid OTP"}, status=400)

        return JsonResponse({"message": "OTP verified successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        pin = data.get("pin")

        if not all([name, email, phone, password, pin]):
            return JsonResponse({"error": "All fields are required"}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error':'user already exists'},status=403)
        # Verify OTP before registering
        otp_instance = OtpCode.objects.filter(email=email).first()
        if not otp_instance or otp_instance.is_expired() or str(otp_instance.otp) != str(pin):
            return JsonResponse({"error": "Invalid or expired OTP"}, status=400)

        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # Create user
        user = CustomUser.objects.create(
            username=name,
            email=email,
            phone_number=phone,
            is_active=True
        )
        user.set_password(password)
        user.save()

        # Delete OTP after successful registration
        otp_instance.delete()

        return JsonResponse({"message": "Registration successful"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)












