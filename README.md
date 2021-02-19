# Movie Rating System

A Flask web application that predicts movie ratings (out of 10) from user-written reviews using NLTK's VADER sentiment analysis.

Built as a college project at VIT.

## Features

- **Sentiment-based rating prediction** -- paste a movie review and get a predicted rating out of 10
- **User authentication** -- sign up and log in with a SQLite-backed account system
- **Prediction history** -- logged-in users can view and delete their past predictions
- **Admin portal** -- manage user accounts and view all activity
- **Guest mode** -- try the rating predictor without creating an account
- **Profanity filter** -- reviews are screened for profanity before processing
- **Heroku-ready** -- configured for deployment with Gunicorn

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask                     |
| NLP         | NLTK (VADER Sentiment Analyzer)   |
| Database    | SQLite                            |
| Frontend    | HTML, CSS, Bootstrap, Jinja2      |
| Deployment  | Heroku, Gunicorn                  |

## Getting Started

### Prerequisites

- Python 3.14
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/sidhanthapoddar99/Movie-Rating-System.git
cd Movie-Rating-System

# Create and activate a virtual environment
python3.14 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize the SQLite database
python usersdatabasegenerator.py

# Run the application
python app_movie.py
```

The app will start on `http://127.0.0.1:5000` by default.

## Project Structure

```
Movie_rating_system/
├── app_movie.py                 # Main Flask application and routes
├── usersdatabasegenerator.py    # Script to initialize the SQLite database
├── softwareproject.db           # SQLite database (generated)
├── requirements.txt             # Python dependencies
├── Procfile                     # Heroku deployment config
├── nltk.txt                     # NLTK data packages for Heroku
├── templates/                   # Jinja2 HTML templates
│   ├── LandingPage.html         # Home / landing page
│   ├── login.html               # User login
│   ├── sign_up.html             # User registration
│   ├── results.html             # Rating prediction results
│   ├── adminportal.html         # Admin dashboard
│   ├── display_history.html     # User prediction history
│   └── ...                      # Additional pages
└── static/                      # CSS, JS, images, and vendor assets
```

## How It Works

1. The user submits a free-text movie review.
2. The review is checked for profanity. If profanity is detected, the review is rejected.
3. NLTK's **VADER (Valence Aware Dictionary and sEntiment Reasoner)** analyzer computes a compound sentiment score between -1 (most negative) and +1 (most positive).
4. The compound score is mapped to a rating out of 10:
   - **Negative reviews:** `rating = 10 - |compound * 10| + 0.5`
   - **Positive reviews:** `rating = compound * 10 - 0.5`
5. The result is displayed to the user. For logged-in users, the review and rating are saved to the database for future reference.

## License

This project is licensed under the MIT License.
