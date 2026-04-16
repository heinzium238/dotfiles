#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import sys, subprocess

class BrightnessDialog(Gtk.Window):
    def __init__(self, option):
            super().__init__(title="Session")
            screen = self.get_screen()
            visual = screen.get_rgba_visual()
            if visual and screen.is_composited():
                self.set_visual(visual)
            css = b"""
            window {
                background-color: rgba(45, 45, 105, 0.5);
                border-radius: 10px;
            }

            progressbar trough {
                border-radius: 1px;
                background-color: #3b3b4f;

            }

            progressbar progress {
                border-radius: 1px;
                background-color: #5f5ff3;
                background-image: none;
            }

            label {
            color: #b9b9b9;
            }
            """

            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(css)
            Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.set_border_width(12)
            self.set_position(Gtk.WindowPosition.CENTER)
            self.set_keep_above(True)
            self.set_wmclass("brightness-dialog", "BrightnessDialog")
            self.connect("key-press-event", self.on_key_press)


            grid = Gtk.Grid()
            self.add(grid)

            match option:

                case 'brightness':
                    brightness = self.calc_brightness()
                    brightness_level = Gtk.Label(label=f'------- {int(brightness)} -------')
                    grid.attach(brightness_level, 1, 0, 1, 1)

                    progress = Gtk.ProgressBar()
                    progress.set_fraction(brightness/100)
                    grid.attach(progress, 1, 2, 1, 1)
                    progress.set_valign(Gtk.Align.CENTER)

                    label_1 = Gtk.Label(label=' 󰃞  ')
                    grid.attach(label_1, 0, 2, 1, 1)

                    label_2 = Gtk.Label(label=' 󰃠 ')
                    grid.attach(label_2, 2, 2, 1, 1)

                case 'volume':
                    volume = self.calc_volume()
                    volume_level = Gtk.Label(label=f'------- {volume[0]} -------')
                    grid.attach(volume_level, 1, 0, 1, 1)

                    progress = Gtk.ProgressBar()
                    progress.set_fraction(volume[1]/100)
                    grid.attach(progress, 1, 2, 1, 1)
                    progress.set_valign(Gtk.Align.CENTER)

                    label_1 = Gtk.Label(label=' 󰕿  ')
                    grid.attach(label_1, 0, 2, 1, 1)

                    label_2 = Gtk.Label(label=' 󰕾 ')
                    grid.attach(label_2, 2, 2, 1, 1)

            GLib.timeout_add(400, self.auto_close)

    def calc_brightness(self):

            result = subprocess.run(['brightnessctl', 'g'], capture_output=True, text=True)
            current = int(result.stdout.strip())
            result = subprocess.run(['brightnessctl', 'm'], capture_output=True, text=True)
            max_brightness = int(result.stdout.strip())
            percentage = (current / max_brightness) * 100
            return percentage

    def calc_volume(self):
        result = subprocess.run(['pamixer', '--get-volume'], capture_output=True, text=True)
        if 'false' in subprocess.run(['pamixer', '--get-mute'], capture_output=True, text=True).stdout:
            return int(result.stdout.strip('\n')), int(result.stdout.strip('\n'))
        else:
            return '󰝟', int(result.stdout.strip('\n'))

    def on_key_press(self, widget, event):
        if event.keyval == 65307:  # Escape key
            self.close()

    def auto_close(self):
        self.close()
        return False


win = BrightnessDialog(sys.argv[1])
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
print(type(1) == int)
