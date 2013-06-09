import sublime, sublime_plugin
import os, re

class SelectColorSchemeCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.paths = []
        self.maps = {}
        color_schemes = self.get_color_schemes()
        def on_done(index):
            if index >= 0:
                self.set_color_scheme(color_schemes[index])

        self.window.show_quick_panel(color_schemes, on_done)

    def get_color_schemes(self):
        current_color_scheme = self.load_settings().get('color_scheme')
        #files = filter(lambda f: f.endswith('tmTheme'), os.listdir(self.color_scheme_dir()))
        files = []
        dirs = self.color_scheme_dirs()
        for i in range(len(dirs)):
            cur_files = filter(lambda f: f.lower().endswith('tmtheme'), os.listdir(dirs[i]))
            for file in cur_files:
                self.maps[str(file)] = self.paths[i]
            files = files + cur_files
        return files

    def set_color_scheme(self, color_scheme):
        # color_scheme_file = os.path.join(os.path.join(sublime.packages_path(), self.maps[color_scheme]), color_scheme)
        color_scheme_file = 'Packages/' + str(self.maps[color_scheme]) + '/' + color_scheme
        self.load_settings().set('color_scheme', color_scheme_file)
        sublime.save_settings('Preferences.sublime-settings')

    def color_scheme_dir(self):
        return os.path.join(sublime.packages_path(), "Color Scheme - Default")

    def color_scheme_dirs(self):
        paquetes = os.listdir(sublime.packages_path())
        self.paths = []
        for paquete in paquetes:
            if re.search(r".*colou?r.?scheme.*|user", paquete, re.IGNORECASE):
                self.paths.append(paquete)
        dirs = []
        for schema in self.paths:
            dirs.append(os.path.join(sublime.packages_path(), str(schema)))
        return dirs

    def load_settings(self):
        return sublime.load_settings('Preferences.sublime-settings')