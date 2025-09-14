# QR & Barcode Scanner & Generator

A Python tool to **scan QR codes and barcodes** from video or images, and **generate QR codes and barcodes** from text.  

This repository contains two modules:

1. **QR_Code** → For QR code generation and scanning  
2. **BarCode** → For Barcode (Code128) generation and scanning  

---

## Features

### QR Codes
- Scan QR codes from **webcam** or **video files**.  
- Scan QR codes from **all images in a folder**.  
- Generate QR codes from any **string**.  
- Save annotated images and videos automatically.  

### Barcodes
- Scan barcodes from **webcam** or **video files**.  
- Scan barcodes from **all images in a folder**.  
- Generate **Code128 barcodes** from any string.  
- Save annotated images and videos automatically.  

---

## Demo Images

<table>
<tr>
<td align="center">
<b>QR Code Generation</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/QR_Code/images/p1.png" width="400" height="400" />
</td>
<td align="center">
<b>QR Code Scanning</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/QR_Code/images/p2.jpg" width="400" height="400" />
</td>
</tr>
<tr>
<td align="center">
<b>Barcode Generation</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/BarCode/images/p1.png" width="400" height="400" />
</td>
<td align="center">
<b>Barcode Scanning</b><br>
<img src="https://github.com/Gaurav14cs17/QRCode_BARCode_Gen-Scanner/blob/main/BarCode/images/p1.png" width="400" height="400" />
</td>
</tr>
</table>

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/QRCode_BARCode_Gen-Scanner.git
cd QRCode_BARCode_Gen-Scanner
````

Install dependencies:

```bash
# For QR Code
pip install opencv-python qreader segno

# For Barcode
pip install opencv-python pyzbar pillow ultralytics python-barcode
```

---

## Usage

### QR Code

#### Generate QR code from string

```bash
python QR_Code/qr_scanner.py --generate "https://example.com"
```

#### Scan video (webcam or file)

```bash
# Webcam
python QR_Code/qr_scanner.py --video ""
# Video file
python QR_Code/qr_scanner.py --video "video.mp4"
```

#### Scan all images in a folder

```bash
python QR_Code/qr_scanner.py --images "images_folder"
```

---

### Barcode

#### Generate barcode from string

```bash
python BarCode/barcode_scanner.py --generate "123456789012"
```

#### Scan video (webcam or file)

```bash
# Webcam
python BarCode/barcode_scanner.py --video ""
# Video file
python BarCode/barcode_scanner.py --video "video.mp4"
```

#### Scan all images in a folder

```bash
python BarCode/barcode_scanner.py --images "images_folder"
```

---

### Combine commands

```bash
# QR code example
python QR_Code/qr_scanner.py --generate "Hello" --video "" --images "images_folder"

# Barcode example
python BarCode/barcode_scanner.py --generate "123456789012" --video "" --images "images_folder"
```

---

## Output

All annotated images, frames, and videos are saved in the respective folders:

* `QR_Code/qr_results/`
* `BarCode/barcode_results/`

---


