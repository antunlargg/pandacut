import os
import subprocess
import time
import re
import requests
from dotenv import load_dotenv
from google import genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_DIR = os.path.join(BASE_DIR, "media-inference-worker")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

FIXED_DESCRIPTION = "" # recommended description: #Shorts #KidsShorts #ToddlerLearning #CuteAnimation #3DAnimation #ShortsFeed #ViralKids #KidsVideos
HASHTAGS_FOR_TITLE = "" # recommended hashtags: #Shorts #KidsShorts #ToddlerLearning #CuteAnimation #3DAnimation #ShortsFeed #ViralKids #KidsVideos

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def generate_prompt_with_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            "" #recommended prompt: Generate a single creative, extremely cute, and engaging 3D animation prompt for toddlers and young children. It should feature cute animals, vibrant primary colors, fast-paced fun action, and a smooth motion or loop. Output ONLY the prompt text in English, optimized for an AI video generator. Include keywords like 'vibrant 3D cartoon style, vertical 9:16 aspect ratio'.
        ),
    )
    return response.text.strip().replace('"', '')

def authenticate_youtube():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return build("youtube", "v3", credentials=creds)

def run_pipeline():
    prompt = generate_prompt_with_gemini()
    print(f"[*] Prompt: {prompt}")
    
    os.chdir(WORKER_DIR)
    
    cmd_generate = f'python generate.py veo-3.1-fast "{prompt}"'
    result = subprocess.run(cmd_generate, shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    url_match = re.search(r'(https://[^\s]+\.mp4)', result.stdout)
    if not url_match:
        print("[!] URL not found.")
        return
    
    video_url = url_match.group(1)
    
    os.chdir(BASE_DIR)
    timestamp = int(time.time())
    temp_raw_filename = os.path.join(DOWNLOADS_DIR, f"raw_{timestamp}.mp4")
    
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(temp_raw_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("[!] Download error.")
        return

    output_file = os.path.join(DOWNLOADS_DIR, f"out_{timestamp}.mp4")
    ffmpeg_cmd = f'ffmpeg -i "{temp_raw_filename}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy "{output_file}"'
    subprocess.run(ffmpeg_cmd, shell=True)

    upload_to_youtube(output_file, prompt)

    try:
        os.remove(temp_raw_filename)
    except:
        pass

def upload_to_youtube(file_path, prompt_text):
    youtube = authenticate_youtube()
    
    full_title = f"/* {prompt_text} */ {HASHTAGS_FOR_TITLE}"[:100]

    body = {
        "snippet": {
            "title": full_title,
            "description": FIXED_DESCRIPTION,
            "tags": ["Shorts", "KidsShorts", "ToddlerLearning", "CuteAnimation", "3DAnimation"],
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": True
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[*] Upload: {int(status.progress() * 100)}%")

    print(f"[ok] Done! ID: {response.get('id')}")

if __name__ == "__main__":
    run_pipeline()