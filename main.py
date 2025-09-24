from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
import datetime
import json
import os

Window.size = (400, 700)

# --- Classes de telas ---
class LoginScreen(Screen):
    def validar_login(self):
        usuario_digitado = self.ids.entrada_usuario.text.strip()
        senha_digitada = self.ids.entrada_senha.text.strip()

        if not os.path.exists("usuario.json"):
            popup = Popup(title='Erro',
                          content=Label(text='Nenhum usuário cadastrado!'),
                          size_hint=(0.6,0.3))
            popup.open()
            return

        with open("usuario.json", "r") as f:
            dados = json.load(f)

        if usuario_digitado == dados.get("nome") and senha_digitada == dados.get("senha"):
            self.manager.current = "welcome"
        else:
            popup = Popup(title='Erro',
                          content=Label(text='Usuário ou senha incorretos!'),
                          size_hint=(0.6,0.3))
            popup.open()

class RegisterScreen(Screen):
    def check_campos(self):
        """Ativa o botão Registrar apenas se todos os campos estiverem preenchidos"""
        nome = self.ids.nome_input.text.strip()
        email = self.ids.email_input.text.strip()
        senha = self.ids.senha_input.text.strip()
        confirma = self.ids.confirma_input.text.strip()
        
        # Verifica se todos os campos têm conteúdo
        if nome and email and senha and confirma:
            self.ids.btn_registrar.disabled = False
        else:
            self.ids.btn_registrar.disabled = True

    def validar_e_salvar(self):
        nome = self.ids.nome_input.text.strip()
        email = self.ids.email_input.text.strip()
        senha = self.ids.senha_input.text.strip()
        confirma = self.ids.confirma_input.text.strip()

        if not nome or not email or not senha or not confirma:
            popup = Popup(title='Erro',
                          content=Label(text='Todos os campos devem ser preenchidos!'),
                          size_hint=(0.6,0.3))
            popup.open()
            return

        if senha != confirma:
            popup = Popup(title='Erro',
                          content=Label(text='As senhas não coincidem!'),
                          size_hint=(0.6,0.3))
            popup.open()
            return

        dados = {"nome": nome, "email": email, "senha": senha}
        with open("usuario.json", "w") as f:
            json.dump(dados, f)

        popup = Popup(title='Sucesso',
                      content=Label(text='Usuário registrado com sucesso!'),
                      size_hint=(0.6,0.3))
        popup.open()

        self.ids.nome_input.text = ''
        self.ids.email_input.text = ''
        self.ids.senha_input.text = ''
        self.ids.confirma_input.text = ''

        self.manager.current = "login"

class WelcomeScreen(Screen):
    def update_welcome(self, label):
        def _update(dt):
            hora = datetime.datetime.now().hour
            if 5 <= hora < 12:
                saudacao = "Bom dia"
            elif 12 <= hora < 18:
                saudacao = "Boa tarde"
            else:
                saudacao = "Boa noite"
            label.text = f'{saudacao}, [color=e55c5c]Fulano[/color]!'
        Clock.schedule_interval(_update, 60)
        _update(0)

class TreinoScreen(Screen): 
    pass

class ScheduleScreen(Screen):
    def on_enter(self):
        try:
            grid = self.ids.agenda_grid
        except AttributeError:
            print("O ID 'agenda_grid' não foi encontrado no KV.")
            return

        grid.clear_widgets()
        dados = [
            {"tipo": "Time", "nome": "Bom de Bola", "temporada": "2025", "categoria": "Sub-10", "tecnico": "Evandro M.P. Jadijisky"},
            {"tipo": "Treino", "descricao": "Treinos Fixos", "horario": "Seg e Ter: 18h às 20:30h"},
            {"tipo": "Jogo", "nome": "Amistoso", "data": "28/09/2025", "horario": "16:00", "local": "Campo Municipal", "adversario": "Time Oponente"}
        ]

        for item in dados:
            card = BoxLayout(orientation='vertical', size_hint_x=None, width=250, padding=15, spacing=8)

            with card.canvas.before:
                if item["tipo"] == "Time":
                    Color(0.2, 0.6, 0.9, 0.9)
                elif item["tipo"] == "Treino":
                    Color(0.1, 0.7, 0.4, 0.9)
                else:
                    Color(0.9, 0.6, 0.2, 0.9)
                card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[15])

            def update_rect(instance, value):
                card.rect.pos = instance.pos
                card.rect.size = instance.size
            card.bind(pos=update_rect, size=update_rect)

            if item["tipo"] == "Time":
                card.add_widget(Label(text=f'Nome do Time: {item["nome"]}', bold=True, font_size=16, color=(1,1,1,1)))
                card.add_widget(Label(text=f'Temporada: {item["temporada"]}', font_size=14, color=(1,1,1,1)))
                card.add_widget(Label(text=f'Categoria: {item["categoria"]}', font_size=14, color=(1,1,1,1)))
                card.add_widget(Label(text=f'Técnico: {item["tecnico"]}', font_size=14, color=(1,1,1,1)))
            elif item["tipo"] == "Treino":
                card.add_widget(Label(text=item["descricao"], bold=True, font_size=16, color=(1,1,1,1)))
                card.add_widget(Label(text=item["horario"], font_size=14, color=(1,1,1,1)))
            else:
                card.add_widget(Label(text=item["nome"], bold=True, font_size=16, color=(1,1,1,1)))
                self.ids.amistoso_data = TextInput(text=item["data"], multiline=False, size_hint_y=None, height=30)
                self.ids.amistoso_horario = TextInput(text=item["horario"], multiline=False, size_hint_y=None, height=30)
                self.ids.amistoso_local = TextInput(text=item["local"], multiline=False, size_hint_y=None, height=30)
                self.ids.amistoso_adversario = TextInput(text=item["adversario"], multiline=False, size_hint_y=None, height=30)
                card.add_widget(Label(text="Data:"))
                card.add_widget(self.ids.amistoso_data)
                card.add_widget(Label(text="Horário:"))
                card.add_widget(self.ids.amistoso_horario)
                card.add_widget(Label(text="Local:"))
                card.add_widget(self.ids.amistoso_local)
                card.add_widget(Label(text="Adversário:"))
                card.add_widget(self.ids.amistoso_adversario)
            grid.add_widget(card)

        if os.path.exists("amistoso.json"):
            with open("amistoso.json", "r") as f:
                dados_salvos = json.load(f)
                self.ids.amistoso_data.text = dados_salvos.get("data", "28/09/2025")
                self.ids.amistoso_horario.text = dados_salvos.get("horario", "16:00")
                self.ids.amistoso_local.text = dados_salvos.get("local", "Campo Municipal")
                self.ids.amistoso_adversario.text = dados_salvos.get("adversario", "Time Oponente")

    def salvar_amistoso(self):
        dados = {
            "data": self.ids.amistoso_data.text,
            "horario": self.ids.amistoso_horario.text,
            "local": self.ids.amistoso_local.text,
            "adversario": self.ids.amistoso_adversario.text
        }
        with open("amistoso.json", "w") as f:
            json.dump(dados, f)
        popup = Popup(title='Sucesso',
                      content=Label(text='Dados do amistoso salvos!'),
                      size_hint=(0.6, 0.3))
        popup.open()


# --- Gerenciador de telas ---
class ScreenManagement(ScreenManager): 
    pass


# --- App principal ---
class MyApp(App):
    def build(self):
        Builder.load_file("app.kv")
        Builder.load_file("welcome.kv")
        Builder.load_file("treino.kv")
        Builder.load_file("schedule.kv")
        Builder.load_file("register.kv")  # tela register

        sm = ScreenManagement()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(TreinoScreen(name='treino'))
        sm.add_widget(ScheduleScreen(name='schedule'))
        return sm

if __name__ == '__main__':
    MyApp().run()