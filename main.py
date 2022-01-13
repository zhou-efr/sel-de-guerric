from kivy.app import App
from kivy.clock import Clock

from game.Game import WoShiFan


class WoShiFanApp(App):
    def build(self):
        game = WoShiFan()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    WoShiFanApp().run()
