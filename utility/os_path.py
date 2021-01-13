import os

def save_images(path, image):
    num = len(os.listdir(path))
    full_path = f'{path}/{num}.png'
    cv2.imwrite(full_path, image)

    return full_path