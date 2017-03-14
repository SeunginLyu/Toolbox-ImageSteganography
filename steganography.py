"""A program that encodes and decodes hidden messages
   in images through LSB steganography"""

from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode.
    By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)

    for x in range(x_size):
        for y in range(y_size):
            red_pixel = red_channel.getpixel((x, y))
            red_binary = bin(red_pixel)
            red_lsb = int(red_binary[-1])
            if(red_lsb == 0):
                decoded_image.putpixel((x, y), (0, 0, 0))
            elif(red_lsb == 1):
                decoded_image.putpixel((x, y), (255, 255, 255))
    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding.
                    An image is provided by default.
    """
    raw_image = Image.open(template_image)
    text_image = write_text(text_to_encode, raw_image.size)

    x_size = raw_image.size[0]
    y_size = raw_image.size[1]

    encoded_image = Image.new("RGB", raw_image.size)

    red_channel = raw_image.split()[0]
    green_channel = raw_image.split()[1]
    blue_channel = raw_image.split()[2]
    #  text hidden in RED_Channel LSB
    for x in range(x_size):
        for y in range(y_size):
            text_pixel = text_image.getpixel((x, y))

            # if text exsits for (x, y), change the red channel LSB value to 1
            encoded_red_pixel = red_channel.getpixel((x, y))
            if(text_pixel == (255, 255, 255)):
                red_pixel = red_channel.getpixel((x, y))
                red_binary = bin(red_pixel)
                red_binary = red_binary[:-1] + "1"
                encoded_red_pixel = int(red_binary, 2)
            else:  # if text does not exist for (x, y), change LSB value to 0
                red_pixel = red_channel.getpixel((x, y))
                red_binary = bin(red_pixel)
                red_binary = red_binary[:-1] + "0"
                encoded_red_pixel = int(red_binary, 2)
            encoded_rgb = (encoded_red_pixel,
                           green_channel.getpixel((x, y)),
                           blue_channel.getpixel((x, y)))
            encoded_image.putpixel((x, y), encoded_rgb)
    encoded_image.save("images/my_secret_message_sample.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    text = "'SOFTDES IS AWESOME'"
    print("Encoding the image with text:" + text + "...")
    encode_image(text)
