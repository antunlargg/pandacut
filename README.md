<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/antunlargg/pandacut/refs/heads/main/repo/pandacut-logo-Photoroom.png" alt="PandaCut" width="230">
  <br>
  PandaCut
  <br>
</h1>

<h4 align="center">Simple automated pipeline to generate, format, and upload YouTube Shorts using Gemini and Veo.</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#setup">Setup</a> •
  <a href="#first-start">First start</a> •
</p>

## Features

* **AI Prompt Generation** - Automatically creates cute 3D animation prompts using Google Gemini (`gemini-3.5-flash-lite`).
* **Auto Formatting** - Resizes and pads videos to vertical 9:16 format (`1080:1920`) via FFmpeg.
* **Direct YouTube Upload** - Handles OAuth2 authentication and uploads videos instantly with kids-friendly settings (`MadeForKids`).
* **Clean Storage** - Automatically saves raw and final videos inside a dedicated `downloads/` folder.

## Project Structure

```text
pandacut/
├── pandacut.py
├── loop.py
├── client_secret.json
├── token.json
├── .env
├── downloads/
└── media-inference-worker/
```
## Dependencies
* **Python (at least 3.13)**
* **FFmpeg**
* **Git**
* **Node.js**
* **
## Setup

```bash
# Clone this repository
$ git clone https://github.com/antunlargg/pandacut.git

# Go into the repository
$ cd pandacut

# Clone media-inference-worker
$ git clone https://github.com/framepipe-dev/media-inference-worker.git

# Paste your Gemini API key (aistudio.google.com/api-keys)
$ echo GEMINI_API_KEY=(your_api_key) > .env
# or just open it in your IDE

# Install requirements
$ pip install -r requirements.txt
```
**Now head to console.google.com:**
* Create new project, name doesn't matter, same as ID,
* Press "**.**" and click on **APIs and services**
* Now press **Enable APIs and services** and search for **Youtube Data API v3**
* Press it, and at the next screen choose **Enable API**
* Then on the left, click on **OAuth Consent Screen**
* Under Metrics, press **Create OAuth client** and as application type choose **Desktop app**, name doesn't matter
* Hit **Create** and scroll down and press **Download JSON**
* After downloading it, rename it to **client_secret.json** and move to PandaCut directory
* Now hit **Audience** and scroll down, until you see **Test users**, hit **Add users** and enter your Gmail, where you have YouTube channel set up.
* Hit **Save** and you're done!

## First start
* For the first time, run:
```bash
$ python3 pandacut.py
```
* When the video is generated, you will be prompted in browser to authenticate, choose account, which you flagged as **Test user**, and ignore all warnings about **"Google didn't check this app"** etc.
* After this, you can run **loop.py**, which essentially just loops **pandacut.py** as many times as you need. Note: this loop ends, when error appears.
