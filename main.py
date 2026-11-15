
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.035, 0.05, 0.10, 1)

class StyledButton(Button):
    bg_color = ListProperty([0.12, 0.17, 0.27, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = 25

        with self.canvas.before:
            self.bg = Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[18]
            )

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.bind(bg_color=self.update_color)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, *args):
        self.bg.rgba = self.bg_color


class CalculatorApp(App):

    def build(self):
        self.expression = ""

        root = BoxLayout(
            orientation="vertical",
            padding=16,
            spacing=14
        )

        title = Label(
            text="CALCULATOR",
            font_size=19,
            color=(0.3, 0.7, 1, 1),
            size_hint_y=0.10
        )
        root.add_widget(title)

        self.display = Label(
            text="0",
            font_size=45,
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.25
        )

        self.display.bind(
            size=lambda obj, size:
            setattr(obj, "text_size", size)
        )

        root.add_widget(self.display)

        buttons = [
            ["AC", "DEL", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "00", "="]
        ]

        grid = GridLayout(
            cols=4,
            spacing=9,
            size_hint_y=0.65
        )

        for row in buttons:
            for value in row:

                if value == "=":
                    color = [0.05, 0.48, 0.95, 1]
                elif value == "AC":
                    color = [0.90, 0.20, 0.25, 1]
                elif value == "DEL":
                    color = [0.85, 0.40, 0.12, 1]
                elif value in ["%", "÷", "×", "−", "+"]:
                    color = [0.12, 0.30, 0.53, 1]
                else:
                    color = [0.12, 0.16, 0.24, 1]

                btn = StyledButton(
                    text=value,
                    bg_color=color
                )

                btn.bind(on_press=self.button_click)
                grid.add_widget(btn)

        root.add_widget(grid)

        return root

    def button_click(self, instance):
        value = instance.text

        if value == "AC":
            self.expression = ""

        elif value == "DEL":
            self.expression = self.expression[:-1]

        elif value == "=":
            try:
                exp = self.expression
                exp = exp.replace("×", "*")
                exp = exp.replace("÷", "/")
                exp = exp.replace("−", "-")

                allowed = "0123456789.+-*/() "

                if not exp or any(c not in allowed for c in exp):
                    raise ValueError("Invalid input")

                result = eval(
                    exp,
                    {"__builtins__": None},
                    {}
                )

                if isinstance(result, float) and result.is_integer():
                    result = int(result)

                self.expression = str(result)

            except Exception:
                self.expression = "Error"

        elif value == "%":
            try:
                result = float(self.expression) / 100
                self.expression = str(result)
            except Exception:
                self.expression = "Error"

        else:
            if self.expression == "Error":
                self.expression = ""

            self.expression += value

        self.display.text = self.expression or "0"


if __name__ == "__main__":
    CalculatorApp().run()
    
