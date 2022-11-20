from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx, AudioFileClip, CompositeAudioClip, afx, ImageClip
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
import uuid
import os

from model import U2NET
from torch.autograd import Variable
from skimage import io, transform
from PIL import Image

currentDir = os.path.dirname(__file__)


def save_output(image_name, output_name, pred, d_dir, type):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()
    im = Image.fromarray(predict_np*255).convert('RGB')
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]))
    pb_np = np.array(imo)
    if type == 'image':
        # Make and apply mask
        mask = pb_np[:, :, 0]
        mask = np.expand_dims(mask, axis=2)
        imo = np.concatenate((image, mask), axis=2)
        imo = Image.fromarray(imo, 'RGBA')
    imo.save(d_dir+output_name)
# Remove Background From Image (Generate Mask, and Final Results)
def removeBg(imagePath):
    results_dir = os.path.join(currentDir, 'images/no_bg/')
    results_blk_dir = os.path.join(currentDir, 'images/blacked/')
    # convert string of image data to uint8
    with open(imagePath, "rb") as image:
        f = image.read()
        img = bytearray(f)
    nparr = np.frombuffer(img, np.uint8)
    if len(nparr) == 0:
        return '---Empty image---'
    # decode image
    try:
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except:
        # build a response dict to send back to client
        return "---Empty image---"
    # save image to inputs
    unique_filename = str(uuid.uuid4())
    # processing
    image = transform.resize(img, (320, 320), mode='constant')
    tmpImg = np.zeros((image.shape[0], image.shape[1], 3))
    tmpImg[:, :, 0] = (image[:, :, 0]-0.485)/0.229
    tmpImg[:, :, 1] = (image[:, :, 1]-0.456)/0.224
    tmpImg[:, :, 2] = (image[:, :, 2]-0.406)/0.225
    tmpImg = tmpImg.transpose((2, 0, 1))
    tmpImg = np.expand_dims(tmpImg, 0)
    image = torch.from_numpy(tmpImg)
    image = image.type(torch.FloatTensor)
    image = Variable(image)
    d1, d2, d3, d4, d5, d6, d7 = net(image)
    pred = d1[:, 0, :, :]
    ma = torch.max(pred)
    mi = torch.min(pred)
    dn = (pred-mi)/(ma-mi)
    pred = dn
    save_output('Bushna.jpg', unique_filename +
                '.png', pred, results_dir, 'image')
    #save_output(inputs_dir+unique_filename+'.jpg', unique_filename +
    #            '.png', pred, masks_dir, 'mask')
    image = Image.open(results_dir + unique_filename +
                '.png')
    image.thumbnail((500,500), Image.ANTIALIAS)
    image.save(results_dir + 'edit.png', "PNG")
    image = Image.open(results_dir + 'edit.png')
    img_data = image.getdata()
    alpha = image.getchannel('A')
    lst=[]
    for i in img_data:
        # make all black
        lst.append((9,106,159)) 
    image.putdata(lst)
    image.putalpha(alpha)
    image.save(results_blk_dir + 'edit.png', "PNG")
    return "---Success---"
def makeVideo():
    print("---Making Video File---")
    clip1 = VideoFileClip("Who_That.mp4").subclip(0,5).fx(vfx.fadeout, 1)
    clip2 = VideoFileClip("Who_That.mp4").subclip(8,13).fx(vfx.fadein,1)
    black_dir = os.path.join(currentDir, 'images/blacked/')
    color_dir = os.path.join(currentDir, 'images/no_bg/')
    black1 = (ImageClip(black_dir + "edit.png")
            .set_start(1)
            .set_duration(clip1.duration - 1)
            .set_position((200, 150)).fx(vfx.fadeout, 1))
    black2 = (ImageClip(black_dir + "edit.png")
            .set_start(0)
            .set_duration(1)
            .set_position((200, 150)).fx(vfx.fadein,1))
    color = (ImageClip(color_dir + "edit.png")
            .set_start(1)
            .set_duration(clip1.duration - 1)
            .set_position((200, 150)).fx(vfx.fadein,1))

    clip = CompositeVideoClip([clip1,black1])
    clip1 = clip

    clip = CompositeVideoClip([clip2,black2,color])
    clip2 = clip

    combined = concatenate_videoclips([clip1,clip2])
    combined.write_videofile("Who_That_Out1.mp4")


    clip1 = VideoFileClip("Who_That_Out1.mp4")
    audio1 = AudioFileClip("Who_That_Out1.mp4").fx(afx.volumex, 2)
    audio2 = AudioFileClip("Name2.wav")
    audio2 = audio2.set_start(6.875)

    audio = CompositeAudioClip([audio1,audio2])

    combined = concatenate_videoclips([clip1])
    combined.audio = audio

    combined.write_videofile("Who_That_Out.mp4")
    return "---Success---"
# ------- Load Trained Model --------
print("---Loading Model---")
model_name = 'u2net'
model_dir = os.path.join(currentDir, 'saved_models',
                         model_name, model_name + '.pth')
net = U2NET(3, 1)
if torch.cuda.is_available():
    net.load_state_dict(torch.load(model_dir))
    net.cuda()
else:
    net.load_state_dict(torch.load(model_dir, map_location='cpu'))
# ------- Load Trained Model --------
print("---Removing Background...")
# ------- Call The removeBg Function --------
imgPath = "Bushna.jpg"  # Change this to your image path
print(removeBg(imgPath))
print(makeVideo())
os.remove(currentDir + "/Who_That_Out1.mp4") 

