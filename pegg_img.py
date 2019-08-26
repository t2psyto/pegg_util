# -*- coding: utf-8 -*-
# image convert util for pegg-format

from PIL import Image

def loaddata(filename, base=128):
    data = open(filename, "rb").read()
    width = base
    height = len(data) * 8 // width
    size = (width, height)
   
    # image = w:128 x h:512 , 1bit/pixel
    img = Image.frombytes('1', size, data, 'raw', '1;R', 0, -1)
    #img.show()

    # 白黒反転 ＆ -90度 回転
    img2 = img.point(lambda x: 1 if x < 128 else 0).rotate(-90,expand=True)
    #img2.show()

    return img2

def savedata(img, filename):
    gray = img.convert("L")
    imgtmp = gray.point(lambda x: 255 if x < 128 else 0).convert(mode='1')
    imgout = imgtmp.rotate(90,expand=True)
    #print("image out")
    #imgout.show()

    bytesdata = imgout.tobytes('raw', '1;R', 0, -1)

    f = open(filename, "wb")

    if filename[-4:] == ".pbm":
        pbm_header = "P4\n{} {} ".format(imgout.width,imgout.height)
        f.write(pbm_header.encode())

    f.write(bytesdata)
    f.close()


def test_loaddata():
    pegg_el_test_raw = r"test_raw"
    loaddata(pegg_el_test_raw).show()

def test_savedata():
    pegg_el_testsource_raw = r"test_raw"
    pegg_el_testout_raw = r"testout_raw.dat"
    testimg = loaddata(pegg_el_testsource_raw)
    savedata(testimg, pegg_el_testout_raw)
    loaddata(pegg_el_testout_raw).show()
    
def test_savedata2():
    testpng = r"testimage.png"
    testimg_raw = r"testimage.dat"
    testimg = Image.open(testpng)

    resize_height = 128

    # 画像の解像度を取得して、リサイズする高さを計算
    img_width,img_height = testimg.size
    resize_width = (resize_height / img_height) * img_width
    # 画像をリサイズ
    testimg_data = testimg.resize((int(resize_width),int(resize_height)))

    testimg_data.show()

    savedata(testimg_data, testimg_raw)
    loaddata(testimg_raw).show()
