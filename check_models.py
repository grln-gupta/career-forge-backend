import google.generativeai as genai

# --- PASTE YOUR API KEY BELOW ---
API_KEY = "AIzaSyB01fXdhW3Fwc_zKsVA_LzghWI5CeTcjuw"

genai.configure(api_key=API_KEY)

print("--- CHECKING AVAILABLE MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE: {m.name}")
except Exception as e:
    print(f"ERROR: {e}")
print("--- END OF LIST ---")