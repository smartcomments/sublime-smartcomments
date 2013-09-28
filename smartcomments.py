import sublime, sublime_plugin


class SmartCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().run_command('set_build_system', {
                  'file': 'Packages/sublime-smartcomments/smartcomments.sublime-build'
                      })
        self.view.window().run_command('build')
