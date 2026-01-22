### InsightBoard – Dependency Engine

A backend service that converts meeting transcripts into a validated dependency graph of actionable tasks, ensuring logical consistency and safe AI processing.

--> Live URL :
--> GitHub Repo :

**_Tech Stack_**
--> Backend: Python, FastAPI

--> LLM: Google Gemini (gemini-2.5-flash)

--> Database: MongoDB Atlas

--> Hosting: Vercel

**_Idempotency_**
--> Each transcript is hashed (SHA-256)

--> Submitting the same transcript again returns the same job

--> Prevents duplicate LLM calls and costlts

**_Cycle Detection_**

--> Tasks are modeled as a directed graph

--> DFS-based cycle detection is used

--> Tasks involved in cycles are marked as BLOCKED

--> The system never crashes on invalid graphs

**_Local Setup_**

1. git clone <repo-url>

   cd backend
   
   python -m venv venv
   
   venv\Scripts\activate
   
   pip install -r requirements.txt

3. Create .env
   
   GEMINI_API_KEY=your_key
   
   MONGODB_URI=your_mongodb_uri

5. Run
   uvicorn app.main:app --reload

6. Open http://127.0.0.1:8000/docs
7. The provided Project Odyssey transcript was used during testing
8. Frontend visualization (Level 3) is built on top of this API
