import numpy as np
from img_processing_utils import *
from PIL import Image

def encode_image(img: np.ndarray | Image.Image, msg: str, bits_engaged = 2) -> Image.Image:
    if isinstance(img, Image.Image):
        img = np.array(img)
    
    
    if img.size < bytes_needed_for_message(msg):
        raise ValueError('Image size is not enough to put all the data into')
    
    encoded_image = img.flatten()
    
    # Insert bits_engaged parameter in the first 8 bits in the image with 2 bits from color
    index = insert_bits(f'{bits_engaged:08b}', encoded_image)
    
    # Create a bit array from the message 
    bits_to_put = msg_to_bits(msg)
    
    # Insert it into the image with custom bits_engaged, 
    # starting from the position where we finished adding bits_engaged information
    insert_bits(bits_to_put, encoded_image, bits_engaged, index)

    # Save the image
    # Image.fromarray(np.reshape(encoded_image, img.shape)).save(dest_folder+image_name.replace('jpg','png'))
    return Image.fromarray(np.reshape(encoded_image, img.shape))


def decode_image(img: np.ndarray | Image.Image) -> str:
    if isinstance(img, Image.Image):
        img = np.array(img)
    
    decoded_image = img.flatten()
    
    message_in_bits = retrieve_bits(decoded_image)
    
    message_in_bytes = bytes([int(el, base=2) for el in message_in_bits])
    return message_in_bytes.decode(encoding='UTF-8')

    
if __name__ == '__main__':
    image_name = 'file_0.jpg'
    img = np.array(Image.open('source_images/'+image_name))
    msg = "Oh hell, I love you soooooo much 😍🤩💋💋💋"
    
    encode_image(img, msg)

    decode_image(Image.open(dest_folder+image_name.replace('jpg','png')))