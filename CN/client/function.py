def transpose(s):
    string =""
    lis = s.split()

    for i in range(len(lis)):
        lis[i] = lis[i][::-1]

    for i in range(len(lis)):
        string += lis[i] + " "

    return string

def sub(msg):
    # Predefining the offset as 5
    offset = 2
    encrypted_msg = ""

    # Traversing through the message
    for i in range(len(msg)):
        char = msg[i]
        isInt = isinstance(msg[i], int)

        if (isInt):
            char = chr(msg[i])

        if(char.isalnum()):
            # Encrypting upper case letters
            if(char.isupper()):
                encrypted_msg += chr((ord(char) - 65 + offset) % 26 + 65)

            # Encrypting lower case letters
            elif(char.islower()):
                encrypted_msg += chr((ord(char) - 97 + offset) % 26 + 97)

            # Encrypting numbers
            else:
                encrypted_msg += chr((ord(char) - 48 + offset) % 10 + 48)
        else:
            encrypted_msg += char

    return encrypted_msg


def desub(msg):
    # Predefining the offset as 5
    offset = 2
    decrypted_msg = ""

    # Traversing through the message
    for i in range(len(msg)):
        char = msg[i]
        isInt = isinstance(msg[i], int)

        if (isInt):
            char = chr(msg[i])

        if(char.isalnum()):
            # Decrypting upper case letters
            if(char.isupper()):
                decrypted_msg += chr((ord(char) - 65 - offset) % 26 + 65)

            # Decrypting lower case letters
            elif(char.islower()):
                decrypted_msg += chr((ord(char) - 97 - offset) % 26 + 97)

            # Decrypting numbers
            else:
                decrypted_msg += chr((ord(char) - 48 - offset) % 10 + 48)
        else:
            decrypted_msg += char

    return decrypted_msg