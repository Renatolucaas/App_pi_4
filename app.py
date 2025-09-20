from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label

# Tamanho da janela
Window.size = (400, 700)

# Carregar KV
Builder.load_file('app.kv')

# --- Classes de telas ---
class LoginScreen(Screen):
    pass

class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    def on_enter(self):
        # Limpar e adicionar horários
        grid = self.ids.horarios_grid
        grid.clear_widgets()
        
        horarios = ["07:00", "08:00", "09:00 ✓", "10:00", "11:00", "14:00", "15:00", "16:00"]
        
        for h in horarios:
            label = Label(text=h, 
                         size_hint_y=None, 
                         height=40,
                         color=(0, 0, 0, 1))  # Cor preta
            grid.add_widget(label)

class ScheduleScreen(Screen):
    def on_enter(self):
        # Limpar e adicionar dados da agenda
        grid = self.ids.agenda_grid
        # Manter apenas o cabeçalho (primeiras 5 labels)
        while len(grid.children) > 5:
            grid.remove_widget(grid.children[0])
        
        # Dados de exemplo
        dados = [
            ["Sub-12", "Seg", "15/01", "08:00-10:00", "Treino técnico"],
            ["Sub-15", "Ter", "16/01", "09:00-11:00", "Preparação física"],
            ["Sub-17", "Qua", "17/01", "10:00-12:00", "Tática"],
            ["Sub-12", "Qui", "18/01", "08:00-10:00", "Coletivo"],
            ["Sub-15", "Sex", "19/01", "09:00-11:00", "Amistoso"]
        ]
        
        for linha in dados:
            for item in linha:
                label = Label(text=item, 
                             size_hint_y=None, 
                             height=40,
                             color=(0, 0, 0, 1))  # Cor preta
                grid.add_widget(label)

# --- ScreenManager ---
class ScreenManagement(ScreenManager):
    pass

# --- App ---
class MyApp(App):
    def build(self):
        sm = ScreenManagement()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ScheduleScreen(name='schedule'))
        return sm

if __name__ == '__main__':
    MyApp().run()