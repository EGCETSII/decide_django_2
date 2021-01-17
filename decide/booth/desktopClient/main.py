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
        self.builder.add_from_file('main.ui')
        self.builder.connect_signals(self)

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

    def on_login_clicked(self, button, false=None):
        username = self.builder.get_object('username').get_text()
        password = self.builder.get_object('password').get_text()
        voting_id = self.builder.get_object('votingId').get_text()

        COLOR_INVALID = Color(50000, 0, 0)
        self.builder.get_object('usernameLabelError').modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
        self.builder.get_object('passwordLabelError').modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
        self.builder.get_object('votingIdLabelError').modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)

        if not username:
            self.builder.get_object('usernameLabelError').set_text("Empty Username")
        else:
            self.builder.get_object('usernameLabelError').set_text("")

        if not password:
            self.builder.get_object('passwordLabelError').set_text("Empty Password")
        else:
            self.builder.get_object('passwordLabelError').set_text("")

        if not voting_id:
            self.builder.get_object('votingIdLabelError').set_text("Must insert voting identifier")
        else:
            self.builder.get_object('votingIdLabelError').set_text("")

        if password and username and voting_id and voting_id:
            self.cur.execute("SELECT id, username, password from public.auth_user where username = %s", [username])
            user = self.cur.fetchone()

            if not user:
                print("User not found")
                self.builder.get_object('usernameLabelError').set_text("Invalid user or password")
            else:
                cryptedPassword = user[2]
                passOk = django.contrib.auth.hashers.check_password(password, cryptedPassword)
                check_voting_access = self.check_voting_access(user, voting_id)
                check_already_voted = self.check_already_voted(user, voting_id)
                if passOk and check_voting_access and check_already_voted == False:
                    print("Correct user")
                    user_token = user[0]
                    print("User token " + str(user_token))
                    self.voting(user, voting_id)
                elif passOk:
                    self.builder.get_object('votingIdLabelError').set_text("You don't have access to the voting")
                else:
                    print("Invalid password")
                    self.builder.get_object('usernameLabelError').set_text("Invalid user or password")

    def logged_user(self, user):
        self.builder.add_from_file('list_votings.ui')
        self.cur.execute("SELECT * from voting_voting")
        votings = self.cur.fetchall()

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        for voting in votings:
            print(voting[1] + " - "+ voting[2])

    def check_voting_access(self, user, voting_id):
        start_date_ok = False
        end_date_ok = False
        voting_id_ok = False

        self.cur.execute("SELECT NOW()")
        current_date_str = str(self.cur.fetchone()[0])[:-6]
        current_date = datetime.datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S.%f')

        self.cur.execute("SELECT * from voting_voting where id = %s", [voting_id])
        voting = self.cur.fetchone()

        if voting == None:
            self.builder.get_object('votingIdLabelError').set_text("No se ha encontrado")
        else:
            start_date_str = str(voting[3])[:-6]
            start_date = datetime.datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S.%f')
            start_date_ok = start_date <= current_date

            end_date_ok = voting[4] == None

            self.cur.execute("SELECT * from census_census where voting_id = %s and voter_id = %s", [voting_id, user[0]])
            select = self.cur.fetchone()
            voting_id_ok = select != None

        return start_date_ok and end_date_ok and voting_id_ok

    def check_already_voted(self, user, voting_id):

        self.cur.execute("SELECT * from store_vote where voting_id = %s and voter_id = %s", [voting_id,user[0]])
        result = self.cur.fetchone()

        return result != None

    def voting(self, user, voting_id):
        # self.builder.add_from_file('voting.ui')
        self.cur.execute("SELECT * from voting_voting where id = %s", [voting_id])
        voting = self.cur.fetchone()

        votingWin = VotingWindow(voting)
        votingWin.show_all()
        votingWin.fullscreen()

class VotingWindow(Gtk.Window):
    def __init__(self, voting):
        Gtk.Window.__init__(self, title=str(voting[0]) + " - " + str(voting[1]))

        try:
            conn = psycopg2.connect(dbname="decidedb2", user="decide2", password="decide", host="127.0.0.1", port="5432")
            self.cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            print("Conectado")
        except Exception as e:
            print(e)

        self.box = Gtk.Box(spacing=6, orientation="vertical")
        self.add(self.box)

        self.label = Gtk.Label(label=str(voting[0]) + " - " + str(voting[1]))
        self.box.pack_start(self.label, True, True, 0)
        self.label = Gtk.Label(label="Ejemplo de pregunta")
        self.box.pack_start(self.label, True, True, 0)
        radioButton1 = Gtk.RadioButton("Opción 1")
        self.box.pack_start(radioButton1, True, True, 0)
        radioButton2 = Gtk.RadioButton.new_from_widget(radioButton1)
        radioButton2.set_label("Opción 2")
        self.box.pack_start(radioButton2, True, True, 0)
        radioButton3 = Gtk.RadioButton.new_from_widget(radioButton1)
        radioButton3.set_label("Opción 3")
        self.box.pack_start(radioButton3, True, True, 0)
        '''
        self.cur.execute("SELECT question_id from voting_voting_question where voting_id = %s", [voting[0]])
        questionsIdentifiers = self.cur.fetchall()

        questions = []
        questionsOptions = []

        for questionId in questionsIdentifiers:
            self.cur.execute("SELECT * from voting_question where id = %s", [questionId[0]])
            question = self.cur.fetchall()
            questions.append((question[0][0], question[0][1]))

        for q in questions:
            self.cur.execute("SELECT * from voting_questionoption where question_id = %s", [q[0]])
            options = self.cur.fetchall()
            for option in options:
                questionsOptions.append((option[0], option[1], option[2], option[3]))

        for q in questions:
            question_description = Gtk.Label(label="Question: "+str(q[1]))
            self.box.pack_start(question_description, True, True, 0)

            for option in questionsOptions:
                i = 0
                if option[3] == q[0]:
                    if i == 0:
                        radioButton1 = Gtk.RadioButton("Option: "+str(option[0]))
                        self.box.pack_start(radioButton1, True, True, 0)
                    else:
                        radioButton2 = Gtk.RadioButton.new_from_widget(radioButton1)
                        radioButton2.set_label("Option: "+str(option[0]))
                        self.box.pack_start(radioButton2, True, True, 0)
        '''
        sendButton = Gtk.Button.new_with_label("Votar")
        self.box.pack_start(sendButton, True, True, 0)

    def on_logout_clicked(self, window):
        user = []
        Gtk.VotingWindow.destroy()



def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
