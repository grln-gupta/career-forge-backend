# ⚡ Career Forge AI - Backend API

A high-performance **FastAPI** microservice that powers the Career Forge platform. It serves as the intelligent orchestration layer between the Angular frontend and **Google's Gemini Pro LLM**, transforming raw user inputs into professional, ATS-optimized career assets.

## 🏗 Architecture & Design Decisions

* **Framework:** **FastAPI** (Python) chosen for its async capabilities and automatic Swagger UI generation (`/docs`).
* **AI Engine:** **Google Gemini Pro** (via `google-generativeai`).
* **Smart Model Discovery:** Implemented a dynamic model selector that queries Google's available models at startup to prevent `404` errors if a specific version (e.g., `gemini-1.5-flash`) is deprecated or unavailable.
* **Resilience:**
    * **Global Exception Handling:** Catches API failures and returns clean `500` errors to the client.
    * **Keep-Alive Strategy:** Configured for high availability on Render's free tier using external cron-job pings.
* **Security:** Environment-variable based API key management (`GEMINI_API_KEY`) and strict CORS configuration for authorized frontend origin access.

## 🚀 Key Features

* **Resume Optimization:** Converts rough notes into **STAR Method** (Situation, Task, Action, Result) bullet points.
* **LinkedIn Viral Generator:** Rewrites updates into engaging, high-impression posts with hooks and hashtags.
* **Portfolio Builder:** Structures technical projects into **Problem-Solution-Impact** case studies.
* **Contextual Prompt Engineering:** Uses distinct system instructions based on the selected `mode` (resume vs. linkedin vs. portfolio) to ensure tonal accuracy.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI, Uvicorn
* **AI/LLM:** Google Generative AI (Gemini)
* **Validation:** Pydantic Models
* **Deployment:** Render (Web Service)

## 🔧 Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/career-forge-api.git](https://github.com/YOUR_USERNAME/career-forge-api.git)
    cd career-forge-api
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**
    Create a `.env` file and add your Google Gemini Key:
    ```bash
    GEMINI_API_KEY=your_api_key_here
    ```

5.  **Run the Server:**
    ```bash
    uvicorn brain:app --reload
    ```
    API will run at `http://localhost:8000`. Documentation at `http://localhost:8000/docs`.

## 📦 Deployment (Render)

This project is configured for seamless deployment on **Render**.
* **Build Command:** `pip install -r requirements.txt`
*
