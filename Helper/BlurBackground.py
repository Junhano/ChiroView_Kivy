import numpy as np
import cv2
def createEmptyGridImage(height, width, horizontal, vertical):
    white_image = 255 * np.ones((height, width, 3), np.uint8)
    if vertical > 40:
        vertical = 40
    if horizontal > 40:
        horizontal = 40

    for i in range(horizontal):
        cv2.line(white_image, (0, int((height / (horizontal+1)) * (i+1))), (width, int(( height / (horizontal+1))*(i+1))), (0,0,0), 1)
    for z in range(vertical):
        cv2.line(white_image, (int((width / (vertical + 1)) * (z+1)), 0), (int((width / (vertical + 1)) * (z+1)), height), (0,0,0), 1)

    return white_image

def IdentifyBackgroundSep(img):
    '''
    mask = np.zeros(img.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
    rectangle = (0, 0, img.shape[0], img.shape[1])
    cv2.grabCut(img, mask, rectangle, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    img = img * mask[:, :, np.newaxis]
    '''
    return img


def AddingImageTogether(img, horizontal, vertical):
    height, width, _ = img.shape
    white_image = createEmptyGridImage(height, width, horizontal, vertical)
    for i in range(width):
        for k in range(height):
            pixel = img[k, i]
            if np.all(pixel == [0, 0, 0]):
                img[k, i] = white_image[k, i]
    return img



if __name__ == "__main__":
    img = cv2.imread('../TestImage/Human.jpg')
    modify_image = IdentifyBackgroundSep(img)
    cv2.imshow('modify', modify_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
