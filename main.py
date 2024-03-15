import tkinter as tk
import numpy as np #нужен для рандомного заполнения поля, а также переноса и очистки

class LifeGame:
    def __init__(self, master, wid=40, hei=40, cell_size=15):
        #иницализация класса
        self.master = master
        self.wid = wid
        self.hei = hei
        self.cell_size = cell_size
        #создаем массив типа bool для ячеек
        self.pole = np.zeros((hei, wid), dtype=bool)

        canvas_width = wid * cell_size
        canvas_height = hei * cell_size

        #настройка окна
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack()

        #создание возможности добавлять поле по щелчкам
        self.canvas.bind('<Button-1>', self.changePole)

        #создание кнопок
        self.start_button = tk.Button(master, text='Start', command=self.startEvolution, bg='green', width=10)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text='Stop', command=self.stopEvolution, bg='red', width=10)
        self.stop_button.pack()
        self.stop_button.config(state=tk.DISABLED)

        self.clear_button = tk.Button(master, text='Clear', command=self.clearPole, bg='green',width=10)
        self.clear_button.pack()

        self.random_button = tk.Button(master, text='Random Fill', command=self.randomFillPole, bg='green',width=10)
        self.random_button.pack()

        #параметр скорости, может быть изменен
        self.evolve_speed = 100  # in milliseconds
        self.running = False

        #рандомное заполнение поля сразу, при запуске игры
        self.randomFillPole()

    #функция для переключения ячеек
    def changePole(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.pole[y, x] = not self.pole[y, x]
        self.drawPole()

    #функция отрисовки поля
    def drawPole(self):
        self.canvas.delete('cells')
        for y in range(self.hei):
            for x in range(self.wid):
                if self.pole[y, x]:
                    x0 = x * self.cell_size
                    y0 = y * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black', tags='cells')
                else:
                    x0 = x * self.cell_size
                    y0 = y * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline='gray', tags='cells')

        #отрисовка сетки
        for i in range(self.wid):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.hei * self.cell_size, fill='gray', tags='grid')

        for i in range(self.hei):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.wid * self.cell_size, y, fill='gray', tags='grid')

    #функция для подсчета живых соседей
    def countNeighbors(self, x, y):
        count = 0
        for oy in [-1, 0, 1]:
            for ox in [-1, 0, 1]:
                if ox == 0 and oy == 0:
                    continue
                nx = x + ox
                ny = y + oy
                if 0 <= nx < self.wid and 0 <= ny < self.hei:
                    count += self.pole[ny, nx]
        return count

    # функция для изменения клеток на поле
    def evolution(self):
        new_gr = np.copy(self.pole)
        for y in range(self.hei):
            for x in range(self.wid):
                neighbors = self.countNeighbors(x, y)
                if self.pole[y, x]:
                    if neighbors < 2 or neighbors > 3:
                        new_gr[y, x] = False
                else:
                    if neighbors == 3:
                        new_gr[y, x] = True
        self.pole = new_gr
        self.drawPole()
        if self.running:
            self.master.after(self.evolve_speed, self.evolution)

    #запуск эволюции
    def startEvolution(self):
        self.evolve_speed = 100
        self.running = True
        self.start_button.config(state=tk.DISABLED, bg='gray')
        self.stop_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.DISABLED, bg='gray')
        self.random_button.config(state=tk.DISABLED, bg='gray')
        self.evolution()

    #остановка эволюции
    def stopEvolution(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL, bg='green')
        self.stop_button.config(state=tk.DISABLED, bg='red')
        self.clear_button.config(state=tk.NORMAL, bg='green')
        self.random_button.config(state=tk.NORMAL, bg='green')

    #функция для очистки поля
    def clearPole(self):
        self.pole = np.zeros((self.hei, self.wid), dtype=bool)
        self.drawPole()

    #функция для рандомного заполнения заполнения поля
    def randomFillPole(self):
        # выбираем, заполнится ли ячейка через функцию np.random.choice
        self.pole = np.random.choice([False, True], size=(self.hei, self.wid), p=[0.5, 0.5])
        self.evolve_speed = 100
        self.drawPole()

#создание окна и запуск игры
qwe = tk.Tk()
qwe.title("Life game by pluffohman")
game = LifeGame(qwe)
qwe.mainloop()
