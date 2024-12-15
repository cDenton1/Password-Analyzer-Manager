# class used for storing passwords in pickle file
class services:
    def __init__(self, service, name, password):
        self.service = service
        self.name = name
        self.password = password
