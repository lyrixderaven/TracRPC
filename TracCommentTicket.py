import sublime
import sublime_plugin

from .active_views import ActiveViews
from .base import TracController


class OnCloseUpdateMessage(sublime_plugin.EventListener):

    def on_close(self, view):
        if not ActiveViews.exists(view):
            return

        view_dict = ActiveViews.get(view)
        if not 'ticket_id' in view_dict:
            print("No ticket id found")
            return
        ActiveViews.remove(view)
        comment_text = view.substr(sublime.Region(0, view.size()))
        comment_text = "\n".join(
            [line for line in iter(comment_text.splitlines()) if not line.startswith("#")])

        controller = TracController(view)
        if sublime.ok_cancel_dialog("Create Comment for ticket #{}?".format(view_dict['ticket_id']), "Create"):
            controller.post_comment(view_dict['ticket_id'], comment_text)


class TracCommentCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.controller = TracController(self.view)
        self.active_tickets = self.controller.get_active_user_tickets()
        print("ActiveTickets {}".format(self.active_tickets))
        ticket_list = [t['title_string'] for t in self.active_tickets]
        self.view.window().show_quick_panel(ticket_list, self.on_done, 1, 2)

    def on_done(self, index):
        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return
        ticket_id = self.active_tickets[index]['id']
        ticket_title = self.active_tickets[index]['title_string']

        update_view = self.view.window().new_file()
        ActiveViews.set(update_view, ticket_id=ticket_id)

        changelog = self.controller.get_changelog(ticket_id)
        changelogs = []

        for change in changelog:
            change_type = change[2]
            change_desc = ""
            if change_type == 'status':
                change_desc = "status: {} -> {}".format(change[3], change[4])
            if change_type == 'comment':
                change_desc = 'comment added'
            if change_type == 'blocking':
                change_desc = 'blocking -> {}'.format(change[4])
            if change_type == 'blockedby':
                change_desc = 'blocked by -> {}'.format(change[5])

            change_text = "# {} @ {}: {}".format(
                change[1],
                change[0],
                change_desc
            )
            changelogs.append(change_text)

        changelog_list = "\n".join(changelogs)
        comment = "\n\n\n\n# Commenting on \n# Ticket {}\n#\n#\n# Enter your comment above and close when you're done.\n# Any line starting with a '#' will be ignored.\n# Changelist:\n#\n{}".format(
            ticket_title,
            changelog_list)

        # for change in changelog:
        #     comment = comment + "\n\n" + "\n".join([str(c) for c in change])

        update_view.run_command(
            "insert",
            {'characters': comment}
        )
        update_view.set_scratch(True)
        update_view.sel().clear()
        update_view.sel().add(sublime.Region(0))
