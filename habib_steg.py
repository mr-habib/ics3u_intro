from PIL import Image

def load_image(filepath):
  """Load an image from the PIL Image

  Args:
    filepath: The fath of the image file.

  Returns:
    A PIL image.

  Raises:
    FileNotFoundError: Raises an exception if the file is not found.
  """
  image = None
  try:
    image = Image.open(filepath)
  except FileNotFoundError:
    print("Oops, you typed in the wrong filename")
  return image
  

def encode_message_to_image(img, message):
  """Encode a message to a file.

  A Stegnography Method that encodes a message in ASCII to a file. This is done by chaning the last bit of every blue value of each pixel of the image to a bit of the ASCII message.

  Args:
    image: A PIL image
    message: An ASCII message to be encoded

  Returns:
    A PIL image.
  """
  # Hangle empty message
  if not message:
    return img

  # Decode the message into bits
  bits = _decode_message(message)
  # Create a copy of the image so as to not modify original
  image = img.copy()
 # _prep_image(image)
  pixels = image.load()

  bits_index = -1
  for x in range(image.size[0]):
    for y in range(image.size[1]):
      bits_index += 1
      # Get the current bit from the string
      # Get the byte of the blue value of this pixel
      pixel = pixels[x, y]
      pixel_b = pixel[2]
      pixel_b_bin = "{0:08b}".format(pixel_b)

      if bits_index < len(bits):
        # Replace the last bit with the next bit of our decoded message
        new_pixel_b_bin = pixel_b_bin[0:7] + bits[bits_index]
        new_pixel_b = int(new_pixel_b_bin,2)
        new_pixel = (pixel[0], pixel[1], new_pixel_b)
        pixels[x, y] = new_pixel
      else:
        # Done encoding image
        return image
  
  return image

def get_message_from_image(image):
  """Decode a message to a file.

  A Stegnography Method that decodes a message in ASCII from a PIL image file. This is done by reading the last bit of every blue value of each pixel of the image and decoding it to ASCII.

  Args:
    image: A PIL image

  Returns:
    message: The message hidden in the image
  """
  pixels = image.load()
  last_bits = []
  for i in range(image.size[0]):
    for j in range(image.size[1]):
      # Get the blue value
      blue_val = pixels[i,j][2]
      # Convert int to byte
      last_bit = int("{0:08b}".format(blue_val)[-1])
      # Extract the last bit of the byte
      last_bits.append(last_bit)
  
  # Return hidden message from bits
  return _get_message_from_bits(last_bits)

def _decode_message(message):
  """ASCII string to list of bits conversion

  Args:
    message: ASCII String

  Returns:
    bits: A list of bits representing an ASCII string
  """
  bits = []
  for char in message:
    # Charcter to 8 bit string
    byte_string = "{0:08b}".format(ord(char))
    # Add that 8 bits to list
    bits.extend([b for b in byte_string])
  
  # Add \\x00 terminator byte
  bits.extend(['0' for _ in range(8)])
  return bits


def _get_message_from_bits(bits):
  """List of bits to ASCII string conversion

  Args:
    bits: A list of bits

  Returns:
   message: The ASCII representation of the bits terminated with \\x00
  """
  message = ""
  for byte_start in range(0,len(bits),8):
    byte = bits[byte_start:byte_start+8]
    byte = "".join([str(b) for b in byte])
    message += chr(int(byte,2))
    # Return on null termination character
    if byte == "00000000":
      return message

  return message
        
      
