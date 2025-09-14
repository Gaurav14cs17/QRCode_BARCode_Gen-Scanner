import cv2
import os
from glob import glob
from qreader import QReader
import segno
import argparse


class QRScanner:
    def __init__(self, save_folder="qr_output"):
        self.qreader = QReader()
        self.save_folder = save_folder
        os.makedirs(save_folder, exist_ok=True)
        self.frame_count = 0

    def scan_and_annotate(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        decoded_qrs = self.qreader.detect_and_decode(rgb_frame, return_detections=True)
        decoded_texts, detections = decoded_qrs

        qr_found = False
        for det, text in zip(detections, decoded_texts):
            if text is None:
                continue
            qr_found = True
            bbox = det['bbox_xyxy'].astype(int)
            x1, y1, x2, y2 = bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            print(f"Frame {self.frame_count}: QR Code Detected -> {text}")
        return frame, qr_found

    def process_video(self, video_source=0, output_video="output.avi"):
        cap = cv2.VideoCapture(video_source)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(os.path.join(self.save_folder, output_video), fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                print("No more frames. Exiting...")
                break

            annotated_frame, qr_found = self.scan_and_annotate(frame)

            if qr_found:
                frame_filename = os.path.join(self.save_folder, f"video_frame_{self.frame_count:04d}.jpg")
                cv2.imwrite(frame_filename, annotated_frame)

            out.write(annotated_frame)
            cv2.imshow("QR Video Scanner", annotated_frame)
            self.frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"Video saved in '{self.save_folder}' as '{output_video}'")

    def process_images_folder(self, images_folder="images"):
        image_paths = glob(os.path.join(images_folder, "*.*"))
        if not image_paths:
            print(f"No images found in folder '{images_folder}'")
            return

        for img_path in image_paths:
            frame = cv2.imread(img_path)
            annotated_frame, _ = self.scan_and_annotate(frame)
            save_path = os.path.join(self.save_folder, f"img_{os.path.basename(img_path)}")
            cv2.imwrite(save_path, annotated_frame)
            print(f"Saved annotated image: {save_path}")
            self.frame_count += 1

    def generate_qr_code(self, data, filename=None, scale=10):
        if filename is None:
            safe_data = "".join(c for c in data if c.isalnum())[:10]
            filename = f"qr_{safe_data}.png"
        save_path = os.path.join(self.save_folder, filename)
        qr = segno.make(data)
        qr.save(save_path, scale=scale)
        print(f"QR code generated and saved at: {save_path}")
        return save_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QR Scanner CLI")
    parser.add_argument("--generate", type=str, help="Generate QR code from string")
    parser.add_argument("--video", type=str, default=None, help="Path to video file or leave empty for webcam")
    parser.add_argument("--images", type=str, help="Path to folder with images to scan")
    parser.add_argument("--save", type=str, default="qr_results", help="Folder to save outputs")
    args = parser.parse_args()

    scanner = QRScanner(save_folder=args.save)

    if args.generate:
        scanner.generate_qr_code(args.generate)

    if args.video is not None:
        source = 0 if args.video == "" else args.video
        scanner.process_video(video_source=source)

    if args.images:
        scanner.process_images_folder(images_folder=args.images)
