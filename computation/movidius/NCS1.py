import mvnc.mvncapi as fx
import sys
import numpy
import cv2


path_to_networks = 'setup/'
graph_filename = 'graph'
image_filename = 'data/' + 'Tiger.jpg'


devices = fx.enumerate_devices()
if len(devices) == 0:
    print('No devices found')
    quit()

device = fx.Device(devices[0])
device.open()


with open(path_to_networks + graph_filename, mode='rb') as f:
    graphfile = f.read()



categories = []
with open(path_to_networks + 'categories.txt', 'r') as f:
    for line in f:
        cat = line.split('\n')[0]
        if cat != 'classes':
            categories.append(cat)
    f.close()
    print('Number of categories:', len(categories))


with open(path_to_networks + 'inputsize.txt', 'r') as f:
    reqsize = int(f.readline().split('\n')[0])



graph = fx.Graph('graph1')

with open(path_to_networks+graph_filename, 'rb') as f:
    graph_buffer = f.read()

input_fifo, output_fifo = graph.allocate_with_fifos(device, graph_buffer)

def preprocess_input(x):
    x /= 255.0
    x -= 0.5
    x *= 2.0
    return x


#Reading the input
img = cv2.imread(image_filename)



img = cv2.resize(img, (reqsize, reqsize))

img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img = img.astype(float)
img = preprocess_input(img)



import time

print('Start download to NCS...')

starttime=time.time()

for i in range(1000):
    graph.queue_inference_with_fifo_elem(input_fifo, output_fifo, img.astype(numpy.float32), 'user object')
    output, userobj = output_fifo.read_elem()

endtime=time.time()

print('*'*79)
print('Time taken is:',endtime-starttime)
top_inds = output.argsort()[::-1][:5]

print(''.join(['*' for i in range(79)]))
print('MobileNet on NCS')
print(''.join(['*' for i in range(79)]))
for i in range(5):
    print(top_inds[i], categories[top_inds[i]], output[top_inds[i]])


print(''.join(['*' for i in range(79)]))


input_fifo.destroy()
output_fifo.destroy()
graph.destroy()
device.close()
device.destroy()
print('Finished')
