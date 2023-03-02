import cv2
import os


def image_extraction(video_number, path):

    # create folder where we'll save all pics
    if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+'_files')):
        os.mkdir(os.path.join(path, 'video_'+str(video_number)+'_files'))

    # create folder where we'll save the raw pics
    if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')):
        os.mkdir(os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics'))

    new_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')

    # to open the video - name of video file in the folder
    cap = cv2.VideoCapture(os.path.join(path, r'files\video_'+str(video_number)+'.avi'))

    i = 0
    j = 0

    while cap.isOpened():

        ret, frame = cap.read()
        # print(i)

        if not ret or i == 4000:  # if the file does not return another frame (i.e. at the end of the video or if the video is disrupted)
            print('ret = False')
            break
        if i % 2 == 0:
            cv2.imwrite(os.path.join(new_path, 'raw_worms_' + str(j) + '.jpg'), frame)
            j += 1

        i += 1

    cap.release()
    cv2.destroyAllWindows()
