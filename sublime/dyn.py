import sublime

try:
    from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
except ModuleNotFoundError as error:
    if error.name not in ("LSP", "LSP.plugin"):
        raise
    AbstractPlugin = None

if AbstractPlugin is not None:
    class Dyn(AbstractPlugin):
        @classmethod
        def name(cls):
            return "Dyn"

        @classmethod
        def configuration(cls):
            return sublime.load_settings("LSP-Dyn.sublime-settings"), "Packages/Dyn/LSP-Dyn.sublime-settings"


def plugin_loaded():
    if AbstractPlugin is None:
        sublime.status_message("Dyn: install LSP through Package Control, then restart Sublime Text.")
    else:
        register_plugin(Dyn)


def plugin_unloaded():
    if AbstractPlugin is not None:
        unregister_plugin(Dyn)
