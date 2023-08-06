"""
    Client exceptions.
"""
import http
import typing


class AuthenticationError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"{self.status_code}: {self.args[0]}"
        return str(self.args[0])


class MultipleObjectMatchedError(Exception):
    def __init__(self, results: list, message):
        super().__init__(message)
        self.results: list = results

    def __str__(self):
        return str(self.args[0])


class ItemNotFoundException(Exception):
    def __init__(
        self,
        status_code: str = "404",
        uuid: str | None = None,
        type: str | None = None,
        sub_type: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.uuid = uuid
        self.type = type
        self.sub_type = sub_type

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        details_default: str = "No detailed available"
        details: str = ""
        if self.uuid:
            details = f"UUID={self.uuid}"
        if self.type and not self.sub_type:
            details = details + f" [ObjectType={self.type}]"
        elif self.type and self.sub_type:
            details = details + f" [ObjectType={self.type}|{self.sub_type}]"
        details = details if details else details_default

        return f"{class_name}:: status_code={self.status_code!r}. Requested object: {details}"

    def __str__(self) -> str:
        return self.__repr__()


class HTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: typing.Optional[str] = None,
        headers: typing.Optional[dict] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class SubProcessError(Exception):
    def __init__(self, stacktrace: str, cmd: str):
        self.stacktrace = stacktrace
        self.cmd = cmd

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{self.stacktrace}\n{class_name}: ENA submission failed."
