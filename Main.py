import socket
from tkinter import *
from PIL import ImageTk, Image


# constants
IP = "127.0.0.1"
PORT = 1234

root = Tk()
root.title("Rock,Paper and Scissors")
root.geometry("1120x600")

global frame

frame = LabelFrame(root)

########################################################################################################################
#                                                      Image List                                                      #
########################################################################################################################

game = ImageTk.PhotoImage(Image.open("src/game_logo.png"))
play = ImageTk.PhotoImage(Image.open("src/play_button.jpg"))
rock = ImageTk.PhotoImage(Image.open("src/Rock.jpg"))
paper = ImageTk.PhotoImage(Image.open("src/Paper.jpg"))
scissors = ImageTk.PhotoImage(Image.open("src/Scissors.jpg"))
rock_op = ImageTk.PhotoImage(Image.open("src/Rock 1.jpg"))
paper_op = ImageTk.PhotoImage(Image.open("src/Paper 1.jpg"))
scissors_op = ImageTk.PhotoImage(Image.open("src/Scissors 1.jpg"))

image = [rock, scissors, paper]
opp = [rock_op, scissors_op, paper_op]

########################################################################################################################
#                                                      Functions                                                      #
########################################################################################################################


def result(user_in, option_no, string):
    global start
    global nframe

    newframe.destroy()
    nframe = LabelFrame(root)

########################################################################################################################
#                                                Declaring Buttons                                                     #
########################################################################################################################

    new_status = Label(nframe, text=string, padx=530, bd=4, relief=SUNKEN, anchor="center")
    you = Label(nframe, image=image[user_in], padx=5, pady=5, bd=1)
    bot = Label(nframe, image=opp[option_no], padx=5, pady=5, bd=1)
    you_te = Button(nframe, text="YOU", padx=5, pady=5, bd=1)
    bot_te = Button(nframe, text="Opponent", padx=5, pady=5, bd=1)
    vs = Label(nframe, text="vs", padx=5, pady=5, bd=1)
    leave_game = Button(nframe, text="EXIT GAME", padx=50, pady=10, bd=1, relief=SUNKEN, command=root.quit)
    start = Button(nframe, text="REMATCH", padx=10, pady=10, bd=2, relief=SUNKEN, command=lambda: StartF(1))

########################################################################################################################
#                                                      Buttons                                                      #
########################################################################################################################

    nframe.pack()
    new_status.grid(row=0, column=0, columnspan=3, pady=30, sticky=E + W)
    you_te.grid(row=1, column=0, padx=2)
    bot_te.grid(row=1, column=2, padx=2)
    you.grid(row=2, column=0, padx=2)
    vs.grid(row=2, column=1, padx=2)
    bot.grid(row=2, column=2, padx=2, pady=20)
    leave_game.grid(row=3, column=1, padx=50, pady=20, sticky=W + E)
    start.grid(row=3, column=2, padx=50, pady=20, sticky=W + E)


def win(user_in):
    '''

    :param user_in:
    :return:
    '''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((IP, PORT))

    client_socket.setblocking(False)

    while True:
        user_in = str(user_in)
        client_socket.send(bytes(user_in, 'utf-8'))
        j = 0
        for k in range(100000):
            j += k
        while True:
            try:
                winner = client_socket.recv(1024)
                if winner:
                    winner = winner.decode('utf-8')
                    break
            except BlockingIOError:
                continue
            except ConnectionRefusedError:
                StartF(0)
        user_in = int(winner[6])
        print(user_in)
        option_no = int(winner[7])
        print(option_no)
        strng = winner[:6]

        result(user_in, option_no, strng)
        break


def StartF(i):
    global newframe
    if i == 0:
        frame.destroy()
    else:
        nframe.destroy()
    newframe = LabelFrame(root)

    n_status = Label(newframe, text="Choose", padx=530, bd=4, relief=SUNKEN, anchor="center")
    rock_te = Button(newframe, text="ROCK", padx=5, pady=5, bd=1, command=lambda: win(0))
    paper_te = Button(newframe, text="PAPER", padx=5, pady=5, bd=1, command=lambda: win(2))
    scissors_te = Button(newframe, text="SCISSORS", padx=5, pady=5, bd=1, command=lambda: win(1))
    rock_in = Button(newframe, image=rock, padx=5, pady=5, bd=1, command=lambda: win(0))
    paper_in = Button(newframe, image=paper, padx=5, pady=5, bd=1, command=lambda: win(2))
    scissors_in = Button(newframe, image=scissors, padx=5, pady=5, bd=1, command=lambda: win(1))
    leave_game = Button(newframe, text="EXIT GAME", padx=50, pady=10, bd=1, relief=SUNKEN, command=root.quit)

    newframe.pack()
    n_status.grid(row=0, column=0, columnspan=3, pady=30, sticky=E + W)
    rock_te.grid(row=1, column=0, padx=2)
    paper_te.grid(row=1, column=1, padx=2)
    scissors_te.grid(row=1, column=2, padx=2)
    rock_in.grid(row=2, column=0, padx=2)
    paper_in.grid(row=2, column=1, padx=2)
    scissors_in.grid(row=2, column=2, padx=2, pady=20)
    leave_game.grid(row=3, column=1, padx=50, pady=20, sticky=W + E)


status = Label(frame, text="Welcome!", padx=530, bd=4, relief=SUNKEN, anchor="center")

frame.pack()

start = Button(frame, image=play, padx=10, pady=10, bd=2, relief=SUNKEN, command=lambda: StartF(0))
lab = Label(frame, image=game, padx=10, pady=50, bd=2, relief=SUNKEN)

status.grid(row=0, column=0, columnspan=3, pady=20, sticky=E + W)
lab.grid(row=1, column=0, columnspan=3, pady=50, sticky=W + E)
start.grid(row=2, column=0, columnspan=3, sticky=W + E)
root.mainloop()
