import sublime, sublime_plugin
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

class TracListTicketsCommand(sublime_plugin.TextCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return

        # if user picks from list, return the correct entry
        url = self.tickets[index]['url']
        webbrowser.open_new_tab(url)

    def collect_tickets(self):
        qstr = "owner=~{}&status!=closed".format(self.user)
        #qstr = "owner=~{}&order=id".format(self.user)
        url = self.rpc_url.replace('https://','https://{}:{}@'.format(
            self.user,
            self.pw))
        print(url)
        trac_server = xmlrpc.client.ServerProxy(url)
        ticket_ids = trac_server.ticket.query(qstr)

        multicall = xmlrpc.client.MultiCall(trac_server)

        for ticket_id in ticket_ids:
            multicall.ticket.get(ticket_id)

        tickets = multicall()

        for ticket in tickets:
            ticket_string = "#{} {}".format(ticket[0], ticket[3]['summary'])
            ticket_url = "{}/ticket/{}".format(self.base_url, ticket[0])
            self.tickets.append({
                'id': ticket[0],
                'title_string': ticket_string,
                'url': ticket_url
                })

    def init(self):
        self.base_url = self.view.settings().get("trac_url")
        self.rpc_url = "{}/login/rpc".format(self.base_url)
        self.user = self.view.settings().get("trac_user")
        self.pw = self.view.settings().get("trac_pw")
        self.auth = (self.user, self.pw)

        self.tickets = []
        self.collect_tickets()

    def run(self, edit, **args):
        self.init()

        ticket_list = [t['title_string'] for t in self.tickets]

        self.view.window().show_quick_panel(ticket_list, self.on_done, 1, 2)


class TracPasteReferenceCommand(TracListTicketsCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return
        ref_string = "[refs #{}]".format(self.tickets[index]['id'])
        print(ref_string)
        print(self.view.sel()[0].begin())

        # if user picks from list, paste
        self.view.run_command(
            "insert",
            {'characters': ref_string}
            )