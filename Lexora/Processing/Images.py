from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText
from io import BytesIO

#Image Captioning using Salesforce's Blip Image Captioning model
def process_image(path):
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")
    image = Image.open(path)
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def process_image_bytes(image_bytes):
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")
    image = Image.open(BytesIO(image_bytes))
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption
#Example
#print(process_image('D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder\Additional_Files\Images\pexels-ibertola-2681319.jpg'))