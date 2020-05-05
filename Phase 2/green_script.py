import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# dir = os.getcwd()+"\\ward collection\\"
dir = os.path.dirname(os.getcwd())+"\\Phase 1\\Screenshots\\"
files = os.listdir(dir)

f = open("green.csv", "w")
f.write("Percentage,Location,Image 1 (outline),Image 2 (satellite)\n")

no_border = [2, 17, 18, 22, 34, 38, 58, 60, 64, 65, 75, 77, 87, 94, 102, 106, 108, 115, 119, 126, 129, 138, 139, 142, 143, 157, 165, 166, 178, 196]

for i in range(len(no_border)):
    no_border[i] = str(no_border[i])

borderless = 0

for i in range(0, len(files), 2):
    if(not files[i][0].isdigit()):
        continue
    
    map_view = cv2.imread(dir+files[i])
    satellite_view = cv2.imread(dir+files[i+1])

    num = ""
    for j in files[i]:
        if j.isdigit():
            num = num + j
        else:
            break

    location = ""
    for c in range(len(files[i+1])-5, 0, -1):
        if(files[i+1][c].isdigit()):
            break
        location = files[i+1][c] + location
    location = location[1::]

    if(num not in no_border):
        black = np.zeros(satellite_view.shape).astype(satellite_view.dtype)

        grid_RGB1 = cv2.cvtColor(map_view, cv2.COLOR_BGR2RGB)
        lower_red = np.array([0,15,0])
        upper_red = np.array([20,255,255])
        grid_HSV1 = cv2.cvtColor(grid_RGB1, cv2.COLOR_RGB2HSV) # Converting to HSV
        mask1 = cv2.inRange(grid_HSV1, lower_red, upper_red)

        ret,thresh = cv2.threshold(mask1, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours)>0:
            cv2.drawContours(black, [max(contours, key = cv2.contourArea)], -1, [255, 255, 255], thickness=-1)
            only_ward = cv2.bitwise_and(satellite_view, black)
        else:
            print(i, ": Couldn't find any contours")
            continue

        grid_RGB2 = cv2.cvtColor(only_ward, cv2.COLOR_BGR2RGB)
        grid_HSV2 = cv2.cvtColor(grid_RGB2, cv2.COLOR_RGB2HSV) # Converting to HSV
        lower_green = np.array([48,18,0])
        upper_green = np.array([179,255,121])
        mask2 = cv2.inRange(grid_HSV2, lower_green, upper_green)

        green_in_ward = cv2.bitwise_and(only_ward, only_ward, mask=mask2) # Generating image with the green part

        gray1 = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(green_in_ward, cv2.COLOR_BGR2GRAY)

        ward_area = cv2.countNonZero(gray1)
        green_area = cv2.countNonZero(gray2)
        green_percentage = green_area / ward_area * 100

        print(location, ": ", green_percentage, "%")

    else:
        borderless+=1
        grid_RGB = cv2.cvtColor(satellite_view, cv2.COLOR_BGR2RGB)

        grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV) # Converting to HSV
        lower_green = np.array([48,18,0])
        upper_green = np.array([179,255,121])

        mask= cv2.inRange(grid_HSV, lower_green, upper_green)
        res = cv2.bitwise_and(satellite_view, satellite_view, mask=mask) # Generating image with the green part

        green_percentage = (mask>0).mean()*100
        print(location, "(no border): ", green_percentage, "%")

    f.write(str(round(green_percentage, 3)) + "," + location + ",\'" + files[i] + "\',\'" + files[i+1] + "\'\n")

print("Number of images with no border outline:", borderless)
print("Completed successfully")