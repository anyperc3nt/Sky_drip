import settings


def buttons_handler(name):
    if name == "режим звездопада":
        if(settings.time_speed == 1):
            settings.time_speed = 5000
            settings.motionblur_on = True
        else:
            settings.time_speed = 1
            settings.motionblur_on = False


class Interface(object):
    def __init__(self, graphics):
        self.graphics = graphics
        self.time = 0
        button = Button("режим звездопада", 20, graphics.Yscreensize-60, 30)
        self.buttons = [button]
        self.information = Information(
            ["fov: ", "alpha: ", "theta: ", "time speed: "], graphics.Xscreensize-250, 10, 30*10, 30)

    def buttons_update(self):
        for button in self.buttons:
            button.update(self.graphics)

    def information_update(self, values):
        self.information.update(values, self.graphics)

    def check(self, x, y):
        for button in self.buttons:
            if button.collide(x, y):
                buttons_handler(button.text)


class Button(object):
    def __init__(self, text, x, y, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = h*int(len(text)/1.6)
        self.h = h

    def update(self, graphics):
        graphics.draw_text(self.text, self.x, self.y, self.w, self.h)

    def collide(self, x, y):
        if(0 < x-self.x < self.w) and (0 < y-self.y < self.h):
            return True
        else:
            return False


class Information(object):
    def __init__(self, lines, x, y, w, h):
        self.lines = lines
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self, values, graphics):
        for i in range(0, len(self.lines)):
            graphics.draw_text(
                self.lines[i] + str(round(values[i], 2)), self.x, self.y+self.h*2*(i), self.w, self.h)
