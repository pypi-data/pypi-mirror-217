from enum import Enum


class GetScriptByPathWithDraftResponse200Language(str, Enum):
    PYTHON3 = "python3"
    DENO = "deno"
    GO = "go"
    BASH = "bash"
    POSTGRESQL = "postgresql"
    NATIVETS = "nativets"

    def __str__(self) -> str:
        return str(self.value)
