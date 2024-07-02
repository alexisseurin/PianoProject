import time
import tkinter as tk
import threading
from tkinter import PhotoImage, ttk
#import pyglet

class App(tk.Tk):
	def __init__(self):

		super().__init__()

		# Création de la fenêtre principale
		self.title("Rozik")
		self.iconbitmap("icons/myIcon.ico")
		self.app_width = 490
		self.app_height = 600

		self.screen_width = self.winfo_screenwidth()
		self.screen_height = self.winfo_screenheight()

		self.x = (self.screen_width/2) - (self.app_width/2)
		self.y = (self.screen_height/2) - (self.app_height/2)

		self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
		self.resizable(False, False)

		# Define style
		self.style = ttk.Style(self)
		self.style.theme_use("clam")

		#down = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0e\x00\x00\x00\x07\x08\x06\x00\x00\x008G|\x19\x00\x00\x00\tpHYs\x00\x00\x10\x9b\x00\x00\x10\x9b\x01t\x89\x9cK\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00OIDAT\x18\x95\x95\xce\xb1\x0e@P\x0cF\xe1\xefzI\x8fc$\x12\x111\x19\xec\x9e\x12\xcb\x95 A\x9d\xa4K\xff\x9e\xb6\t\x13J\xffX \xa1\xc7\x16\xac\x19\xc5\xb1!*\x8fy\xf6BB\xf7"\r_\xff77a\xcd\xbd\x10\xedI\xaa\xa3\xd2\xf9r\xf5\x14\xee^N&\x14\xab\xef\xa9\'\x00\x00\x00\x00IEND\xaeB`\x82'
		#imgDown = tk.PhotoImage(master=self, data=down)
		#self.style.element_create('down', 'image', imgDown)

		self.style.layout('down.TMenubutton', [('Menubutton.border',
		{'sticky': 'nswe',
		'children': [('Menubutton.focus',
			{'sticky': 'nswe',
			'children': [('Menubutton.down', {'side': 'right', 'sticky': ''}),  # replace the indicator by down arrow
			('Menubutton.padding',
				{'expand': '1',
				'sticky': 'we',
				'children': [('Menubutton.label',
				{'side': 'left', 'sticky': ''})]})]})]})])

		self.style.configure('my.TButton', font=('Montserrat ExtraBold', 11))

		#self.montserrat_medium = pyglet.font.add_file('./fonts/Montserrat-Medium.ttf')
		#self.montserrat_black = pyglet.font.add_file('./fonts/Montserrat-ExtraBold.ttf')
	  
		self.canvas = tk.Canvas(self, bg='white', width=350, height=200)

		# Creating a photoimage object to use image
		photo_2 = PhotoImage(file = "./icons/note.png")
		# Resizing image to fit on button
		photoimage_2 = photo_2.subsample(2, 2)
		label_bis2 = tk.Label(image=photoimage_2)
		label_bis2.image = photoimage_2
	  
		# Création de la liste déroulante pour la tonalité
		self.tonality_label = tk.Label(text=" Gamme", image = photoimage_2, compound = "left")
		self.tonality_label.config(font=("Montserrat Medium", 10))
		self.tonality_label.grid(row=0, column=0, sticky="W", padx=15,pady=15)

		tonalities = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
		self.tonality_var = tk.StringVar(self)
		self.tonality_var.set(tonalities[0])
		self.tonality_dropdown = ttk.OptionMenu(self, self.tonality_var, *tonalities, style='my.TButton'  )
		self.tonality_dropdown.configure(style='down.TMenubutton')
		self.tonality_dropdown["menu"].configure(font=("Montserrat Medium",9))
		
		self.tonality_dropdown.grid(row=0, column=0, sticky="W", padx=120,pady=15)
		self.tonality_dropdown.config(width=10)
		

		# Creating a photoimage object to use image
		photo_1 = PhotoImage(file = "./icons/text.png")
		# Resizing image to fit on button
		photoimage_1 = photo_1.subsample(2, 2)
		label_bis = tk.Label(image=photoimage_1)
		label_bis.image = photoimage_1

		# Création de la zone de texte pour le texte à convertir
		self.text_label = tk.Label(text=" Texte à convertir", image = photoimage_1, compound = "left")
		self.text_label.config(font=("Montserrat Medium", 10))
		self.text_label.grid(row=1, column=0, sticky="W", padx=15,pady=0)

		self.text_entry = tk.Text(self, width=50, height=10)
		self.text_entry.config(font=("Montserrat Medium", 10))
		self.text_entry.grid(row=2, column=0, padx=15,pady=5)

		self.text_label_2 = tk.Label(text="")
		self.text_label_2.config(font=("Montserrat Medium", 11))
		self.text_label_2.grid(row=3, column=0, sticky="W", padx=80,pady=10)

		# Creating a photoimage object to use image
		photo = PhotoImage(file = "./icons/play.png")
		# Resizing image to fit on button
		photoimage = photo.subsample(2, 2)
		label = tk.Label(image=photoimage)
		label.image = photoimage

		self.play_button = ttk.Button(text="Jouer", command=self.callback, image = photoimage, compound = "left" , style='my.TButton')
		self.play_button.grid(row=3, column=0, padx=15,pady=15)

		# Création de l'octave de piano
		self.piano = tk.Canvas(self, width=350, height=200)
		self.piano.grid(row=4, column=0, padx=10 ,pady=10)

		# Dessin des touches blanches et noires de l'octave de piano
		self.y1 = 0
		self.y2_white = 200
		self.y2_black = 100
		self.fill_white = "white"
		self.fill_black = "black"
		self.outline = "black"

		# 7 white rectangles
		self.rect_1 = self.piano.create_rectangle(0, self.y1, 50, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_2 = self.piano.create_rectangle(50, self.y1, 100, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_3 = self.piano.create_rectangle(100, self.y1, 150, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_4 = self.piano.create_rectangle(150, self.y1, 200, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_5 = self.piano.create_rectangle(200, self.y1, 250, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_6 = self.piano.create_rectangle(250, self.y1, 300, self.y2_white, fill=self.fill_white, outline=self.outline)
		self.rect_7 = self.piano.create_rectangle(300, self.y1, 350, self.y2_white, fill=self.fill_white, outline=self.outline)
		# 5 black rectangles
		self.rect_8 = self.piano.create_rectangle(37.5, self.y1, 62.5, self.y2_black, fill=self.fill_black, outline=self.outline)
		self.rect_9 = self.piano.create_rectangle(87.5, self.y1, 112.5, self.y2_black, fill=self.fill_black, outline=self.outline)
		self.rect_10 = self.piano.create_rectangle(187.5, self.y1, 212.5, self.y2_black, fill=self.fill_black, outline=self.outline)
		self.rect_11 = self.piano.create_rectangle(237.5, self.y1, 262.5, self.y2_black, fill=self.fill_black, outline=self.outline)
		self.rect_12 = self.piano.create_rectangle(287.5, self.y1, 312.5, self.y2_black, fill=self.fill_black, outline=self.outline)
	
		self.rectangles = [
			[self.rect_1, self.fill_white],
			[self.rect_2, self.fill_white],
			[self.rect_3, self.fill_white],
			[self.rect_4, self.fill_white],
			[self.rect_5, self.fill_white],
			[self.rect_6, self.fill_white],
			[self.rect_7, self.fill_white],
			[self.rect_8, self.fill_black],
			[self.rect_9, self.fill_black],
			[self.rect_10, self.fill_black],
			[self.rect_11, self.fill_black],
			[self.rect_12, self.fill_black]
		]

		# Dictionnaire
		self.characters = {
			"C": {
				".": {[1,1]},
				"q": {[1,2],[1,2]}, # 1,8 = touche blanche + place couleur alternative dans le clavier du piano
				"u": {[1,3],[1,9]}, # MAJEURE et MINEURE
				
				"m": {[1,4]},
				"s": {[1,5],[1,10]},
				"@": {[2,8,1]},
				"x": {[2,8,2,8]},
				"o": {[2,8,3,9]},
				"p": {[2,8,4]},
				"n": {[2,8,5,10]},
				"?": {[3,9,1]},
				"j": {[3,9,2,8]},
				"i": {[3,9,3,9]},
				"g": {[3,9,4]},
				"r": {[3,9,5,10]},
				",": {[4,1]},
				"k": {[4,2,8]},
				"e": {[4,3,9]},
				"b": {[4,4]},
				"t": {[4,5,10]},
				"!": {[5,10,1]},
				"w": {[5,10,2,8]},
				"a": {[5,10,3,9]},
				"v": {[5,10,4]},
				"l": {[5,10,5,10]},
				"\"": {[6,11,1]},
				"z": {[6,11,2,8]},
				"y": {[6,11,3,9]},
				"h": {[6,11,4]},
				"d": {[6,11,5,10]},
				"(": {[7,12,1]},
				";": {[7,12,2,8]},
				"w": {[7,12,3,9]},
				"f": {[7,12,4]},
				"c": {[7,12,5,10]}
			}
		}


		self.colors = {  
			"C": ["SlateGray3", "red3", "aquamarine", "goldenrod1", "green3", "dodger blue", "magenta3", "red3", "aquamarine", "green3", "dodger blue", "magenta3"],
			"C#": ["magenta3", "red3", "aquamarine", "aquamarine", "green3", "dodger blue", "magenta3", "SlateGray3", "red3", "goldenrod1", "green3", "dodger blue"],
			"D": ["magenta3", "SlateGray3", "red3", "aquamarine", "goldenrod1", "green3", "dodger blue", "magenta3", "red3", "aquamarine", "green3", "dodger blue"],
			"D#": ["dodger blue", "magenta3", "red3", "red3", "aquamarine", "green3", "dodger blue", "magenta3", "SlateGray3", "aquamarine", "goldenrod1", "green3"],
			"E": ["dodger blue", "magenta3", "SlateGray3", "red3", "aquamarine", "goldenrod1", "green3", "dodger blue", "magenta3", "red3", "aquamarine", "green3"],
			"F": ["green3", "dodger blue", "magenta3", "SlateGray3", "red3", "aquamarine", "green3", "dodger blue", "magenta3", "red3", "aquamarine", "goldenrod1"],
			"F#": ["green3" "dodger blue", "magenta3", "magenta3", "red3", "aquamarine", "goldenrod1", "green3", "dodger blue", "SlateGray3", "red3", "aquamarine"],
			"G": ["goldenrod1", "green3", "dodger blue", "magenta3", "SlateGray3", "red3", "aquamarine", "green3", "dodger blue", "magenta3", "red3", "aquamarine"],
			"G#": ["aquamarine", "green3", "dodger blue", "dodger blue", "magenta3", "red3", "aquamarine", "goldenrod1", "green3", "magenta3", "SlateGray3", "red3"],
			"A": ["aquamarine", "goldenrod1", "green3", "dodger blue", "magenta3", "SlateGray3", "red3", "aquamarine", "green3", "dodger blue", "magenta3", "red3"],
			"A#": ["red3", "aquamarine", "green3", "green3", "dodger blue", "magenta3", "red3", "aquamarine", "goldenrod1", "dodger blue", "magenta3", "SlateGray3"],
			"B": ["red3", "aquamarine", "goldenrod1", "green3", "dodger blue", "magenta3", "SlateGray3", "red3", "aquamarine", "green3", "dodger blue", "magenta3"]
		}

	# Fonction pour convertir un caractère en note musicale
	def char_to_note(self, myString, tonality):
		
		# Récupération de la liste des notes de la tonalité sélectionnée
		self.color_list = self.colors[tonality]

		self.listOfChars = list()
		
		for character in myString:
			self.listOfChars.append(character)

		print("texte en char : ",self.listOfChars)

		return self.color_list, self.listOfChars
	
	# Define a function to change the state of the Widget
	def change_color(self, tab, tonality):
		print("change color")
		
		for row in tab[1]:

			for key, value in self.characters[tonality].items():

				if row == key:
					print("key: ", key)
					print("value: ", value)
					value[0] -= 1
					value[1] -= 1

					self.text_label_2.config(text=key)
					time.sleep(0.4)
					self.piano.itemconfig(self.rectangles[value[0]][0], fill=tab[0][value[0]])
					time.sleep(0.4)
					self.piano.itemconfig(self.rectangles[value[0]][0], fill=self.rectangles[value[0]][1])
					
					time.sleep(0.4)

					self.piano.itemconfig(self.rectangles[value[1]][0], fill=tab[0][value[1]])
					time.sleep(0.4)
					self.piano.itemconfig(self.rectangles[value[1]][0], fill=self.rectangles[value[1]][1])

					value[0] += 1
					value[1] += 1  
		
		self.play_button["state"] = "normal"
		self.text_label_2.config(text="")
		

	# Fonction pour jouer une note musicale
	"""def play_music_note(self, note):
		player = musicalbeeps.Player(volume = 0.3, mute_output = False)

		# Lecture de la note
		#player.play_note("B", 0.4)
		
		#piano.delete(myrect) #Deletes the rectangle
		#piano.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
		#player.play_note("C5", 0.4)
	"""
	
	def callback(self):
		self.play_button["state"] = "disabled"
		print("--------")
		print("CALLBACK")
		print("--------")

		# Récupération de la tonalité sélectionnée et du texte à convertir
		tonality = self.tonality_var.get()
		text = self.text_entry.get("1.0", "end").lower()
		

		print("tonalité:", tonality)
		print("texte:", text)

		self.text_length = len(text)-1
		print(self.text_length)

		# Conversion du texte en notes musicales (liées à la tonalité choisie)
		self.text_convert = self.char_to_note(text, tonality)
		print(self.text_convert)

		
		t = threading.Thread(target=self.change_color, args=(self.text_convert, tonality,)) 
		t.start()
   

		

if __name__ == '__main__':
	app = App()
	app.mainloop()