import gi
import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from gi.repository.Gdk import Color
import os, sys, psycopg2, psycopg2.extras, hashlib
import django.contrib.auth.hashers

class GUI:
    def __init__(self):
        django.contrib.auth.hashers.settings.configure()

        self.builder = Gtk.Builder()
        self.builder.add_from_file('login.ui')
        self.builder.connect_signals(self)

        self.builder.get_object('username').set_text("alvaro")
        self.builder.get_object('votingId').set_text("1")


        try:
            conn = psycopg2.connect(dbname="decidedb2", user="decide2", password="decide", host="127.0.0.1", port="5432")
            self.cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            print("Conectado")
        except Exception as e:
            print(e)

        window = self.builder.get_object('window')
        window.show_all()
        window.fullscreen()

    def on_window_destroy(self, window):
        Gtk.main_quit()

    def button_clicked(self, button, false=None):
        username = self.builder.get_object('username').get_text()
        password = self.builder.get_object('password').get_text()


        COLOR_INVALID = Color(50000, 0, 0)
        self.builder.get_object('usernameLabelError').modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
        self.builder.get_object('passwordLabelError').modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)

        if not username:
            self.builder.get_object('usernameLabelError').set_text("Empty Username")
        else:
            self.builder.get_object('usernameLabelError').set_text("")

        if not password:
            self.builder.get_object('passwordLabelError').set_text("Empty Password")
        else:
            self.builder.get_object('passwordLabelError').set_text("")

        if password and username:
            self.cur.execute("SELECT id, username, password from public.auth_user where username = %s", [username])
            user = self.cur.fetchone()

            if not user:
                print("User not found")
                self.builder.get_object('usernameLabelError').set_text("Invalid user or password")
            else:
                

def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
