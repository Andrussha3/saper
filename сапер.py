import tkinter as tk
from tkinter import messagebox, font
import random


class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=15):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # Настройки стилей
        self.big_font = font.Font(size=16, weight='bold')  # Увеличенный шрифт
        self.large_font = font.Font(size=14)  # Шрифт для кнопки новой игры
        self.opened_color = '#f0f0f0'
        self.closed_color = '#c0c0c0'
        self.flag_color = '#ffcccc'
        self.mine_color = '#ff0000'

        self.create_ui()
        self.new_game()

    def create_ui(self):
        # Увеличиваем размер кнопки новой игры
        self.reset_button = tk.Button(self.master,
                                      text="Новая игра",
                                      command=self.new_game,
                                      height=2,
                                      font=self.large_font,
                                      bg='#e0e0e0')
        self.reset_button.grid(row=self.rows, columnspan=self.cols, sticky="we")

        # Создаем увеличенные клетки поля
        self.buttons = {}
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.master,
                                   text='',
                                   width=3,  # Уменьшаем width для квадратных кнопок
                                   height=2,
                                   font=self.big_font,
                                   bg=self.closed_color,
                                   relief='raised',
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.bind('<Button-3>', lambda e, r=row, c=col: self.on_right_click(r, c))
                button.grid(row=row, column=col, padx=2, pady=2)  # Увеличили отступы
                self.buttons[(row, col)] = button

    def new_game(self):
        self.mine_positions = set()
        self.opened = 0
        self.game_active = True

        # Сбрасываем все кнопки
        for button in self.buttons.values():
            button.config(text='',
                          state='normal',
                          bg=self.closed_color,
                          relief='raised',
                          fg='black')

        # Размещаем мины
        self.place_mines()

    def place_mines(self):
        """Размещение мин на поле"""
        while len(self.mine_positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.mine_positions.add((row, col))

    def count_adjacent_mines(self, row, col):
        """Подсчет мин вокруг клетки"""
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mine_positions:
                    count += 1
        return count

    def on_click(self, row, col):
        """Обработка клика левой кнопкой мыши"""
        if not self.game_active:
            return

        button = self.buttons[(row, col)]

        # Игнорируем открытые клетки и клетки с флагами
        if button['state'] == 'disabled' or button['text'] == '🚩':
            return

        # Проверка на мину
        if (row, col) in self.mine_positions:
            button.config(bg=self.mine_color, text='💣', font=self.big_font)
            self.game_over()
            return

        # Подсчет соседних мин
        mines_nearby = self.count_adjacent_mines(row, col)

        # Настройка внешнего вида открытой клетки
        button.config(text=str(mines_nearby) if mines_nearby else '',
                      state='disabled',
                      bg=self.opened_color,
                      relief='sunken',
                      fg=self.get_number_color(mines_nearby),
                      font=self.big_font)

        self.opened += 1

        # Проверка победы
        if self.opened == self.rows * self.cols - self.mines:
            self.victory()
            return

        # Автоматическое открытие пустых областей
        if mines_nearby == 0:
            for r in range(max(0, row - 1), min(self.rows, row + 2)):
                for c in range(max(0, col - 1), min(self.cols, col + 2)):
                    if (r, c) != (row, col) and self.buttons[(r, c)]['state'] == 'normal':
                        self.on_click(r, c)

    def get_number_color(self, num):
        """Возвращает цвет для цифры"""
        colors = ['', 'blue', 'green', 'red', 'darkblue',
                  'brown', 'teal', 'black', 'gray']
        return colors[num] if 0 < num < len(colors) else 'black'

    def on_right_click(self, row, col):
        """Обработка клика правой кнопкой мыши (установка флажка)"""
        if not self.game_active:
            return

        button = self.buttons[(row, col)]

        if button['state'] == 'normal':
            if button['text'] == '':
                button.config(text='🚩', bg=self.flag_color, font=self.big_font)
            elif button['text'] == '🚩':
                button.config(text='', bg=self.closed_color)

    def game_over(self):
        """Обработка проигрыша"""
        self.game_active = False
        # Показываем все мины
        for (row, col) in self.mine_positions:
            self.buttons[(row, col)].config(text='💣', bg=self.mine_color, font=self.big_font)
        messagebox.showinfo("Game Over", "Вы наступили на мину!")

    def victory(self):
        """Обработка победы"""
        self.game_active = False
        # Помечаем все мины флагами
        for (row, col) in self.mine_positions:
            self.buttons[(row, col)].config(text='🚩', bg=self.flag_color, font=self.big_font)
        messagebox.showinfo("Победа!", "Вы нашли все мины!")


# Настройка главного окна
root = tk.Tk()
root.title("Сапёр")
root.minsize(600, 600)  # Увеличили минимальный размер окна

# Запуск игры
game = Minesweeper(root)
root.mainloop()