def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    plain_text = bytes([cell for row in matrix for cell in row])
    # ""
    # for row in matrix:
    #     plain_text += "".join(chr(r) for r in row)
    return plain_text

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

if __name__ == "__main__":
    print(matrix2bytes(matrix).decode())
