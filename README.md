# 🍜 Food Story ITS — Image to Speech
Hệ thống nhận diện món ăn từ ảnh, tự động tạo nội dung tiếng Việt và đọc thành giọng nói.
## Lưu ý: Về Testing đã được gộp chung với source code để tiện cho chạy trên Google Colab
---

## 👤 Thông tin sinh viên

| Thông tin | Chi tiết |
|-----------|----------|
| **Họ và tên** | `Lê Tấn Dũng` |
| **MSSV** | `24120290` |
| **Lớp** | `24CTT05` |
| **Môn học** | `Tư duy tính toán` |

---

## 🤖 Mô hình sử dụng

| Mô hình | Mục đích | Liên kết |
|---------|----------|----------|
| **Moondream2** | Nhận diện hình ảnh (Image Captioning) | [vikhyatk/moondream2](https://huggingface.co/vikhyatk/moondream2) |
| **LLaMA 3.3 70B** | Sinh nội dung tiếng Việt (qua Groq API) | [meta-llama/Llama-3.3-70B-Versatile](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) |
| **Edge TTS** | Chuyển văn bản thành giọng nói tiếng Việt | [rany2/edge-tts](https://github.com/rany2/edge-tts) |

---

## 📝 Mô tả chức năng

Hệ thống hoạt động theo pipeline 4 bước:

```
📷 Upload ảnh món ăn
      ↓
🔍 Nhận diện món ăn (Moondream2)
      ↓
✍️ Tạo bài viết tiếng Việt về lịch sử, đặc điểm, cách thưởng thức (LLaMA 3.3 qua Groq)
      ↓
🔊 Chuyển thành giọng nói tiếng Việt (Edge TTS)
```

**Chức năng chính:**
- Nhận diện món ăn từ hình ảnh bất kỳ
- Tự động sinh nội dung tiếng Việt hấp dẫn về món ăn (lịch sử, đặc điểm, cách thưởng thức)
- Chuyển đổi nội dung thành file audio giọng nói tiếng Việt tự nhiên
- Cung cấp API để tích hợp với các ứng dụng khác


## 📁 Cấu trúc dự án

```
Model_Image_to_Speech/
├── [NOTEBOOK]_Food_Story_ITS.ipynb   # Notebook chính (API server + Testing)
├── requirements.txt                  # Danh sách thư viện cần cài
└── README.md                         # File hướng dẫn này
```

## 🎬 Video Demo

> 📹 **Link video demo:** [![Video Demo](https://img.youtube.com/vi/fcjItExAs68/maxresdefault.jpg)](https://youtu.be/fcjItExAs68)
> 📹 **Link video demo:** `https://youtu.be/fcjItExAs68`

---

## ⚙️ Hướng dẫn cài đặt thư viện

### Chạy trên Google Colab (Khuyến nghị)

Chạy các lệnh sau trong cell đầu tiên của notebook:

```python
# Thư viện chính
!pip install fastapi nest-asyncio accelerate scipy torch pillow -q
!pip install transformers==4.41.0 -q
!pip install uvicorn==0.29.0 -q

# Xử lý ảnh
!pip install pyvips -q
!apt-get install -y libvips -q

# Text-to-Speech
!pip install edge-tts -q

# LLM (Groq API)
!pip install groq -q
```

### Thiết lập API Keys

Chương trình cần 2 API key được lưu trong **Colab Secrets** (🔑 icon bên trái):

| Key | Mô tả | Lấy ở đâu |
|-----|--------|-----------|
| `HF_TOKEN` | Token Hugging Face để tải model Moondream2 | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `GROQ_API_KEY` | API key của Groq để dùng LLaMA | [console.groq.com/keys](https://console.groq.com/keys) |

---

## 🚀 Hướng dẫn chạy chương trình

### Bước 1: Mở notebook trên Google Colab

Mở file **`[NOTEBOOK]_Food_Story_ITS.ipynb`** trên Google Colab.

> 📎 **Link Colab backup:** [Mở trên Colab](https://colab.research.google.com/drive/11LX4KwDjQT2Swwcz8mF3jryk7XQYo21R?usp=sharing)

### Bước 2: Thiết lập Runtime

- Vào **Runtime → Change runtime type**
- Chọn **GPU: T4** (cần GPU để chạy Moondream2)

### Bước 3: Thêm API Keys

- Click icon 🔑 **Secrets** ở sidebar bên trái
- Thêm `HF_TOKEN` và `GROQ_API_KEY`

### Bước 4: Chạy tất cả các cell

- Vào **Runtime → Run all** hoặc nhấn `Ctrl + F9`
- Đợi server khởi động (khoảng 1-2 phút lần đầu do tải model)
- Khi thấy `Uvicorn running on http://0.0.0.0:8000` là đã sẵn sàng

### Bước 5: Test API

Phần test API đã được tích hợp sẵn trong notebook chính — cell cuối cùng **"Call Local API (Testing)"** sẽ tự động test tất cả các endpoint sau khi server khởi động.

---

## 📡 Hướng dẫn gọi API

Server chạy tại: `http://127.0.0.1:8000`

### 1. `GET /` — Thông tin hệ thống

```bash
curl http://127.0.0.1:8000/
```

**Response:**
```json
{
  "name": "Food Story API",
  "description": "Hệ thống API upload ảnh ẩm thực → nhận diện → tạo nội dung → đọc thành giọng nói",
  "endpoints": {
    "GET  /": "Giới thiệu hệ thống",
    "GET  /health": "Kiểm tra trạng thái",
    "POST /predict": "Nhận diện món ăn từ ảnh",
    "POST /generate": "Nhận diện + generate story + TTS",
    "GET  /audio": "Trả về file audio"
  }
}
```

---

### 2. `GET /health` — Kiểm tra trạng thái

```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "OK",
  "models": {
    "moondream": "loaded",
    "groq": "loaded",
    "tts": "loaded",
    "gpu": "Tesla T4 is ok"
  }
}
```

---

### 3. `POST /predict` — Nhận diện món ăn

Upload ảnh để nhận diện món ăn (chỉ trả về mô tả, không tạo story).

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "file=@pho.jpg"
```

**Ví dụ bằng Python:**
```python
import requests

url = "http://127.0.0.1:8000/predict"
files = {"file": ("pho.jpg", open("pho.jpg", "rb"), "image/jpeg")}
response = requests.post(url, files=files)
print(response.json())
```

**Response thành công (200):**
```json
{
  "food_description": "This is a bowl of beef pho soup."
}
```

**Response lỗi (400):**
```json
{
  "detail": {
    "success": false,
    "message": "Chỉ chấp nhận file ảnh: image/jpeg, image/png, image/webp. Nhận được: text/plain"
  }
}
```

---

### 4. `POST /generate` — Full Pipeline (Nhận diện + Story + TTS)

Upload ảnh để thực hiện toàn bộ pipeline: nhận diện → tạo story → tạo audio.

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -F "file=@pho.jpg"
```

**Ví dụ bằng Python:**
```python
import requests

url = "http://127.0.0.1:8000/generate"
files = {"file": ("pho.jpg", open("pho.jpg", "rb"), "image/jpeg")}
response = requests.post(url, files=files)
data = response.json()

print(f"Món ăn: {data['data']['food_description']}")
print(f"Story: {data['data']['story'][:200]}...")
print(f"Audio: {data['data']['audio_url']}")
```

**Response thành công (200):**
```json
{
  "success": true,
  "data": {
    "food_description": "This is a bowl of beef pho soup.",
    "story": "Phở bò - món ăn dân tộc của Việt Nam, là một trong những biểu tượng văn hóa ẩm thực nổi tiếng trên toàn thế giới...",
    "audio_url": "/audio"
  }
}
```

**Response lỗi (500):**
```json
{
  "detail": {
    "success": false,
    "message": "Lỗi nhận diện ảnh: CUDA out of memory"
  }
}
```

---

### 5. `GET /audio` — Tải file audio

Trả về file MP3 audio của story vừa được tạo bởi `/generate`.

```bash
curl http://127.0.0.1:8000/audio --output food_story.mp3
```

**Ví dụ bằng Python:**
```python
import requests

response = requests.get("http://127.0.0.1:8000/audio")
if response.status_code == 200:
    with open("food_story.mp3", "wb") as f:
        f.write(response.content)
    print("Đã lưu audio!")
```

**Response thành công:** File MP3 (audio/mpeg)

**Response lỗi (404):**
```json
{
  "detail": {
    "success": false,
    "message": "Chưa có file audio. Hãy gọi /generate trước."
  }
}
```

---

## 📋 Ràng buộc đầu vào

| Ràng buộc | Giá trị |
|-----------|---------|
| Định dạng ảnh | `image/jpeg`, `image/png`, `image/webp` |
| Kích thước tối đa | 10 MB |
| File rỗng | Không chấp nhận |

---

### Cấu trúc notebook chính

Notebook **`[NOTEBOOK]_Food_Story_ITS.ipynb`** được tổ chức theo các phần:

| # | Section | Mô tả |
|---|---------|--------|
| 1 | **Install Libraries** | Cài đặt các thư viện cần thiết |
| 2 | **Build class model (moondream2)** | Class nhận diện hình ảnh |
| 3 | **LLM Class** | Class sinh nội dung tiếng Việt (Groq API) |
| 4 | **Build class model (edge-tts)** | Class chuyển văn bản thành giọng nói |
| 5 | **Initialize API and Class Model** | Khởi tạo FastAPI app và các model |
| 6 | **API Endpoints** | Định nghĩa các endpoint (GET /, GET /health, POST /predict, POST /generate, GET /audio) |
| 7 | **Running in localhost** | Khởi chạy Uvicorn server |
| 8 | **Call Local API (Testing)** | Test tất cả các endpoint |

---


## 📎 Liên kết

- 🔗 **Google Colab:** [Mở notebook trên Colab](https://colab.research.google.com/drive/11LX4KwDjQT2Swwcz8mF3jryk7XQYo21R?usp=sharing)
- 🤗 **Moondream2:** [huggingface.co/vikhyatk/moondream2](https://huggingface.co/vikhyatk/moondream2)
- 🦙 **Groq Console:** [console.groq.com](https://console.groq.com)
- 🔊 **Edge TTS:** [github.com/rany2/edge-tts](https://github.com/rany2/edge-tts)
