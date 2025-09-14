# QR Scanner & Generator

A simple Python tool to **scan QR codes from video or images** and **generate QR codes from text**.  

---

## Features

- Scan QR codes from **webcam** or **video files**.  
- Scan QR codes from **all images in a folder**.  
- Generate QR codes from any **string**.  
- Save annotated images and videos automatically.  

---

## Installation

```bash
git clone https://github.com/yourusername/qr-scanner.git
cd qr-scanner
pip install opencv-python qreader segno
````

---

## Usage

### Generate QR code from string

```bash
python qr_scanner.py --generate "https://example.com"
```

### Scan video (webcam or file)

```bash
# Webcam
python qr_scanner.py --video ""
# Video file
python qr_scanner.py --video "video.mp4"
```

### Scan all images in a folder

```bash
python qr_scanner.py --images "images_folder"
```

### Combine commands

```bash
python qr_scanner.py --generate "Hello" --video "" --images "images_folder"
```

---

## Output

All annotated images, frames, and videos are saved in the folder `qr_results/` (default).

---

## License

MIT License

```

