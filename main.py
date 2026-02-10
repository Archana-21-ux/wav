from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
import os
import uuid

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube to WAV</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #1e293b;
            padding: 25px;
            border-radius: 15px;
            width: 90%;
            max-width: 420px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        input {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            background: #22c55e;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        button:disabled {
            background: gray;
            cursor: not-allowed;
        }
        iframe {
            margin-top: 15px;
            width: 100%;
            height: 220px;
            border-radius: 10px;
            border: none;
        }
        #status {
            margin-top: 10px;
            font-size: 14px;
            color: #a5f3fc;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>YouTube → WAV</h2>
        <form id="form" action="/convert" method="post">
            <input id="url" type="text" name="url" placeholder="Paste YouTube link" oninput="showPreview()">
            <button id="btn" type="submit">Convert</button>
            <div id="status"></div>
        </form>
        <iframe id="preview" style="display:none;"></iframe>
    </div>

<script>
function extractVideoID(url) {
    let regExp = /(?:youtube\\.com.*(?:\\?|&)v=|youtu\\.be\\/)([^&]+)/;
    let match = url.match(regExp);
    return match ? match[1] : null;
}

function showPreview() {
    let url = document.getElementById("url").value;
    let videoID = extractVideoID(url);
    let iframe = document.getElementById("preview");

    if (videoID) {
        iframe.src = "https://www.youtube.com/embed/" + videoID;
        iframe.style.display = "block";
    } else {
        iframe.style.display = "none";
    }
}

document.getElementById("form").addEventListener("submit", function() {
    document.getElementById("btn").disabled = true;
    document.getElementById("btn").innerText = "Processing...";
    document.getElementById("status").innerText = "Downloading and converting audio...";
});
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/convert")
def convert(url: str = Form(...)):
    filename = str(uuid.uuid4())
    command = f"yt-dlp -f bestaudio --extract-audio --audio-format wav -o '{filename}.%(ext)s' {url}"
    os.system(command)

    wav_file = filename + ".wav"
    return FileResponse(wav_file, media_type="audio/wav", filename="audio.wav")

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

