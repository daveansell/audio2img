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
height = 3000
nchannels, sampwidth, framerate, nframes, comptype, compname = pcm_data.getparams()

ditherNum = 16
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
		data.append(d1+d2)
		m = max(m, data[i][0], -data[i][0])
		numframe+=1
	elif(len(frame)==2):
		f = frame[0:2]
		data.append(struct.unpack("<h",  f))
#	data.append( int(struct.unpack("<h",  pcm_data.readframes(1)[0])))
		m = max(m, data[i][0], -data[i][0])
		numframe+=1
print str(m)+" miin="+str(m)
scale= 1.0/m
print scale
tx=0
tn=10000
for i in range(0, numframe, sampleEvery):
	x = i/sampleEvery
	col=int((scale*data[i][0]+1)*128)
	dither = col * (ditherNum) / 256 
	dither = max(0, dither)
	dither = min(dither, ditherNum)
	tx=max(tx,dither)
	tn=min(tn,dither)
	#print dither
	for j in range(0,height/(ditherNum-1)):
		if dither>0:
			if j%2:
				draw.line([(x,j*(ditherNum-1)), (x,j*(ditherNum-1)+dither-1)], fill=(255,255,255))
			else:
				draw.line([(x,(j+1)*(ditherNum-1)-1), (x,(j+1)*(ditherNum-1)-dither)], fill=(255,255,255))
print str(tx)+" -> "+str(tn)
print filename+".png"
img.save(filename+".audio"+str(ditherNum)+".png")
