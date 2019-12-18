#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



import qrcode
qr = qrcode.QRCode(
    # version=2,
    # error_correction=qrcode.constants.ERROR_CORRECT_L,
    # box_size=10,
    # border=1
)   #设置二维码大小
qr.add_data("https://www.baidu.com/")
qr.make(fit=True)
img = qr.make_image()
img.save("my_blog.png")