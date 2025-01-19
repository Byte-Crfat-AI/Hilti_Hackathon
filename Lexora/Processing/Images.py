from PIL import Image as PILImage
from transformers import AutoProcessor, AutoModelForImageTextToText
from io import BytesIO

class Image:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")
    #Image Captioning using Salesforce's Blip Image Captioning model
    def process_image(self,path):
        image = PILImage.open(path)
        inputs = self.processor(image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        return caption

    def process_image_bytes(self,image_bytes):
        image = PILImage.open(BytesIO(image_bytes))
        inputs = self.processor(image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        return caption
#Example
#print(process_image('D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder\Additional_Files\Images\pexels-ibertola-2681319.jpg'))