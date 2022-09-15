import socket
import os
from function import sub, desub, transpose

# storing the mode of encryption in FORMAT
FORMAT = "utf-8"

# storing the path of folder where the content from server will be downloaded
downloadDir = os.getcwd()

# We define our socket object s and the family type is AF_INET which represents IPV4 address type 
# sock_stream corresponds to TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket is connected to client
# gethostname will find the IP address
s.connect((socket.gethostname(), 4040))

# asking to select the encryption method from the below three methods
data = input("[client]: Select any one method of encryption from the following: PlainText, Substitution, Transpose: ")

# sending the data to server in bytes format by encoding it with UTF-8
s.send(bytes(data,FORMAT))

# checking if the mode of encryption is plain text or not
if (data == 'PlainText'):

    # taking the input from the user. Basically, asking for the command
    data = input("[client]: ")

    # using while loop for handling multiple requests from the client
    while True :

        # storing the command in a list
        x = data.split()

        # sending the command to the server in bytes format by encoding it with UTF-8
        s.send(data.encode(FORMAT))

        # checking whether the command is dwd or not
        if (x[0]=='dwd'):

            # storing the name of the file to download
            name = x[1]

            # creating the file by joining the path of the client.py to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'wb') as file_to_write:

                # receiving multiple chunks of data from the server and each chunk is of 1024 bytes
                while True:

                    # storing the received data from the server to the data variable
                    data = s.recv(1024)

                    # if no data received then the task is over
                    if len(data) == 0:
                    
                        # closing the file because whole data is already written in the file
                        file_to_write.close()

                        # breaking the loop
                        break

                    # writing the data received from the server into the file
                    file_to_write.write(data)

                    # if length of the data received is less than 1024 then it means that we received the file 
                    if len(data)<1024:

                        # we will close the file because whole data is written in it
                        file_to_write.close()

                        # we will break the loop
                        break
            
            # printing the message so that the user can see it.
            print('[server]: File Downloaded!')

            break

        # checking whether the command is upd or not
        elif (x[0]=='upd'):

            # storing the name of the file to upload
            file = x[1]

            # opening the file to read the data of the file and we are reading its bytes
            with open(file, 'rb') as file_to_send:

                # sending the data inside the file to the server
                for data in file_to_send:
                    s.sendall(data)
                
                # closing the file as all the data is sent to the server
                file_to_send.close()
            
            print("File uploaded!")
            break
        
        # if the command is different than UPD and DWD
        else :

            # if the command is q then it means user do not want to continue anymore
            if (data == 'q'):
                break

            #client is receiving the data from the server and the size of the message is 1024 bytes
            # message is decoded first using UTF-8 decoding format
            message = s.recv(1024).decode(FORMAT)
            
            # we are printing the message after decoding it because the server sent an encoded message
            print('[server]: ' + message)

            # taking the input from the client
            data = input("[client]: ")

# checking if the mode of encryption is Substitution or not
elif (data == 'Substitution'):

    # taking the input from the user. Basically, asking for the command
    data = input("[client]: ")

    # using while loop for handling multiple requests from the client
    while True :

        # storing the command in a list
        x = data.split()

        # sending the command to the server in bytes format by encoding it with UTF-8
        # Before encoding, we will pass the data into sub to apply the layer of caesar cypher
        s.send(sub(data).encode(FORMAT))

        # checking whether the command is dwd or not
        if (x[0]=='dwd'):

            # storing the name of the file to download
            name = x[1]

            # creating the file by joining the path of the client.py to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'wb') as file_to_write:

                # receiving multiple chunks of data from the server and each chunk is of 1024 bytes
                while True:

                    # storing the received data from the server to the data variable
                    # First of all, decoding the data then passing it into the desub which removes caesar cipher
                    data = desub(s.recv(1024).decode())
                    
                    # if no data received then the task is over
                    if not data:

                        # closing the file because whole data is already written in the file
                        file_to_write.close()

                        # breaking the loop
                        break

                    # writing the data received from the server into the file
                    file_to_write.write(data.encode("latin-1"))

                    # if length of the data received is less than 1024 then it means that we received the file 
                    if len(data)<1024:

                        # we will close the file because whole data is written in it
                        file_to_write.close()

                        # we will break the loop
                        break

            

            # printing the message so that the user can see it.
            print('[server]: File downloaded!')

            # breaking the loop
            break

        # checking whether the command is upd or not
        elif (x[0]=='upd'):

            # storing the name of the file to upload
            file = x[1]

            # Opening the file which is needed to upload and reading its data in bytes
            with open(file, 'rb') as file_to_send:

                # loop will read data in chunks and also send the data in a chunk of 1024 bytes
                while True:

                    # reading the data from the file and storing it
                    data = file_to_send.read(1024)

                    # if there is no data left then finishing the process
                    if not data:
                        break

                    # sending the data after doing caesar cipher by passing it in the sub
                    s.sendall(sub(data).encode(FORMAT))

                # closing the file
                file_to_send.close()

            print("File uploaded!")
            # breaking the loop
            break

        # if the command is different than UPD and DWD
        else :

            #client is receiving the data from the server and the size of the message is 1024 bytes
            # message is decoded first using UTF-8 decoding format then it is passed into the desub which removes caesar cypher
            message = desub(s.recv(1024).decode(FORMAT))
            
            # we are printing the message after decoding it because the server sent an encoded message
            print('[server]: ' + message)

            # taking the input from the client
            data = input("[client]: ")

            # if the command is q then it means user do not want to continue anymore
            if (data == 'q'):
                break

# checking if the mode of encryption is Transpose or not
elif (data == 'Transpose'):

    # taking command from the user
    data = input("[client]: ")

    # using while loop for handling multiple requests from the client
    while True :

        # storing the command in a list
        x = data.split()

        # sending the command to the server in bytes format by encoding it with UTF-8
        # Before encoding, we will encrypt the data by using transpose function which reverses the data
        s.send(transpose(data).encode(FORMAT))
        
        # checking whether the command is dwd or not
        if (x[0]=='dwd'):

            # storing the name of the file to download
            name = x[1]

            # creating the file by joining the path of the client.py to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'w') as file_to_write:

                # receiving multiple chunks of data from the server and each chunk is of 1024 bytes
                while True:

                    # after receiving the data, it will be passed into transpose to remove reversing from it
                    data = transpose(s.recv(1024).decode(FORMAT))

                    # if no data received then the task is over
                    if not data:
                        # closing the file because whole data is already written in the file
                        file_to_write.close()
                        # breaking the loop
                        break

                    # data will be written in the created file
                    file_to_write.write(data)

                    # if length of the data received is less than 1024 then it means that we received the file 
                    if len(data)<1024:
                        # closing the file because whole data is already written in the file
                        file_to_write.close()
                        break

            # printing the message so that the user can see it.
            print('[server]: File downloaded!')

            # breaking the loop
            break

        # checking whether the command is upd or not
        elif (x[0]=='upd'):

            # storing the name of the file to upload
            file = x[1]

            # Opening the file to upload so that we can read the data from it in string
            with open(file, 'r') as file_to_send:

                # loop will read data in chunks and also send the data in a chunk of 1024 bytes
                while True:

                    # reading the data from the file and storing it in data variable.
                    # only 1024 bytes at a time
                    data = file_to_send.read(1024)

                    # if no data read then we will break the loop to stop sending the data to the server
                    if not data:
                        break

                    # data is sent to the server by applying the layer of reversing through transpose function
                    s.sendall(transpose(data).encode(FORMAT))

                # closing the file because the data is sent to the server
                file_to_send.close()

                # printing the message so that the user can see it.
            print('[server]: File uploaded!')
            
            # breaking the loop
            break

        # if the command is different than UPD and DWD
        else :

            # if the command is q then it means user do not want to continue anymore
            if (data == 'q'):
                break

            #client is receiving the data from the server and the size of the message is 1024 bytes
            # message is decoded first using UTF-8 decoding format and then it is passed into transpose which reverse the data
            message = transpose(s.recv(1024).decode(FORMAT))
            
            # we are printing the message after decoding it because the server sent an encoded message
            print('[server]: ' + message)

            # taking the input from the client
            data = input("[client]: ")

            

# Printing the message to select a valid encryption mode
else:
    print("[client]: Please select a valid encryption method")

# closing the socket from the client side
s.close()