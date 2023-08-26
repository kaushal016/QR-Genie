import pyqrcode
import os
import validators #to validate url
from PIL import Image
import qrcode
import cv2
from urllib.parse import urlparse

def main():

    os.system('clear')
    print('\nCS50P Final Project - KAUSHAL LOHAR\n')
    print('\nQR GENIE - Python-Powered QR Scanning and Generation\n')

    while True:
        print('\n******************************\n')
        print('1.Create QR Code From [URL]')
        print('2.Create QR Code From [TXT]')
        print('3.Custom QR With LOGO & BG-Color ')
        print('4.Create File with (jpg/jpeg) Ext\'s')
        print('5.SCAN QR')
        print('6.Exit\n')
        print('******************************')

        choice = int (input('\nEnter Choice : '))

        match choice:
            case 1 :
                user_url=accept_url()
                if not (validate_url(user_url)):
                    print('\n!!! Not a valid url ')
                    print(' url format -> https://www.example.com')
                else:
                    img=simple_qr(user_url)
                    if (img == False) :
                        print("QR Not Generated")
                    print(f"File {img} created")

            case 2 :
                n = int(input('\n\tHow many Qr wanna Generate ? :'))
                for i in range (1 , n+1):
                    user_ip_txt=input('\nEnter text ')
                    qr = pyqrcode.create(user_ip_txt)
                    qr.png(f"text_qr_{i}.png",scale=6)
                    print(f"\nFile text_qr_{i}.png created")

            case 3 :
                user_url=accept_url()
                if not (validate_url(user_url)):
                    print('\n!!! Not a valid url ')
                    print('enter url in this format -> https://www.example.com')
                else:
                    back_clr_img=input('Enter bg-color : ')
                    logo_path = 'example_assets/gdsc-logo.png'
                    filename = custom_qr(user_url, logo_path , back_clr_img)
                    print(f"file {filename}.png created")

            case 4 :
                path="/workspaces/115169467/project/"
                list_qr_codes(path)
                src_img=input('\n\tWhich File :')
                path=f"/workspaces/115169467/project/{src_img}"
                print("\n")
                target_extensions = ["jpeg", "jpg"]
                more_extension_qrcodes(path,target_extensions)

            case 5 :
                path = "/workspaces/115169467/project"
                list_qr_codes(path)
                img=input('\n\tEnter path of file you wanna scan :')
                path=f"/workspaces/115169467/project/{img}"
                read_qr(path)

            case 6 :
                print('\n******* Program Exited *******\n')
                exit()

def accept_url():
    user_url=input('Enter Url ')
    return user_url

def validate_url(user_url):
    if validators.url(user_url):
        return True
    else:
        return False

def read_qr(file_path):
    img = cv2.imread(file_path)
    qr_det = cv2.QRCodeDetector()
    ret_val , decoded_info, points , _ = qr_det.detectAndDecodeMulti(img)
    if ret_val :
        print("Decoded QR code : \n\t",decoded_info)
    else:
        print("No QR found in image")

def list_qr_codes(folder_path):
    img_exts = ['.png','.jpg','.jpeg']
    print("\n\tScan-able's are : ")
    for root,dirs,files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in img_exts):
                file=str(os.path.join(root,file)).replace(folder_path,'')
                print('\t',file)

def simple_qr(url_str):
    if (validate_url(url_str)):
        url = pyqrcode.create(url_str)
        parsed_url = urlparse(url_str)
        domain = parsed_url.netloc.replace("www.", "").replace('.com','').replace('.ac','').replace('.edu','').replace('.gov','').replace('.in','')
        image_name = f"{domain}.png"
        url.png(f'{image_name}', scale = 6)
        return image_name
    else:
        return False


def more_extension_qrcodes(source_filename, target_extensions):
    with open(source_filename, 'rb') as source_file:
        content = source_file.read()

    for extension in target_extensions:
        target_filename = f"{source_filename.rsplit('.', 1)[0]}.{extension}"
        with open(target_filename, 'wb') as target_file:
            target_file.write(content)
        print(f"File {target_filename} created.")

def custom_qr(url, logo_path, qr_color):
    logo = Image.open(logo_path)
    basewidth = 100
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.BILINEAR)
    QRcode = qrcode.QRCode( error_correction=qrcode.constants.ERROR_CORRECT_H )
    QRcode.add_data(url)
    QRcode.make()

    QRimg = QRcode.make_image(fill_color=qr_color, back_color='white').convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "").replace('.com','').replace('.ac.in','').replace('.edu','')
    image_name = f"{domain}"
    QRimg.save(f'{image_name}.png')

    return image_name



if __name__ == "__main__":
    main()