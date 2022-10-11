from pytube import YouTube
import os
import ffmpeg

def percentage(stream,chunk,bytes_remaining):
    byte = stream.filesize - bytes_remaining
    percent = byte*100/stream.filesize
    print("telechargement :",int(percent),"%")


def choix_resolution(filter):
        itag = filter[0]
        return itag


def get_url_from_user(url):
    if url.lower().startswith("https://www.youtube.com"):
       BASE_URL = url
    elif not url:
        print("erreur")
        return get_url_from_user(url)
    else:
        print("Address url inconnue")
        return get_url_from_user(url)


    youtube_video = YouTube(BASE_URL)
    youtube_video.register_on_progress_callback(percentage)

    titre = "le titre de la video : "
    fiter_for_video = youtube_video.streams.filter(progressive=False, file_extension="mp4",type="video").order_by("resolution").desc()
    fiter_for_audio = youtube_video.streams.filter(progressive=False, file_extension="mp4",type="audio").order_by("abr").desc()

    stream_qualite_video = choix_resolution(fiter_for_video)
    stream_qualite_for_audio = choix_resolution(fiter_for_audio)

    print(titre,stream_qualite_video.title)
    #print("Telechargement  de la video, resolution = ", stream_qualite_video.resolution)
    stream_qualite_video.download("video")

    #print("Telechargement  de l'audio = ", stream_qualite_for_audio.abr)
    stream_qualite_for_audio.download("audio")
    file_audio = os.path.join("audio",stream_qualite_video.default_filename)
    file_video = os.path.join("video",stream_qualite_video.default_filename)
    file_output = stream_qualite_video.default_filename

    ffmpeg.output(ffmpeg.input(file_audio),ffmpeg.input(file_video),file_output,vcodec ="copy", acodec= "copy" ,loglevel= "quiet")\
        .run(overwrite_output=True)
    os.remove(file_audio)
    os.remove(file_video)
    os.rmdir("audio")
    os.rmdir("video")
    print("reconstruction  OK ")

