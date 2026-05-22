# VoiceWave Studio 🎬🎧

VoiceWave Studio is a full-stack AI-powered video audio enhancement platform that enables users to upload videos, remove background noise, apply professional audio effects, edit specific video segments, and embed custom subtitles directly into videos.

---

# 🚀 Features

* 🎧 AI-Based Noise Reduction
* 🔊 Bass Boost & Audio Enhancement
* 🌊 Multiple Echo & Reverb Effects
* ✂️ Segment-Based Audio Processing
* 🎬 Video Audio Extraction & Merging
* 📝 Custom Subtitle Embedding
* 📊 Real-Time Waveform & Timeline Editing
* ⬇️ Download Processed Videos
* ⚡ High-Speed FFmpeg Processing Pipeline

---

# 🛠️ Tech Stack

## Frontend

* React.js
* React Bootstrap
* Axios
* React Dropzone
* React Icons

## Backend

* Flask
* Python
* FFmpeg
* DeepFilterNet
* REST APIs

---



# ⚙️ Core Functionalities

## 🎧 Audio Processing

* Background noise cancellation using FFmpeg filters
* AI-powered noise reduction support with DeepFilterNet
* Loudness normalization and dynamic compression
* Equalization and bass enhancement

## 🌊 Echo & Reverb Effects

* Analog Delay
* Basic Delay
* Standard Echo
* Flutter Echo
* Reverberation

## ✂️ Segment-Based Editing

* Process selected video segments independently
* Timeline-based editing workflow
* Extract and preview audio clips

## 📝 Subtitle System

* Add custom subtitles to videos
* Generate SRT subtitle files
* Burn subtitles directly into video using FFmpeg

## 🎬 Media Processing Pipeline

* Audio extraction from uploaded videos
* Real-time audio transformation
* Audio-video synchronization and merging
* Export final processed video

---

# 🔗 API Endpoints

## Upload Video

```http
POST /video/upload
```

## Process Video

```http
GET /video/process
```

## Extract Audio Clip

```http
GET /video/cut-audio
```

## Compile Edited Segments

```http
POST /video/compile
```

## Add Subtitles

```http
POST /video/subtitled
```

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/Talhadeveloperr/Voice-Wave-Studio.git
cd video-voice-setup
```

---

# 🔧 Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Flask Server

```bash
python run.py
```

---

# 💻 Frontend Setup

```bash
cd frontend/voice
npm install
npm start
```

---

# 🎥 Supported Video Formats

* MP4
* MOV
* AVI
* MKV
* WEBM

---

# 📸 Main Features Preview

* Upload Videos
* Apply Audio Filters
* Remove Background Noise
* Edit Specific Segments
* Add Subtitles
* Download Processed Videos

---

# 🧠 Audio Processing Techniques Used

* Spectral Noise Reduction
* Dynamic Audio Gating
* Loudness Normalization
* Audio Compression
* Frequency Equalization
* Multi-Layer Echo Processing

---

# 🔥 Future Enhancements

* Real-Time AI Subtitle Generation
* Voice Cloning
* Speech-to-Text Integration
* GPU-Based Video Rendering
* Multi-Language Subtitle Support

---

# 👨‍💻 Author

**Talha Khalid**


---


