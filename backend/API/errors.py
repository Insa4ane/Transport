class AppError(Exception):
    status_code = 400
    default_detail = "Błędne żądanie"
    headers: dict[str, str] | None = None

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class BadRequest(AppError):
    status_code = 400


class Unauthorized(AppError):
    status_code = 401
    default_detail = "Musisz się zalogować"
    headers = {"WWW-Authenticate": "Bearer"}


class Forbidden(AppError):
    status_code = 403
    default_detail = "Brak uprawnień"


class NotFound(AppError):
    status_code = 404
    default_detail = "Nie znaleziono zasobu"


class Conflict(AppError):
    status_code = 409
    default_detail = "Konflikt danych"
