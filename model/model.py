from google import genai

from util import load_images_from_directory,encode_image_to_base64
# These variables are imported from __init__.py
from . import gemini_api_key, system_prompt




def gemini_prompt(content, img_dir,model="gemini-2.5-pro"):
    client = genai.Client(api_key=gemini_api_key)

    # Create a list for content parts
    contents = []
    
    # Add text prompt if provided
    if content:
        contents.append(content)
    
    # Add images from the directory
    image_paths = load_images_from_directory(img_dir)
    for img_path in image_paths:
        contents.append({
                "inline_data": {
                    "mime_type": "image/jpeg", 
                    "data": encode_image_to_base64(img_path)
                }
            })
    
    # Generate content with the properly formatted prompt
    from google.genai import types
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
    )
    return response.text

