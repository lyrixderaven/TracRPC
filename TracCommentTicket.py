import sublime
import sublime_plugin

from .open_views import OpenViews
from .base import BaseTracCommand


class OnCloseUpdateMessage(sublime_plugin.EventListener):

    def on_close(self, view):
        if not OpenViews.exists(view):
            return

        OpenViews.remove(view)
        comment_text = view.substr(sublime.Region(0, view.size()))
        comment_text = "\n".join(
            [line for line in iter(comment_text.splitlines()) if not line.startswith("#")])
        print(comment_text)
        view.run_command(
            "trac_comment",
            {'comment': comment_text}
        )


class TracCommentCommand(BaseTracCommand):

    def run(self, edit, comment=None):
        if not comment:
            update_view = self.view.window().new_file()
            OpenViews.set(update_view)

            comment = "\n\n# Enter your comment  here and save + close when you're done.\n# Every line starting with a '#' will be ignored."

            update_view.run_command(
                "insert",
                {'characters': comment}
            )
            update_view.set_scratch(True)
            update_view.sel().clear()
            update_view.sel().add(sublime.Region(0))
            return
        else:
            print('Updating with comment now!')

        # 'something' is the default message
        # self.view.window().show_input_panel(
        #     "Say something:", 'something', self.on_done, None, None)

    # def on_done(self, user_input):
    # this is displayed in status bar at bottom
    #     sublime.status_message("User said: " + user_input)
    # this is a dialog box, with same message
    #     sublime.message_dialog("User said: " + user_input)
