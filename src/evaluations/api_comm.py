from dataclasses import dataclass, field

import requests
from .exec_outcome import ExecOutcome

@dataclass
class ExtendedUnittest:
    input: str
    output: list[str] = field(default_factory=list)
    result: str | None = None
    exec_outcome: ExecOutcome | None = None

    def json(self):
        _json = self.__dict__
        if self.exec_outcome is not None:
            _json["exec_outcome"] = self.exec_outcome.name

        return _json

    @classmethod
    def from_json(cls, _json):
        return cls(
            input=_json.get("input", ""),
            output=_json.get("output", list()),
            result=_json.get("result", None),
            exec_outcome=_json.get("exec_outcome", None),
        )


class EmptyValueError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmptyUnittestError(EmptyValueError):
    pass


class EmptyLanguageError(EmptyValueError):
    pass


class EmptySourceCodeError(EmptyValueError):
    pass


class APICommunication:
    _session: requests.Session

    def __init__(self, server_url: str = "http://localhost:5000"):
        self._session = requests.Session()
        self.execute_code_url = f"{server_url}/api/execute_code"
        self.get_runtimes_url = f"{server_url}/api/all_runtimes"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def get_runtimes(self):
        return self._session.get(self.get_runtimes_url).json()

    def execute_code(
        self,
        language: str,
        source_code: str,
        unittests: list[dict],
        limits: dict | None,
        block_network: bool = True,
        stop_on_first_fail: bool = True,
        use_sanitizer: bool = False,
        compiler_program_name: str | None = None,
        compiler_flags: str | None = None,
        interpreter_cmd: str | None = None,
        interpreter_flags: str | None = None,
        sample_id: int | None = None,
        task_id: str | int | None = None,
    ) -> tuple[list[ExtendedUnittest], int | None, str | int | None]:
        if language is None:
            raise EmptyLanguageError

        if source_code is None:
            raise EmptySourceCodeError

        if unittests is None or len(unittests) == 0:
            raise EmptyUnittestError

        request_body = dict(
            language=language,
            source_code=source_code,
            unittests=unittests,
            limits=limits if isinstance(limits, dict) else dict(),
            compile_cmd=compiler_program_name,
            compile_flags=compiler_flags,
            execute_cmd=interpreter_cmd,
            execute_flags=interpreter_flags,
            block_network=block_network,
            stop_on_first_fail=stop_on_first_fail,
            use_sanitizer=use_sanitizer,
        )
        json_response = self._session.post(
            self.execute_code_url,
            json=request_body,
            headers={"Content-Type": "application/json"},
        ).json()

        if "data" not in json_response:
            return "error", sample_id, task_id

        return (
            json_response["data"],
            sample_id,
            task_id,
        )
