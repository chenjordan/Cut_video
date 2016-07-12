import os
import time
import logging
import datetime
import subprocess
import multiprocessing
from glob import glob


class Cut_video:

    def __init__(self, in_video_path, out_root_folder, NUM_PROCESS, CUT_PERIOD):
        self.in_video_path = in_video_path
        self.out_root_folder = out_root_folder
        self.NUM_PROCESS = NUM_PROCESS
        self.CUT_PERIOD = CUT_PERIOD

        # for each worker usage
        self.queue = multiprocessing.Queue()

    def pre_processing(self):

        logging.info('!!!!!!!!!! preprocessing start !!!!!!!!!!')

        # parse video path
        video_name = glob(self.in_video_path)

        # # parse each video name
        for i in video_name:
            self.queue.put(i)

        logging.info('!!!!!!!!!! preprocessing end !!!!!!!!!!')


    def worker(self):
        period = time.strftime('%H:%M:%S', time.gmtime(self.CUT_PERIOD))
        print period

        while not self.queue.empty():
            task_name = self.queue.get()
            v_name = os.path.basename(task_name)
            print '#####################################'
            print task_name

            # get video length
            get_len_cmd = 'ffmpeg -i ' + task_name + ' 2>&1 | grep Duration | cut -d \' \' -f 4 | sed s/,//'
            rc = subprocess.Popen(get_len_cmd, shell=True, stdout=subprocess.PIPE)
            len = rc.communicate()[0]
            n = time.strptime(len[0:8], "%H:%M:%S")
            total_len = datetime.timedelta(hours=n.tm_hour, minutes=n.tm_min, seconds=n.tm_sec).total_seconds()

            # create output file
            file_name = v_name.split('.mp4')[0]
            out_folder = self.out_root_folder + file_name
            print out_folder

            if not os.path.exists(out_folder):
                os.makedirs(out_folder)

            for j in range(0, int(total_len), self.CUT_PERIOD):

                # generate output file name
                out_file = out_folder + '/' + file_name +'_' + str(j) + '.mp4'
                b_time = time.strftime('%H:%M:%S', time.gmtime(j))
                cut_cmd = 'ffmpeg -i ' + task_name + ' -ss ' + b_time + ' -t ' + period + ' ' + out_file
                print cut_cmd
                rc = subprocess.Popen(cut_cmd, shell=True)
                rc.wait()


    def start_process(self):

        # prepare process list
        process = map(lambda  i:multiprocessing.Process(target=self.worker), xrange(self.NUM_PROCESS))

        # start process
        map(lambda pc: pc.start(), process)

        # wait process fininsh
        map(lambda pc: pc.join(), process)


