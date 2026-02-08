import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --- CONFIGURATION ---
# ⚠️ PASTE YOUR API KEY HERE
API_KEY = "AIzaSyB01fXdhW3Fwc_zKsVA_LzghWI5CeTcjuw"

genai.configure(api_key=API_KEY)
# Using the alias that works for your account
model = genai.GenerativeModel('gemini-flash-latest')

app = FastAPI()

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class OptimizeRequest(BaseModel):
    text: str
    target_role: str  # e.g. "Nurse", "Python Dev", "Sales Manager"
    mode: str         # "resume", "linkedin", "portfolio"

# --- ENDPOINT ---
@app.post("/optimize")
async def optimize_text(request: OptimizeRequest):
    try:
        # DYNAMIC & AGGRESSIVE PROMPTS
        role = request.target_role if request.target_role else "Professional"
        
        prompts = {
            "resume": f"""
            ACT AS: A Ruthless Senior Recruiter & ATS Algorithm Expert for {role} roles.
            TASK: Rewrite the user's raw input into a single, high-impact "Bullet-Proof" resume point.
            MODE: AGGRESSIVE & METRIC-FOCUSED.

            RULES:
            1. START immediately with a Power Verb (e.g., Engineered, Spearheaded, Slashed, Revitalized).
            2. DESTROY passive language (Never use: "responsible for", "helped", "tried").
            3. FORCE METRICS: If the user provides numbers, emphasize them. If not, structure the sentence to highlight efficiency/impact.
            4. KEYWORDS: Inject ATS keywords relevant to {role}.
            5. FORMAT: Return ONLY the optimized bullet point text. No intro. No quotes.
            """,
            
            "linkedin": f"""
            ACT AS: A Viral Content Strategist for {role} professionals.
            TASK: Rewrite the input into a professional, engaging LinkedIn post.
            
            STRUCTURE:
            1. The Hook (Grab attention immediately).
            2. The Insight (The core professional lesson or story).
            3. The Call to Action (Question or takeaway).
            4. Hashtags (3-5 relevant tags).
            """,
            
            "portfolio": f"""
            ACT AS: A Portfolio Curator for a {role}.
            TASK: Structure the input into a professional 'Case Study' entry.
            
            STRUCTURE:
            1. Challenge: (The specific problem you faced).
            2. Action: (The tools, skills, or strategies used).
            3. Result: (The outcome - Revenue, Speed, Safety, etc.).
            """
        }
        
        system_instruction = prompts.get(request.mode, "Make this professional.")
        final_prompt = f"{system_instruction}\n\nUSER INPUT: {request.text}"
        
       max_tokens = 150 if request.mode == "resume" else 400

response = model.generate_content(
    final_prompt,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=max_tokens, # <--- STOPS IT FROM RAMBLING
        temperature=0.7 # <--- KEEPS IT FOCUSED
    )
)
        return {"optimized": response.text}
    except Exception as e:
        return {"optimized": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)