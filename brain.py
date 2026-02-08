from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# 1. Enable CORS (Allows Angular to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SMART MODEL SETUP (Fixes the 404 Crash) ---
API_KEY = os.getenv("GEMINI_API_KEY")
active_model = None

def configure_genai():
    global active_model
    if not API_KEY:
        print("❌ CRITICAL: GEMINI_API_KEY is missing!")
        return

    try:
        genai.configure(api_key=API_KEY)
        print("🔍 Searching for available Gemini models...")
        
        # List what models your API key can actually see
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"📋 Found models: {available_models}")

        # Smart Selection: Prefer Flash (Fast), then Pro, then whatever works
        model_name = "models/gemini-1.5-flash" # Default wish
        
        if "models/gemini-1.5-flash" in available_models:
            model_name = "models/gemini-1.5-flash"
        elif "models/gemini-pro" in available_models:
            model_name = "models/gemini-pro"
        elif available_models:
            model_name = available_models[0] # Fallback to first available
        
        print(f"✅ ACTIVATED MODEL: {model_name}")
        active_model = genai.GenerativeModel(model_name)

    except Exception as e:
        print(f"⚠️ Configuration Error: {e}")

# Run setup immediately
configure_genai()

# --- DATA MODELS ---
class OptimizeRequest(BaseModel):
    text: str
    mode: str
    role: str

# --- THE MISSING INSTRUCTIONS (RESTORED) ---
@app.post("/optimize")
async def optimize_text(request: OptimizeRequest):
    # If model crashed, try to restart it
    if not active_model:
        configure_genai()
        if not active_model:
            raise HTTPException(status_code=500, detail="AI Model unavailable. Check Server Logs.")

    # 1. RESUME MODE (STAR Method)
    if request.mode == "resume":
        prompt = f"""
        Act as an Expert Resume Writer and ATS Specialist.
        TASK: Rewrite the user's rough bullet point for a '{request.role}' resume.
        
        RULES:
        1. Use the STAR Method (Situation, Task, Action, Result).
        2. Start with a strong Power Verb (e.g., Engineered, Spearheaded, Optimized).
        3. Quantify results with numbers/percentages where possible (e.g., "improved efficiency by 20%").
        4. Remove fluff and make it concise (1-2 sentences max).
        5. Output ONLY the rewritten bullet point. No intro.

        INPUT: "{request.text}"
        """

    # 2. LINKEDIN MODE (Viral/Professional)
    elif request.mode == "linkedin":
        prompt = f"""
        Act as a LinkedIn Influencer and Personal Branding Expert.
        TASK: Rewrite the user's update into an engaging LinkedIn post for a '{request.role}'.
        
        RULES:
        1. Start with a "Hook" (a catchy first line to stop the scroll).
        2. Use short paragraphs and plenty of white space.
        3. Maintain a professional yet authentic tone.
        4. Include 3-5 relevant hashtags at the bottom.
        5. Use appropriate emojis to make it visually appealing.

        INPUT: "{request.text}"
        """

    # 3. PORTFOLIO MODE (Case Study)
    elif request.mode == "portfolio":
        prompt = f"""
        Act as a Technical Writer and Portfolio Coach.
        TASK: Convert the user's rough notes into a structured Case Study for a '{request.role}' portfolio.
        
        RULES:
        1. Organize the output into three distinct sections: 
           - 🛑 PROBLEM: (What was the challenge?)
           - 💡 SOLUTION: (What technologies/strategies did you use?)
           - 🚀 IMPACT: (What was the outcome/benefit?)
        2. Keep it professional, technical, and concise.
        3. Focus on the "Why" and "How".

        INPUT: "{request.text}"
        """

    # 4. DEFAULT/COVER LETTER
    else:
        prompt = f"""
        Act as a Professional Career Coach.
        TASK: Rewrite the following text to be more professional, persuasive, and clear for a '{request.role}'.
        Keep the original meaning but elevate the vocabulary and tone.
        
        INPUT: "{request.text}"
        """

    try:
        response = active_model.generate_content(prompt)
        return {"optimized": response.text}
    except Exception as e:
        print(f"❌ Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)