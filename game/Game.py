from copy import deepcopy
from os import listdir

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

from game import Player
from game.Map import Map
from game.Player import KeyInput

Builder.load_file('./game/Game.kv')


class WoShiFan(Widget):
    map = ObjectProperty(None)
    maps = ListProperty([])

    def __init__(self, **kwargs):
        super(WoShiFan, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.load_maps()

    def load_maps(self):
        self.maps = []
        for i in listdir('./file/maps/temp'):
            temp = Map(filename='./file/maps/temp/'+i)
            if temp.loaded:
                self.maps.append(temp)

        self.clear_widgets()
        stack = StackLayout(pos=[0, 500])
        for i in range(len(self.maps)):
            stack.add_widget(Button(text='map-' + str(i),
                                    font_size=14,
                                    on_press=lambda x, map_id=i: self.load_map(map_id, x)))
        self.add_widget(stack)

    def update(self, dt):
        if self.map is not None:
            self.map.update()

    def load_map(self, map_id, button):
        self.clear_widgets()
        self.add_widget(self.maps[map_id])
        self.map = self.maps[map_id]
        self.map.move_in(0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.map is not None and self.map.player is not None:
            if keycode[1] == 'a':
                self.map.player.inputs[KeyInput.LEFT.value] = True
            elif keycode[1] == 's':
                self.map.player.inputs[KeyInput.DOWN.value] = True
            elif keycode[1] == 'd':
                self.map.player.inputs[KeyInput.RIGHT.value] = True
            elif keycode[1] == 'spacebar':
                self.map.player.inputs[KeyInput.JUMP.value] = True

        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            self.load_maps()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if self.map is not None and self.map.player is not None:
            if keycode[1] == 'a':
                self.map.player.inputs[KeyInput.LEFT.value] = False
            elif keycode[1] == 's':
                self.map.player.inputs[KeyInput.DOWN.value] = False
            elif keycode[1] == 'd':
                self.map.player.inputs[KeyInput.RIGHT.value] = False
            elif keycode[1] == 'spacebar':
                self.map.player.inputs[KeyInput.JUMP.value] = False

        return True
