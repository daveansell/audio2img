
from PIL import Image
from PIL import ImageDraw
import audiotools
#f = "/usr/share/kivy-examples/audio/12927_sweet_trip_mm_sweep_z.wav"
#f = '/home/dave/cnc/software/media/audio2/cochlear/clean/classical.wav.mp3'
#f='/home/dave/cnc/software/media/audio2/ageing/rock.wav.mp3'
f='rock.wav'
pcm_data = audiotools.open(f).to_pcm()
width = 20000 #pcm_data.frames
height = 100
framelist = pcm_data.read(20000).to_float()

img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)
m = 0
for i in range(0, len(framelist)):
	m = max(m, framelist[i])
scale= 1.0/m

for i in range(0, len(framelist)):
	col=int((framelist[i]*scale+1)*128)
	draw.line([(i,0), (i,100)], fill=(col,col,col))
	print( (framelist[i]*3+1)*128)

img.save("test.png")
