import sys

from PIL import Image
from PIL import ImageDraw
import wave, struct
#f = "/usr/share/kivy-examples/audio/12927_sweet_trip_mm_sweep_z.wav"
#f = '/home/dave/cnc/software/media/audio2/cochlear/clean/classical.wav.mp3'
#f='/home/dave/cnc/software/media/audio2/ageing/rock.wav.mp3'
filename=sys.argv[1]
print filename
pcm_data = wave.open(filename)
width = 1200*30 #pcm_data.frames
height = 1000
nchannels, sampwidth, framerate, nframes, comptype, compname = pcm_data.getparams()

ditherNum = 2
sampleEvery = 2

print "nchannels="+str(nchannels)
print "nframes="+str(nframes)
width = nframes/sampleEvery #min(width, nframes)
print "nframes="+str(nframes)+" width="+str(width)
#width = 20

#framelist = pcm_data.readframes(width)

#print framelist

img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)
m = 0
mn =0
data=[]
numframe = 0;
for i in range(0, nframes):
#	data.append(struct.unpack("<h",  pcm_data.readframes(1)))
	frame = pcm_data.readframes(1)
	if len(frame)==4:
		f = frame[0:2]
		d1 = struct.unpack("<h",  f)
		f = frame[2:4]
		d2 = struct.unpack("<h",  f)
		print "d1i="+str(d1)
		data.append(d1+d2)
		m = max(m, data[i][0], -data[i][0])
		numframe+=1
	elif(len(frame)==2):
		f = frame[0:2]
		data.append(struct.unpack("<h",  f))
		print "data="+data[i][0]
#	data.append( int(struct.unpack("<h",  pcm_data.readframes(1)[0])))
		m = max(m, data[i][0], -data[i][0])
		numframe+=1
print str(m)+" miin="+str(m)
scale= 1.0/m
print scale
for i in range(0, numframe, sampleEvery):
	x = i/sampleEvery
	col=int((scale*data[i][0]+1)*128)
	if data[i][0] >0:
		col=0
	else:
		col=255
        draw.line([(x,0), (x,height)], fill=(col,col,col))
	#print dither
print filename+".png"
img.save(filename+".bin.png")
