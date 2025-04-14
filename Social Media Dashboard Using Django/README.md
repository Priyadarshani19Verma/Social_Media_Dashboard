# 🌐 Social Media Dashboard using Django

This is a **Social Media Dashboard** built with Django, where users can log in, view, and interact with their Twitter and Facebook posts — all in one place.

---

## ✨ Features

- 🔐 User Registration and Login
- 📝 Post creation within the dashboard
- ❤️ Like & 💬 Comment on posts
- ✏️ Edit and ❌ Delete comments
- 📄 Analytics (Most liked post, total likes, comments, posts)
- 🐦 Twitter integration (fetch latest tweets)
- 📘 Facebook integration (fetch latest posts)
- 🌙 Light/Dark mode toggle
- 📱 Clean, responsive and modern UI

---

## 🛠️ Technologies Used

- Django
- Python
- Tweepy (for Twitter API)
- Facebook SDK
- HTML/CSS
- Bootstrap (for styling)
- SQLite (default Django database)

---

## 🚀 How to Run the Project Locally

1. **Clone this repo**
   ```bash
   git clone https://github.com/your-username/social-media-dashboard.git
   cd social-media-dashboard
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv env
   env\Scripts\activate  # for Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (create a file `twitter_credentials.py` and `facebook_credentials.py` in the `utils` folder)


i. Go to `twitter_credentials.py` and `facebook_credentials.py`
ii. Replace placeholder values with your actual API tokens:

   ```python
   BEARER_TOKEN = "your real Twitter token"
   FACEBOOK_ACCESS_TOKEN = "your real Facebook token"



5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

8. Open in browser: `http://127.0.0.1:8000`

---

## 🙋‍♀️ Admin Login

Once superuser is created, go to:

- Admin: `http://127.0.0.1:8000/admin`
- Login with your credentials and add Twitter/Facebook usernames under Profile

---

## ⚠️ Important Notes

⚠️ This project uses private API tokens (Twitter & Facebook).
To run this project, create a file called:
- utils/twitter_credentials.py
- utils/facebook_credentials.py

And add your API tokens in the following format:

BEARER_TOKEN = "your_twitter_bearer_token_here"
FACEBOOK_ACCESS_TOKEN = "your_facebook_access_token_here"

These values must be generated from your own developer account.

