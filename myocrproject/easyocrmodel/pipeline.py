import cv2, os
import matplotlib.pyplot as plt
import easyocr.easyocr
from django.conf import settings

def draw_bounding_boxes(image, detections, threshold=0.25):
    print("<<<<<<<<<<<<<<<<<<<<<Inside draw_bounding_boxes")

    for bbox, text, score in detections:
        if score > threshold:
            cv2.rectangle(image, 
                          (int(bbox[0][0]), int(bbox[0][1])), 
                          (int(bbox[2][0]), int(bbox[2][1])), 
                          (0, 255, 0), 
                          2)

    # Encode the image to PNG or JPEG before returning it
    # success, encoded_image = cv2.imencode('.jpg', image)
    # if not success:
    #     raise ValueError("Could not encode image")

    # # Convert to binary data
    # binary_image_data = encoded_image.tobytes()
    
    # return binary_image_data

    return image

def easy_process(file_path, language, output_dir):
    reader = easyocr.Reader([language])
    img = cv2.imread(file_path)

    if img is None:
        raise ValueError("Error loading the image. Please check the file path.")

    ocr_result = reader.readtext(img, detail=1)
    img_with_boxes = draw_bounding_boxes(img, ocr_result, threshold=0.25)

    # Construct the output filename
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    processed_filename = f"{base_filename}.jpg"
    processed_file_path = os.path.join(output_dir, processed_filename)

    # Save the processed image
    cv2.imwrite(processed_file_path, img_with_boxes)
    print(f"Processed image saved at {processed_file_path}")

    # Extract and return the texts
    extracted_texts = [text[1] for text in ocr_result if text[2] > 0.5]
    return processed_file_path, extracted_texts


    