
# Barcode Scanner & Generator

A simple Python tool to **scan barcodes from video or images** and **generate barcodes from text**.  

---

## Features

- Scan barcodes from **webcam** or **video files**.  
- Scan barcodes from **all images in a folder**.  
- Generate **Code128 barcodes** from any string.  
- Save annotated images and videos automatically.  

---

## Demo Images

<table>
<tr>
<td align="center">
<b>Barcode Generation</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/QR_Code/images/p1.png" width="500" height="500" />
</td>
<td align="center">
<b>Barcode Scanning</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/QR_Code/images/p2.jpg" width="500" height="500" />
</td>
</tr>
</table>

---

## Installation

```bash
git clone https://github.com/yourusername/barcode-scanner.git
cd barcode-scanner
pip install opencv-python pyzbar pillow ultralytics python-barcode
````

---

## Usage

### Generate barcode from string

```bash
python barcode_scanner.py --generate "123456789012"
```

### Scan video (webcam or file)

```bash
# Webcam
python barcode_scanner.py --video ""
# Video file
python barcode_scanner.py --video "video.mp4"
```

### Scan all images in a folder

```bash
python barcode_scanner.py --images "images_folder"
```

### Combine commands

```bash
python barcode_scanner.py --generate "123456789012" --video "" --images "images_folder"
```

---

## Output

All annotated images, frames, and videos are saved in the folder `barcode_results/` (default).

---
