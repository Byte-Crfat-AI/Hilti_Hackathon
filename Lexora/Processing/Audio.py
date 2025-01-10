import torch
import librosa
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification


class Audio:
    def __init__(self):
        self.transcript_model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-small")
        self.transcript_processor = AutoProcessor.from_pretrained("openai/whisper-small")
        self.caption_model = AutoModelForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
        self.caption_extractor = AutoFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
        
    def Audio_transcript(self,path, chunk_length=30):
        audio, sampling_rate = librosa.load(path, sr=16000)
        chunk_size = chunk_length * sampling_rate
        audio_chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]
        transcriptions = []
        for chunk in audio_chunks:
            inputs = self.transcript_processor(chunk, sampling_rate=sampling_rate, return_tensors="pt")
            outputs = self.transcript_model.generate(**inputs)
            transcription = self.transcript_processor.decode(outputs[0], skip_special_tokens=True)
            transcriptions.append(transcription)
        full_transcription = " ".join(transcriptions)
        return full_transcription

    def Audio_captioning(self,path):
        audio, sampling_rate = librosa.load(path, sr=16000)
        inputs = self.caption_extractor(audio, sampling_rate=sampling_rate, return_tensors="pt")
        outputs = self.caption_model(**inputs)
        predicted_class_idx = torch.argmax(outputs.logits)
        predicted_class = self.caption_model.config.id2label[predicted_class_idx.item()]
        return predicted_class

    def process_audio(self,path):
        transcript = self.Audio_transcript(path)
        caption = self.Audio_captioning(path)
        return f'It is a {caption}. {transcript}'
# Example
#print(process_audio(r'D:/Hilti_Hackathon/Hilti_Hackathon/Target_Folder/Target_Folder/Additional_Files/Audio/Jfk_berlin_address_high.ogg.mp3'))