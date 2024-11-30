from app.models.models import Error


class RestApiException(Exception):
    response: Error
    
    def __init__(self, res: Error, *args):
        super().__init__(*args)
        self.response = res