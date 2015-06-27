import sublime
import sublime_plugin
import webbrowser
import xmlrpc.client


class Settings():

    def __init__(self, view, args):
        self.user = sublime.load_settings('TracRPC.sublime-settings')

        if not args:
            self.proj = view.settings().get('tracrpc', {})
        else:
            self.proj = args

    def get(self, key, default):
        return self.proj.get(key, self.user.get(key, default))


class TracController():

    def __init__(self, view, trac_url=None, trac_user=None, trac_pw=None):
        self.view = view
        self.base_url = trac_url or self.view.settings().get("trac_url")
        self.rpc_url = "{}/login/rpc".format(self.base_url)

        self.user = trac_user or self.view.settings().get("trac_user")
        self.pw = trac_pw or self.view.settings().get("trac_pw")

        self.rpc_url = self.rpc_url.replace('https://', 'https://{}:{}@'.format(
            self.user,
            self.pw))

    def _get_tickets(self, query):

        trac_server = xmlrpc.client.ServerProxy(self.rpc_url)
        ticket_ids = trac_server.ticket.query(query)

        multicall = xmlrpc.client.MultiCall(trac_server)

        for ticket_id in ticket_ids:
            multicall.ticket.get(ticket_id)

        return multicall()

    def get_active_user_tickets(self):
        qstr = "owner=~{}&status!=closed".format(self.user)
        #qstr = "owner=~{}&order=id".format(self.user)

        tickets_response = self._get_tickets(qstr)
        tickets = []
        for ticket in tickets_response:
            ticket_string = "#{} {}".format(ticket[0], ticket[3]['summary'])
            ticket_url = "{}/ticket/{}".format(self.base_url, ticket[0])
            tickets.append({
                'id': ticket[0],
                'title_string': ticket_string,
                'url': ticket_url
            })

        return tickets


class BaseTracCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(BaseTracCommand, self).__init__(*args, **kwargs)
        self.controller = TracController(self.view)


class TracListTicketsCommand(BaseTracCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return

        # if user picks from list, return the correct entry
        url = self.active_tickets[index]['url']
        webbrowser.open_new_tab(url)

    def run(self, edit, **args):

        self.active_tickets = self.controller.get_active_user_tickets()
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
