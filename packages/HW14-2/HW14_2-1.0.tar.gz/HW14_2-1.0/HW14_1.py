class Note:
    """
    class Note for init note
    
    :param title: Заголовок замітки
    :type title: str
    :param text: Текст замітки
    :type text: str
    """
    def __init__(self,
                 title,
                 text):
        """Initialized method
        """
        self.title = title        
        self.text = text

class User:
    """
    class User to work with the user
    """
    def __init__(self):
    """
    :param self.notes: Список нотатків
    :type self.notes: list
    """
        self.notes = []

    def create_note(self):
        """
        Method create_note

        :param title: Заголовок замітки, який вводить користувач
        :type title: str
        :param text: Текст замітки, який вводить користувач
        :type text: str
        :param note: об`єкт класу Note
        :type note: list
        """
        title = input("Введіть заголовок: ")
        text = input("Введіть текст: ")
        note = Note(title, text)
        self.notes.append(note)

    def show_notes(self):
    """
    Method show_notes

    :return: TrueЯкщо список заміток не порожній
    :rtype: bool
    """
        if self.notes:
            for note in self.notes:
                print(f"""Заголовок - {note.title}
Текст - {note.text}""")

user = User()

while True:
    choise = input("1 створити замітку 2 прочитати замітки 3 вихід: ")
    if choise == "1":
        user.create_note()
    if choise == "2":
        user.show_notes()
    if choise == "3":
        break
