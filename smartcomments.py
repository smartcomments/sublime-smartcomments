import sublime, sublime_plugin
from subprocess import PIPE, Popen
from io import open as io_open
from os import remove
from os.path import dirname as path_dirname
from tempfile import mkstemp
import platform

def get_command():
    command = "smartcomments"
    if platform.system() == "Windows":
        command = "smartcomments.cmd"
    return command 

def fn_execute(cmd_args=[], cmd=None):
    """
    """
    result = None
    try:
        if cmd:
            result = Popen(cmd_args, executable=cmd,
                           stdout=PIPE, stderr=PIPE).communicate()
        else:
            result = Popen(cmd_args, stdout=PIPE, stderr=PIPE).communicate()
    except TypeError as err:
        print("Error {0} ocurrido al ejecutar el comando {1} \
              ".format(err, cmd))
    except FileNotFoundError as err:
        print("Error {0} ocurrido al ejecutar el comando {1} \
              ".format(err, cmd))
    return result


class SmartCommentsFolderCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name:
            return

        file_dir = path_dirname(file_name)
        result = fn_execute([get_command(), "-g","-t", file_dir])
        print(result)


class SmartCommentsFileCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name or not str(file_name).endswith("js"):
            return

        result = fn_execute([get_command(), "-g", "-t", file_name])
        print(result)


class SmartCommentsTextCommand(sublime_plugin.TextCommand):
    """
    """
    def run(self, edit):
        file_name = self.view.file_name()
        if not file_name or not str(file_name).endswith("js"):
            return

        selection = self.view.sel()
        for region in selection:
            if not region.empty():
                s = self.view.substr(region)
                js_tmpfile = mkstemp(suffix='.js', text=True)
                with io_open(js_tmpfile[1], 'w+') as tmpf:
                    tmpf.write(s)
                try:
                    fn_execute([get_command(), "-g", "-t", js_tmpfile[1]])
                except:
                    remove(js_tmpfile[1])
                with io_open(js_tmpfile[1], 'r') as tmpf:
                    file_size = tmpf.seek(0, 2)
                    tmpf.seek(0, 0)
                    data = tmpf.read(file_size)
                    if data != '':
                        self.view.replace(edit, region, data)
                remove(js_tmpfile[1])
