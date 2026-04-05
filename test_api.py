import requests
import argparse
import os
import platform
import subprocess

def test_api(image_path="pho.jpg", base_url="http://127.0.0.1:8000"):
    print(f"Using server URL: {base_url}\n")
    
    print("--- 1. Testing / ---")
    try:
        root_resp = requests.get(f"{base_url}/")
        print("Status:", root_resp.status_code)
        print(root_resp.json())
    except Exception as e:
        print(f"Lỗi kết nối server: {e}")
        return

    print("\n--- 2. Testing /health ---")
    try:
        health_resp = requests.get(f"{base_url}/health")
        print("Status:", health_resp.status_code)
        print(health_resp.json())
    except Exception as e:
        print(f"Lỗi: {e}")

    if not os.path.exists(image_path):
        print(f"\n[LỖI] Không tìm thấy ảnh tại: {image_path}. Vui lòng tạo/sử dụng một ảnh để test.")
        return

    print(f"\n--- Upload ảnh: {image_path} ---")
    with open(image_path, "rb") as f:
        file_content = f.read()

    # Determine type
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = 'image/jpeg'
    if ext == '.png': mime_type = 'image/png'
    elif ext == '.webp': mime_type = 'image/webp'
    
    filename = os.path.basename(image_path)

    print("\n--- 3. Testing /predict ---")
    try:
        predict_resp = requests.post(
            f"{base_url}/predict",
            files={'file': (filename, file_content, mime_type)}
        )
        print(f"Status: {predict_resp.status_code}")
        print(predict_resp.json())
    except Exception as e:
        print(f"Lỗi: {e}")

    print("\n--- 4. Testing /generate ---")
    try:
        generate_resp = requests.post(
            f"{base_url}/generate",
            files={'file': (filename, file_content, mime_type)}
        )
        print(f"Status: {generate_resp.status_code}")
        if generate_resp.status_code == 200:
            result = generate_resp.json()
            data = result.get('data', {})
            print(f"\nDescription: {data.get('food_description')}")
            print(f"Story: {str(data.get('story'))[:250]}...\n")
        else:
            print(generate_resp.text)
    except Exception as e:
        print(f"Lỗi: {e}")

    print("\n--- 5. Testing /audio ---")
    try:
        audio_resp = requests.get(f"{base_url}/audio")
        print(f"Status: {audio_resp.status_code}")
        if audio_resp.status_code == 200:
            output_file = "test_output.mp3"
            with open(output_file, "wb") as f:
                f.write(audio_resp.content)
            print(f"Lưu audio thành công tại {output_file}!")
            
            # Tự động phát audio
            print("Đang phát audio...")
            try:
                if platform.system() == "Windows":
                    os.startfile(output_file)
                elif platform.system() == "Darwin":
                    subprocess.call(["open", output_file])
                else:
                    subprocess.call(["xdg-open", output_file])
            except Exception as e:
                print(f"Không thể tự động phát audio: {e}")
        else:
            print(f"Lỗi: {audio_resp.status_code}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Food Story API")
    parser.add_argument("--image", type=str, default="pho.jpg", help="Đường dẫn đến file ảnh cần test")
    parser.add_argument("--url", type=str, default="http://127.0.0.1:8000", help="URL của server (Ví dụ: public URL từ pinggy hoặc localhost)")
    args = parser.parse_args()
    
    url = args.url.rstrip("/")
    test_api(args.image, url)
