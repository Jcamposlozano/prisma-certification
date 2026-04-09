from app.repositories.example_repository import ExampleRepository


class ExampleService:
    def __init__(self, repository: ExampleRepository | None = None):
        self.repository = repository or ExampleRepository()

    def get_status_message(self) -> str:
        return self.repository.get_message()
