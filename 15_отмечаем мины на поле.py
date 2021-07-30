"""
10_Сапер_Обход в ширину. Minesweeper in Python Tkinter.py

редактируем def click: -> убираем



"""
import tkinter as tk
from random import shuffle  # перемешивает нашу коллекцию
from tkinter.messagebox import showinfo, showerror  # позволяет создавать диологовое окно

colors = {
    0: 'red',
    1: 'blue',
    2: '#008200',
    3: '#FF0000',
    4: '#000084',
    5: '#840000',
    6: '#008284',
    7: '#840084',
    8: '#000000',
}


class MyButton(tk.Button):  # создаем класс с наследованием у класса tk.Button,  чтоб так НЕ распечатывалась <tkinter.Button object .!button29>, а по другому
    # !!! и ВЛОЖИТЬ дополнительную информацию в кнопки
    # !!! для этого нам нужно переинициализировать класс
    # number добавили для нумерации кнопок
    def __init__(self, master, x, y, number=0, *args,
                 **kwargs):  # master - окно на котором будет создаваться наша кнопка, x,y-координаты(строка, столбец), # и дальше принимаем все входящие аргументы при помощи *args, **kwargs
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False # атрибут открытия кнопки / изначально мы не открывали

    def __repr__(self):  # функция как будет распечатываться объекты внутри консоли
        return f'MyButton {self.x, self.y, self.number, self.is_mine}'  # теперь в консоли видим координаты кнопок; номера кнопок; бомба кнопка или нет;


class MineSweeper:
    window = tk.Tk()
    ROW = 7
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True # добавляем переменную для первого клика/ чтоб только после него создавались бомбы

    def __init__(self):
        self.buttons = []

        for i in range(MineSweeper.ROW+2): # +2 это барьерные элементы
            temp = []
            for j in range(MineSweeper.COLUMNS+2): # +2 это барьерные элементы
                btn = MyButton(MineSweeper.window, x=i, y=j)  # создание кнопки при помощи нашего класса MyButton

                btn.config(command=lambda knopka=btn: self.click(knopka))  # knopka - произвольно выдуманное имя

                temp.append(btn)

            self.buttons.append(temp)

    def click(self,clicked_button: MyButton):  # метод нажатия кнопок , принимает кнопку и аннотация-ожидаем объект MyButton

        if MineSweeper.IS_GAME_OVER: # Убираем подолжение игры после проигрыша (кнопки не нажимаются)
            return        # тоже самое что и return None

        if MineSweeper.IS_FIRST_CLICK: # если это первое нажатие / делаем для того чтоб только после него создавались бомбы
            self.insert_mines(clicked_button.number)  # расставляем бомбы
            self.count_mines_in_buttons()  # подсчитываем бомбы
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False # закрываем создание игрового поля после первого нажатия ( исправили баг с 11части)


        if clicked_button.is_mine:  # если кнопка мина, то
            clicked_button.config(text="*", background='red', disabledforeground='black')  # , то на кнопке звездочка при нажатии,
                                                            # disabledforeground='black' - при блокировке звездочка будет черного цвета
            clicked_button.is_open = True # отмечаем что кнопку нажали
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW + 1):  # вставляем этот цикл из insert_mines чтоб при Game over показывались все мины
                for j in range(1, MineSweeper.COLUMNS + 1):  #
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text']='*'

        else:
            color_btn = colors.get(clicked_button.count_bomb,'black')  # из словаря получаем значение ключа(цвет), если нет такого ключа то 'black'
            # clicked_button.config(text=clicked_button.number, disabledforeground='black')  # выводим при нажатиии на кнопку её номер
            # clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color_btn)  # выводим при нажатиии на кнопку кол-во бомб
            if clicked_button.count_bomb: # если True т.е. если нажатая кнопка имееет бомбы вокруг
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color_btn)  # выводим при нажатиии на кнопку кол-во бомб
                '''теперь получилось ячейка с 0 не будет показываться ЗАЧЕМ дублировать эффект else_ом???'''
                clicked_button.is_open = True  # отмечаем что кнопку нажали

            else:
                #'''если 0 бомб вокруг то выводим пустую строку '''
                # clicked_button.config(text='', disabledforeground=color_btn)  # убираем в 10_уроке
                # =>
                ''' если 0 бомб вокруг то используем функцию передавая ту кнопку которая нажата'''
                self.breadth_first_search(clicked_button) # обход в ширину пкстых клеток / добавляем  в 10_уроке


        clicked_button.config(state='disabled') # блокируем повторное нажатие и текст становиться серым, а disabledforeground='black' этим мы делаем его черным
        clicked_button.config(relief=tk.SUNKEN)  # кнопка после нажатия остается вдавлена

    def breadth_first_search(self, btn: MyButton): # принимает кнопку и добавляем анотацию что она принадлежит классу MyButton
        queue = [btn] # в этот список кладем нашу кнопку
        while queue: # пока в списке есть кнопки

            cur_btn = queue.pop()    # переменая "текущая кромка" , мы будем брать ее из списка "queue" методом .pop()
            color_btn = colors.get(cur_btn.count_bomb,'black')  # из словаря получаем значение ключа(цвет), если нет такого ключа то 'black'
            if cur_btn.count_bomb: # если текущая кромка имеет бомбы (граничит с бомбами)
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color_btn)  # выводим надпись кол-во бомб в определенном цвете
            else: # в противном случая текущая кромка НЕ имеет бомбы (НЕ граничит с бомбами)
                cur_btn.config(text='', disabledforeground=color_btn)  # выводим пустой текст

            cur_btn.is_open = True  # отмечаем что кнопку нажали

            cur_btn.config(state='disabled')  # блокируем повторное нажатие и текст становиться серым, а disabledforeground='black' этим мы делаем его черным
            cur_btn.config(relief=tk.SUNKEN)  # кнопка после нажатия остается вдавлена

            if cur_btn.count_bomb == 0: # если текущая кнопка не имеет бомб , т.е. равна 0
                x, y = cur_btn.x, cur_btn.y # присваеваем X и Y , значения X и Y от текущей кнопки
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1: # коментируем в 11части чтоб клетки открывались и на искосок
                        #     continue

                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<=next_btn.x<=MineSweeper.ROW and 1<=next_btn.y<=MineSweeper.COLUMNS and next_btn not in queue:
                        # если кнопка не была открыта, не является барьерным элементом и её нет в списке queue
                            queue.append(next_btn) # добавляем ее в список

    def reload(self):
        #self.window.winfo_children()[0].destroy() # self.window.winfo_children() лежит список элементов окна игры в том числе кнопки, к элементам [...] обращаемся по индексу, методом .destroy() уничтожаем элемент
        [child.destroy() for child in self.window.winfo_children()] # вызываем метод .destroy() у каждого элемента списка и в итоге получаем пустое окно tkinter
        self.__init__() # инициализируем метод init для создания кнопок
        self.create_widget() # создаем окно с кнопками
        MineSweeper.IS_FIRST_CLICK=True # устанавливаем параметр первого клика в первоначальное значение (обнуляем первое нажатие)
        MineSweeper.IS_GAME_OVER=False # прописываем на случай если игра закончилась и запустили настройки


    def create_settings_win(self):
        win_settings=tk.Toplevel(self.window) # создаем дочернее окно вызывая класс tk  Toplevel и пердаем к какому окну будет относится
        win_settings.wm_title('Настройки')    # вставляем название Окна
        tk.Label(win_settings, text='Колличество  строк').grid(row=0, column=0)   # создаем первый лейбл и сразу с помощью .grid() распологаем его в окне
        tk.Label(win_settings, text='Колличество  колонок').grid(row=1, column=0)   # создаем второй лейбл и сразу с помощью .grid() распологаем его в окне
        tk.Label(win_settings, text='Колличество  мин').grid(row=2, column=0)   # создаем третий лейбл и сразу с помощью .grid() распологаем его в окне

        row_entry = tk.Entry(win_settings)      # окно ввода колличества рядов
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        column_entry = tk.Entry(win_settings)   # окно ввода колличества колонок
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        mines_entry = tk.Entry(win_settings)    # окно ввода колличества мин
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        # создаем кнопку - применить настройки
        '''для функции change_settings будут недоступны параметры содержимого окон ввода create_settings_win
        для этого создадим функцию lambda: которая принимает  change_settings(...) с аргументами'''
        save_btn = tk.Button(win_settings, text='Применить', command=lambda :self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20) # выводим кнопку в окно  третий ряд-нулевая колонка-объединяем две колонки, и делаем отступы

    def change_settings(self, row: tk.Entry, column:tk.Entry, mines: tk.Entry):
        # сделаем исключение для обработки ввода других символов вместо цифр
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение') # для вывода окна ошибки добавим модуль  tkinter.messagebox  -> showerror
            return

        MineSweeper.ROW = int(row.get())               # получаем данные с окна настроек переводя в инт и сохраняем в нашу глобальную переменную
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())

        '''после настроек перезапускаем игру'''
        self.reload()


    def create_widget(self):

        # создаем главное меню
        menubar = tk.Menu(self.window) # создаем меню и крепим его к окну(self.window)
        self.window.config(menu=menubar) # присваиваем переменную меню

        # создаем под меню
        setting_menu = tk.Menu(menubar, tearoff=0) # tearoff=0 -убираем кнопку пунктирную линию в под меню
        setting_menu.add_command(label='Играть', command=self.reload) # добавляем название первой кнопки / команда функция - def reload
        setting_menu.add_command(label='Настройки', command=self.create_settings_win) # добавляем название второй кнопки / команда метода(функции) - def create_settings_win
        setting_menu.add_command(label='Выход', command=self.window.destroy) # добавляем название третьей кнопки / команда закрытия окна
        menubar.add_cascade(label='Файл', menu=setting_menu) # добавляем кнопку Главного меню



        count = 1
        for i in range(1, MineSweeper.ROW + 1): # убираем из окна кнопки барьерных элементов
            for j in range(1, MineSweeper.COLUMNS + 1): # убираем из окна кнопки барьерных элементов
        # for i in range(MineSweeper.ROW+2): # +2 это барьерные элементы
        #     for j in range(MineSweeper.COLUMNS+2): # +2 это барьерные элементы
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')  # метод stick='NWES' позволяет растянуть кнопки относительно сторонам света Север-Запад-Восток-Юг
                count += 1


        # фиксируем размер кнопок относительно окна
        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1) # weight=1 - вес Единица, т.е. каждому ряду будет по одной равной части (допустим 10рядов то поле делится на 10 и кождому по 1части)
        for i in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1) # weight=1 - вес Единица, т.е. каждой колонке будет по одной равной части (допустим 5колонок то поле делится на 5 и кождой по 1части)



    def open_all_buttons(self): # открыть все кнопки ( техническая функция для барьерных элементов)
        for i in range(MineSweeper.ROW+2): # +2 это барьерные элементы
            for j in range(MineSweeper.COLUMNS+2): # +2 это барьерные элементы
                btn = self.buttons[i][j]
                if btn.is_mine:  # если кнопка мина, то
                    btn.config(text="*", background='red', disabledforeground='black')  # , то на кнопке звездочка при нажатии,
                # elif btn.count_bomb == 1:
                #     btn.config(text=btn.count_bomb, fg='blue') # fg='blue' текст(цифра 1)  синий


                elif btn.count_bomb in colors: # если кнопка есть в словаре цветов
                    color_btn = colors.get(btn.count_bomb, 'black') # из словаря получаем значение ключа(цвет), если нет такого ключа то 'black'
                    btn.config(text=btn.count_bomb, fg=color_btn)  # выводим при нажатиии на кнопку её номер


    def start(self):
        self.create_widget()

        ###--- ниже код переносим в def click / чтоб бомбы создавались послле первого клика
        # self.insert_mines()  # расставляем бомбы
        # self.count_mines_in_buttons() # подсчитываем бомбы
        # self.print_buttons()

        # print(self.get_mines_places()) # выводим в консоль наш список мин
        # self.open_all_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):  # не берем 0 индекс и последний не включаем в диапазон
            for j in range(1, MineSweeper.COLUMNS + 1):  # не берем 0 индекс и последний не включаем в диапазон
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end='') # end='' убираем перенос строки
                else:
                    print(btn.count_bomb, end='') # сколько мин вокруг кнопки , end='' убираем перенос строки
            print()

    def insert_mines(self, number:int):  # метод вставляет бомбы в кнопки (ячейки) / number:int - добавили в 11части и пойдет в .get_mines_places()
        index_mines = self.get_mines_places(number)  # получаем индексы наших бомб / number исключается из списка бомб т.к. это первая нажатая кнопка
        print(index_mines)  # просто посмотреть как проставились бомбочки
        # count=1 # переносим в 11части в def create_widget
        for i in range(1, MineSweeper.ROW + 1):  # не берем 0 индекс и последний не включаем в диапазон
            for j in range(1, MineSweeper.COLUMNS + 1):  # не берем 0 индекс и последний не включаем в диапазон
                btn = self.buttons[i][j]
                # btn.number=count # переносим в 11части def create_widget
                if btn.number in index_mines:  # если номер кнопки есть в списке бомб , то
                    btn.is_mine = True  # то кнопка становится миной
                # count += 1 # переносим в 11части def create_widget

    def count_mines_in_buttons(self): # вычисляем соседей кнопки
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn=self.buttons[i][j] # бомба (положение бомбы)
                count_bomb = 0 # счетчик бомб
                if not btn.is_mine: # получаем соседей для тех кто не является бомбой
                    for row_dx in [-1, 0, 1]: #  обращение к соседям бомбы (может находится -1 строка:этаже строка:+1строка
                        for column_dx in [-1, 0, 1]: # обращение к соседям бомбы (может находится -1 ряд:этотже ряд:+1ряд
                            neighbour = self.buttons[i+row_dx][j+column_dx] # нахождение соседа
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb









    @staticmethod
    def get_mines_places(exclude_number:int):  # метод для получения бомб
        indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMNS + 1))  # индексы бомб
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number) # удаляем из списка первую кнопку которую мы нажали
        shuffle(indexes)  # перемешиваем список индексов
        return indexes[:MineSweeper.MINES]  # берем срез индексев по кол-вы мин (т.е. выираем положение наших мин)


game = MineSweeper()  # соЗдаем экземрляр класса

game.start()

