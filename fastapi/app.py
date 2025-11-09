from fastapi import FastAPI, UploadFile, File
from speechbrain.inference.interfaces import foreign_class
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import shutil

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = FastAPI(title="Speech Processing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# ✅ 模型初始化（加载一次）
# ------------------------------
print("🔹 Loading SpeechBrain Emotion Recognition model...")
emotion_classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier",
)
print("✅ SpeechBrain model loaded.")

print("🔹 Loading Whisper ASR model...")
whisper_model = whisper.load_model("base")  # 可选 tiny / base / small / medium / large
print("✅ Whisper model loaded.")


# ------------------------------
# 🎙️ Whisper 语音转文字接口
# ------------------------------
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """上传音频文件，返回转录文本"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    result = whisper_model.transcribe(tmp_path)
    return {
        "text": result.get("text", "")
    }


# ------------------------------
# 😃 SpeechBrain 情绪识别接口
# ------------------------------
@app.post("/emotion")
async def analyze_emotion(file: UploadFile = File(...)):
    """上传音频文件，返回情绪分类结果"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    out_prob, score, index, text_lab = emotion_classifier.classify_file(tmp_path)

    return {
        "emotion": text_lab,
        # "score": float(score),
        "index": int(index),
        "probabilities": out_prob.tolist(),
    }