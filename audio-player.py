from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from random import sample


class App(tb.Window):
    def __init__(self, title, size, theme='darkly', playlist=[]):
        '''
        # Main window
        ### Parameters:
        - title: Title of the app
        - size: x and y dimensions of the window. This is also the minimum size
        - playlist: array of objects ex. [{"name": "song_name", "filepath": "path/to/file.mp3"}]
        - theme: your custom theme or one of the above:\n
                  'cosmo', 'flatly', 'litera',\n
                  'minty', 'lumen', 'sandstone', 'yeti',\n
                  'pulse', 'united', 'morph', 'journal',\n
                  'darkly', 'superhero', 'solar',\n
                  'cyborg', 'vapor', 'simplex', 'cerculean'
        '''
        super().__init__(themename=theme)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.is_playing = False
        self.playlist = playlist
        self.current_playlist_song_index = 0
        self.current_song = None

        self.main = Main(self)
        self.mainloop()

    def change_theme(self, theme):
        self.style.theme_use(theme)

    def set_playing(self, status: bool):
        self.is_playing = status

    def set_playlist_song_index(self, value: int):
        self.current_playlist_song_index = value

    def set_current_song(self, index: int):
        self.current_song = self.playlist[index]

    def play_next(self):
        self.set_playing(True)
        song_index = self.get_set_next_song_index()
        self.set_current_song(song_index)

    def play_song_by_index(self, index: int):
        self.set_playing(True)
        self.set_current_song(index)

    def pause(self):
        self.set_playing(False)

    def resume(self):
        if not self.current_song:
            self.play_song_by_index(0)
        self.set_playing(True)

    def play_previous(self):
        self.set_playing(True)
        song_index = self.get_set_previous_song_index()
        self.set_current_song(song_index)

    def get_set_next_song_index(self) -> int:
        # Playlist has been played completely
        if self.current_playlist_song_index == len(self.playlist)-1:
            next_index = 0
            self.set_playlist_song_index(next_index)
            return next_index
        next_index = self.current_playlist_song_index + 1
        self.set_playlist_song_index(next_index)
        return next_index

    def get_set_previous_song_index(self) -> int:
        if self.current_playlist_song_index == 0:
            return 0
        next_index = self.current_playlist_song_index - 1
        self.set_playlist_song_index(next_index)
        return next_index

    def shuffle_playlist(self):
        self.playlist = sample(self.playlist, k=len(self.playlist))
        current_song_filepath = self.current_song['filepath']
        new_index = self.get_song_index_by_value(current_song_filepath)
        self.set_playlist_song_index(new_index)

    def get_status(self) -> dict:
        if not self.current_song:
            return None
        return {"is_playing": self.is_playing, "song": self.current_song["name"]}

    def get_playlist(self):
        return self.playlist

    def get_song_index_by_value(self, value: str) -> int:
        for i in range(len(self.playlist)):
            song_name = self.playlist[i]['name']
            song_filepath = self.playlist[i]['filepath']
            if value == song_name or value == song_filepath:
                return i
        return None


class Main(tb.Frame):
    def __init__(self, parent):
        '''
        # Main window
        '''
        self.parent = parent
        default_button_width = 30

        frame = tb.Frame(self.parent, padding=8, width=2)
        frame.grid(column=0, row=0, sticky=N)

        now_playing_label = Label(frame, (0, 0), "Now Playing: ")
        self.song_name_label = Label(frame, (0, 1), "")
        previous_btn = tb.Button(
            frame, text="Previous", command=self.on_previous)
        self.play_pause_btn = tb.Button(
            frame, text="Play", command=self.on_play_pause)
        next_btn = tb.Button(frame, text="Next", command=self.on_next)
        print_btn = tb.Button(frame, text="Print", command=self.on_print)
        shuffle_btn = tb.Button(frame, text="Shuffle", command=self.on_shuffle)

        previous_btn.grid(row=1, column=0, padx=1)
        self.play_pause_btn.grid(row=1, column=1, padx=1)
        next_btn.grid(row=1, column=2, padx=1)
        print_btn.grid(row=1, column=3, padx=5)
        shuffle_btn.grid(row=1, column=4, padx=5)

    def on_previous(self):
        print("Clicked previous")
        self.parent.play_previous()
        self.play_pause_btn.configure(text="Pause")
        self.set_now_playing_label()

    def on_play_pause(self):
        if self.parent.is_playing:
            self.parent.is_playing = False
            self.play_pause_btn.configure(text="Play")
            self.parent.pause()
            print("Clicked pause")
        else:
            self.parent.is_playing = True
            self.play_pause_btn.configure(text="Pause")
            self.parent.resume()
            print("Clicked play (resume)")
            self.set_now_playing_label()

    def on_next(self):
        print("Clicked next")
        self.parent.play_next()
        self.play_pause_btn.configure(text="Pause")
        self.set_now_playing_label()

    def on_shuffle(self):
        print("Clicked shuffle")
        self.parent.shuffle_playlist()

    def on_print(self):
        print(self.parent.get_status())
        print(self.parent.get_playlist())
        print(self.parent.get_song_index_by_value("/to/file/path3.mp3"))

    def set_now_playing_label(self):
        current_song = self.parent.get_status()
        self.song_name_label.change_label(text=current_song['song'])


class ImageWithImport(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, image_path: str, image_dimensions=(150, 150), button_text='Lisää kuva', customizations={}):
        '''
        Uses tkinter Label to show the image and\n
        has button on top to load image from disk.
        '''
        super().__init__(parent)
        default_customizations = {}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        row, col = row_and_column
        load_image = Image.open(image_path)
        load_image = load_image.resize(image_dimensions)
        image = ImageTk.PhotoImage(load_image)

        import_picture_button = tb.Button(
            parent, text=button_text, command=lambda: self.open_image(image_dimensions))
        import_picture_button.grid(column=col, row=row)
        self.picture_field = tb.Label(parent, image=image)
        self.picture_field.image = image
        self.picture_field.grid(column=col, row=row+1, rowspan=3,
                                sticky=N)

    def open_image(self, image_dimensions: tuple):
        file_path = filedialog.askopenfilename(
            filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            load_image = Image.open(file_path)
            load_image = load_image.resize(image_dimensions)
            image = ImageTk.PhotoImage(load_image)

            self.picture_field.configure(image=image)
            self.picture_field.image = image


class Select(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, values: tuple | list, placeholder: str, customizations=None):
        '''
        Uses tkinter Combobox and has on_select binding available\n
        in customizations that returns the selected value

        ### Parameters:
        - values: list or tuple of options that can be selected
        - placeholder: Text shown when nothing is selected
        - customizations: {'width': 100, 'sticky': W, 'state': 'readonly', 'pady': 5, 'on_select': self.bind_function}
        '''
        super().__init__(parent)
        default_customizations = {'width': 100,
                                  'sticky': W,
                                  'state': 'readonly',
                                  'pady': 5,
                                  'on_select': self.bind_function}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        state = default_customizations['state']
        width = default_customizations['width']
        pady = default_customizations['pady']
        sticky = default_customizations['sticky']
        self.binded_command = default_customizations['on_select']
        row, col = row_and_column

        self.select = tb.Combobox(parent,
                                  values=values,
                                  state=state,
                                  width=width)

        self.select.set(placeholder)
        self.select.bind('<<ComboboxSelected>>', self.on_select)
        self.select.grid(row=row, column=col, sticky=sticky, pady=pady)

    def on_select(self, e):
        selected_value = self.select.get()
        self.binded_command(selected_value)

    def bind_function(self, e):
        pass


class EntryWithLabel(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, label_text: str, entry_variable=None, side_by_side=False, validate=None, customizations=None):
        '''
        ttkbootsrap Entry and Label combo.\n
        Can be positioned either label ontop or side by side

        ### Parameters:
        - label_text: What is shown in the label
        - entry_variable: Binding variable for Entry
        - side_by_side: If True then Label is shown on left side and on the same row as the Entry
        - validate: 'number'
            - 'number': Only allows numbers to be inserted to the Entry
        - customizations: {'entry-width': 30, 'label-padding': 10}
        '''

        super().__init__(parent)
        default_customizations = {'entry-width': 30,
                                  'label-padding': 10}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        row, col = row_and_column
        label_padding = default_customizations['label-padding']
        entry_width = default_customizations['entry-width']

        if side_by_side:
            entry_row = row
            entry_col = col + 1
        else:
            entry_row = row + 1
            entry_col = col

        label = tb.Label(parent, text=label_text, padding=label_padding)
        entry = tb.Entry(parent, textvariable=entry_variable,
                         width=entry_width)
        if validate == 'number':
            validatecommand = (self.register(self.validate_digit), '%P')
            entry.config(validate='key', validatecommand=validatecommand)

        label.grid(row=row, column=col, sticky='E')
        entry.grid(row=entry_row, column=entry_col)

    def validate_digit(self, new_text):
        if new_text.isdigit():
            return True
        elif new_text == '':
            return True
        else:
            return False


class Label(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, text: str, customizations=None):
        '''
        ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left'}
        '''
        super().__init__(parent)

        default_customizations = {'sticky': None,
                                  'columnspan': 1,
                                  'justify': 'left'}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        sticky = default_customizations['sticky']
        colspan = default_customizations['columnspan']
        justify = default_customizations['justify']

        row, col = row_and_column

        self.label = tb.Label(parent, text=text, justify=justify)
        self.label.grid(row=row, column=col, columnspan=colspan, sticky=sticky)

    def change_label(self, text: str):
        self.label.configure(text=text)


playlist = [{"name": "song1", "filepath": "/to/file/path.mp3"},
            {"name": "song2", "filepath": "/to/file/path2.mp3"},
            {"name": "song3", "filepath": "/to/file/path3.mp3"}]
App(title='Audio Player', size=(350, 100), playlist=playlist)
