import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

def send_email(subject, message, email_list):

    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    print(gmail_user)
    print(gmail_password)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ", ".join(email_list)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(gmail_user, gmail_password)

    
        server.sendmail(gmail_user, email_list, msg.as_string())
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")


def send_activation_email(user):
  
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    activation_url = f'http://localhost:8000/activate_account/{uid}/{token}/'

    subject = 'Activate your account'
    message = render_to_string('user/email.html', {'user': user,'activation_url': activation_url,})
    send_email(subject, message, [user.email])