import av
from PIL import Image
import cv2

WIDTH = 1920
HEIGHT = 1080
DURATION = 120

def write_rgb_rotate(output):
    input_video = cv2.VideoCapture("../Test Data/Overwatch-1080p-100M.mp4")

    output.metadata["title"] = "container"
    output.metadata["key"] = "value"

    stream = output.add_stream("libx264", 60)
    stream.width = WIDTH
    stream.height = HEIGHT
    stream.pix_fmt = "yuv420p"
    stream.bit_rate = 10*1024*1024
    stream.max_bit_rate = stream.bit_rate + 1
    stream.buffer_size = stream.bit_rate * 2

    while True:
        ret, image = input_video.read()
        if ret:
            frame = av.VideoFrame(WIDTH, HEIGHT, "rgb24")

            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            frame.planes[0].update(image.tobytes())

            for packet in stream.encode(frame):
                output.mux(packet)
            # stream.bit_rate = 10240000
        else:
            break
        
        # stream.bit_rate = 10240000
        # stream.max_bit_rate = 10240000 + 1
        # stream.buffer_size = 10240000 * 2
        # ctx.min_bit_rate = 10240000 -1 
        # ctx.rc_initial_buffer_occupancy = ctx.rc_buffer_size;
    
    for packet in stream.encode(None):
        output.mux(packet)

if __name__ == '__main__':
    with av.open('test.mp4', "w") as output:
        write_rgb_rotate(output)