import cv2
import yt_dlp
import pytesseract
import subprocess
import numpy as np

# YouTubeアーカイブ動画のURL
youtube_url = 'https://www.youtube.com/live/yB0rd8Cqqsk?si=JgQlFnvolxs7F4vb'

# yt-dlpを使って動画の実際のURLを取得
def get_video_url(youtube_url):
    ydl_opts = {
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict['url']

video_url = get_video_url(youtube_url)
if not video_url:
    print("Error: Could not extract video URL.")
    exit()

# OpenCVで動画をキャプチャ
cap = cv2.VideoCapture(video_url)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# フレームレートを取得
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
# OCRを実行するためのフレーム間隔を設定（例：1秒ごと）
interval = frame_rate

texts = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # フレームをグレースケールに変換
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # pytesseractを使用してOCRを実行
    text = pytesseract.image_to_string(gray_frame, lang='jpn')
    texts.append(text)
    
    # 次のフレームに移動（1秒ごとに処理）
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + interval)
    
    # 途中経過を表示（任意）
    print(text)

cap.release()

# 抽出した文字列を結合
extracted_text = "\n".join(texts)
print(extracted_text)
