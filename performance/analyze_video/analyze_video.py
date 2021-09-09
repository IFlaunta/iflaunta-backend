from math import ceil
import moviepy.editor as mp
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings
import cv2
from .gaze_tracking import GazeTracking

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
        self.video_score = 0

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

    def analyze_video(self):
        # Capturing the video from videofile
        cap = cv2.VideoCapture(self.videoLocation)

        # Keeping the frame size 640*480
        # http://opencvinpython.blogspot.com/2014/09/capture-video-from-camera.html
        cap.set(3, 640)     # Width of the frame in the captured video
        cap.set(4, 480)     # Height of the frame in the captured video

        # Setting Parameters
        total = 0
        center = 0
        gaze = GazeTracking()
        frame_interval = 4  # Frames to skip between two analyze points
        while(cap.isopened()):
            for _ in range(frame_interval):
                retval, frame = cap.read()

            # Checking if frame grabbed or not
            if(not retval):
                break

            # Refreshing the frame
            gaze.refresh(frame)
            # Making the pupil (if located) highlighted in the frame
            frame = gaze.annotated_frame()
            total += 1
            if(frame.is_center()):
                center += 1

            # Activating q button for development process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Closing the video file
        cap.release()

        if(total!=0):
            self.video_score = ceil(center/total)*100
    