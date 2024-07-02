import torch



model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
model.conf = 0.8
#
def findNetwork(img):
    results = model(img)
    results.render()

    return results.ims[0]
