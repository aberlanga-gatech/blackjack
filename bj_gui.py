import tkinter as tk

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

CARD_WIDTH = 256
CARD_HEIGHT = 362
MARGIN = -200
XSPACING = CARD_WIDTH + MARGIN
YSPACING = CARD_HEIGHT + MARGIN
OFFSET = 5
BACKGROUND = '#070'

# define the window
window = tk.Tk()
window.title('Blackjack')
window.configure(width=720, height=480)
window.configure(background=BACKGROUND)
window.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

card_frame = tk.Frame(window, background=BACKGROUND)
card_frame.pack()

# dealer canvas
dealer_canvas = tk.Canvas(card_frame, background='blue', width=WINDOW_WIDTH/1.5, height=CARD_HEIGHT/2)
dealer_canvas.grid(row=0, column=0)

# make a spacer
spacer = tk.Frame(card_frame, background=BACKGROUND, height=CARD_HEIGHT/2)
spacer.grid(row=1, column=0)

# player canvas
player_canvas = tk.Canvas(card_frame, background='yellow', width=WINDOW_WIDTH/1.5, height=CARD_HEIGHT/2)
player_canvas.grid(row=2, column=0)
    
img = tk.PhotoImage(file="cardimgs/ace_clubs.png")

#resize the image
img = img.subsample(2, 2)

counter = -1

def more():
    global counter
    counter += 1
    player_canvas.create_image(CARD_WIDTH*0.5*counter, 0, image=img, anchor="nw")

button = tk.Button(window, text="Hit", command=more).pack()

window.mainloop()



