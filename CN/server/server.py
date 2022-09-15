import socket
import os
from function import sub, desub, transpose

# storing the mode of encryption in FORMAT
FORMAT = "utf-8"

# storing the path of folder where the content from server will be downloaded
downloadDir = os.getcwd()

# We define our socket object s and the family type is AF_INET which represents IPV4 address type
# sock stream corresponds to TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# we will bind our socket with the server address and port value
# gethostname will find the IP address
s.bind((socket.gethostname(), 4040))

# server is ready to connect to the client
s.listen()
print("[+]server created successfully!")
print("[+]Server is listening...")

# server is connected to the client and taking it's IP address
clientsocket, address = s.accept()

print(f"Device {address} is connected to the server!")

# receiving the data from the client that which encryption mode to choose
data = clientsocket.recv(1024).decode(FORMAT)

# checking if the mode of encryption is plain text or not
if (data == 'PlainText'):

    # using while loop for handling multiple requests from the client
    while True:

        # server is receiving the data from the client. Basaically, it's a command 
        data = clientsocket.recv(1024).decode(FORMAT)

        # storing the command in a list
        x = data.split()

        # if no data received from the client then we will break the loop
        if not data:
            break

        # checking whether the command is cwd or not
        elif (x[0] == 'cwd') :

            # used OS library to get the current working directory of the server
            cwd = os.getcwd()

            # encoded the message to send it to the client because data can't be transfered as string
            clientsocket.send(cwd.encode(FORMAT))

        # checking whether the command is ls or not
        elif (x[0] == 'ls') :

            # got the current working directory
            cwd = os.getcwd()

            # got the list of files and folders present in the current working directory using the path of cwd
            liste = os.listdir(cwd)

            # converting the list into string to convert it into bytes
            liste = str(liste)

            # sending the data to the client
            clientsocket.send(liste.encode(FORMAT))

        # checking whether the command is cd or not. Here, x[0] represents the command and x[1] represents the parameter passed
        elif (x[0] == 'cd'):

            # got the current working directory
            cwd = os.getcwd()

            # got the list of files and folders present in the current working directory using the path of cwd
            liste = os.listdir(cwd)

            # storing the file name in add
            add = x[1]
            if x[1] in liste:
                # using OS library for changing the directory using the file or folder name
                os.chdir(x[1])
                # f string is used to use the variable add 
                msg = f"Directory has been changed to {add}"

                # sending the message to the client by encoding it with FORMAT="UTF-8"
                clientsocket.send(msg.encode(FORMAT))

            else:
                msg = "File does not exist!"
                clientsocket.send(msg.encode(FORMAT))

        # checking whether the command is dwd or not
        elif (x[0] == 'dwd'):

            # storing file name in file
            file = x[1]

            # opening the file whose name is given by the client and reading its data in bytes
            with open(file, 'rb') as file_to_send:

                # using loop to transfer the file's data in chunks of 1024 bytes
                while True:

                    # storing 1024 bytes from the file to data variable by reading the file
                    data = file_to_send.read(1024)

                    # if no data read then it means that no more data is remaining in the file
                    if not data:
                        # closing the file after sending all the data to the client
                        file_to_send.close()
                        break

                    # sending all the data to client
                    clientsocket.sendall(data)

                    if len(data)<1024:
                        # closing the file after sending all the data to the client
                        file_to_send.close()
                        break

            #closing the connection from client
            clientsocket.close()

            # breaking the loop as connection closed
            break

        # checking whether the command is upd or not
        elif (x[0] == 'upd'):

            # storing the name of the file to upload
            name = x[1]

            # creating the file by joining the path of the server.py to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'wb') as file_to_write:

                # receiving multiple chunks of data from the client
                while True:

                    # storing the received data from the client to data variable
                    data = clientsocket.recv(1024)

                    # if no data received then the task is over
                    if not data:
                        break

                    # writing the data received from the client to the created file in the server
                    file_to_write.write(data)
                
                # closing the file as whole data is already written in the file
                file_to_write.close()

            # closing the connection of client
            clientsocket.close()

            break

        # if the command given by the client is different from the five commands then sending the wrong command message to the client
        else:
            msg2 = f"wrong command"
            clientsocket.send(msg2.encode(FORMAT))

# checking if the mode of encryption is Substitution or not
elif (data == 'Substitution'):

    # using while loop for handling multiple requests from the client
    while True:

        # server is receiving the data from the client. Basaically, it's a command 
        # first the command will be decoded and then it will be passed in desub which removes the caesar cipher from the data received 
        data = desub(clientsocket.recv(1024).decode(FORMAT))

        # storing the command into the list by breaking the command with spaces 
        x = data.split()

        # if no data received then we will break the loop
        if not data:
            break

        # checking whether the command is cwd or not
        elif (x[0] == 'cwd') :

            # getting current working directory by using OS library
            cwd = os.getcwd()

            # applying the layer of caesar cipher on the data to send and then encoding it with UTF-8 format
            clientsocket.send(sub(cwd).encode(FORMAT))

        # checking whether the command is ls or not
        elif (x[0] == 'ls') :

            # getting current working directory by using OS library and storing it in cwd
            cwd = os.getcwd()

            # getting the list of files and folders from the cwd
            liste = os.listdir(cwd)

            # converting the list into string
            liste = str(liste)

            # sending the data by applying the layer of caesar cipher on the data and then encoding it with UTF-8 format
            clientsocket.send(sub(liste).encode(FORMAT))

        # checking whether the command is cd or not
        elif (x[0] == 'cd'):

            # getting current working directory by using OS library and storing it in cwd
            cwd = os.getcwd()

            # getting the list of files and folders from the cwd
            liste = os.listdir(cwd)

            # storing the directory name in add
            add = x[1]

            if x[1] in liste:
                # using OS library for changing the directory using the file or folder name
                os.chdir(x[1])
                # f string is used to use the variable add 
                msg = f"Directory has been changed to {add}"

                # sending the message to the client by encoding it with FORMAT="UTF-8"
                clientsocket.send(sub(msg).encode(FORMAT))

            else:
                msg = "File does not exist!"
                clientsocket.send(sub(msg).encode(FORMAT))

        # checking whether the command is dwd or not
        elif (x[0] == 'dwd'):

            # storing file's name
            file = x[1]

            # opening the file whose name is given by the client and reading its data in bytes
            with open(file, 'rb') as file_to_send:

                # using loop to transfer the file's data in chunks of 1024 bytes
                while True:

                    # storing 1024 bytes from the file to data variable by reading the file
                    data = file_to_send.read(1024)

                    # if no data read then it means that no more data is remaining in the file
                    if not data:
                        break
                   
                    # sending all the data to client by passing the data into sub which applies caesar cipher and then encoding the data
                    clientsocket.sendall(sub(data).encode())
                
                file_to_send.close()
                
            # # sending the message to the client that the data is downloaded
            # clientsocket.send("Downloaded!".encode(FORMAT))

            # closing the client's connection
            clientsocket.close()

            # breaking the loop
            break

        # checking whether the command is upd or not
        elif (x[0] == 'upd'):
            
            # storing the name of the file to upload
            name = x[1]

             # creating the file by joining the path of the server to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'wb') as file_to_write:

                # receiving multiple chunks of data from the client
                while True:

                    # storing the received data from the client to data by passing it in the desub which removes the layer of caesar cipher
                    # data is received in chunks of 1024 bytes
                    data = desub(clientsocket.recv(1024).decode(FORMAT))

                    # if no data received then the task is over
                    if not data:
                        break

                    # writing the data received from the client to the created file in the server
                    file_to_write.write(data.encode())

                # closing the file as whole data is already written in the file
                file_to_write.close()
            
            # closing the connection of client
            clientsocket.close()
            break

        # if the command given by the client is different from the five commands then sending the wrong command message to the client
        else:
            msg2 = f"wrong command"

            # sending the data after applying caesar cipher
            clientsocket.send(sub(msg2).encode(FORMAT))

# checking if the mode of encryption is Transpose or not
elif (data == 'Transpose'):

    # using while loop for handling multiple requests from the client
    while True:

        # server is receiving the data from the client. Basaically, it's a command 
        # first the command will be decoded and then it will be passed to transpose which reverses the data because we received reversed data from the client
        data = transpose(clientsocket.recv(1024).decode(FORMAT))

        # storing the command into the list by breaking the command with spaces 
        x = data.split()

        # if no data received then we will break the loop
        if not data:
            break

        # checking whether the command is cwd or not
        elif (x[0] == 'cwd') :

            # getting current working directory by using OS library
            cwd = os.getcwd()

            # reversing the data to send and then encoding it with UTF-8 format
            clientsocket.send(transpose(cwd).encode(FORMAT))

        # checking whether the command is ls or not
        elif (x[0] == 'ls') :

            # getting current working directory by using OS library and storing it in cwd
            cwd = os.getcwd()

            # getting the list of files and folders from the cwd
            liste = os.listdir(cwd)

            # converting the list into string
            liste = str(liste)

            # sending the data by reversing it and then encoding it with UTF-8 format
            clientsocket.send(transpose(liste).encode(FORMAT))

        # checking whether the command is cd or not
        elif (x[0] == 'cd'):

            # getting current working directory by using OS library and storing it in cwd
            cwd = os.getcwd()

            # getting the list of files and folders from the cwd
            liste = os.listdir(cwd)
            
            # storing the directory name in add
            add = x[1]

            if x[1] in liste:
                # using OS library for changing the directory using the file or folder name
                os.chdir(x[1])
                # f string is used to use the variable add 
                msg = f"Directory has been changed to {add}"

                # sending the message to the client by encoding it with FORMAT="UTF-8"
                clientsocket.send(transpose(msg).encode(FORMAT))

            else:
                msg = "File does not exist!"
                clientsocket.send(transpose(msg).encode(FORMAT))
    
        # checking whether the command is dwd or not
        elif (x[0] == 'dwd'):
            file = x[1]

            # opening the file whose name is given by the client and reading its data as string
            with open(file, 'r') as file_to_send:

                # using loop to transfer the file's data in chunks of 1024 bytes
                while True:

                    # storing 1024 bytes from the file to data variable by reading the file
                    data = file_to_send.read(1024)

                    # if no data read then it means that no more data is remaining in the file
                    if not data:
                        break

                    # sending all the data to client by passing the data into transpose which reverses the data and then encoding the data
                    clientsocket.sendall(transpose(data).encode(FORMAT))

                file_to_send.close()
                

            # closing the connection of client
            clientsocket.close()

            # breaking the loop
            break
        
        elif (x[0] == 'upd'):

            # storing the name of the file to upload
            name = x[1]

             # creating the file by joining the path of the server to file name and writing the data into the file
            with open(os.path.join(downloadDir, name), 'w') as file_to_write:

                # receiving multiple chunks of data from the client
                while True:

                    # storing the received data from the client to data by passing it into transpose which again reverses the data
                    data = transpose(clientsocket.recv(1024).decode(FORMAT))

                    # if no data received then the task is over
                    if not data:
                        break

                    # writing the data received from the client to the created file in the server
                    file_to_write.write(data)

                # closing the file as whole data is already written in the file
                file_to_write.close()

            # closing the connection of client
            clientsocket.close()
            break
        
        # if the command given by the client is different from the five commands then sending the wrong command message to the client
        else:
            msg = f"Wrong command :("

            #sending the message by reversing its data and encoding it
            clientsocket.send(transpose(msg).encode(FORMAT))

# closing the socket to shutdown the server
s.close()
    

