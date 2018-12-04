class Item():
    def __init__(self, title, subtitle='', arg=None, autocomplete=None,
                 match=None, valid=False, uid=None, icon=None, icontype=None,
                 type=None, largetext=None, copytext=None, quicklookurl=None,
                 mask=None):
        self.title = title
        self.subtitle = subtitle
        self.arg = arg
        self.autocomplete = autocomplete
        self.match = match
        self.valid = valid
        self.uid = uid
        self.icon = icon
        self.icontype = icontype
        self.type = type
        self.quicklookurl = quicklookurl
        self.largetext = largetext
        self.copytext = copytext

        self.modifiers = {}

        self.config = {}
        self.variables = {}
        self.mask = mask

    def setvar(self, name, value):
        self.variables[name] = value

    def get(self, name, default=None):
        return self.variables.get(name, default)