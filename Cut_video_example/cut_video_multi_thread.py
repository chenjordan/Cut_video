import time
import os
import subprocess
from glob import glob
from threading import Thread
from Queue import Queue

NUM_THREADS = 4

root_path = './car_video_all/*'
output_root_path = './car_video_output/'

path_list = glob(root_path)
print path_list

# craete queue to save cmd list
queue = Queue()

def worker():
    while not queue.empty():
        cmd = queue.get()
        # rc = subprocess.Popen(cmd, shell=True)
        # rc.wait()
        print cmd
        time.sleep(1)
        # ffmpeg -i ./car_video/BMW/1.bmw_far.mp4 -vf fps=2 ./car_video_output/bmw_out_%d.jpg


def pre_processing():
    for i in path_list:

        # parse brand name
        brand_name = i.split('/')[2]
        output_path = output_root_path + brand_name

        # create output folder
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # parse file path
        file_list = glob(i + '/*.mp4')
        print  file_list
        for i in file_list:
            print i
            name = (i.split('/')[3]).split('.mp4')[0]
            print name
            out_name = output_path + '/' + name + '_out_%d.jpg'
            cmd = 'ffmpeg -i ' + i + ' -vf fps=2 ' + out_name

            # put all cmd into queue
            queue.put(cmd)


def start_thread():
    # prepare thread list
    threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))

    # start thread
    map(lambda  th: th.start(), threads)

    # wait for thread
    map(lambda  th: th.join(), threads)
    print 'thread all done'


if __name__ == "__main__":

    start_time = time.time()
    pre_processing()
    start_thread()
    end_time = time.time()
    total_cost = end_time - start_time
    print 'cost time=> %d s' % total_cost
