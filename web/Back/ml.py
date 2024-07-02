import cv2
import numpy as np
import base64



def correctImage(volume):
    byteData = volume.split(',')[-1].encode('utf-8') 
    
    im_bytes = base64.b64decode(byteData)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img



def findfigureImage(src, model):
    results = model(src)
    results.render()

    return results
