import tkinter as tk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db

    def init_main(self):
        # верхняя панель
        toolbar = tk.Frame(bg='white',bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка случайного анекдота
        self.random_img = tk.PhotoImage(file='random.png')
        btn_random = tk.Button(toolbar,bg='white',bd=0,image=self.random_img, command = self.random_joke)
        btn_random.pack(side = tk.TOP)

        # поле вывода анекдота
        self.text = tk.Text(width=640, height=320, bg='white',fg='black', state='normal')
        self.text.pack()

    # метод случайного анекдота
    def random_joke(self):
        # разблокировка редактирования поля
        self.text.configure(state='normal')
        # очищение поля для анекдота
        self.text.delete(0.0, tk.END)
        # вставка анекдота в поле
        self.db.cursor.execute('''SELECT joke FROM jokes ORDER BY RANDOM () LIMIT 1''')
        self.text.insert(0.0, self.db.cursor.fetchone()[0])
        # блокировка редактирования поля
        self.text.configure(state = 'disabled')

# класс бд
class Db:
    def __init__(self):
        self.connection = sqlite3.connect('jokes.db')
        self.cursor = self.connection.cursor()
        query_create_table = '''
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            joke TEXT NOT NULL
        )
        '''
        self.cursor.execute(query_create_table)
        self.cursor.executemany(
            ''' INSERT INTO jokes (joke)
            VALUES (?) ''',
            [
                ['Мальчик с консервной банкой подходит к полицейскому: — Дядя полицейский, откройте банку! Полицейский стучит в банку и говорит: — Откройте, полиция!'],
                ['Садится в такси \n-куда вам  \n-я не хочу куда вам \n-да куда вам надо!? \n-ну раз надо'],
                ['-Капитан, земля! \n-Мы еще не отплыли...'],
                ['Попал мужик в сумасшедший дом. Приводят его в палату. Там его спрашивают: \n– Ты кто?\n– Наполеон, – отвечает мужик.\nОстальные пациенты разочарованно: – Императоров у нас полно...\nМужик гордо: – А я не император! Я торт!'],
                ['Девушка говорит парню: — Приходи завтра, дома никого не будет. Парень пришёл, а дома никого.'],
                ['Купил мёд, оказался липовый']
            ]
        )
        self.connection.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title('Генератор анекдотов')
    root.geometry('640x400')
    root.resizable(False,False)
    root.mainloop()