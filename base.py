import sublime
import sublime_plugin
import xmlrpc.client

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
        try:
            self.trac_server = xmlrpc.client.ServerProxy(self.rpc_url)
            print("Created server proxy @ {}".format(self.rpc_url))
        except:
            print("Couldn't create server proxy @ {}".format(self.rpc_url))

    def _get_tickets(self, query):

        ticket_ids = self.trac_server.ticket.query(query)

        multicall = xmlrpc.client.MultiCall(self.trac_server)

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
