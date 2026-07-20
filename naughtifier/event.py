class Event:
    def __init__(self, id, name, description, date, location):
        self.id = id
        self.name = name
        self.description = description
        self.date = date
        self.location = location

    def __str__(self):
        return f"**{self.name}**\n{self.description}\n {self.date}\n {self.location}"