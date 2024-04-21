class InvalidInputException(Exception):
    def __init__(self, args: object) -> None:
        """
        Exception raised for invalid input provided to a function.

        Args:
            args (object): Details about the invalid input.
        """
        self.invalid_input = args


class NotFoundException(Exception):
    def __init__(self, args: object) -> None:
        """
        Exception raised when a resource is not found or does not exist.

        Args:
            args (object): Details about the resource not found.
        """
        self.not_found = args


class ConflictException(Exception):
    def __init__(self, args: object) -> None:
        """
        Exception raised when there is a conflict with existing data or state.

        Args:
            args (object): Details about the conflict.
        """
        self.conflict_input = args
