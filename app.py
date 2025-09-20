from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label

# Tamanho da janela (simulando celular)
Window.size = (400, 700)

# --- Classes de telas ---
class LoginScreen(Screen): pass
class WelcomeScreen(Screen): pass
class TreinoScreen(Screen): pass
class ScheduleScreen(Screen):
    def on_enter(self):
        # Atualiza a agenda dinamicamente
        grid = self.ids.agenda_grid
        while len(grid.children) > 5:
            grid.remove_widget(grid.children[0])

        dados = [
            ["Sub-12", "Seg", "15/01", "08:00-10:00", "Treino técnico"],
            ["Sub-15", "Ter", "16/01", "09:00-11:00", "Preparação física"],
            ["Sub-17", "Qua", "17/01", "10:00-12:00", "Tática"],
            ["Sub-12", "Qui", "18/01", "08:00-10:00", "Coletivo"],
            ["Sub-15", "Sex", "19/01", "09:00-11:00", "Amistoso"]
        ]

        for linha in dados:
            for item in linha:
                grid.add_widget(Label(text=item, size_hint_y=None, height=40, color=(0,0,0,1)))

# --- Gerenciador de telas ---
class ScreenManagement(ScreenManager): pass

# --- App ---
class MyApp(App):
    def build(self):
        # Carregar KV separadamente
        Builder.load_file("app.kv")
        Builder.load_file("welcome.kv")
        Builder.load_file("treino.kv")
        Builder.load_file("schedule.kv")

        sm = ScreenManagement()
        sm.add_widget(LoginScreen(name='app'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(TreinoScreen(name='treino'))
        sm.add_widget(ScheduleScreen(name='schedule'))
        return sm

if __name__ == '__main__':
    MyApp().run()
