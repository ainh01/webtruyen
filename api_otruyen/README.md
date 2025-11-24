# FastAPI Controller


## 1. Clone repository

```bash
git clone https://github.com/JONNYDAN/API_OTruyen.git
cd API_OTruyen
```

## 2. Tạo môi trường ảo

Trên Windows
```bash
python -m venv venv
venv\Scripts\activate
```

Trên macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 4. Chạy ứng dụng
```bash
uvicorn main:app --reload --port 8001
```