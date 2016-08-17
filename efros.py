from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from time import time

output_file = "out2.png"

# Efros and Leung 1999 implementation

def distance(data_1, data_2, mask):

    #xs, ys = data_1.shape
    #xs2, ys2 = data_2.shape
    #xs3, ys3 = mask.shape

    #if(xs != xs2 or ys != ys2) :
    #    print "Warning!!"
    #if(xs3 != xs or ys3 != ys): print "Warning, mask size: ", mask.shape, " different from data1 ", data_1.shape

    # TO-DO Gaussian Kernel

    s = data_1 - data_2

    summ = s

    summ = np.extract(mask, summ)

    if(len(summ) == 0): 
        print "warning neighs"
        return 0.0

    return np.sum(summ) / len(summ)

def find_similar(img_data, neigh_window, mask_window):
    
    xs, ys = neigh_window.shape
    img_xsize, img_ysize = img_data.shape

    candidates = []
    dists = []

    for i in range(xs, img_xsize - xs):
        for j in range(ys, img_ysize - ys):
            sub_window = img_data[i : i+xs, j : j+ys]

            d = distance(sub_window, neigh_window, mask_window)
            cx = int(np.floor(xs/2))
            cy = int(np.floor(ys/2))
            candidates.append(sub_window[cx, cy])
            dists.append(d)

    min_dist = np.min(dists)
    mask = dists - min_dist < 0.5

    candidates = np.extract(mask, candidates)
    #print min_dist, candidates
    

    # pick random among candidates
    if len(candidates) < 1:
        return 0.0
    else:
        if len(candidates) != 1:
            r = randint(0, len(candidates) - 1)
        else:
            r = 0


    center_value = candidates[r]
    return center_value

def process_pixel(i, j, img, new_img_data, mask, kernel_size):

    img_data = np.array(img)

    x0 = max(0, i - kernel_size)
    y0 = max(0, j - kernel_size) 
    x1 = min(new_img_data.shape[0] - 1, i + kernel_size)
    y1 = min(new_img_data.shape[1] - 1, j + kernel_size)

    neigh_window = new_img_data[x0 : x1, y0 : y1]

    mask_window = mask[x0 : x1, y0 : y1]

    return find_similar(img_data, neigh_window, mask_window)

def efros(img, new_size_x, new_size_y, kernel_size, t):

    img = img.convert("L")

    patch_size_x, patch_size_y = img.size 
    size_seed_x = size_seed_y = 3

    seed_x = randint(0, size_seed_x)
    seed_y = randint(0, size_seed_y)


    img_data = np.array(img)

    # take 3x3 start image (seed) in the original image
    seed_data = img_data[seed_x : seed_x + size_seed_x, seed_y : seed_y + size_seed_y]

    new_image_data = np.zeros((new_size_x, new_size_y))
    mask = np.ones((new_size_x, new_size_y)) == False

    mask[0: size_seed_x, 0: size_seed_y] = True

    new_image_data[0: size_seed_x, 0: size_seed_y] = seed_data


    # TO DO: non-square images

    it = 0
    for i in range(size_seed_x, new_size_x ):
        print "Process ", i, " / ", new_size_x, ". Time: ", time() - t, " seconds"

        last_y = size_seed_x + it
        # xxxxxxx
        for j in range(0, last_y + 1):
            #print "process pixel" , i, j
            v = process_pixel(i, j, img, new_image_data, mask, kernel_size)

            new_image_data[i, j] = v
            mask[i, j] = True
            

        # x
        # x
        # x
        for x in range(0, size_seed_y + it + 1):
            #print "process pixel" , x, last_y
            v = process_pixel(x, last_y, img, new_image_data, mask, kernel_size)

            new_image_data[x, last_y] = v
            mask[x, last_y] = True

        it += 1


        img_new = Image.fromarray(new_image_data)
        img_new.convert("RGB").save(output_file)


    return img_new

# main program

filename = "img2.png"
new_size_x = 256
new_size_y = 256
kernel_size = 21

img = Image.open(filename)

print "Starting..."

t = time()

img_new = efros(img, new_size_x, new_size_y, kernel_size/2, t)

print "Total Time: ", time() - t, " seconds"

print "Finished!"

plt.imshow(img_new, cmap = "Greys")
plt.show()


img_new.convert("RGB").save(output_file)

