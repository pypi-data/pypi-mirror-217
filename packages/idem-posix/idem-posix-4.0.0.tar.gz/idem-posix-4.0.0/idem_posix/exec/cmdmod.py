"""Exec module for executing commands on a posix systems."""
import asyncio
import copy
import json
import os
import sys
import traceback
from typing import Any
from typing import Dict
from typing import List

__virtualname__ = "cmd"


def __virtual__(hub):
    return os.name == "posix", "idem-posix only runs on posix systems"


async def run(
    hub,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    stdin: str = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    render_pipe: str = None,
    env: Dict[str, Any] = None,
    timeout: int or float = None,
    is_string_output: bool = False,
    success_retcodes: List[int] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """Execute the passed command and return the output as a string

    Args:
        cmd(str or list[str]):
            The command to run. ex: ``ls -lart /home``

        cwd(str, Optional):
            The directory from which to execute the command. Defaults
            to the home directory of the user specified by ``runas`` (or the user
            under which Salt is running if ``runas`` is not specified).

        shell(bool):
            If ``False``, let python handle the positional
            arguments. Set to ``True`` to use shell features, such as pipes or
            redirection. Defaults to False.

        stdin(str, Optional):
            A string of standard input can be specified for the
            command to be run using the ``stdin`` parameter. This can be useful in
            cases where sensitive information must be read from standard input.

        stdout(int):
            A string of standard input can be specified for the
            command to be run using the ``stdout`` parameter.

        stderr(int):
            A string of standard input can be specified for the
            command to be run using the ``stderr`` parameter.

        render_pipe(str, Optional):
            The render pipe to use on the output. Defaults to None.

        env(dict[str], Optional):
            Environment variables to be set prior to execution. Defaults to None.

            .. note::
                When passing environment variables on the CLI, they should be
                passed as the string representation of a dictionary.

            .. code-block:: bash

                idem exec cmd.run 'some command' env='{"FOO": "bar"}'

        timeout(int or float, Optional):
            A timeout in seconds for the executed process to return. Defaults to None.

        is_string_output(bool):
            Give the output in string format irrespective of format the command executed returns. Defaults to False.

        success_retcodes(list[int], Optional):
            The result will be True if the command's return code is in this list. Defaults to [0].

        args: args that will be forwarded to subprocess.

        kwargs: kwargs that will be forwarded to subprocess.

    Returns:
        Dict[str, Any]:
            Returns command output

            * stdout(str): The plaintext output of the command.

            * stderr(str): The plaintext error/logging output of the command.

            * retcode(str): The return code from the command.

            * state(str): "The output as rendered from the render_pipe (if one was given), for use in arg_binding.

    Example:
        .. code-block:: bash

            idem exec cmd.run "shell command --with-flags" cwd=/home render_pipe=json timeout=10

    """
    ret = dict(
        result=True,
        comment="",
        ret={"retcode": 0, "state": {}, "stdout": b"", "stderr": b""},
    )

    if success_retcodes is None:
        success_retcodes = [0]
    else:
        success_retcodes = [int(retcode) for retcode in success_retcodes]

    if getattr(sys, "frozen", False):
        env = copy.copy(os.environ.copy())
        # Remove the LOAD LIBRARY_PATH for running commands
        # https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#ld-library-path-libpath-considerations
        env.pop("LD_LIBRARY_PATH", None)  # Linux
        env.pop("LIBPATH", None)  # AIX

    # Run the command
    try:
        if shell:
            proc = await asyncio.create_subprocess_shell(
                cmd, cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                *cmd, *args, cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
            )
    except Exception as e:
        ret["result"] = False
        ret["ret"]["retcode"] = sys.exc_info()[1].errno
        ret["comment"] = traceback.format_exc()
        ret["ret"]["stderr"] = f"{e.__class__.__name__}: {e}"
        return ret

    # This is where the magic happens
    out, err = await asyncio.wait_for(proc.communicate(input=stdin), timeout=timeout)
    std_out = out.decode()
    if not is_string_output:
        # check if we can parse the output to json.
        try:
            std_out = json.loads(std_out)
        except Exception:
            hub.log.info("command output is not json")
    ret["ret"]["stdout"] = std_out
    ret["comment"] = ret["ret"]["stderr"] = err.decode()
    ret["ret"]["retcode"] = await asyncio.wait_for(proc.wait(), timeout=timeout)
    ret["result"] = ret["ret"]["retcode"] in success_retcodes

    if render_pipe:
        block = {"bytes": out}
        rendered = await hub.rend.init.parse_bytes(block, pipe=render_pipe)
        ret["ret"]["state"] = rendered

    return ret
