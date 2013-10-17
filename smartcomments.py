import sublime, sublime_plugin
from subprocess import PIPE, Popen
from os.path import dirname as path_dirname


def fn_execute(cmd_args=[], cmd=None):
    """
    """
    result = None
    try:
        if cmd:
            result = Popen(cmd_args, executable=cmd, stdout=PIPE, stderr=PIPE).communicate()
        else:
            result = Popen(cmd_args, stdout=PIPE, stderr=PIPE).communicate()
    except (TypeError, err):
        print ("Error %1 ocurrido al ejecutar el comando %2 ".args(err, cmd ))
    except (FileNotFoundError, err):
        print ("Error %1 ocurrido al ejecutar el comando %2 ".args(err, cmd ))
    return result


class SmartCommentsFolderCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name:
            return

        file_dir = path_dirname(file_name)
        result = fn_execute(["smartcomments","-g", "-t", file_dir])


class SmartCommentsFileCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name or not str(file_name).endswith("js"):
            return

        result = fn_execute(["smartcomments","-g", "-t", file_name])


class SmartCommentsTextCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name or not str(file_name).endswith("js"):
            return

