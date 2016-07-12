import time
from  cut_video import Cut_video



if __name__ == "__main__":

    # define the number of processor
    NUM_PROCESS = 4
    CUT_PERIOD = 10

    # output video root folder
    out_root_folder = './test_cut_output/'
    in_video_path = './tmp_video/*.mp4'

    cut_class = Cut_video(in_video_path, out_root_folder, NUM_PROCESS, CUT_PERIOD)
    cut_class.pre_processing()
    start_time = time.time()
    cut_class.start_process()
    end_time = time.time()
    cost = end_time - start_time
    print 'cost time %d s' % cost
