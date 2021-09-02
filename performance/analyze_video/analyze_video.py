import moviepy.editor as mp

class AnalyzeVideo:
    '''
    Class for analyzing a video from the following factors:
    * Eye Gazing
    * Audio Confidence
    '''

    def __init__(self, videoLocation):
        self.videoLocation = videoLocation

    
