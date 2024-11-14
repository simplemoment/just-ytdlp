from yt_dlp import YoutubeDL

def run():
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
    except Exception as e:
        print(f"{e}")

if __name__ == '__main__':
    print("enter video url, like a 'https://youtu.be/qwerty01234' or 'https://youtube.com/watch?v=abcdf01234'")
    input("•> ")
