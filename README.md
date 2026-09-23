# IRCE Coaching Website

IRCE (Inter Rural Competition Exam) Coaching के लिए Landing Page, Online Admission Form और Admin Panel.

## VS Code में चलाने का तरीका

1. इस folder को VS Code में खोलें।
2. Terminal खोलें।
3. Windows में:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
4. Browser में खोलें: http://127.0.0.1:5000

## Admin
URL: http://127.0.0.1:5000/admin/login
Default username: admin
Default password: irce123

Production में ADMIN_USER, ADMIN_PASSWORD और SECRET_KEY environment variables जरूर बदलें।

## मुख्य URL
/                 Landing Page
/admission        Admission Form
/admin/login      Admin Login
/application/ID   Application Status
