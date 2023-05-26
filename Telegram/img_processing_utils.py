import numpy as np, math
max_message_length = 64 # In bytes
source_folder = './source_images/'
dest_folder = './encoded_images/'

def bytes_needed_for_message(msg: str, bits_engaged=2) -> int:
    # (Bits_for_message + bits_for_control_info + bits_for_bits_engaged_info) / data_bit_capacity
    return np.ceil( (len(msg.encode())*8 + max_message_length + 8) / bits_engaged ) 

def msg_to_bits(msg: str) -> str:
    bits_to_put = f"{len(msg.encode()):064b}"
    
    for b in msg.encode(encoding='UTF-8'):
        bits_to_put += f"{b:08b}"
    
    return bits_to_put

def insert_bits(bits_to_put, enc_img, bits_engaged=2, index=0):
    """Insert string bit array bits_to_put into flatten image array enc_img starting from index and using last bits_engaged bits to store data

    Returns:
        index: index in a flatten image array where we finished adding data
    """
    while bits_to_put:
        bits, bits_to_put = bits_to_put[:bits_engaged], bits_to_put[bits_engaged:]
        
        # We ran out of message – pad last bits with zeroes
        if not bits_to_put and (len(bits) < bits_engaged): bits.ljust(bits_engaged, "0")
        
        bits = int(bits, base=2)
        enc_img[index] = ((enc_img[index] >> bits_engaged) << bits_engaged) | bits
        
        index+=1
    
    return index

def retrieve_bits(enc_img):
    bits_engaged = int(''.join(f'{enc_img[i]:08b}'[-2:] for i in range(4)), base=2)

    message_info_bytes = math.ceil(64/bits_engaged)
    message_length = int(''.join(f'{enc_img[i]:08b}'[-bits_engaged:] for i in range(4, 4 + message_info_bytes)), base=2)
    
    bytes_inspected = 4 + message_info_bytes
    bytes_to_inspect = math.ceil(message_length * 8 / bits_engaged)
    
    message_in_bits = ''.join(f'{enc_img[index]:08b}'[-bits_engaged:] + (' ' if (i+1)%4==0 else '') for i, index in enumerate(range(bytes_inspected, bytes_inspected + bytes_to_inspect)))
    message_in_bits = message_in_bits.split()
    
    return message_in_bits
    