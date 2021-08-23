import os
import time




url = 'allo_result'
img_path = os.getcwd() + '\\orig_pictures'
path = r'C:\Users\jiayun.ma\Desktop\webDetection\webDetection\preparation\orig_pictures'
for file in os.listdir(path):
    filename = os.path.splitext(file)[0]
    if url == filename.partition('-')[0]:
        t = filename.partition('-')[2]
        t_int = time.mktime(time.strptime(t, '%Y-%m%d-%H%M%S'))
        ttt = time.time()
        if time.time() - t_int > 60:
            save_resp_img()
            os.remove(os.path.join(path, file))
