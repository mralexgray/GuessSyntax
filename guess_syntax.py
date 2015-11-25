import sublime, sublime_plugin, os


class GuessSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        view.run_command('guess_syntax')

    def on_post_save(self, view):
        view.run_command('guess_syntax')


class GuessSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        # buffer has never been saved
        if self.view.is_scratch() or not self.view.file_name:
            return

        self.file = self.view.file_name()
        self.syn = self.view.settings().get('syntax')

        # print("guessing syntax of " + file + "(" + current_syntax + ")")

        # Only operate on files with no file extension (i.e. no dots)
        if (self.syn or not os.path.basename(self.file).find('.')):
            if not self.syn.find('Plain'):
                print('Skipping syntaxed/extensioned document: ' + self.syn)
                return

        args = [
            '/usr/local/bin/coffee',
            '-e',
            '\'x=require("language-detect"); z=x.sync("'
            + self.file
            + '"); console.log(z) \''
        ]

        try:
            cmd = ' '.join(args)
            proc = os.popen(cmd, 'r', 1)
            lang = proc.read().rstrip('\r\n')
            if lang:
                self.set_syntax(self.fix_syntax(lang))
            else:
                print("couldnt find language!")
            proc.close()

        except OSError:
            sublime.error_message('Error calling NodeJS app')

    def set_syntax(self, syntax):

        name = syntax[0].replace('/', os.path.sep)
        name = name.replace('\\', os.path.sep)

        dirs = syntax[0].split(os.path.sep)
        name = dirs.pop()
        path = os.path.sep.join(dirs)

        if not path:
            path = syntax[0]

        file_name = syntax[1] + '.tmLanguage'
        new_syntax = 'Packages/' + path + '/' + file_name

        # only set the syntax if it's different
        if new_syntax != self.syn:
            # let's make sure it exists first!
            # if os.path.exists(new_syntax_path):
            self.view.set_syntax_file(new_syntax)
            print('Syntax set to ' + name + ' using ' + new_syntax)
            # else:
                # print('Syntax file for ' + name + ' does not exist at ' + new_syntax_path)
    
    def fix_syntax(self, nameof):
        if nameof == 'Shell':
            return ('ShellScript', 'Shell-Unix-Generic')
        elif nameof == 'JSON':
            return ('JavaScript', nameof)
        elif nameof == 'RestructuredText':
            return (nameof,'reStructuredText')
        else:
            return (nameof, nameof)