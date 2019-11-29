import cv2
import os,glob

out_dir="./"

inFile=glob.glob("./*")
for i in range(len(inFile)):
    ofile,oext=os.path.splitext(os.path.basename(str(inFile[i])))
    print(ofile)
    img = cv2.imread(str(inFile[i]))
    img_resize = cv2.resize(img, dsize=(64,64))
    fileName=os.path.join(out_dir,ofile+".jpg")
    cv2.imwrite(str(fileName),img_resize)
