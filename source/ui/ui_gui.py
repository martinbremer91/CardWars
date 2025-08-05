from pyforms_gui.basewidget import BaseWidget

quit_func = None

class CardWarsGUI(BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__('CardWars')

    def before_close_event(self):
        super().before_close_event()
        if quit_func is None:
            print("No Quit Function found: calling generic exit()")
            exit()
        else:
            quit_func()

def init(in_quit_func):
    global quit_func
    from pyforms_gui.appmanager import start_app
    quit_func = in_quit_func
    print("Init GUI")
    start_app(CardWarsGUI)
