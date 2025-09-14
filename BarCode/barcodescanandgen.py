import cv2
import os
from PIL import Image
from pyzbar.pyzbar import decode
from ultralytics import YOLO
from glob import glob
import argparse
from barcode import Code128
from barcode.writer import ImageWriter

class DLBarcodeScanner:
    def __init__(self, model_path, save_folder="barcode_output"):
        """
        Initialize DL Barcode Scanner with YOLOv8 model.
        :param model_path: Path to YOLOv8 barcode detection weights (.pt)
        :param save_folder: Folder to save annotated images/videos
        """
        self.model = YOLO(model_path)
        os.makedirs(save_folder, exist_ok=True)
        self.save_folder = save_folder
        self.frame_count = 0

    @staticmethod
    def get_crops(image: Image.Image, results, expand_percent: float = 5):
        """
        Crop regions around detected bounding boxes with optional expansion.
        """
        crops = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                width = x2 - x1
                height = y2 - y1
                expand_x = int(width * (expand_percent / 100))
                expand_y = int(height * (expand_percent / 100))
                x1_expanded = max(x1 - expand_x, 0)
                y1_expanded = max(y1 - expand_y, 0)
                x2_expanded = x2 + expand_x
                y2_expanded = y2 + expand_y
                crop = image.crop((x1_expanded, y1_expanded, x2_expanded, y2_expanded))
                crops.append((crop, (x1_expanded, y1_expanded, x2_expanded, y2_expanded)))
        return crops

    @staticmethod
    def read_barcode(image: Image.Image):
        """
        Decode barcode from a PIL image.
        """
        decoded_objects = decode(image)
        if not decoded_objects:
            return None
        barcode_data = decoded_objects[0].data.decode("utf-8")
        barcode_type = decoded_objects[0].type
        return {"barcode": barcode_data, "barcode_type": barcode_type}

    def scan_frame(self, frame):
        """
        Scan a single frame using YOLOv8 + pyzbar.
        Draws rectangles and barcode text on the frame.
        """
        results = self.model.predict(source=frame, conf=0.15, save=False, verbose=False)
        decoded_any = False

        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        crops = self.get_crops(pil_frame, results)

        for crop, (x1, y1, x2, y2) in crops:
            result = self.read_barcode(crop)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            if result:
                decoded_any = True
                data = result["barcode"]
                print(f"Frame {self.frame_count}: Barcode -> {data}")
                cv2.putText(frame, data, (x1, max(y1-10,10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return frame, decoded_any

    def run_video(self, video_source=0, output_video="output.avi"):
        """
        Run live webcam or video file barcode scanner.
        """
        cap = cv2.VideoCapture(video_source)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(os.path.join(self.save_folder, output_video), fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            annotated_frame, _ = self.scan_frame(frame)
            out.write(annotated_frame)
            cv2.imshow("DL Barcode Scanner", annotated_frame)
            self.frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"Video saved to {os.path.join(self.save_folder, output_video)}")

    def process_images_folder(self, images_folder="images"):
        """
        Scan all images in a folder.
        """
        image_paths = glob(os.path.join(images_folder, "*.*"))
        if not image_paths:
            print("No images found!")
            return

        for img_path in image_paths:
            frame = cv2.imread(img_path)
            annotated_frame, _ = self.scan_frame(frame)
            save_path = os.path.join(self.save_folder, f"img_{os.path.basename(img_path)}")
            cv2.imwrite(save_path, annotated_frame)
            print(f"Saved annotated image: {save_path}")

    @staticmethod
    def generate_barcode(data, save_folder="barcode_output", filename=None):
        """
        Generate a barcode image (Code128) from a string.
        """
        os.makedirs(save_folder, exist_ok=True)
        if filename is None:
            safe_data = "".join(c for c in data if c.isalnum())[:10]
            filename = f"barcode_{safe_data}.png"
        path = os.path.join(save_folder, filename)
        barcode = Code128(data, writer=ImageWriter(), add_checksum=False)
        barcode.save(path)
        print(f"Barcode generated at: {path}")
        return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BARcode Scanner CLI")
    parser.add_argument("--generate", type=str, help="Generate Barcode from string")
    parser.add_argument("--video", type=str, default=None, help="Path to video file or leave empty for webcam")
    parser.add_argument("--images", type=str, help="Path to folder with images to scan")
    parser.add_argument("--save", type=str, default="barcode_results", help="Folder to save outputs")
    parser.add_argument("--model", type=str, required=True, help="Path to YOLOv8 trained barcode model (.pt)")
    args = parser.parse_args()

    scanner = DLBarcodeScanner(model_path=args.model, save_folder=args.save)

    if args.generate:
        DLBarcodeScanner.generate_barcode(args.generate, save_folder=args.save)

    if args.video is not None:
        source = 0 if args.video == "" else args.video
        scanner.run_video(video_source=source)

    if args.images:
        scanner.process_images_folder(images_folder=args.images)
