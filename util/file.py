from pdf2image import convert_from_path
import os
import base64
import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

def convert_pdf_to_images(pdf_path, output_dir):
    # Optional: Specify the output directory for images
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert PDF to a list of images
    # dpi parameter controls the resolution (e.g., 200 is a good default)
    images = convert_from_path(pdf_path, dpi=200)
    print("Converting PDF to images...")
    # Save each image with a unique name
    for i, image in enumerate(images):
        output_file = os.path.join(output_dir, f"page_{i+1}.png")
        image.save(output_file, "PNG")
        print(f"Saved {output_file}")

    return output_dir

def convert_pdf_to_text(pdf_path, output_dir=None):
    """
    Convert a PDF file to text with position information.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str, optional): Directory to save the text output. If None, no file is saved.
        
    Returns:
        list: List of dictionaries containing page number, text blocks with their positions and content
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    result = []
    print("Converting PDF to text...")
    laparams = LAParams(
        char_margin=2.0,
        word_margin=0.1,
        line_margin=0.3,
        detect_vertical=True,
    )
    
    for page_num, layout in enumerate(extract_pages(pdf_path, laparams=laparams), start=1):
        page_data = {
            "page": page_num,
            "blocks": []
        }
        for element in layout:
            if isinstance(element, LTTextBox):
                for line in element:
                    if isinstance(line, LTTextLine):
                        text = line.get_text().strip()
                        if not text:
                            continue
                        x0, y0, x1, y1 = line.bbox
                        page_data["blocks"].append({
                            "text": text,
                            "position": {"x0": x0, "y0": y0, "x1": x1, "y1": y1}
                        })
        result.append(page_data)
    
    if output_dir:
        import json
        output_file = os.path.join(output_dir, "txt.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved text with positions to {output_file}")
    
    return result

def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def load_images_from_directory(directory):
    """
    Load all images from a directory
    Returns a list of image paths
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    image_paths = []
    
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_paths.append(os.path.join(directory, file))
    
    return sorted(image_paths)

def get_latex_from_response_text(response):

    # Try to extract content between ```latex and ``` markers
    latex_pattern = r"```latex([\s\S]*?)```"
    match = re.search(latex_pattern, response)
    
    if match:
        # Return the content inside the backticks
        return match.group(1)
    
    # If no triple backticks found at all, return the original text
    return response