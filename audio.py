import sys

from PIL import Image
from PIL import ImageDraw
import wave, struct
#f = "/usr/share/kivy-examples/audio/12927_sweet_trip_mm_sweep_z.wav"
#f = '/home/dave/cnc/software/media/audio2/cochlear/clean/classical.wav.mp3'
#f='/home/dave/cnc/software/media/audio2/ageing/rock.wav.mp3'
f=sys.argv[1]
print f
pcm_data = wave.open(f)
width = 1200*30 #pcm_data.frames
height = 1000
nchannels, sampwidth, framerate, nframes, comptype, compname = pcm_data.getparams()
print "nchannels="+str(nchannels)
print "nframes="+str(nframes)
width = nframes #min(width, nframes)
print "nframes="+str(nframes)+" width="+str(width)
#width = 20

framelist = pcm_data.readframes(width)

#print framelist

img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)
m = 0
mn =0
data=[]
numframe = 0;
for i in range(0, width):
#	data.append(struct.unpack("<h",  pcm_data.readframes(1)))
	frame = pcm_data.readframes(1)
	print (frame)
	if len(frame)==4:
		f = frame[0:2]
		d1 = struct.unpack("<h",  f)
		f = frame[2:4]
		d2 = struct.unpack("<h",  f)
		print "d1i="+d1
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
for i in range(0, numframe):
	col=int((scale*data[i][0]+1)*128)
	for j in range(0,30):
		draw.line([(i,j*32), (i,j*32+col/8)], fill=(255,255,255))
	print( (data[i][0]*3+1)*128)
img.save(f+".png")
