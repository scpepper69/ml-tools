import os, sys
import cv2
import glob
from scipy import ndimage

in_dir = sys.argv[1]
out_dir = sys.argv[2]
width = int(sys.argv[3])
height = int(sys.argv[4])

img_size=(width,height)

os.makedirs(out_dir, exist_ok=True)

in_jpg=glob.glob(in_dir+"/*")

#img_file_name_list=os.listdir(.gundam_images)

target_ext = {"jpg", "jpeg", "bmp", "png"}
for name in target_ext:
    for i in range(len(in_jpg)):
        if name in str(in_jpg[i]):
            ofile,oext=os.path.splitext(os.path.basename(str(in_jpg[i])))
            print(ofile)
            img = cv2.imread(str(in_jpg[i]))
            # Rotate
            for ang in [-10,0,10]:
                img_rot = ndimage.rotate(img,ang)
                img_rot = cv2.resize(img_rot,img_size)
                fileName=os.path.join(out_dir,ofile+"_"+str(ang)+"."+oext)
                cv2.imwrite(str(fileName),img_rot)
                # Threshold
                img_thr = cv2.threshold(img_rot, 100, 255, cv2.THRESH_TOZERO)[1]
                fileName=os.path.join(out_dir,ofile+"_"+str(ang)+"thr."+oext)
                cv2.imwrite(str(fileName),img_thr)
                # Blur
                img_filter = cv2.GaussianBlur(img_rot, (5, 5), 0)
                fileName=os.path.join(out_dir,ofile+"_"+str(ang)+"filter."+oext)
                cv2.imwrite(str(fileName),img_filter)

print("Succeeded.")
