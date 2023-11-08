from pytube import YouTube

def download_video(url):
    print('Getting Youtube video')

    try:
        yt = YouTube(url)
        filePath = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(skip_existing=False,output_path="media")
    except:
        print("Connection Error")
        return None
    
    print('Task Completed!')
    with open(filePath, 'rb') as file:
        return file