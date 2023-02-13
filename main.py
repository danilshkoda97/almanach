import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

connection = sqlite3.connect(r"D:\DataBases\almonach.db")

if (connection):
    print("Соединение установлено")
else:
    print("Ошибка соединения")

cur = connection.cursor()

def receiveCategory():
    """Функция для получения имеющихся категорий"""
    values_combo = []
    cur.execute('SELECT * FROM categories ')
    sel = cur.fetchall()
    for i in range(len(sel)):
        values_combo.append(sel[i][1])
    return values_combo

def deletEditProblem(event):
    """Функция для просмота, удаления и редактирования проблемы"""
    print("Событие нажатие на категорию")
    window_problem = Tk()
    window_problem.geometry("500x500")
    window_problem.title(event.widget.cget('text'))
    id = event.widget.master.winfo_children()[0].get()

    def deleteProblem():
        """Функция для удаления проблемы"""
        print("Событие нажатие на кнопку 'Удалить'")
        query = "DELETE FROM problems WHERE id = " + id + ";"
        cur.execute(query)
        connection.commit()
        showinfo("Успешно!", "Проблема успешно удалена")
        print(query)
        window_problem.destroy()

    def editProblem():
        """Функция для редактирования проблемы"""
        print("Событие нажатие на кнопку 'Редактировать'")
        new_name_problem = input_name_problem.get()
        new_information_problem = text_information_problem.get("1.0","end")
        new_decision_problem = text_decision_problem.get("1.0","end")
        query = "UPDATE problems SET name = '" + new_name_problem + "', " \
            "information = '" + new_information_problem + "', decision = '" + new_decision_problem + "' WHERE id = " + id + ";"
        cur.execute(query)
        connection.commit()
        showinfo("Успешно!", "Вы изменили проблему!")
        print(query)
        window_problem.destroy()
        deletEditProblem(event)

    query = "SELECT * FROM problems WHERE id = " + id + ";"
    cur.execute(query)
    result = cur.fetchall()
    print(query)
    name_problem = result[0][1]
    information_problem = result[0][3]
    decision_problem = result[0][4]

    input_name_problem = Entry(  # поле c названием проблемы
        window_problem,
        font=("Times new Roman", 12),
        width = 50
    )
    input_name_problem.insert(0, name_problem)
    input_name_problem.pack(
        anchor = W,
        pady=5,
        padx = 5
    )
    text_information_problem = Text( # Поле с информацией о проблеме
        window_problem,
        font=("Times new Roman", 12),
        height = 5
    )
    text_information_problem.insert(END, information_problem)
    text_information_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )

    text_decision_problem = Text( # Поле с решением проблемы
        window_problem,
        font=("Times new Roman", 12),
        height = 5
    )
    text_decision_problem.insert(END, decision_problem)
    text_decision_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )

    frame_for_button = Frame(
        window_problem,
    )
    frame_for_button.pack(
        fill=X
    )

    button_problem = Button(  # Кнопка для удаления проблемы
        frame_for_button,
        font=("Times new Roman", 12),
        text="Удалить",
    )
    button_problem.bind('<Button-1>', deleteProblem)
    button_problem.pack(
        side=LEFT,
        padx=5,
        pady=10
    )

    button_problem = Button(  # Кнопка для редактирвоания проблемы
        frame_for_button,
        font=("Times new Roman", 12),
        text="Редактировать",
        command=editProblem
    )
    button_problem.pack(
        side=LEFT,
        padx=5,
        pady=10
    )


def searchProblem(event):
    """Функция для поиска проблем"""
    print("Событие нажатие на кнопку 'Найти'")
    name_category = event.widget.master.winfo_children()[1].get()
    name_problem = event.widget.master.winfo_children()[3].get()
    if (frame_result_search_problems.winfo_children() == []):
        pass
    else:
        for widget in frame_result_search_problems.winfo_children():
           widget.destroy()
    print(frame_result_search_problems.winfo_children())
    if (name_problem == ""):
        showinfo("Ошибка!", "Заполните все обязательные поля!")
    else:
        pass
        query = "SELECT * FROM problems WHERE name LIKE '%" + name_problem + "%' AND categori = (SELECT id FROM categories WHERE name = '" + name_category + "') ORDER BY id DESC"
        cur.execute(query)
        result = cur.fetchall()
        if (result == []):
            showinfo("Не далось!", "Такой проблемы не существует!")
        else:
            print(query)
            for i in range(len(result)):
                frame_result_search_problem = Frame(  # Контейнер для найденной проблемы
                    frame_result_search_problems
                )
                frame_result_search_problem.pack(
                    fill=X,
                )

                input_id_problem = Entry( # id проблемы
                    frame_result_search_problem,
                )
                input_id_problem.insert(0, result[i][0])

                button_problem = Button( # Кнопка - название проблемы
                    frame_result_search_problem,
                    font=("Times new Roman", 12),
                    text = result[i][1],
                )
                button_problem.bind('<Button-1>', deletEditProblem)
                button_problem.pack(
                    side = LEFT,
                    padx=5,
                    pady=10
                )

def showWindowAddProblem(): # Показать окно, где добавляется категория
    """Функция для показа окна с добавлением категории"""

    def addProblem():
        """Функция для добавления проблемы"""
        print("Событие нажатие на кнопку 'Добавить'")
        name = input_name_problem.get()
        category = combo_name_category.get()
        information = text_information_problem.get("1.0","end")
        decision = text_decision_problem.get("1.0","end")
        if (name == "" or decision == ""):
            showinfo("Ошибка!", "Заполните все обязательные поля!")
        else:
            cur.execute('SELECT * FROM problems')
            sel = cur.fetchall()
            flag = True
            for row in sel:
                if (row[1].upper() == name.upper()):
                    flag = False

            if (flag == True):
                query_add_problem = "INSERT INTO problems (name, categori, information, decision) VALUES ('" + name + "', (SELECT id FROM categories WHERE name = '" + category + "'), '" + information + "', '" + decision + "');"
                cur.execute(query_add_problem)
                connection.commit()
                showinfo("Успешно!", "Проблема успешно добавлениа!")
                print(query_add_problem)
                window_add_problem.destroy()
            else:
                showinfo("Ошибка!", "Такая проблема уже существует!")

    print("Событие нажатие на кнопку 'Добавить проблему'")
    window_add_problem = Tk()
    window_add_problem.geometry("500x500")
    window.title("Добавление проблемы")

    lable_name_problem = Label(
        window_add_problem,
        font=("Times new Roman", 12),
        text = "Введите название проблемы"
    )
    lable_name_problem.pack(
        anchor = W,
        pady=5,
        padx = 5
    )
    input_name_problem = Entry(  # поле ввода для названия проблемы
        window_add_problem,
        font=("Times new Roman", 12),
        width = 50
    )
    input_name_problem.pack(
        anchor = W,
        pady=5,
        padx = 5
    )
    lable_name_category = Label(
        window_add_problem,
        font=("Times new Roman", 12),
        text = "Выберите название категории"
    )
    lable_name_category.pack(
        anchor = W,
        pady=5,
        padx = 5
    )
    combo_name_category = ttk.Combobox(
        window_add_problem,
        font=("Times new Roman", 12),
        values = receiveCategory()
    )
    combo_name_category.current(0)
    combo_name_category.pack(
        anchor=W,
        pady = 5,
        padx=5
    )
    lable_information_problem = Label(
        window_add_problem,
        font=("Times new Roman", 12),
        text="Введите информацию о проблеме"
    )
    lable_information_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )
    text_information_problem = Text(
        window_add_problem,
        font=("Times new Roman", 12),
        height = 5
    )
    text_information_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )
    lable_decision_problem = Label(
        window_add_problem,
        font=("Times new Roman", 12),
        text="Введите решение проблемы"
    )
    lable_decision_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )
    text_decision_problem = Text(
        window_add_problem,
        font=("Times new Roman", 12),
        height=5
    )
    text_decision_problem.pack(
        anchor=W,
        pady=5,
        padx=5
    )

    btn_add_problem = Button(  # кнопка для показа проблем
        window_add_problem,
        font=("Times new Roman", 12),
        text="Добавить проблему",
        command=addProblem
    )
    btn_add_problem.pack(
        padx=5,
        pady=10
    )

def addCategory():
    """Добавление категории в таблицу categories"""
    print("Событие нажатие на кнопку 'Добавить'")
    cur.execute('SELECT * FROM problems ')
    sel = cur.fetchall()
    name = input_add_category.get()
    if (name == ""):
        showinfo("Ошибка!", "Категория не может быть пустой!")
    else:
        flag = True
        for row in sel:
            if (row[1].upper() == name.upper()):
                flag = False

        if (flag == True):
            query = "INSERT INTO categories (name) VALUES ('" + name + "');"
            cur.execute(query)
            connection.commit()
            showinfo("Успешно!", "Категория успешно добавлениа!")
            print(query)
            showCatgories()
        else:
            showinfo("Ошибка!", "Такая категория уже существует!")


def editCategory(event):
    """Редактирование категории"""
    print("Событие нажатие на кнопку 'Редактировать'")
    id = event.widget.master.winfo_children()[1].get()
    name = event.widget.master.winfo_children()[0].get()
    query = "UPDATE categories SET name = '" + name + "' WHERE id = " + id + ";"
    cur.execute(query)
    connection.commit()
    showinfo("Успешно!", "Категория успешно изменена!")
    showCatgories()

def showCatgories():
    """Показать категории"""

    for widget in frame_show_categories_funk.winfo_children():
        widget.destroy()

    print("Событие нажатие на кнопку 'Показать категории'")

    query = "SELECT * FROM categories ORDER BY id DESC"
    cur.execute(query)
    result = cur.fetchall()
    print(query)

    for i in range(len(result)):
        frame_show_category = Frame(  # Контейнер для конкретной категории категорий
            frame_show_categories_funk,
            borderwidth=0
        )
        frame_show_category.pack(
            fill = X,
        )
        input_category = Entry(
            frame_show_category,
            font=("Times new Roman", 12)
        )
        input_category.insert(0, result[i][1])
        input_category.pack(
            side = LEFT,
            padx = 5,
            pady = 5
        )
        input_id = Entry(
            frame_show_category,
            font=("Times new Roman", 12)
        )
        input_id.insert(0, result[i][0])
        btn_edit_category = Button(  # кнопка для редактирования категории
            frame_show_category,
            font=("Times new Roman", 12),
            text="Редактировать",
        )
        btn_edit_category.bind('<Button-1>', editCategory)
        btn_edit_category.pack(
            side=LEFT,
            padx=5,
            pady=10
        )

window = Tk()
window.geometry("1000x750")
window.title("Almanac")

# Блок для добавления категории

frame_categories = LabelFrame( # Контейнер для блока работы с категориями
    text = "Категории",
    font = ("Times new Roman", 14, "bold"),
    width = "400"
)
frame_categories.pack_propagate(False)
frame_categories.pack(
    side = RIGHT,
    fill = Y
)

frame_add_categories = LabelFrame( # Контейнер для добавления категорий
    frame_categories,
    text = "Добавить категорию",
    font = ("Times new Roman", 12, "bold"),
    height = "200"
)
frame_add_categories.pack(
    side = TOP,
    fill = X
)

input_add_category = Entry( # поле ввода для названия категории
    frame_add_categories,
    font = ("Times new Roman", 12),
    width = 50
)
input_add_category.pack(
    padx=5,
    pady=10
)

btn_add_category = Button( # кнопка для добавления категории
    frame_add_categories,
    font = ("Times new Roman", 12),
    text = "Добавить категорию",
    command = addCategory
)
btn_add_category.pack(
    anchor = W,
    padx=5,
    pady=10
)

frame_show_categories = LabelFrame( # Контейнер для показа категорий
    frame_categories,
    text = "Показать категории",
    font = ("Times new Roman", 12, "bold"),
    width = "400"
)
frame_show_categories.pack_propagate(False)
frame_show_categories.pack(
    side = LEFT,
    fill = Y
)

frame_show_categories_btn = Frame( # Контейнер для кнопки в блоке показать категории
    frame_show_categories,
    height = "100"
)
frame_show_categories_btn.pack(
    side = TOP,
    fill = X
)

frame_show_categories_funk = Frame( # Контейнер для показа категорий в блоке показа категорий
    frame_show_categories
)

frame_show_categories_funk.pack(
    side = LEFT,
    fill = Y
)

btn_show_categories = Button(
    frame_show_categories_btn,
    font = ("Times new Roman", 12),
    text = "Показать категории",
    command = showCatgories
)
btn_show_categories.pack(
    anchor=W,
    padx=5,
    pady=10
)

# Блок для поиска проблем

frame_problems = LabelFrame(
    text = "Проблемы",
    font = ("Times new Roman", 14, "bold"),
    width = "600"
)
frame_problems.pack_propagate(False)
frame_problems.pack(
    side = LEFT,
    fill = Y
)

frame_add_problems = Frame(  # Контейнер для добавления проблемы
    frame_problems
)
frame_add_problems.pack(
    fill=X,
)

btn_show_window_add_problem = Button( # кнопка для показа проблем
    frame_add_problems,
    font = ("Times new Roman", 12),
    text = "Добавить проблему",
    command = showWindowAddProblem
)
btn_show_window_add_problem.pack(
    anchor = W,
    padx = 5,
    pady = 10
)

frame_search_problems = LabelFrame(  # Контейнер для блока поиска проблемы
    frame_problems,
    text = "Поиск проблем",
    font = ("Times new Roman", 12, "bold")
)
frame_search_problems.pack(
    fill=X,
)

input_search_problem = Label(
    frame_search_problems,
    font = ("Times new Roman", 12),
    text = "Выберите категорию проблемы"
)
input_search_problem.pack(
    anchor = W,
    padx=5,
    pady=10
)

combo_name_category = ttk.Combobox(
    frame_search_problems,
    font=("Times new Roman", 12),
    values=receiveCategory()
)
combo_name_category.current(0)
combo_name_category.pack(
    anchor=W,
    pady=5,
    padx=5
)

label_search_problem = Label(
    frame_search_problems,
    font = ("Times new Roman", 12),
    text = "Введите название проблемы"
)
label_search_problem.pack(
    anchor = W,
    padx=5,
    pady=10
)

input_search_problem = Entry( # поле ввода для названия категории
    frame_search_problems,
    font = ("Times new Roman", 12),
    width = 50
)
input_search_problem.pack(
    anchor = W,
    padx=5,
    pady=10
)

button_search_problem = Button(
    frame_search_problems,
    font = ("Times new Roman", 12),
    text = "Найти"
)
button_search_problem.bind('<Button-1>', searchProblem)
button_search_problem.pack(
    side = LEFT,
    padx=5,
    pady=10
)

frame_result_search_problems = LabelFrame(  # Контейнер для вывода найденных проблем
    frame_problems,
    text = "Результат",
    font = ("Times new Roman", 12, "bold")
)
frame_result_search_problems.pack(
    fill=X,
)

window.mainloop()






