import moviepy.editor as mp
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings

IBM_API_KEY = settings.IBM_API_KEY
IBM_URL = settings.IBM_URL

class AnalyzeVideo:
    '''
    Class for analyzing a video from the following factors:
    * Eye Gazing
    * Audio Confidence
    '''

    def __init__(self, videoLocation):
        self.videoLocation = videoLocation
        self.audioLocation = None
        self.confidence = 0
        self.transcript = ""

    def get_audio(self):
        '''
        For generating audio from the video in wav format
        '''
        # Keeping the audio file name same as the video file, 
        # just changing the externsion to wav
        audioLocation = self.videoLocation[0:self.videoLocation.rindex(".")]+".wav"
        video_clip = mp.VideoFileClip(self.videoLocation)
        video_clip.audio.write_audiofile(audioLocation)
        self.audioLocation = audioLocation
    
    def analyze_audio(self):
        '''
        For getting the confidence and transcript from the audio
        '''
        with open(self.audioLocation, 'rb') as audio_file:
            data = audio_file.read()

        try:
            # Setup Service
            authenticator = IAMAuthenticator(IBM_API_KEY)
            stt = SpeechToTextV1(authenticator=authenticator)
            stt.set_service_url(IBM_URL)
            
            # Perform conversion
            res = stt.recognize(audio=data, content_type='audio/wav', model='en-IN_Telephony', continuous=True).get_result()
            self.confidence = int((res['results'][0]['alternatives'][0]['confidence'])*100)
            self.transcript = res['results'][0]['alternatives'][0]['transcript']

        except Exception as e:
            pass
