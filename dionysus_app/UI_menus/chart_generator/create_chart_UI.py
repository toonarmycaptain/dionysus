import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from dionysus_app.UI_menus.UI_functions import save_as_dialogue


def save_chart_dialogue(default_chart_name: str, class_save_folder_path):
    """
    Calls save as dialogue to get user input for chart image file save
    name and location. Supplies defaults, returns user chosen path
    string.

    :param default_chart_name: str
    :param class_save_folder_path: Path or str
    :return: str
    """
    class_save_folder_str = str(class_save_folder_path)
    save_chart_path_str = save_as_dialogue(title_str='Save chart image as:',
                                           filetypes=[('.png', '*.png'), ("all files", "*.*")],
                                           suggested_filename=default_chart_name,
                                           start_dir=class_save_folder_str
                                           )
    return save_chart_path_str


def display_image_save_as(chart_image_path: str):
    """
    Displays the given image path in a window titled with the filename.
    Supplies a button "Save as" below, which quits the window. Save as
    dialogue is called separately (ideally directly subsequently, from
    a UI perspective.

    :param chart_image_path: str or Path object.
    :return: None
    """
    root = tk.Tk()
    root.title(Path(chart_image_path).name)  # Adding Path() allows string or Path object.
    root.geometry("960x580")  # Half dimensions, about a quarter of full image.

    image_display = ImageDisplay(image_path=chart_image_path, master=root)
    image_display.mainloop()

    root.destroy()


class ImageDisplay(tk.Frame):
    def __init__(self, image_path=None, master=None):
        super().__init__(master)
        self.master = master

        if image_path:
            self.image_path = image_path
            self.pack()
            self.create_image_and_button()
        else:
            pass  # don't instantiate?

    def create_image_and_button(self):
        self.create_image_widget()
        self.create_save_as_button_widget()

    def create_image_widget(self):
        self.full_chart_image = Image.open(self.image_path)
        self.display_sized_image = self.full_chart_image.resize((960, 540), Image.ANTIALIAS)

        self.display_image = ImageTk.PhotoImage(self.display_sized_image, master=self.master)
        self.image_panel = tk.Label(self, image=self.display_image)
        self.image_panel.pack(side="top", fill="both", expand="yes")

    def create_save_as_button_widget(self):
        self.quit = tk.Button(self, text="Save as", font=('Arial', 24),
                              command=self.quit)
        self.quit.pack(side="bottom")