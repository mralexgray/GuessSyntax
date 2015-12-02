import sublime
import sublime_plugin
import os

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
		self.syn = view.settings().get('syntax') or ''

		print('guessing syntax of' + self.file + '(' + self.syn + ')')

		# Only operate on files with no file extension (i.e. no dots)
		# if self.syn
		# if not 'Plain' in self.syn
			# print('Skipping syntaxed/extensioned document: ' + self.syn)
			# return
		if '.' in os.path.basename(self.file):
			print('Skipping extensioned document: ' + os.path.basename(self.file))
			return

		os.environ['PATH'] += ':/usr/local/bin:/usr/local/sbin'

		args = [
			'/usr/local/bin/coffee',
			'-e',
			'\'x=require("language-detect"); z=x.sync("' + self.file + '"); console.log(z) \''
		]

		try:
			cmd = ' '.join(args)
			proc = os.popen(cmd, 'r', 1)
			lang = proc.read().rstrip('\r\n')
			print("got lang: " + lang)
			if lang:
				self.set_syntax(self.fix_syntax(lang))
			else:
				print("couldnt find language! got: " + lang)
			proc.close()

		except OSError:
			sublime.error_message('Error calling NodeJS app')

	def set_syntax(self, syntax):

		langs = sublime.find_resources('*language')
		langs += sublime.find_resources('*sublime-syntax')
		new_syntax = next((s for s in langs if syntax[0] in s), None)
		print('new syntax is ' + new_syntax)

		if new_syntax != self.syn:
			# let's make sure it exists first!
			# if os.path.exists(new_syntax_path):
			self.view.set_syntax_file(new_syntax)
			print('Syntax set to ' + syntax[0] + ' using ' + new_syntax)
			# else:
			# print('Syntax file for ' + name + ' does not exist at ' + new_syntax_path)

	def fix_syntax(self, nameof):
		lname = nameof.lower()
		choices = {
			'json'					: ('JavaScript', 			               'JSON'),
			'shell' 					: ('ShellScript', 		 'Shell-Unix-Generic'),
			'restructuredtext'	: ('RestructuredText',     'reStructuredText')
		}
		return choices.get(lname,(nameof, nameof))

# class GetSyntaxesCommand(sublime_plugin.TextCommand):
#     def run(self, edit):


			# next(i for i in  if syntax in i)


		# name = syntax[0].replace('/', os.path.sep)
		# name = name.replace('\\', os.path.sep)

		# dirs = syntax[0].split(os.path.sep)
		# name = dirs.pop()
		# path = os.path.sep.join(dirs)

		# if not path:
			# path = syntax[0]

		# file_name = syntax[1] + '.tmLanguage'
		# new_syntax = '/'.join(['Packages', path, file_name])

		# only set the syntax if it's different
