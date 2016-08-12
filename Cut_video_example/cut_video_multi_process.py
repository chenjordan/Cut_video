import time
import os
import subprocess
import multiprocessing
from glob import glob

root_path = './car_video_all/*'
output_root_path = './car_video_output/'


path_list = glob(root_path)
print path_list

def worker(cmd):
    rc = subprocess.Popen(cmd, shell=True)
    rc.wait()
    # time.sleep(2)
    # ffmpeg -i ./car_video/BMW/1.bmw_far.mp4 -vf fps=2 ./car_video_output/bmw_out_%d.jpg


def pre_processing():

    # create a pool and assign 4 cpu
    pool = multiprocessing.Pool(processes = 4)
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
        for j in file_list:
            print j
            name = (j.split('/')[3]).split('.mp4')[0]
            print name
            out_name = output_path + '/' + name + '_out_%d.jpg'
            cmd = 'ffmpeg -i ' + j + ' -vf fps=2 ' + out_name
            print 'start to call worker !!!'
            pool.apply_async(worker, (cmd, ))
    pool.close()
    pool.join()
    print 'subprocess done !!!'


if __name__ == "__main__":

    start_time = time.time()
    pre_processing()
    end_time = time.time()
    total_cost = end_time - start_time
    print 'cost time=> %d s' % total_cost
