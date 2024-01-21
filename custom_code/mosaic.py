import cv2



def mosaic(src, ratio=0.1):

    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)

    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)



def mosaic_area(src, x, y, width, height, ratio=0.1):

    dst = src.copy()

    dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)

    return dst



# Example usage

img_path = 'example.jpg'

image = cv2.imread(img_path)



x, y, w, h = 20, 20, 30, 20

mosaic_img = mosaic_area(image, x, y, w, h)



cv2.imshow('Mosaic', mosaic_img)

cv2.waitKey(0)

cv2.destroyAllWindows()
