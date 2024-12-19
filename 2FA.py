import hashlib
import os
import time
import base64
import hmac
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Step 1: Secure Hashing for Password Storage
def hash_password(password):
    salt = "my_salt"  # Static salt (replace with random salts in production)
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest() #hexdigest is used to convert raw binary bytes to readable hexadecimal
    return hashed_password


# Step 2: Verify Password
def verify_password(stored_hash, password):
    salt = "my_salt"
    return stored_hash == hashlib.sha256((salt + password).encode()).hexdigest()


# Step 3: TOTP Generation
def generate_otp(secret_key, interval=120):
    key = base64.b32decode(secret_key, casefold=True)
    current_time_step = int(time.time() // interval)
    time_bytes = current_time_step.to_bytes(8, byteorder="big")
    hmac_hash = hmac.new(key, time_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    binary_code = int.from_bytes(hmac_hash[offset:offset + 4], byteorder="big") & 0x7FFFFFFF
    otp = binary_code % 1000000
    return str(otp).zfill(6)


# Step 4: Verify OTP
def verify_otp(secret_key, otp, interval=120):
    return otp == generate_otp(secret_key, interval)


# Step 5: Send OTP via Email
def send_email_otp(receiver_email, otp):
    sender_email = "tahboubtareq06@gmail.com"
    sender_password = "otasnexouirpuhql"

    subject = "Your OTP Code for Authentication"
    body = f"Your One-Time Password (OTP) is: {otp}\nThis OTP is valid for 120 seconds."

    # Email message setup
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the OTP message
    message.attach(MIMEText(body, "plain"))

    try:
        # Use SSL instead of STARTTLS
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"OTP sent successfully to {receiver_email}")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


# Main Functionality
def main():
    print("Two-Factor Authentication System")

    # Step 1: User Registration (Password and Shared Secret Key)
    password = input("Set your password: ")
    hashed_password = hash_password(password)

    # Generate a random shared secret key for OTP
    secret_key = base64.b32encode(os.urandom(10)).decode()
    print(f"Your shared secret key for OTP: {secret_key}")
    print("(Store this key securely, or use it in an authenticator app)")

    # Step 2: User Login
    print("\n------------ Login ------------")
    login_password = input("Enter your password: ")

    # Verify Password
    if not verify_password(hashed_password, login_password):
        print("Invalid password!")
        return

    # Generate OTP and send via email
    receiver_email = input("Enter your email address to receive the OTP: ")
    otp = generate_otp(secret_key)
    send_email_otp(receiver_email, otp)

    # OTP Verification
    user_otp = input("Enter the OTP sent to your email: ")
    if verify_otp(secret_key, user_otp):
        print("Authentication successful!")
    else:
        print("Invalid OTP!")


if __name__ == "__main__":
    main()
