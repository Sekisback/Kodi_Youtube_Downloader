from pytube import YouTube

vurl = 'https://www.youtube.com/watch?v=pX3_1r6obyc'
yt = YouTube(vurl)

stream = yt.streams.all()
for x in stream:
    out = x.split(',')
    print(out)