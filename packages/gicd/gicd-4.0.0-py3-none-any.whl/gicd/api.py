import logging
import subprocess
import traceback
from functools import wraps
from typing import Any, List, Optional

LOGGER = logging.getLogger(__name__)


def gicd(
    repo_owner: str,
    repo_name: str,
    issue_label: str = "bug",
    exception_types: Optional[List[Exception]] = None,
) -> Any:
    """Decorator to create a GitHub issue on exception throw.

    Args:
        repo_owner (str): The owner of the repo to create the issue in.
        repo_name (str): The name of the repo to create the issue in.
        issue_label (str): The label to give the issue.
        exception_types (Optional[List[Exception]], optional): The exception types to create an issue for. If None, create the issue for any exception. Defaults to None.

    Returns:
        Any: The return value of the decorated function.
    """
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if exception_types is None or any(
                    isinstance(e, e_type) for e_type in exception_types  # type: ignore
                ):
                    s = str(e)
                    issue_url = (
                        subprocess.run(
                            [
                                "gh",
                                "issue",
                                "create",
                                "--title",
                                f"{s[:25].strip()}..." if len(s) > 28 else s,
                                "--body",
                                f"```python\n{traceback.format_exc().strip()}\n```",
                                "--label",
                                issue_label,
                                "-R",
                                f"{repo_owner}/{repo_name}",
                            ],
                            capture_output=True,
                        )
                        .stdout.decode()
                        .strip()
                    )
                    LOGGER.info(
                        f"A GitHub issue for the thrown exception was created at {issue_url}"
                    )
                raise e

        return wrapper

    return actual_decorator
