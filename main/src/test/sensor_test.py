import sys
sys.path.append('../')


from core.sensor import sensor

type='camera'

attributes = {
   'frame_rate':30
}

camera = sensor(type,attributes)
print(camera)
