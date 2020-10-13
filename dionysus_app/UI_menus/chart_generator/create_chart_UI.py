import tkinter as tk

from pathlib import Path
from typing import Optional

from PIL import Image, ImageTk

from dionysus_app.UI_menus.UI_functions import save_as_dialogue


def save_chart_dialogue(default_chart_name: str,
                        class_save_folder_path: Path) -> Optional[Path]:
    """
    Calls save as dialogue to get user input for chart image file save
    name and location. Supplies defaults, returns user chosen path, or
    None if user cancels save.

    :param default_chart_name: str
    :param class_save_folder_path: Path
    :return: Path or None
    """
    class_save_folder_str = str(class_save_folder_path)
    return save_as_dialogue(title_str='Save chart image as:',
                            filetypes=[('.png', '*.png'), ("all files", "*.*")],
                            suggested_filename=default_chart_name,
                            start_dir=class_save_folder_str
                            )


def display_image_save_as(chart_image_path: Path) -> bool:
    """
    Displays given image in a window titled with the default filename.

    Supplies a button "Save as" below, which quits the window. Save as
    dialogue is called separately (ideally directly subsequently, from
    a UI perspective).

    Returns a bool based on whether user desires to save image, as
    indicated by clicking "Save as" button or clicking 'x' to quit the
    image display window.

    :param chart_image_path: Path object.
    :return: bool
    """
    root = tk.Tk()
    root.title(chart_image_path.name)
    root.geometry("960x580")  # Half dimensions, about a quarter of full image.

    image_display = ImageDisplay(image_path=chart_image_path, master=root)
    user_did_not_cancel = True

    def user_cancels() -> None:
        """
        Callback where user quit/clicked x on the image display window.

        Register by changing user_did_not_cancel to False.
        Quit the root window, as it will not be closed by the save-as
        button click handler in ImageDisplay.
        """
        user_did_not_cancel = False
        # Destroy window:
        root.quit()

    root.protocol("WM_DELETE_WINDOW", user_cancels)

    root.mainloop()
    user_wants_to_save = user_did_not_cancel and image_display.save_as_button_clicked
    # Destroy tk instance.
    root.destroy()
    return user_wants_to_save


class ImageDisplay(tk.Frame):
    def __init__(self, image_path: Path = None, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.save_as_button_clicked = False

        if image_path:
            self.image_path = image_path
            self.pack()
            self.create_image_and_button()
        # else:
        #     pass  # don't instantiate?

    def create_image_and_button(self) -> None:
        self.create_image_widget()
        self.create_save_as_button_widget()

    def create_image_widget(self) -> None:
        self.full_chart_image = Image.open(self.image_path)
        self.display_sized_image = self.full_chart_image.resize((960, 540), Image.ANTIALIAS)

        self.display_image = ImageTk.PhotoImage(self.display_sized_image, master=self.master)
        self.image_panel = tk.Label(self, image=self.display_image)
        self.image_panel.pack(side="top", fill="both", expand=True)

    def create_save_as_button_widget(self) -> None:
        self.save_as_button = tk.Button(self, text="Save as", font=('Arial', 24),
                                        command=self.register_save_as_click)
        self.save_as_button.pack(side="bottom")

    def register_save_as_click(self) -> None:
        self.save_as_button_clicked = True
        self.quit()
