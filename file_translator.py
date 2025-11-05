from model import gemini_prompt
from util import convert_pdf_to_images, convert_pdf_to_text, get_latex_from_response_text, convert_latex_to_pdf
from pathlib import Path
import os

if __name__ == "__main__":
    # Input file path
    file_path = "Auto+New+ID+Card - 2025-11-03T163558.949.pdf"
    path = Path(file_path)
    stem = path.stem
    
    # Create output directory paths
    img_path = Path("img") / stem
    text_path = Path("text") / stem
    latex_path = Path("latex") / stem
    output_pdf_path = Path("translated_pdf") / stem
    
    # Create output file paths - use the existing file name pattern
    latex_file_path = latex_path / f"{stem}.tex"
    output_pdf_file_path = output_pdf_path / f"{stem}_translated.pdf"
    
    # Create directories
    os.makedirs(img_path, exist_ok=True)
    os.makedirs(text_path, exist_ok=True)
    os.makedirs(latex_path, exist_ok=True)
    os.makedirs(output_pdf_path, exist_ok=True)

    # Process PDF
    convert_pdf_to_images(file_path, img_path)
    prompt = convert_pdf_to_text(file_path, text_path)

    # Generate LaTeX from Gemini
    gemini_result = gemini_prompt(str(prompt), img_path)
    latex = get_latex_from_response_text(gemini_result)
    
    # Save LaTeX file
    with open(latex_file_path, "w", encoding="utf-8") as f:
        f.write(latex)
    
    # Convert LaTeX to PDF
    convert_latex_to_pdf(latex_file_path, output_pdf_file_path)