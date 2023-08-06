class error_message(Exception):
    def __init__(self, messaggio):
        self.messaggio = messaggio
        super().__init__(messaggio)