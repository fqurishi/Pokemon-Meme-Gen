from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx, AudioFileClip, CompositeAudioClip, afx, ImageClip, TextClip
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

from flask import Flask, flash, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

currentDir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__)
CORS(app)


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
    save_output(imagePath, unique_filename +
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
def makeVideo(NameFile, CryFile, Name):
    print("---Making Video File---")
    clip1 = VideoFileClip("Who_That.mp4").subclip(0,5).fx(vfx.fadeout, 1)
    clip2 = VideoFileClip("Who_That.mp4").subclip(8,13).fx(vfx.fadein,1)
    black_dir = os.path.join(currentDir, 'images/blacked/')
    color_dir = os.path.join(currentDir, 'images/no_bg/')
    black1 = (ImageClip(black_dir + "edit.png")
            .set_start(1)
            .set_duration(clip1.duration - 1)
            .set_position((150, 150)).fx(vfx.fadeout, 1))
    black2 = (ImageClip(black_dir + "edit.png")
            .set_start(0)
            .set_duration(1)
            .set_position((150, 150)).fx(vfx.fadein,1))
    color = (ImageClip(color_dir + "edit.png")
            .set_start(1)
            .set_duration(clip1.duration - 1)
            .set_position((150, 150)).fx(vfx.fadein,1, [9,106,159]))
    print(currentDir + "/Ketchum.otf")
    txtClip = (TextClip(Name, fontsize = 96, color = "rgb(254,213,0)", stroke_color="rgb(64,128,207)", stroke_width=5, font=currentDir + "/Ketchum.otf")
                .set_start(1.5)
                .set_duration(clip1.duration-1.5)
                .set_position((785,190)))

    clip = CompositeVideoClip([clip1,black1])
    clip1 = clip

    clip = CompositeVideoClip([clip2,black2,color,txtClip])
    clip2 = clip

    combined = concatenate_videoclips([clip1,clip2])
    combined.write_videofile("Who_That_Out1.mp4")


    clip1 = VideoFileClip("Who_That_Out1.mp4")
    audio1 = AudioFileClip("Who_That_Out1.mp4").fx(afx.volumex, 2)
    audio2 = AudioFileClip(NameFile)
    audio2 = audio2.set_start(6.875)
    audio3 = AudioFileClip(CryFile)
    audio3 = audio3.set_start(audio2.duration + 6.875)

    audio = CompositeAudioClip([audio1,audio2,audio3])

    combined = concatenate_videoclips([clip1])
    combined.audio = audio

    unique_filename = str(uuid.uuid4())
    combined.write_videofile("./downloads/Who_That_Out" + unique_filename + ".mp4")
    return unique_filename

def generatePokemon(ImageFile,NameFile,CryFile,Name):
    print("---Removing Background...")
    # ------- Call The removeBg Function --------
    imgPath = ImageFile 
    print(removeBg(imgPath))
    print("---Making Video...")
    # ------- Call The makeVideo Function --------
    videoName = makeVideo(NameFile,CryFile,Name)
    video = "downloads\\Who_That_Out" + videoName + ".mp4"
    return "Who_That_Out" + videoName + ".mp4"


@app.route('/upload', methods=['POST'])
def upload_file():
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    file1.save(f'./uploads/{file1.filename}')
    file2.save(f'./uploads/{file2.filename}')
    file3.save(f'./uploads/{file3.filename}')
    Name = request.files['name']
    Name = Name.filename
    file1Name = (f'./uploads/{file1.filename}')
    file2Name = (f'./uploads/{file2.filename}')
    file3Name = (f'./uploads/{file3.filename}')
    return generatePokemon(file1Name,file2Name,file3Name,Name)

@app.route('/upload/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_file('downloads/' + filename, as_attachment=True)

if __name__ == '__main__':  
    app.run(debug=True,host="0.0.0.0",port= 5000 ,use_reloader=False)


