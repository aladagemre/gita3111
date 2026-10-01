# Isınma — İç içe sözlükten değer çek (iki satırı da düzelt)
# Çalıştır: uv run ornekler/00_isinma.py

yanit = {
    "success": True,
    "result": {
        "response": "Merhaba!",
        "usage": {"prompt_tokens": 4, "completion_tokens": 2},
    },
    "errors": [],
}

hatali_yanit = {
    "success": False,
    "result": None,
    "errors": [{"code": 10000, "message": "Authentication error"}],
}

# Tamir 1: Merhaba! yazmalı
print(yanit["response"])

# Tamir 2: Authentication error yazmalı
print(hatali_yanit["errors"]["message"])
