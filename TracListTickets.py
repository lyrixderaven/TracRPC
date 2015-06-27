import webbrowser
import sublime_plugin
from .base import TracController


class TracListTicketsCommand(sublime_plugin.TextCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return

        # if user picks from list, return the correct entry
        url = self.active_tickets[index]['url']
        webbrowser.open_new_tab(url)

    def run(self, edit, **args):
        self.controller = TracController(self.view)

        self.active_tickets = self.controller.get_active_user_tickets()
        print("ActiveTickets {}".format(self.active_tickets))
        ticket_list = [t['title_string'] for t in self.active_tickets]

        self.view.window().show_quick_panel(ticket_list, self.on_done, 1, 2)


class TracPasteReferenceCommand(TracListTicketsCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return
        ref_string = "[refs #{}]".format(self.active_tickets[index]['id'])
        print(ref_string)
        print(self.view.sel()[0].begin())

        # if user picks from list, paste
        self.view.run_command(
            "insert",
            {'characters': ref_string}
        )
