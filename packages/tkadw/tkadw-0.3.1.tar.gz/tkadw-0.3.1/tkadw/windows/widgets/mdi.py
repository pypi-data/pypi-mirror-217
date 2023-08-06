from tkadw import AdwTFrame, AdwTButton


class MDI(AdwTFrame):
    def create_child(self):
        child = AdwTFrame(self.frame)
        child.place(x=10, y=10, width=150, height=150)

        child.closebutton = AdwTButton(child.frame, text="✕", width=25, height=25, command=lambda: child.place_forget())
        child.closebutton.pack(anchor="ne", padx=2, pady=2)

        child.frame.bind("<Button-1>", self._click)
        child.frame.bind("<B1-Motion>", lambda event: self._move(event, child))

        return child

    def _click(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event, child):
        child.place(
            x=event.x-self.x+self.winfo_rootx(),
            y=event.y-self.y+self.winfo_rooty()
        )
        print(child.winfo_x(), child.winfo_y())


if __name__ == '__main__':
    from tkadw import Adwite, set_default_theme

    set_default_theme("win11", "light")

    root = Adwite()

    mdi = MDI()
    mdiChild1 = mdi.create_child()
    mdi.pack(fill="both", expand="yes", padx=10, pady=10)

    root.mainloop()