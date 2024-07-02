from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests
import itertools

app = FastAPI()

NER_URLS = itertools.cycle([
    "https://56ea-203-190-154-106.ngrok-free.app/ner",
    "https://4369-34-139-136-4.ngrok-free.app/ner"
])
LDA_URL = "https://52db-203-190-154-106.ngrok-free.app/lda"

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <head>
            <title>Text Analysis</title>
        </head>
        <body>
            <h1>Text Analysis Form</h1>
            <form action="/analyze" method="post">
                <label for="text">Enter text:</label><br>
                <input type="text" id="text" name="text" required><br><br>
                <label for="analysis_type">Select analysis type:</label><br>
                <input type="radio" id="ner" name="analysis_type" value="ner" checked>
                <label for="ner">NER</label><br>
                <input type="radio" id="lda" name="analysis_type" value="lda">
                <label for="lda">LDA</label><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(text: str = Form(...), analysis_type: str = Form(...)):
    try:
        if analysis_type == "ner":
            ner_url = next(NER_URLS)
            response = requests.post(ner_url, data={'text': text})
        elif analysis_type == "lda":
            response = requests.post(LDA_URL, json={'text': text})
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        response.raise_for_status()
        analysis_response = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Service error: {e}")

    if analysis_type == "ner":
        entities = analysis_response.get('entities', [])
        result_html = "".join(f"<li>{ent[0]}: {ent[1]}</li>" for ent in entities)
        result_title = "Named Entities"
    else:
        topics = analysis_response.get('dominant_topic')
        result_html = topics
        result_title = "LDA Topics"

    return f"""
    <html>
        <head>
            <title>Analysis Result</title>
        </head>
        <body>
            <h1>Analysis Result</h1>
            <p>Text: {text}</p>
            <h2>{result_title}</h2>
            <ul>
                {result_html}
            </ul>
            <a href="/">Go back</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
