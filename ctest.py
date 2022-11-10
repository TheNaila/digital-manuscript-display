import cv2 as cv

folder = "Mogul Period"
im = cv.imread(folder + "/" + "1955-160.jpg")
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
val, more = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(more)
