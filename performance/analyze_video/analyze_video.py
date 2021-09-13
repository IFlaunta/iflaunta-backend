from math import ceil
import moviepy.editor as mp
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings
import requests
import cv2
import os
from .gaze_tracking.gaze_tracking import GazeTracking

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
        self.audioLocation = self.videoLocation[0:self.videoLocation.rindex(".")]+".wav"
        video_clip = mp.VideoFileClip(self.videoLocation)
        if(video_clip.reader.infos["audio_found"]):
            # If audio found
            video_clip.audio.write_audiofile(self.audioLocation)
        video_clip.close()
    
    def analyze_audio(self):
        '''
        For getting the confidence and transcript from the audio
        '''
        with open(self.audioLocation, 'rb') as audio_file:
            data = audio_file.read()

        try:
            # Setup Service

            # Using sdk
            # authenticator = IAMAuthenticator(IBM_API_KEY)
            # stt = SpeechToTextV1(authenticator=authenticator)
            # stt.set_service_url(IBM_URL)
            
            # # Perform conversion
            # res = stt.recognize(audio=data, content_type='audio/wav', model='en-IN_Telephony', continuous=True).get_result()
            # self.confidence = int((res['results'][0]['alternatives'][0]['confidence'])*100)
            # self.transcript = res['results'][0]['alternatives'][0]['transcript']
            
            # Using API (it is faster than sdk method)
            headers = {
                'Content-type': 'audio/wav'
            }
            params = {
                "model": "en-US_NarrowbandModel"
            }
            res = requests.post(IBM_URL+"/v1/recognize",auth=('apikey',IBM_API_KEY),params=params, data=data, headers=headers)
            d = res.json()
            self.confidence = int((d['results'][0]['alternatives'][0]['confidence'])*100)
            self.transcript = d['results'][0]['alternatives'][0]['transcript']

        except Exception as e:
            pass

    def analyze_video(self):
        '''
        For analyzing the video using eye gazing
        '''
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
        while(cap.isOpened()):
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
            if(gaze.is_center()):
                center += 1

            # Activating q button for development process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Closing the video file
        cap.release()

        if(total!=0):
            self.video_score = ceil(center/total)*100
    
    def analyze(self):
        try:
            self.get_audio()
        except Exception as e:
            print("{}, occurred in get_audio method".format(e.__class__))
        
        try:
            self.analyze_audio()
        except Exception as e:
            print("{}, occurred in analyze_audio method".format(e.__class__))

        try:
            self.analyze_video()
        except Exception as e:
            print("{}, occurred in analyze_video method".format(e.__class__))
    
    def clear(self):
        '''
        Method for deleting the video and audio files after analysis being completed
        '''
        try:
            os.remove(self.videoLocation)
        except Exception as e:
            print("{}, occurred in videoLocation clear method".format(e))
            pass

        try:
            os.remove(self.audioLocation)
        except Exception as e:
            print("{}, occurred in audioLocation clear method".format(e))
            pass
