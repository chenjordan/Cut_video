import time
import os
import subprocess
from glob import glob

root_path = './car_video_all/*'
output_root_path = './car_video_output/'


path_list = glob(root_path)
print path_list

def worker(cmd):
    rc = subprocess.Popen(cmd, shell=True)
    rc.wait()
    # print cmd
    # time.sleep(2)
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
            # create file folder
            out_name = output_path + '/' + name + '_out_%d.jpg'
            cmd = 'ffmpeg -i ' + i + ' -vf fps=2 ' + out_name
            print cmd
            worker(cmd)


if __name__ == "__main__":

    start_time = time.time()
    pre_processing()
    end_time = time.time()
    total_cost = end_time - start_time
    print 'cost time=> %d s' % total_cost