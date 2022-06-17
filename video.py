# This module will do some video and audio processing
# to make a video out of the images.

import moviepy.editor as mp

def generate_video(post_id):
    image_title = mp.ImageClip(f"/home/thomas/redditYoutubeBot/posts/" + post_id + f"/main/screenshot_{post_id}.png").set_duration(10).resize(height=1280, width=720).set_position(("center", "center"))
    audio_title = mp.AudioFileClip(f"/home/thomas/redditYoutubeBot/posts/" + post_id + f"/main/audio_title_{post_id}.mp3")
    audio_main_body = mp.AudioFileClip(f"/home/thomas/redditYoutubeBot/posts/" + post_id + f"/main/audio_selftext_{post_id}.mp3").set_start(audio_title.duration+2)
    combined = mp.CompositeVideoClip([image_title])
    # Add the two audio clips with a 2 second gap
    combined.audio = mp.CompositeAudioClip([audio_title, audio_main_body])
    combined.write_videofile(f"/home/thomas/redditYoutubeBot/posts/" + post_id + f"/main/video_{post_id}.mp4", fps=60)