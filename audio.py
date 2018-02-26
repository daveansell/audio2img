
import sys

from PIL import Image
from PIL import ImageDraw
import wave, struct
if sys.argv[0]=='python':
	sys.argv=sys.argv[1:]
if len(sys.argv)==1:
	print "python audio2img filename ditherNum sampleEvery height"
	print 
	print "ditherNum - amplitude will be represented in ditherNum pixels - larger number more accurate but more stripy result"
	print "sampleEvery - only produces a pixel for every nth audio frame"
	print "height - image height in pixels"

filename=sys.argv[1]
print filename
pcm_data = wave.open(filename)
width = 1200*30 #pcm_data.frames
nchannels, sampwidth, framerate, nframes, comptype, compname = pcm_data.getparams()

if len(sys.argv)>2:
	ditherNum = int(sys.argv[2])
else:
	ditherNum = 16
if len(sys.argv)>3:
	sampleEvery = int(sys.argv[3])
else:
	sampleEvery = 8
if len(sys.argv)>4:
	height = int(sys.argv[4])
else:
	height = 3000

print "nchannels="+str(nchannels)
print "nframes="+str(nframes)
width = nframes/sampleEvery #min(width, nframes)
print "nframes="+str(nframes)+" width="+str(width)


img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)
m = 0
mn =0
data=[]
numframe = 0;
for i in range(0, nframes):
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
		m = max(m, data[i][0], -data[i][0])
		numframe+=1
scale= 1.0/m
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
print filename+".png"
img.save(filename+".audio"+str(ditherNum)+".png")
