import ollama

# Kiểm tra danh sách mô hình có sẵn (nếu có)
try:
    models = ollama.models()
    print(models)
except AttributeError as e:
    print("Error:", e)
