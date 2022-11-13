class Command:
    def __init__(self, params):
        self.adapter = None
        self.params = params

    def set_adapter(self, adapter):
        self.adapter = adapter

    def execute(self):
        raise NotImplementedError()
