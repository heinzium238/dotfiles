#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import subprocess

class SessionDialog(Gtk.Window):
    def __init__(self):
        super().__init__(title="Session")
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        css = b"""
        window {
            background-color: rgba(65, 65, 215, 0.65);
            border-radius: 10px;
        }
        button {
            background: #313244;
            color: #cdd6f4;
            border: 2px solid #89b4fa;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        button:hover, button:focus {
            background: #4a74ca;
            border: 2px solid #121272;
        }
        """

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_wmclass("session-dialog", "SessionDialog")
        self.connect("key-press-event", self.on_key_press)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.add(box)

        buttons = [
            ("Lock", self.lock),
            ("Logout", self.logout),
            ("Shutdown", self.shutdown),
            ("Reboot", self.reboot),
            ("Cancel", self.cancel)
        ]

        for label, callback in buttons:
            btn = Gtk.Button(label=label)
            btn.connect("clicked", callback)
            box.pack_start(btn, True, True, 0)

    def lock(self, widget):
        subprocess.run([
            "i3lock-color",
            "-i", "/home/hannese/.cache/betterlockscreen/current/wall_dimpixel.png",
            "--clock",
            "--time-str=%H:%M",
            "--date-str=%D",
            "--keyhl-color=5c5cff",
            "--bshl-color=ff2a2a",
            "--ring-color=1f1fd94e",
            "--inside-color=00000034",
            "--verif-text=Unlocking...",
            "--wrong-text=WRONG",
        ])
        self.close()

    def logout(self, widget):
        subprocess.run(["bspc", "quit"])
        self.close()

    def reboot(self, widget):
        subprocess.run(["systemctl", "reboot"])

    def shutdown(self, widget):
        subprocess.run(["systemctl", "poweroff"])

    def cancel(self, widget):
        self.close()

    def on_key_press(self, widget, event):
        if event.keyval == 65307:  # Escape key
            self.close()

win = SessionDialog()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
