from PIL import Image as PILImage
from transformers import BlipProcessor, BlipForConditionalGeneration
from io import BytesIO

class Image:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # Image Captioning using Salesforce's BLIP Image Captioning model
    def process_image(self, path):
        image = PILImage.open(path)
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        return caption

    def process_image_bytes(self, image_bytes):
        image = PILImage.open(BytesIO(image_bytes))
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        return caption
