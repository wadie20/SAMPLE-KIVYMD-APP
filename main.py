from kivy.animation import Animation
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from freq_calc import CPLFrequencyManager
from kivy.config import Config
Config.set('graphics', 'width', '0')  # Automatically fit screen width
Config.set('graphics', 'height', '0')  # Automatically fit screen height
Config.set('graphics', 'fullscreen', 'auto')  # Enable fullscreen


class MyWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dropdown_options = self.get_dropdown_options()
        self.selected_options = {}
        self.text_inputs = {}
        self.image_widget = None

        self.create_dropdown_buttons()
        self.create_text_inputs()
        self.create_calculate_button()
        self.create_animated_label()

    @staticmethod
    def get_dropdown_options():
        return [
            ("Type du CPL", ["S2/S3", "OPC-1",
             "OPC-2", "STE-N", "ALSPA 1790B", "T390"]),
            ("Type de voie (Emission Voie I)",
             ["voie_direct", "voie_inversée"]),
            ("Type de voie (Emission Voie II)",
             ["voie_direct", "voie_inversée"]),
            ("Type de voie (Reception Voie I)",
             ["voie_direct", "voie_inversée"]),
            ("Type de voie (Reception Voie II)",
             ["voie_direct", "voie_inversée"])
        ]

    def create_dropdown_buttons(self):
        for i, (button_text, options) in enumerate(self.dropdown_options):
            dropdown = DropDown()
            for option in options:
                btn = Button(
                    text=option,
                    size_hint_y=None,
                    height=44,
                    background_color=(0.3059, 0.4196, 0.6235, 1),
                    background_normal='',
                )
                btn.bind(on_release=lambda btn,
                         i=i: self.select_option(btn.text, i))
                dropdown.add_widget(btn)

            main_button = Button(
                text=button_text,
                size_hint=(1, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.95 - i * 0.06},
                background_color=(0.454, 0.745, 0.757, 1),
                background_normal='',
            )
            main_button.bind(on_release=dropdown.open)

            self.add_widget(main_button)
            setattr(self, f'dropdown{i + 1}', dropdown)
            setattr(self, f'main_button{i + 1}', main_button)

    def create_text_inputs(self):
        text_input_data = [
            ("Pilote HF", 0.65, self.validate_float_range, 'float'),
            ("Frequence centrale HF", 0.59, self.validate_freq_centrale, 'int'),
            ("Service BF", 0.53, self.validate_float_range, 'float'),
            ("Frequence de Glissement (T390)", 0.47,
             self.validate_float_range, 'float')
        ]

        for hint_text, pos_y, validate_func, input_filter in text_input_data:
            self.create_text_input(
                hint_text, pos_y, validate_func, input_filter)

        # Set default value for "Frequence de Glissement (T390)" to 0
        self.text_inputs["Frequence de Glissement (T390)"].text = "0"
        self.text_inputs["Frequence de Glissement (T390)"].disabled = True

    def create_calculate_button(self):
        self.calculer_button = Button(
            text="Calculer",
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(0.454, 0.745, 0.757, 1),
            background_normal='',
            disabled=True  # Initially disabled
        )
        self.calculer_button.bind(on_release=self.on_calculer_button_press)
        self.add_widget(self.calculer_button)

    def create_text_input(self, hint_text, pos_y, validate_func=None, input_filter=None):
        text_input = TextInput(
            hint_text=hint_text,
            size_hint=(1, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': pos_y},
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            input_filter=input_filter
        )
        if validate_func:
            text_input.bind(focus=lambda instance, value: validate_func(
                instance) if not value else None)
        self.text_inputs[hint_text] = text_input
        self.add_widget(text_input)

    def validate_freq_centrale(self, instance):
        try:
            freq = int(instance.text)
            if freq < 40 or freq > 500:
                instance.text = ''
        except ValueError:
            instance.text = ''

    def validate_float_range(self, instance):
        try:
            value = float(instance.text)
            if value < 0 or value > 4:
                instance.text = ''
        except ValueError:
            instance.text = ''

    def select_option(self, selected_text, index):
        main_button = getattr(self, f'main_button{index + 1}')
        dropdown = getattr(self, f'dropdown{index + 1}')
        main_button.text = selected_text
        dropdown.dismiss()
        self.selected_options[self.dropdown_options[index][0]] = selected_text

        # Enable the "Calculer" button when an option in "Type du CPL" is selected
        if index == 0:
            self.calculer_button.disabled = False

        # Remove existing image if any
        if self.image_widget:
            self.remove_widget(self.image_widget)
            self.image_widget = None

        # Set default values for "Type de voie (Emission Voie I)", "Type de voie (Emission Voie II)", "Type de voie (Reception Voie I)", and "Type de voie (Reception Voie II)" when "OPC-2" is selected
        if selected_text == "OPC-2":
            self.selected_options["Type de voie (Emission Voie I)"] = "voie_direct"
            self.selected_options["Type de voie (Emission Voie II)"] = "voie_direct"
            self.selected_options["Type de voie (Reception Voie I)"] = "voie_inversée"
            self.selected_options["Type de voie (Reception Voie II)"] = "voie_inversée"
            self.main_button2.text = "voie_direct"
            self.main_button3.text = "voie_direct"
            self.main_button4.text = "voie_inversée"
            self.main_button5.text = "voie_inversée"
            self.text_inputs["Pilote HF"].text = "0.18"

        # Set default values for "Pilote HF", "Type de voie (Emission Voie I)", and "Type de voie (Reception Voie I)" when "OPC-1" is selected
        if selected_text in ["S2/S3", "OPC-1"]:
            self.main_button3.disabled = True
            self.main_button5.disabled = True
        else:
            self.main_button3.disabled = False
            self.main_button5.disabled = False
        if selected_text == "OPC-1":
            self.text_inputs["Pilote HF"].text = "0.18"
            self.selected_options["Type de voie (Emission Voie I)"] = "voie_direct"
            self.selected_options["Type de voie (Reception Voie I)"] = "voie_inversée"
            self.main_button2.text = "voie_direct"
            self.main_button4.text = "voie_inversée"
        elif selected_text == "S2/S3":
            self.text_inputs["Pilote HF"].text = "0"
            self.selected_options["Type de voie (Emission Voie I)"] = "voie_inversée"
            self.selected_options["Type de voie (Reception Voie I)"] = "voie_inversée"
            self.main_button2.text = "voie_inversée"
            self.main_button4.text = "voie_inversée"
            # Add image for S2/S3
            self.image_widget = Image(
                source='/Users/iWadie/Desktop/world_of_coding/Tuto/Programming /Python/My_own_projects/Tkinter/CPL_Frequency_Calculator_Triangle/resources/images/s2-s3_image_test.png',
                size_hint=(1, 0.2),
                pos_hint={'center_x': 0.5, 'center_y': 0.3}
            )
            self.add_widget(self.image_widget)

        # Set default values for "Pilote HF", "Type de voie (Emission Voie I)", "Type de voie (Emission Voie II)", "Type de voie (Reception Voie I)", and "Type de voie (Reception Voie II)" when "STE-N" or "ALSPA 1790B" is selected
        if selected_text in ["STE-N", "ALSPA 1790B"]:
            self.text_inputs["Pilote HF"].text = "0"
            self.selected_options["Type de voie (Emission Voie I)"] = "voie_inversée"
            self.selected_options["Type de voie (Emission Voie II)"] = "voie_direct"
            self.selected_options["Type de voie (Reception Voie I)"] = "voie_inversée"
            self.selected_options["Type de voie (Reception Voie II)"] = "voie_direct"
            self.main_button2.text = "voie_inversée"
            self.main_button3.text = "voie_direct"
            self.main_button4.text = "voie_inversée"
            self.main_button5.text = "voie_direct"

        # Enable "Frequence de Glissement (T390)" only for "T390" and set its value to 0.04
        if selected_text == "T390":
            self.selected_options["Type de voie (Emission Voie I)"] = "voie_inversée"
            self.selected_options["Type de voie (Emission Voie II)"] = "voie_direct"
            self.selected_options["Type de voie (Reception Voie I)"] = "voie_direct"
            self.selected_options["Type de voie (Reception Voie II)"] = "voie_inversée"
            self.main_button2.text = "voie_inversée"
            self.main_button3.text = "voie_direct"
            self.main_button4.text = "voie_direct"
            self.main_button5.text = "voie_inversée"
            self.text_inputs["Pilote HF"].text = "0.04"
            self.text_inputs["Frequence de Glissement (T390)"].disabled = False
            self.text_inputs["Frequence de Glissement (T390)"].text = "0.04"
        else:
            self.text_inputs["Frequence de Glissement (T390)"].disabled = True
            self.text_inputs["Frequence de Glissement (T390)"].text = "0"

    def on_calculer_button_press(self, instance):
        if not self.text_inputs["Frequence centrale HF"].text:
            self.show_popup(
                "Erreur", "Entrez une valeur pour la Fréquence centrale HF !!")
            return

        freq_centrale = int(self.text_inputs["Frequence centrale HF"].text)
        pilote_hf = float(
            self.text_inputs["Pilote HF"].text) if self.text_inputs["Pilote HF"].text else 0
        service_bf = float(
            self.text_inputs["Service BF"].text) if self.text_inputs["Service BF"].text else 0
        freq_glissement = float(
            self.text_inputs["Frequence de Glissement (T390)"].text) if not self.text_inputs["Frequence de Glissement (T390)"].disabled else 0

        # Subtract 4 from "Frequence centrale HF" if "STE-N" or "ALSPA 1790B" is selected
        if self.selected_options.get("Type du CPL") in ["STE-N", "ALSPA 1790B"]:
            freq_centrale -= 4

        manager = CPLFrequencyManager(
            freq_centrale, pilote_hf=pilote_hf, service_bf=service_bf, freq_gl=freq_glissement)
        results_to_display = manager.display_results(self.selected_options)

        self.display_results_popup(results_to_display)

    def show_popup(self, title, message):
        popup_content = BoxLayout(
            orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message, size_hint=(
            1, 0.8), text_size=(380, None), halign='center'))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        popup_content.add_widget(close_button)

        popup = Popup(title=title, content=popup_content, size_hint=(
            None, None), size=(400, 300), auto_dismiss=False)
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def display_results_popup(self, results):
        popup_content = BoxLayout(orientation='vertical')

        with popup_content.canvas.before:
            Color(0.32, 0.38, 0.57, 1)
            self.rect = Rectangle(size=popup_content.size,
                                  pos=popup_content.pos)
            popup_content.bind(size=self._update_rect, pos=self._update_rect)

        result_labels = [
            ("Pilote HF:", results['tx1_ph'], results['tx2_ph'], "Emission"),
            ("Pilote HF:", results['rx1_ph'], results['rx2_ph'], "Reception"),
            ("Service BF:", results['tx1_bf'], results['tx2_bf'], "Emission"),
            ("Service BF:", results['rx1_bf'], results['rx2_bf'], "Reception")
        ]

        for title, val1, val2, phase in result_labels:
            popup_content.add_widget(
                Label(text=f"[b]{title}[/b] {phase}", size_hint=(1, 0.05), markup=True))
            popup_content.add_widget(
                Label(text=f"[i]Voie I:[/i] {val1}", size_hint=(1, 0.05), markup=True, color=(0, 1, 0, 1)))
            popup_content.add_widget(
                Label(text=f"[i]Voie II:[/i] {val2}", size_hint=(1, 0.05), markup=True, color=(0, 1, 0, 1)))

        close_button = Button(text="Close", size_hint=(1, 0.1))
        popup_content.add_widget(close_button)

        popup = Popup(
            title='Résultats',
            content=popup_content,
            size_hint=(None, None),
            size=Window.size,
            auto_dismiss=False
        )

        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def create_animated_label(self):
        self.animated_label = Label(
            text="CPL Calculator App -- © ONEE Telecom Meknes",
            size_hint=(None, None),
            size=(400, 50),
            pos=(Window.width, Window.height * 0.01),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.animated_label)
        self.animate_label()

    def animate_label(self):
        animation = Animation(x=-self.animated_label.width,
                              duration=15) + Animation(x=Window.width, duration=0)
        animation.repeat = True
        animation.start(self.animated_label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CPLCalculatorApp(App):
    def build(self):
        self.title = "CPL Calculator v1.0.0"
        Window.size = (int(3.02 * 96), int(6.23 * 96))
        Window.clearcolor = (0x33 / 255, 0x3a / 255, 0x7b / 255, 1)
        return MyWidget()


if __name__ == "__main__":
    CPLCalculatorApp().run()
