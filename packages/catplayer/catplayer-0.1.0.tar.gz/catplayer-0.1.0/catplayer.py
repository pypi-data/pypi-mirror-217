import sys
from moviepy.editor import VideoFileClip
import pygame

def play_video(video_path):
    clip = VideoFileClip(video_path)
    clip.set_duration(clip.duration)  # Set the duration to the full length of the video
    clip.preview(fps=60)  # Play the video at 60 FPS
    clip.close()

def main():
    # Check if a video file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the path to an MP4 video file.")
        sys.exit(1)

    # Get the video file path from the command-line argument
    video_path = sys.argv[1]
    pygame.display.set_caption("mewplayer MP4 - https://afflicted.sh")
    # Call the play_video function to play the video
    play_video(video_path)

if __name__ == '__main__':
    main()

