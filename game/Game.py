from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from game import Player
from game.Player import KeyInput

Builder.load_file('./game/Game.kv')


class WoShiFan(Widget):
    player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WoShiFan, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.player is not None:
            if keycode[1] == 'a':
                self.player.inputs[KeyInput.LEFT.value] = True
            elif keycode[1] == 's':
                self.player.inputs[KeyInput.DOWN.value] = True
            elif keycode[1] == 'd':
                self.player.inputs[KeyInput.RIGHT.value] = True
            elif keycode[1] == 'spacebar':
                self.player.inputs[KeyInput.JUMP.value] = True

        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if self.player is not None:
            if keycode[1] == 'a':
                self.player.inputs[KeyInput.LEFT.value] = False
            elif keycode[1] == 's':
                self.player.inputs[KeyInput.DOWN.value] = False
            elif keycode[1] == 'd':
                self.player.inputs[KeyInput.RIGHT.value] = False
            elif keycode[1] == 'spacebar':
                self.player.inputs[KeyInput.JUMP.value] = False

        return True

    def update(self, dt):
        if self.player is not None:
            self.player.update()
