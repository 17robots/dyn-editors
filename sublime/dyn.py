from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
import sublime

class Dyn(AbstractPlugin):
    @classmethod
    def name(cls):
        return "Dyn"

    @classmethod
    def configuration(cls):
        return sublime.load_settings("LSP-Dyn.sublime-settings"), "Packages/Dyn/LSP-Dyn.sublime-settings"

def plugin_loaded():
    register_plugin(Dyn)

def plugin_unloaded():
    unregister_plugin(Dyn)
