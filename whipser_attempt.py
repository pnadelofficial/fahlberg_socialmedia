import whisper

model = whisper.load_model("base")
result = model.transcribe("output.aac")
print(result["text"])