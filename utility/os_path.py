import os
import shutil

def save_images(path, image):
    num = len(os.listdir(path))
    full_path = f'{path}/{num}.jpg'
    cv2.imwrite(full_path, image)

    return full_path


def clear_folder(path):
    shutil.rmtree(path)