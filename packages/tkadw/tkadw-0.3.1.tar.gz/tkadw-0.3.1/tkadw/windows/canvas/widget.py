from tkadw.windows.canvas.drawengine import AdwDrawEngine


class AdwWidget(AdwDrawEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Configure>", self._draw, add="+")
        self._other()

    def _other(self):
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def _draw(self, evt=None):
        pass