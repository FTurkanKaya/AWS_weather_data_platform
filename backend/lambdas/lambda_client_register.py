import boto3
import os

cognito_client = boto3.client('cognito-idp', region_name='eu-north-1')

CLIENT_ID = os.environ['CLIENT_ID']  # User Pool App Client ID

def lambda_handler(event, context):
    print("Received event:", event)

    username = event['userName']

    try:
        # Kullanıcı verified değilse, tekrar doğrulama kodu gönder
        cognito_client.resend_confirmation_code(
            ClientId=CLIENT_ID,
            Username=username
        )
        print(f"Verification code resent to user: {username}")

        # Girişi engellemek için exception fırlat
        raise Exception("User is not confirmed. Verification code has been resent.")
    
    except cognito_client.exceptions.UserNotFoundException:
        print(f"User {username} not found in User Pool.")
        raise
    except Exception as e:
        print("Error resending verification code:", e)
        raise

