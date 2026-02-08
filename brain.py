import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# 1. Setup API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini if key exists
if API_KEY:
    genai.configure(api_key=API_KEY)

# 2. Setup the App
app = FastAPI()

# 3. Allow Frontend to talk to Backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Define the Data Model
class OptimizationRequest(BaseModel):
    text: str
    mode: str
    role: str

# 5. The Logic
@app.post("/optimize")
async def optimize_text(request: OptimizationRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server Error: GEMINI_API_KEY not found in environment variables.")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Select prompt based on mode
        if request.mode == "resume":
            prompt = f"""
            Act as a Senior Resume Writer. Rewrite the following bullet point for a {request.role}.
            Rules:
            - Use strong action verbs (Spearheaded, Engineered, Optimized).
            - Include specific metrics/numbers if possible (or placeholders like [X]%).
            - Remove fluff and buzzwords.
            - Keep it under 2 lines.
            - Output ONLY the rewritten bullet point.
            
            Input: {request.text}
            """
        elif request.mode == "linkedin":
            prompt = f"""
            Act as a LinkedIn Influencer. Rewrite this thought into a viral post for a {request.role}.
            Rules:
            - Use a hook in the first line.
            - Add spacing for readability.
            - Use 3-5 relevant hashtags.
            - Keep the tone professional but engaging.
            
            Input: {request.text}
            """
        else: # Portfolio / General
            prompt = f"""
            Act as a Technical Writer. Rewrite this project description for a {request.role} portfolio.
            Rules:
            - Use the STAR method (Situation, Task, Action, Result).
            - Highlight technical challenges and solutions.
            - Keep it professional and concise.
            
            Input: {request.text}
            """

        # Set max tokens based on mode
        max_tokens = 150 if request.mode == "resume" else 400

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7
            )
        )
        
        return {"optimized": response.text.strip()}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 6. Run the Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)