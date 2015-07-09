import xmlrpc.client
from urllib.parse import quote


class TracController():

    def __init__(self, view, trac_url=None, trac_user=None, trac_pw=None):
        self.view = view
        self.base_url = trac_url or self.view.settings().get("trac_url")
        self.rpc_url = "{}/login/rpc".format(self.base_url)

        self.user = trac_user or self.view.settings().get("trac_user")
        self.pw = trac_pw or self.view.settings().get("trac_pw")

        self.rpc_url = self.rpc_url.replace('https://', 'https://{}:{}@'.format(
            quote(self.user),
            quote(self.pw)))
        try:
            self.trac_server = xmlrpc.client.ServerProxy(self.rpc_url)
        except:
            print("Couldn't create server proxy @ {}".format(self.rpc_url))

    def _get_tickets(self, query):

        ticket_ids = self.trac_server.ticket.query(query)

        multicall = xmlrpc.client.MultiCall(self.trac_server)

        for ticket_id in ticket_ids:
            multicall.ticket.get(ticket_id)

        return multicall()

    def _parse_ticket_data(self, ticket):
        status_tag = "[{}]".format(ticket[3]['status'])
        ticket_string = "{}{}#{} {}".format(
            status_tag,
            " " * (12 - len(status_tag)),
            ticket[0],
            ticket[3]['summary'])
        ticket_url = "{}/ticket/{}".format(self.base_url, ticket[0])
        print("{}: {}".format(ticket_string, ticket[3]['status']))

        return {
            'id': ticket[0],
            'title_string': ticket_string,
            'url': ticket_url,
            'ticket': ticket[3]
        }

    def get_active_user_tickets(self):
        qstr = "owner=~{}&status!=closed".format(self.user)

        tickets_response = self._get_tickets(qstr)
        tickets = []
        for ticket in tickets_response:
            ticket_data = self._parse_ticket_data(ticket)
            tickets.append(ticket_data)

        return tickets

    def get_all_active_user_tickets(self):
        qargs = [
            'owner=~{}',
            'status=assigned',
            'status=new',
            'status=reopened',
            'status=testing',
            'or',
            'cc=~{}',
            'or',
            'reporter=~{}',
            'col=id',
            'col=summary',
            'col=status',
            'col=type',
            'col=priority',
            'col=time',
            'col=changetime',
            'order=priority',
        ]
        qstr = "&".join(qargs).format(
            self.user, self.user, self.user)

        tickets_response = self._get_tickets(qstr)
        tickets = []
        for ticket in tickets_response:
            ticket_data = self._parse_ticket_data(ticket)
            if ticket_data['ticket']['status'] != u'closed':
                tickets.append(ticket_data)

        return tickets

    def get_changelog(self, ticket_id):
        resp = self.trac_server.ticket.changeLog(ticket_id)
        print(resp)
        return resp

    def post_comment(self, ticket_id, comment):

        resp = self.trac_server.ticket.update(
            ticket_id,
            comment,
            {},         # Attributes
            True,       # Notifications?
            self.user)  # Author
        print(resp)
