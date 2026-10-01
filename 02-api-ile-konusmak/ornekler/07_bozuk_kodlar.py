# Alıştırma — Bozuk kodlar: beş parçayı sırayla düzelt, her seferinde çalıştır
# Çalıştır: uv run ornekler/07_bozuk_kodlar.py

yanit = {
    "result": {
        "response": "1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. 3) Burada odaklanırsın.",
        "usage": {"prompt_tokens": 24, "completion_tokens": 22, "total_tokens": 46},
    },
    "success": True,
    "errors": [],
}

hatali_yanit = {
    "result": None,
    "success": False,
    "errors": [{"code": 10000, "message": "Authentication error"}],
}

# 1) Modelin cevabını yazmalı
print(yanit["response"])

# 2) İlk hatanın mesajını yazmalı: Authentication error
print(hatali_yanit["errors"]["message"])

# 3) Toplam belirteci yazmalı: 46
print(yanit["result"]["total_tokens"])

# 4) "başarılı" yazmalı
if yanit["success"] == "true":
    print("başarılı")
else:
    print("başarısız")


# 5) Anahtar koda gömülü: anahtarı parametre yap, fonksiyonu baslik_yap("abc") diye çağır
def baslik_yap(anahtar="cf_gercek_anahtarim_12345"):
    return {"Authorization": f"Bearer {anahtar}"}


print(baslik_yap())
