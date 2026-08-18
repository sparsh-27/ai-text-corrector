from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(
    title="Neural Correct API",
    description="AI-powered text spelling & grammar enhancement backend",
    version="1.0.0"
)

# Enable CORS for the frontend (configurable via environment variable)
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    original_text: str
    corrected_text: str
    model_used: str

# Global variable to hold the active corrector
classical_engine = None
modern_engine = None
active_model_name = ""

@app.on_event("startup")
def load_model():
    global classical_engine, modern_engine, active_model_name
    
    # Check environment variable first, then config.json to see which model won the evaluation
    best_model = os.getenv("BEST_MODEL")
    if not best_model:
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    best_model = config.get("best_model", "classical")
            except Exception:
                best_model = "classical"
        else:
            best_model = "classical"
            
    active_model_name = best_model
    print(f"Loading {best_model} model...")
    
    # Always load classical for spelling
    from classical_corrector import ClassicalCorrector
    classical_engine = ClassicalCorrector()

    if best_model == "modern":
        try:
            from modern_corrector import ModernCorrector
            modern_engine = ModernCorrector()
        except Exception as e:
            print(f"Error loading modern model: {e}. Falling back to classical model.")
            active_model_name = "classical"

@app.get("/")
def root():
    return {"message": "Neural Correct API is running", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "active_model": active_model_name if active_model_name else "initializing"
    }

@app.post("/api/correct", response_model=TextResponse)
def correct_text(request: TextRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    if len(request.text) > 2000:
        raise HTTPException(status_code=400, detail="Text length exceeds 2000 character limit.")

    if not classical_engine:
        raise HTTPException(status_code=500, detail="Correction model is not initialized.")
        
    if active_model_name == "modern" and modern_engine:
        # Hybrid Pipeline: Fix spelling first, then grammar
        spell_corrected = classical_engine.correct(request.text)
        final_corrected = modern_engine.correct(spell_corrected)
    else:
        final_corrected = classical_engine.correct(request.text)

    return TextResponse(
        original_text=request.text,
        corrected_text=final_corrected,
        model_used=active_model_name + " (Hybrid Pipeline)"
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
