# Telegram-Medical-Insights
This Repository contains data pipeline from raw Telegram data to an analytical API for Ethiopian medical business insights.

## 🚀 Environment Setup

### 🔹 Step 1: Clone the Repository

    git clone https://github.com/your-username/telegram-medical-insights.git

    cd telegram-medical-insights

### 🔹 Step 2: Create & Activate a Virtual Environment

    python -m venv .venv

    source .venv/bin/activate   # On Windows: .venv\Scripts\activate

### 🔹 Step 3: Install Dependencies

    pip install -r requirements.txt

### 🔹 Step 4: Start the Application with Docker 

    docker-compose up --build

## Structure of the Project
telegram-medical-insights/
├── notebooks/
│   └── ... (your Jupyter notebooks)
├── scripts/
│   ├── telegram_scraper.py
│   ├── load_json_to_postgres.py
│   ├── object_detection.py
│   └── ... (other scripts)
├── detections/
│   └── predictions.csv
├── data/
│   └── images/
├── dbt_project/
│   └── models/
│       ├── staging/
│       └── marts/
│           └── messaging/
│               ├── dim_channels.sql
│               ├── dim_dates.sql
│               └── fct_messages.sql
├── fastapi_app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── dagster_project/
│   ├── pipeline.py         
│   ├── __init__.py
│   └── repository.py       
├── pyproject.toml / requirements.txt
└── README.md
