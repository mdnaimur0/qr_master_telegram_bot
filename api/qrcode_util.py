import qrcode, os, time, requests
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO

MAX_LENGTH = 2900

if not os.path.exists("temp"):
    os.mkdir("temp")


def generate_qr_code(text, filename):
    if len(text) > MAX_LENGTH:
        return False, "Text is too long to generate a QR Code 😐"
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
        return True, "QR Code generated successfully 😃"
    except Exception as e:
        print(e)
        return False, "Couldn't generate QR Code 😞"


def extract_text_from_qr_code_path(image_path):
    try:
        image = Image.open(image_path)
        decoded_objects = decode(image)

        decoded_text = ""

        if decoded_objects:
            for obj in decoded_objects:
                decoded_text += obj.data.decode("utf-8")
            return decoded_text
        else:
            return "No QR code found in the image 😐"
    except Exception as e:
        return "Couldn't extract text from QR Code 😞"


def extract_text_from_qr_code_url(image_url):
    response = requests.get(image_url)

    if response.status_code == 200:
        try:
            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)

            decoded_objects = decode(image)
            decoded_text = ""

            if decoded_objects:
                for obj in decoded_objects:
                    decoded_text += obj.data.decode("utf-8")
                return decoded_text
            else:
                return "No QR code found in the image 😐"
        except Exception as e:
            return "Couldn't extract text from QR Code 😞"
    else:
        return "Something went wrong. Please try again later 😞"


if __name__ == "__main__":
    data_to_encode = "Hello, It's Md. Naimur Rahman!"
    qr_code_filename = str(int(time.time())) + ".png"
    generate_qr_code(data_to_encode, qr_code_filename)
    print(f"QR Code generated and saved as {qr_code_filename}")

    qr_code_image_path = os.path.join("temp", qr_code_filename)
    extract_text_from_qr_code_path(qr_code_image_path)
