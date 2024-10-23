import json
from datetime import datetime
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from os.path import exists


class mainApp(App):
    def build(self):
        layout = FloatLayout()

        # Установка фоновой картинки для основного экрана
        with layout.canvas.before:
            self.main_background = Image(source='5242683866479717251.jpg', allow_stretch=True, keep_ratio=False,
                                         size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_main_background, pos=self._update_main_background)

        # Кнопка меню в правом верхнем углу
        btn_menu = Button(text="Меню", size_hint=(0.25, 0.12), pos_hint={'right': 0.99, 'top': 0.99})  # Увеличил size_hint
        btn_menu.bind(on_press=self.open_menu)
        layout.add_widget(btn_menu)

        # Кнопка добавления действия ниже кнопки меню
        btn_add_action = Button(text="Добавить действие", size_hint=(0.25, 0.12),
                                pos_hint={'right': 0.99, 'top': 0.84})  # Увеличил size_hint
        btn_add_action.bind(on_press=self.add_action_popup)
        layout.add_widget(btn_add_action)

        # Кнопка "История" ниже кнопки "Добавить действие"
        btn_history = Button(text="История", size_hint=(0.25, 0.12),
                             pos_hint={'right': 0.99, 'top': 0.69})  # Увеличил size_hint
        btn_history.bind(on_press=self.open_history)
        layout.add_widget(btn_history)

        # Кнопка "Список дел" ниже кнопки "История"
        btn_todo_list = Button(text="Список дел", size_hint=(0.25, 0.12),
                               pos_hint={'right': 0.99, 'top': 0.54})  # Добавлена кнопка
        btn_todo_list.bind(on_press=self.open_todo_list)
        layout.add_widget(btn_todo_list)

        # BoxLayout для отображения имен участников и их очков (в верхнем левом углу)
        self.participants_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 0.5), pos_hint={'x': 0, 'top': 1})

        # Установка изображения для фона участников
        with self.participants_layout.canvas.before:
            self.participants_background = Image(source='5242683866479717278.jpg', allow_stretch=True,
                                                 keep_ratio=False, size=self.participants_layout.size,
                                                 pos=self.participants_layout.pos)
            self.participants_layout.bind(size=self._update_participants_background,
                                          pos=self._update_participants_background)

        layout.add_widget(self.participants_layout)

        # Загрузка данных участников
        self.participants = self.load_participants()

        # Загрузка данных о действиях
        self.actions = self.load_actions()

        # Загрузка истории действий
        self.history = self.load_history()

        # Обновляем список участников
        self.update_participant_labels()

        return layout

    def _update_main_background(self, instance, value):
        """Обновление фоновой картинки для основного экрана при изменении размера."""
        self.main_background.size = instance.size
        self.main_background.pos = instance.pos

    def _update_participants_background(self, instance, value):
        """Обновление фона для participants_layout"""
        self.participants_background.pos = instance.pos
        self.participants_background.size = instance.size

    def load_participants(self):
        if exists("participants.json"):
            with open("participants.json", "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"Миша": 20}

    def save_participants(self):
        with open("participants.json", "w", encoding='utf-8') as f:
            json.dump(self.participants, f, ensure_ascii=False, indent=4)

    def load_actions(self):
        if exists("actions.json"):
            with open("actions.json", "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return {'Подписать канистру сливов 5 л': 1,}

    def save_actions(self):
        with open("actions.json", "w", encoding='utf-8') as f:
            json.dump(self.actions, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if exists("history.json"):
            with open("history.json", "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

    def save_history(self):
        with open("history.json", "w", encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def update_participant_labels(self):
        # Создаем GridLayout с двумя столбцами и фиксированным количеством строк
        participants_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1), row_default_height=40)

        # Сортируем участников по убыванию очков
        sorted_participants = sorted(self.participants.items(), key=lambda x: x[1], reverse=True)

        # Определяем высоту GridLayout на основе количества участников
        participants_grid.height = len(sorted_participants) * 50  # Высота строки 50 для каждого участника

        # Добавляем участников и их очки в два столбца
        for name, score in sorted_participants:
            rounded_score = round(score, 3)  # Округление до 3 знаков после запятой

            # Левый столбец: имя участника, выравнено по центру
            name_label = Label(text=f"{name}", font_size='20sp', color=(1, 1, 1, 1), size_hint_x=0.5, halign='center',
                               valign='middle')
            name_label.bind(size=name_label.setter('text_size'))  # Для выравнивания текста по центру
            participants_grid.add_widget(name_label)

            # Правый столбец: очки участника, также выравнены по центру
            score_label = Label(text=f"{rounded_score}", font_size='20sp', color=(1, 1, 1, 1), size_hint_x=0.5,
                                halign='center', valign='middle')
            score_label.bind(size=score_label.setter('text_size'))  # Для выравнивания текста по центру
            participants_grid.add_widget(score_label)

        # Очищаем текущий layout и добавляем новый с участниками
        self.participants_layout.clear_widgets()
        self.participants_layout.add_widget(participants_grid)

    def load_password(self):
        if exists("password.json"):
            with open("password.json", "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            # Если файл не существует, возвращаем стандартный пароль
            return "120598"

    def save_password(self, new_password):
        with open("password.json", "w", encoding='utf-8') as f:
            json.dump(new_password, f)

    def open_menu(self, instance):
        # Окно для ввода пароля перед открытием меню
        password_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        password_input = TextInput(hint_text='Введите пароль', password=True, size_hint=(0.8, 0.2),
                                   pos_hint={'center_x': 0.5})
        password_layout.add_widget(password_input)

        # Кнопка подтверждения пароля
        btn_confirm_password = Button(text="Открыть меню", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_password.bind(on_press=lambda x: self.check_password(password_input.text))
        password_layout.add_widget(btn_confirm_password)

        self.password_popup_window = Popup(title="Введите пароль", content=password_layout, size_hint=(0.8, 0.4))
        self.password_popup_window.open()

    def check_password(self, entered_password):
        # Загружаем текущий пароль из файла
        correct_password = self.load_password()
        if entered_password == correct_password:
            # Если пароль верен, открываем меню
            self.password_popup_window.dismiss()
            self.show_menu()
        else:
            # Если пароль неверен, показываем сообщение об ошибке
            error_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            error_label = Label(text="Неверный пароль!", size_hint_y=None, height=40, color=(1, 0, 0, 1))
            error_layout.add_widget(error_label)

            btn_close_error = Button(text="Закрыть", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
            btn_close_error.bind(on_press=self.password_popup_window.dismiss)
            error_layout.add_widget(btn_close_error)

            self.password_popup_window.content = error_layout

    def show_menu(self):
        # Отображаем меню после правильного ввода пароля
        menu_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Кнопка "Редактировать счет"
        btn_edit_score = Button(text="Редактировать счет", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_edit_score.bind(on_press=self.open_edit_score)
        menu_layout.add_widget(btn_edit_score)

        # Кнопка "Добавить/удалить участника"
        btn_edit_participants = Button(text="Добавить/удалить участника", size_hint=(0.5, 0.2),
                                       pos_hint={'center_x': 0.5})
        btn_edit_participants.bind(on_press=self.open_edit_participants)
        menu_layout.add_widget(btn_edit_participants)

        # Кнопка "Редактировать действия"
        btn_edit_actions = Button(text="Редактировать действия", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_edit_actions.bind(on_press=self.open_edit_actions_menu)
        menu_layout.add_widget(btn_edit_actions)

        # Кнопка "Редактировать историю"
        btn_edit_history = Button(text="Редактировать историю", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_edit_history.bind(on_press=self.open_edit_history_menu)
        menu_layout.add_widget(btn_edit_history)

        # Кнопка "Бонус"
        btn_bonus = Button(text="Бонус", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_bonus.bind(on_press=self.open_bonus_menu)
        menu_layout.add_widget(btn_bonus)

        # Кнопка "Изменить пароль"
        btn_change_password = Button(text="Изменить пароль", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_change_password.bind(on_press=self.open_change_password_popup)
        menu_layout.add_widget(btn_change_password)

        self.menu_popup_window = Popup(title="Меню", content=menu_layout, size_hint=(0.8, 0.6))
        self.menu_popup_window.open()

    def open_change_password_popup(self, instance):
        # Окно для изменения пароля
        change_password_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        new_password_input = TextInput(hint_text='Введите новый пароль', password=True, size_hint=(0.8, 0.2),
                                       pos_hint={'center_x': 0.5})
        change_password_layout.add_widget(new_password_input)

        confirm_password_input = TextInput(hint_text='Повторите новый пароль', password=True, size_hint=(0.8, 0.2),
                                           pos_hint={'center_x': 0.5})
        change_password_layout.add_widget(confirm_password_input)

        btn_confirm_new_password = Button(text="Изменить пароль", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_new_password.bind(
            on_press=lambda x: self.change_password(new_password_input.text, confirm_password_input.text))
        change_password_layout.add_widget(btn_confirm_new_password)

        self.change_password_popup = Popup(title="Изменить пароль", content=change_password_layout,
                                           size_hint=(0.8, 0.4))
        self.change_password_popup.open()

    def change_password(self, new_password, confirm_password):
        if new_password == confirm_password and new_password != "":
            # Сохраняем новый пароль
            self.save_password(new_password)
            self.change_password_popup.dismiss()
            self.menu_popup_window.dismiss()

            # Показываем сообщение о том, что пароль изменен
            success_popup = Popup(title="Успех", content=Label(text="Пароль успешно изменен"), size_hint=(0.6, 0.4))
            success_popup.open()
        else:
            # Показываем сообщение об ошибке при несоответствии паролей
            error_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            error_label = Label(text="Пароли не совпадают или пустые!", color=(1, 0, 0, 1))
            error_layout.add_widget(error_label)

            btn_close_error = Button(text="Закрыть", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
            btn_close_error.bind(on_press=self.change_password_popup.dismiss)
            error_layout.add_widget(btn_close_error)

            self.change_password_popup.content = error_layout

    def open_edit_score(self, instance):
        edit_score_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.participant_edit_spinner = Spinner(
            text='Выберите участника для редактирования',
            values=list(self.participants.keys()),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        edit_score_layout.add_widget(self.participant_edit_spinner)

        self.score_input = TextInput(hint_text='Введите новый счет', input_filter='int', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        edit_score_layout.add_widget(self.score_input)

        btn_confirm_edit = Button(text="Сохранить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_edit.bind(on_press=self.edit_score)
        edit_score_layout.add_widget(btn_confirm_edit)

        self.edit_score_popup_window = Popup(title="Редактировать счет", content=edit_score_layout, size_hint=(0.8, 0.6))
        self.edit_score_popup_window.open()

    def edit_score(self, instance):
        selected_participant = self.participant_edit_spinner.text
        new_score = self.score_input.text

        if selected_participant in self.participants and new_score:
            self.participants[selected_participant] = int(new_score)
            self.update_participant_labels()
            self.save_participants()

        self.edit_score_popup_window.dismiss()

    def open_edit_participants(self, instance):
        edit_participants_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.new_participant_input = TextInput(hint_text='Введите имя нового участника', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        edit_participants_layout.add_widget(self.new_participant_input)

        self.participant_delete_spinner = Spinner(
            text='Выберите участника для удаления',
            values=list(self.participants.keys()),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        edit_participants_layout.add_widget(self.participant_delete_spinner)

        btn_add_participant = Button(text="Добавить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_add_participant.bind(on_press=self.add_participant)
        edit_participants_layout.add_widget(btn_add_participant)

        btn_delete_participant = Button(text="Удалить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_delete_participant.bind(on_press=self.delete_participant)
        edit_participants_layout.add_widget(btn_delete_participant)

        self.edit_participants_popup_window = Popup(title="Редактировать участников", content=edit_participants_layout, size_hint=(0.8, 0.6))
        self.edit_participants_popup_window.open()

    def add_participant(self, instance):
        new_participant = self.new_participant_input.text.strip()
        if new_participant and new_participant not in self.participants:
            self.participants[new_participant] = 0
            self.update_participant_labels()
            self.save_participants()

        self.edit_participants_popup_window.dismiss()

    def delete_participant(self, instance):
        selected_participant = self.participant_delete_spinner.text
        if selected_participant in self.participants:
            del self.participants[selected_participant]
            self.update_participant_labels()
            self.save_participants()

        self.edit_participants_popup_window.dismiss()

    def open_edit_actions_menu(self, instance):
        edit_actions_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Кнопка "Удалить действие"
        btn_delete_action = Button(text="Удалить действие", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_delete_action.bind(on_press=self.open_delete_action_menu)
        edit_actions_layout.add_widget(btn_delete_action)

        # Кнопка "Редактировать действие"
        btn_edit_action = Button(text="Редактировать действие", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_edit_action.bind(on_press=self.open_edit_action_menu)
        edit_actions_layout.add_widget(btn_edit_action)

        # Кнопка "Добавить действие"
        btn_add_action = Button(text="Добавить действие", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_add_action.bind(on_press=self.open_add_action_menu)
        edit_actions_layout.add_widget(btn_add_action)

        self.edit_actions_popup_window = Popup(title="Редактировать действия", content=edit_actions_layout, size_hint=(0.8, 0.6))
        self.edit_actions_popup_window.open()

    def open_delete_action_menu(self, instance):
        delete_action_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.action_delete_spinner = Spinner(
            text='Выберите действие для удаления',
            values=list(self.actions.keys()),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        delete_action_layout.add_widget(self.action_delete_spinner)

        btn_confirm_delete = Button(text="Удалить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_delete.bind(on_press=self.delete_action)
        delete_action_layout.add_widget(btn_confirm_delete)

        self.delete_action_popup_window = Popup(title="Удалить действие", content=delete_action_layout, size_hint=(0.8, 0.6))
        self.delete_action_popup_window.open()

    def open_edit_action_menu(self, instance):
        edit_action_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.action_edit_spinner = Spinner(
            text='Выберите действие для редактирования',
            values=list(self.actions.keys()),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        edit_action_layout.add_widget(self.action_edit_spinner)

        self.new_points_input = TextInput(hint_text='Введите новые очки', input_filter='float', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        edit_action_layout.add_widget(self.new_points_input)

        btn_confirm_edit = Button(text="Сохранить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_edit.bind(on_press=self.edit_action)
        edit_action_layout.add_widget(btn_confirm_edit)

        self.edit_action_popup_window = Popup(title="Редактировать действие", content=edit_action_layout, size_hint=(0.8, 0.6))
        self.edit_action_popup_window.open()

    def open_add_action_menu(self, instance):
        add_action_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.new_action_input = TextInput(hint_text='Введите новое действие', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        add_action_layout.add_widget(self.new_action_input)

        self.new_action_points_input = TextInput(hint_text='Введите очки за действие', input_filter='float', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        add_action_layout.add_widget(self.new_action_points_input)

        btn_confirm_add = Button(text="Добавить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm_add.bind(on_press=self.add_new_action)
        add_action_layout.add_widget(btn_confirm_add)

        self.add_action_popup_window = Popup(title="Добавить действие", content=add_action_layout, size_hint=(0.8, 0.6))
        self.add_action_popup_window.open()

    def delete_action(self, instance):
        selected_action = self.action_delete_spinner.text
        if selected_action in self.actions:
            del self.actions[selected_action]
            self.save_actions()
            self.update_participant_labels()

        self.delete_action_popup_window.dismiss()

    def edit_action(self, instance):
        selected_action = self.action_edit_spinner.text
        new_points = self.new_points_input.text

        if selected_action in self.actions and new_points:
            self.actions[selected_action] = float(new_points)
            self.save_actions()
            self.update_participant_labels()

        self.edit_action_popup_window.dismiss()

    def add_new_action(self, instance):
        new_action = self.new_action_input.text.strip()
        new_points = self.new_action_points_input.text

        if new_action and new_points:
            if new_action not in self.actions:
                self.actions[new_action] = float(new_points)
                self.save_actions()
                self.update_participant_labels()
            else:
                # Действие уже существует, можно обновить его или показать предупреждение
                pass  # Для простоты не обрабатываем этот случай

        self.add_action_popup_window.dismiss()

    def add_action_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.participant_spinner = Spinner(
            text='Выберите участника',
            values=list(self.participants.keys()),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        popup_layout.add_widget(self.participant_spinner)

        actions_with_points = [f"{action} ({points})" for action, points in self.actions.items()]
        self.action_spinner = Spinner(
            text='Выберите действие',
            values=actions_with_points,
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        popup_layout.add_widget(self.action_spinner)

        self.qty_input = TextInput(
            hint_text='Введите количество',
            input_filter='int',
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            multiline=False
        )
        popup_layout.add_widget(self.qty_input)

        btn_confirm = Button(text="Подтвердить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm.bind(on_press=self.confirm_action)
        popup_layout.add_widget(btn_confirm)

        # Добавляем квадратную кнопку закрытия внизу слева
        btn_close = Button(text="X", size_hint=(None, None), size=(40, 40), pos_hint={'x': 0, 'y': 0})
        btn_close.bind(on_press=lambda x: self.add_action_popup_window.dismiss())  # Закрытие окна
        popup_layout.add_widget(btn_close)

        self.add_action_popup_window = Popup(title="Добавить действие", content=popup_layout, size_hint=(0.8, 0.6))
        self.add_action_popup_window.open()

    def confirm_action(self, instance):
        selected_participant = self.participant_spinner.text
        selected_action = self.action_spinner.text.split(" (")[0]
        qty = self.qty_input.text

        if not qty:
            qty = 1
        else:
            try:
                qty = int(qty)
            except ValueError:
                qty = 1  # По умолчанию

        if selected_participant in self.participants and selected_action in self.actions:
            points_earned = self.actions[selected_action] * qty
            self.participants[selected_participant] += points_earned
            self.update_participant_labels()
            self.save_participants()

            action_record = {
                'participant': selected_participant,
                'action': selected_action,
                'points': points_earned,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.history.append(action_record)
            self.save_history()

        self.add_action_popup_window.dismiss()

    def open_history(self, instance):
        history_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        scroll_view = ScrollView(size_hint=(1, 0.9))  # Уменьшил высоту scroll_view, чтобы оставить место для кнопки

        # Создаем GridLayout с четырьмя столбцами
        history_grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        history_grid.bind(minimum_height=history_grid.setter('height'))

        # Устанавливаем относительные размеры для заголовков колонок
        headers = {'Дата': 0.2, 'Синтетик': 0.2, 'Действие': 0.4, 'Количество': 0.2}

        # Добавляем заголовки для колонок
        for header in headers:
            header_label = Label(text=header, bold=True, font_size='18sp', size_hint_y=None, height=40,
                                 color=(1, 1, 1, 1), size_hint_x=headers[header], halign='center', valign='middle')
            header_label.bind(size=header_label.setter('text_size'))
            history_grid.add_widget(header_label)

        # Сортируем историю для отображения
        sorted_history = sorted(self.history, key=lambda x: x['date'], reverse=True)

        # Добавляем записи истории в виде строк с четырьмя колонками
        for record in sorted_history:
            # Форматируем дату
            record_datetime = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
            formatted_date = record_datetime.strftime('%Y-%m-%d %H:%M')

            date_label = Label(text=formatted_date, font_size='16sp', size_hint_y=None, height=30, color=(1, 1, 1, 1),
                               size_hint_x=headers['Дата'], halign='center', valign='middle')
            date_label.bind(size=date_label.setter('text_size'))

            participant_label = Label(text=f"{record['participant']}", font_size='16sp', size_hint_y=None, height=30,
                                      color=(1, 1, 1, 1), size_hint_x=headers['Синтетик'], halign='center',
                                      valign='middle')
            participant_label.bind(size=participant_label.setter('text_size'))

            action_label = Label(text=f"{record['action']}", font_size='12sp', size_hint_y=None, height=30,
                                 color=(1, 1, 1, 1), size_hint_x=headers['Действие'], halign='center', valign='middle')
            action_label.bind(size=action_label.setter('text_size'))

            # Округляем количество до трех знаков после запятой
            rounded_points = round(record['points'], 3)
            points_label = Label(text=f"{rounded_points}", font_size='16sp', size_hint_y=None, height=30,
                                 color=(1, 1, 1, 1), size_hint_x=headers['Количество'], halign='center',
                                 valign='middle')
            points_label.bind(size=points_label.setter('text_size'))

            # Добавляем все колонки в строку
            history_grid.add_widget(date_label)
            history_grid.add_widget(participant_label)
            history_grid.add_widget(action_label)
            history_grid.add_widget(points_label)

        scroll_view.add_widget(history_grid)
        history_layout.add_widget(scroll_view)

        # Создаем layout для кнопки закрытия
        button_layout = BoxLayout(orientation='horizontal', padding=5, size_hint=(1, 0.1))

        # Добавляем кнопку закрытия
        btn_close = Button(text="Закрыть", size_hint=(0.2, 1), pos_hint={'x': 0, 'y': 0})
        btn_close.bind(on_press=lambda x: self.history_popup_window.dismiss())  # Закрыть окно
        button_layout.add_widget(btn_close)

        history_layout.add_widget(button_layout)

        self.history_popup_window = Popup(title="История действий", content=history_layout, size_hint=(0.9, 0.9))
        self.history_popup_window.open()

    def open_edit_history_menu(self, instance):
        edit_history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ScrollView для отображения истории с кнопками удаления
        scroll_view = ScrollView(size_hint=(1, 0.8))

        history_box = BoxLayout(orientation='vertical', size_hint_y=None)
        history_box.bind(minimum_height=history_box.setter('height'))

        # Сортируем историю для отображения
        self.sorted_history = sorted(self.history, key=lambda x: x['date'], reverse=True)

        # Создаем кнопки для каждого события в истории
        for idx, record in enumerate(self.sorted_history):
            def create_event_button(idx=idx, record=record):
                event_button = Button(
                    text=f"{record['date']} - {record['participant']} - {record['action']} - {record['points']} очков",
                    size_hint_y=None,
                    height=40
                )
                event_button.bind(on_press=lambda btn, idx=idx: self.confirm_delete_event(idx))
                return event_button

            history_box.add_widget(create_event_button())

        scroll_view.add_widget(history_box)
        edit_history_layout.add_widget(scroll_view)

        # Кнопка закрытия окна редактирования истории
        btn_close = Button(text="Закрыть", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        btn_close.bind(on_press=self.close_edit_history_popup)
        edit_history_layout.add_widget(btn_close)

        self.edit_history_popup_window = Popup(title="Редактировать историю", content=edit_history_layout,
                                               size_hint=(0.8, 0.8))
        self.edit_history_popup_window.open()

    def confirm_delete_event(self, index):
        # Окно подтверждения удаления события
        confirm_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Используем запись из отсортированного списка
        record = self.sorted_history[index]

        confirmation_label = Label(
            text=f"Вы уверены, что хотите удалить это событие?\n"
                 f"{record['date']} - {record['participant']} - {record['action']} - {record['points']} очков",
            size_hint_y=None,
            height=60
        )
        confirm_layout.add_widget(confirmation_label)

        # Кнопки подтверждения и отмены
        btn_confirm = Button(text="Удалить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm.bind(
            on_press=lambda btn: self.delete_history_entry(index))  # Передаем индекс отсортированной записи
        confirm_layout.add_widget(btn_confirm)

        btn_cancel = Button(text="Отмена", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_cancel.bind(on_press=lambda btn: self.confirm_delete_popup.dismiss())
        confirm_layout.add_widget(btn_cancel)

        self.confirm_delete_popup = Popup(title="Подтверждение удаления", content=confirm_layout, size_hint=(0.8, 0.6))
        self.confirm_delete_popup.open()

    def delete_history_entry(self, index):
        # Удаляем запись на основании сортированного списка
        if 0 <= index < len(self.sorted_history):
            # Ищем фактический индекс записи в оригинальной истории
            record_to_delete = self.sorted_history[index]
            original_index = self.history.index(record_to_delete)

            # Убираем очки у участника
            participant = record_to_delete['participant']
            points = record_to_delete['points']
            if participant in self.participants:
                self.participants[participant] -= points
                self.update_participant_labels()
                self.save_participants()

            # Удаляем запись из истории
            del self.history[original_index]
            self.save_history()

            # Закрываем окно подтверждения
            self.confirm_delete_popup.dismiss()

            # Обновляем окно редактирования истории
            self.edit_history_popup_window.dismiss()
            self.open_edit_history_menu(None)

    def close_edit_history_popup(self, instance):
        self.edit_history_popup_window.dismiss()

    def open_todo_list(self, instance):
        todo_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        scroll_view = ScrollView(size_hint=(1, 0.9))  # Уменьшил высоту scroll_view, чтобы было место для кнопки

        # Создаем GridLayout с двумя столбцами
        todo_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        todo_grid.bind(minimum_height=todo_grid.setter('height'))

        # Устанавливаем относительные размеры для заголовков колонок
        headers = {'Название': 0.7, 'Цена': 0.3}

        # Добавляем заголовки для колонок
        for header in headers:
            header_label = Label(text=header, bold=True, font_size='18sp', size_hint_y=None, height=40,
                                 color=(1, 1, 1, 1), size_hint_x=headers[header], halign='center', valign='middle')
            header_label.bind(size=header_label.setter('text_size'))
            todo_grid.add_widget(header_label)

        # Добавляем записи действий из словаря `self.actions` в виде строк с двумя колонками
        for action_name, action_price in self.actions.items():
            name_label = Label(text=action_name, font_size='16sp', size_hint_y=None, height=30,
                               color=(1, 1, 1, 1), size_hint_x=headers['Название'], halign='center', valign='middle')
            name_label.bind(size=name_label.setter('text_size'))

            # Округляем цену до трех знаков после запятой
            rounded_price = round(action_price, 3)
            price_label = Label(text=f"{rounded_price}", font_size='16sp', size_hint_y=None, height=30,
                                color=(1, 1, 1, 1), size_hint_x=headers['Цена'], halign='center', valign='middle')
            price_label.bind(size=price_label.setter('text_size'))

            # Добавляем обе колонки в строку
            todo_grid.add_widget(name_label)
            todo_grid.add_widget(price_label)

        scroll_view.add_widget(todo_grid)
        todo_layout.add_widget(scroll_view)

        # Создаем layout для кнопки закрытия
        button_layout = BoxLayout(orientation='horizontal', padding=5, size_hint=(1, 0.1))

        # Добавляем кнопку закрытия
        btn_close = Button(text="Закрыть", size_hint=(0.2, 1), pos_hint={'x': 0, 'y': 0})
        btn_close.bind(on_press=lambda x: self.todo_popup_window.dismiss())  # Закрыть окно
        button_layout.add_widget(btn_close)

        todo_layout.add_widget(button_layout)

        self.todo_popup_window = Popup(title="Список дел", content=todo_layout, size_hint=(0.9, 0.9))
        self.todo_popup_window.open()

    def open_bonus_menu(self, instance):
        bonus_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Спиннер для выбора участника
        participant_spinner = Spinner(
            text='Выберите участника',
            values=list(self.participants.keys()),  # Список участников
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        bonus_layout.add_widget(participant_spinner)

        # Поле для ввода названия бонуса
        bonus_name_input = TextInput(
            hint_text='Введите название бонуса',
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        bonus_layout.add_widget(bonus_name_input)

        # Поле для ввода количества очков
        bonus_points_input = TextInput(
            hint_text='Введите количество очков',
            input_filter='float',  # Ограничение на ввод только чисел
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}
        )
        bonus_layout.add_widget(bonus_points_input)

        # Кнопка подтверждения
        btn_confirm = Button(text="Подтвердить", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        btn_confirm.bind(on_press=lambda x: self.confirm_bonus_action(participant_spinner.text, bonus_name_input.text,
                                                                      bonus_points_input.text))
        bonus_layout.add_widget(btn_confirm)

        # Открытие окна бонуса
        self.bonus_popup = Popup(title="Начисление бонуса", content=bonus_layout, size_hint=(0.8, 0.6))
        self.bonus_popup.open()

    def confirm_bonus_action(self, participant, bonus_name, points):
        # Проверка корректности ввода
        if participant in self.participants and bonus_name and points:
            try:
                points = float(points)
            except ValueError:
                points = 0  # Если введено некорректное значение, установить очки в 0

            # Начисление очков выбранному участнику
            self.participants[participant] += points
            self.update_participant_labels()
            self.save_participants()

            # Добавление записи в историю
            action_record = {
                'participant': participant,
                'action': bonus_name,  # Название бонуса как действие
                'points': points,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата
            }
            self.history.append(action_record)
            self.save_history()

            # Закрытие окна бонуса
            self.bonus_popup.dismiss()

            # Уведомление об успешном начислении
            success_popup = Popup(title="Успех", content=Label(text="Бонус успешно начислен"), size_hint=(0.6, 0.4))
            success_popup.open()
        else:
            # Ошибка при некорректном вводе
            error_popup = Popup(title="Ошибка", content=Label(text="Неправильные данные, попробуйте снова"),
                                size_hint=(0.6, 0.4))
            error_popup.open()


if __name__ == "__main__":
    mainApp().run()
