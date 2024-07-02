from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import spacy
import time

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

@app.post("/ner", response_class=JSONResponse)
async def analyze_ner(text: str = Form(...)):
    # Simulate a delay of 1 minute
    time.sleep(10)
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {"entities": entities}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)