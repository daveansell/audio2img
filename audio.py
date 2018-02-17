
from PIL import Image
from PIL import ImageDraw
import wave, struct
#f = "/usr/share/kivy-examples/audio/12927_sweet_trip_mm_sweep_z.wav"
#f = '/home/dave/cnc/software/media/audio2/cochlear/clean/classical.wav.mp3'
#f='/home/dave/cnc/software/media/audio2/ageing/rock.wav.mp3'
f='rock.wav'
pcm_data = wave.open(f)
width = 1200*30 #pcm_data.frames
height = 100
nchannels, sampwidth, framerate, nframes, comptype, compname = pcm_data.getparams()

width = min(width, nframes)
print width
#width = 20

framelist = pcm_data.readframes(width)

#print framelist

img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)
m = 0
data=[]
for i in range(0, width):
	data.append(struct.unpack("<h",  pcm_data.readframes(1)))
#	data.append( int(struct.unpack("<h",  pcm_data.readframes(1)[0])))
	m = max(m, data[i][0])
print m
scale= 1.0/m
print scale
for i in range(0, width):
	col=int((data[i][0]*scale+1)*128)
	draw.line([(i,0), (i,100)], fill=(col,col,col))
	print( (data[i][0]*3+1)*128)

img.save("test.png")
