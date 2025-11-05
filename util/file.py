from pdf2image import convert_from_path
import os
import base64
import re

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
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError("PyMuPDF is required. Install it with: pip install PyMuPDF")
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
    result = []
    print("Converting PDF to text...")
    
    # Process each page
    for page_num, page in enumerate(doc):
        # Extract text blocks with their positions
        blocks = page.get_text("dict")["blocks"]
        page_data = {
            "page": page_num + 1,
            "blocks": []
        }
        
        # Process each block (usually paragraphs or text sections)
        for block in blocks:
            if block.get("type") == 0:  # Type 0 is text
                # Get the bounding box (x0, y0, x1, y1)
                bbox = block.get("bbox")
                
                # Process each line in the block
                for line in block.get("lines", []):
                    line_bbox = line.get("bbox")
                    line_text = ""
                    
                    # Concatenate all spans in the line
                    for span in line.get("spans", []):
                        line_text += span.get("text", "")
                    
                    if line_text.strip():  # Only add non-empty lines
                        page_data["blocks"].append({
                            "text": line_text,
                            "position": {
                                "x0": line_bbox[0],
                                "y0": line_bbox[1],
                                "x1": line_bbox[2],
                                "y1": line_bbox[3]
                            }
                        })
        
        result.append(page_data)
    
    # Save to file if output_dir is provided
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