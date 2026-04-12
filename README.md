# 🍜 Food Story ITS — Image to Speech
Hệ thống nhận diện món ăn từ ảnh, tự động tạo nội dung tiếng Việt và đọc thành giọng nói.
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

```text
Model_Image_to_Speech/
├── .env                              # File cấu hình chứa API Keys thực tế (người dùng tự tạo từ .env.example)
├── .env.example                      # File mẫu khai báo cấu trúc API Key
├── .gitignore                        # Chứa danh sách các file/thư mục ẩn không đưa lên Git
├── main.py                           # Mã nguồn chính chạy API Server (FastAPI)
├── test_api.py                       # Script gọi test tự động, gửi ảnh và phát âm thanh
├── [NOTEBOOK]_Food_Story_ITS.ipynb   # File Notebook chạy chính trên Google Colab
├── pho.jpg                           # File ảnh món ăn mẫu dùng để test nhanh
├── test_output.mp3                   # File âm thanh kết quả sinh ra sau khi chạy test_api.py
├── requirements.txt                  # Danh sách thư viện Python cần cài đặt
└── README.md                         # File tài liệu hướng dẫn này
```

## 🎬 Video Demo

> 📹 **Link video demo (6p):** `https://drive.google.com/drive/folders/1uhN9zN65hQXyfGDI2FNbmCv0yHuc9Yxj?usp=sharing`

> 📹 **Link video demo chi tiết (17p):** `https://youtu.be/fcjItExAs68`

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

Chương trình cần 2 API key để hoạt động:
- **Ngữ cảnh Google Colab:** Thêm key vào phần **Colab Secrets** (🔑 icon bên trái).
- **Ngữ cảnh Local (Máy tính cá nhân):** Tạo file `.env` (bạn có thể copy từ `.env.example`) và dán key vào.

| Key | Mô tả | Lấy ở đâu |
|-----|--------|-----------|
| `HF_TOKEN` | Token Hugging Face để tải model Moondream2 | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `GROQ_API_KEY` | API key của Groq để dùng LLaMA | [console.groq.com/keys](https://console.groq.com/keys) |

---

## 🚀 Hướng dẫn chạy chương trình

### ☁️ Cách 1: Chạy trên Google Colab (Khuyến nghị)

#### Bước 1: Mở notebook trên Google Colab

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

### 💻 Cách 2: Chạy trên Local (Máy cá nhân Windows/Mac)

#### Bước 1: Cài đặt và thiết lập môi trường
1. Cài đặt các thư viện từ file requirements (yêu cầu Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. *(Chỉ dành cho Windows)* Cần gỡ `pyvips` do lỗi thiếu thư viện C++: Mở Terminal gõ `pip uninstall -y pyvips` và xóa thủ công tên thư viện khỏi `requirements.txt` (Moondream2 sẽ tự động chuyển sang dùng Pillow thay thế một cách tối ưu).
3. Đổi tên file `.env.example` thành `.env` và điền 2 biến `HF_TOKEN` cùng `GROQ_API_KEY` vào trong file.

#### Bước 2: Khởi động Server
Mở Terminal (tại thư mục chứa code) và gõ lệnh sau để khởi động Server AI:
```bash
python main.py
```
> 🌐 **Tính năng Public (Pinggy):** Nếu bạn muốn công khai API ra ngoài Internet để test trên các thiết bị khác, hãy gõ thêm cờ `--share`: `python main.py --share`. Hệ thống sẽ tự cấp cho bạn một đường link public có dạng `https://xxx.pinggy.link`.

#### Bước 3: Chạy phần mềm Test tự động
Mở thêm một cửa sổ Terminal thứ 2 (để giữ Server vẫn chạy ở Terminal 1). Dùng script test tự động để AI phân tích ảnh `pho.jpg`, viết truyện ẩm thực và **tự động phát âm thanh** trên máy tính của bạn:
```bash
python test_api.py
```
*(Trường hợp bạn test bằng link Pinggy public, hãy truyền link qua tham số url: `python test_api.py --url https://xxx.pinggy.link`)*

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
