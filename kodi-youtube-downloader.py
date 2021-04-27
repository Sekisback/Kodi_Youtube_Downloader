#!/usr/bin/env python 
# YoutubeVideo Downloader fro Kodi V1.0
# Downloads a YoutubeVideo andthe corresponding Image
# Convert the Video from Mp4 to MKV and create a Kodi episode nfo file
import os
import xml.etree.cElementTree as ET
import wget
from pytube import YouTube

x_name = "WORKOUT"
x_session = "03"
x_episode = "07"
path = "Downloads/"

# Step 1 Get Input
def get_input(x_name, x_session, x_episode):
    vurl = input('YouTube-URL: ')
    name = input(f'Serienname (default = {x_name}): ')
    if name == '': name = (x_name)
    session = input(f'Staffel (default = {x_session}): ')
    if session == '': session = (x_session)
    episode = input(f'Episode (default = {x_episode}): ')
    if episode == '': episode = (x_episode)
    prefix = (f"{name} - S{session}E{episode} - ")
    return (prefix, vurl, name)

# Step 2 Get Video, Image and extract duration and publish date
def get_video(vurl, path, prefix):
    yt = YouTube(vurl)
    title = (prefix + (yt.title.split('|')[0]).strip().replace('.', '').replace('&', 'and').replace('"', '').strip())
    lenght = str(yt.length//60)
    air = yt.publish_date.strftime('%Y-%m-%d')
    stream = yt.streams.get_highest_resolution()
    print('\n[+] Downloading Video ' + yt.title)
    stream.download(output_path=(path), filename=(title))

    
    image_url = yt.thumbnail_url
    image_name = (f'{title}.jpg')
    print(f'[+] Downloading Image {image_name}')
    wget.download(image_url, bar=None, out=(path + image_name))
    print(f'[+] Rename to {title}')
    return(lenght, air)

# Step 3 Convert Mp4 to MKV
def convert_video(path, prefix):
    print('[+] Converting MP4 to MKV')
    video = [video for video in os.listdir(path=path) if video.endswith('.mp4')]                
    video_in = repr(video[0])
    video_out = video_in.replace('.mp4', '.mkv')
    os.system(f'ffmpeg -i {path+video_in} -c:v copy -c:a copy {path+video_out} > /dev/null 2>&1')                                            # convert the Video without encoding
    return(video_out[1:-5])

# Step 4 Create xml.nfo File
def xml_output(path, video, lenght, air):
    print('[+] Creating NFO-File')
    episodedetails = ET.Element('episodedetails')
    title = ET.SubElement(episodedetails, "title")
    title.text = (video.split('-')[2].strip())
    showtitle = ET.SubElement(episodedetails, "showtitle")
    showtitle.text = (video.split('-')[2].strip())
    aired = ET.SubElement(episodedetails, "aired")
    aired.text = (air)
    runtime = ET.SubElement(episodedetails, "runtime")
    runtime.text = (lenght)
    thumb = ET.SubElement(episodedetails, "thumb")
    thumb.text = (f'{video}.jpg')
    

    indent(episodedetails)

    tree = ET.ElementTree(episodedetails)
    tree.write((f'{path}{video}.nfo'), xml_declaration=True, encoding='UTF-8', method='xml')

# Step 4 Create tvshow.nfo File
def tvshow_output(path, name, air):
    print('[+] Creating NFO-File')
    tvshow = ET.Element('tvshow')
    title = ET.SubElement(tvshow, "title")
    title.text = (name)
    showtitle = ET.SubElement(tvshow, "showtitle")
    showtitle.text = (name)
    aired = ET.SubElement(tvshow, "aired")
    aired.text = (air)
    thumb = ET.SubElement(tvshow, "thumb")
    thumb.text = (f'{name}.jpg')
    fanart = ET.SubElement(tvshow, "fanart")
    fanart.text = ()
    fanartthumb = ET.SubElement(fanart, "thumb")
    fanartthumb.text = (f'{name}.jpg')

    indent(tvshow)

    tree = ET.ElementTree(tvshow)
    tree.write((f'{path}tvshow.nfo'), xml_declaration=True, encoding='UTF-8', method='xml')
# xml helper to create pretty xml
# it basically walks the tree and adds spaces
# and newlines so the tree is printed in a nice way
def indent(elem, level=0):    
    i = "\n" + level*"     "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "     "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    prefix, vurl, name = get_input(x_name, x_session, x_episode)
    lenght, air = get_video(vurl, path, prefix)
    video = convert_video(path, prefix)
    xml_output(path, video, lenght, air)
    if input("Create tvshow.nfo [Y/N]: ") == ("y"):
        tvshow_output(path, name, air)
    os.system('rm {0}*.mp4'.format(path))
