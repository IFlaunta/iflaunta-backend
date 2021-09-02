import moviepy.editor as mp

class AnalyzeVideo:
    '''
    Class for analyzing a video from the following factors:
    * Eye Gazing
    * Audio Confidence
    '''

    def __init__(self, videoLocation):
        self.videoLocation = videoLocation

    def get_audio(self):
        '''
        For generating audio from the video in mp3 format
        '''
        # Keeping the audio file name same as the video file, 
        # just changing the externsion to mp3
        audioLocation = self.videoLocation[0:self.videoLocation.rindex(".")]+".mp3"
        video_clip = mp.VideoFileClip(self.videoLocation)
        video_clip.audio.write_audiofile(audioLocation)
        self.audioLocation = audioLocation
    
