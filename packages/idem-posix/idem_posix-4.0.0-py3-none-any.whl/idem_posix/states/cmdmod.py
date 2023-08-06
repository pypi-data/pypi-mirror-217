"""State module for executing commands on a posix systems."""
import copy
import os
from typing import Any
from typing import Dict
from typing import List

__virtualname__ = "cmd"


def __virtual__(hub):
    return os.name == "posix", "idem-posix only runs on posix systems"


async def run(
    hub,
    ctx,
    name: str,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    env: Dict[str, Any] = None,
    umask: str = None,
    timeout: int or float = None,
    render_pipe: str = None,
    is_string_output: bool = False,
    success_retcodes: List[int] = None,
    **kwargs,
) -> Dict[str, Any]:
    """Execute the passed command and return the output as a string

    Args:
        name(str):
            The state name.

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

        env(dict[str], Optional):
            Environment variables to be set prior to execution. Defaults to None.

            .. note::
                When passing environment variables on the CLI, they should be
                passed as the string representation of a dictionary.

            .. code-block:: bash

                idem exec cmd.run 'some command' env='{"FOO": "bar"}'

        umask(str, Optional):
            The umask (in octal) to use when running the command.

        timeout(int or float, Optional):
            A timeout in seconds for the executed process to return. Defaults to None.

        render_pipe(str, Optional):
            The render pipe to use on the output. Defaults to None.

        is_string_output(bool):
            Give the output in string format irrespective of format the command executed returns. Defaults to False.

        success_retcodes(list[int], Optional):
            The result will be True if the command's return code is in this list. Defaults to [0].

        kwargs: kwargs that will be forwarded to subprocess.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

          # Execute "ls -l" command
          my_state_name:
            cmd.run:
              cmd: ls -l
              cwd: /
              shell: False
              env:
                ENV_VAR_1: ENV_VAL_1
                ENV_VAR_2: ENV_VAL_2
              timeout: 100
              render_pipe:
              kwargs:

        The "new_state" will have the following keys:

            "stdout": The plaintext output of the command

            "stderr": The plaintext error/logging output of the command

            "retcode": The return code from the command

            "state": The output as rendered from the render_pipe (if one was given), for use in arg_binding
    """
    ret = {
        "name": name,
        "result": True,
        "comment": "",
        "old_state": ctx.get("old_state", {}),
        "new_state": {},
    }

    # Need the check for None here, if env is not provided then it falls back
    # to None and it is assumed that the environment is not being overridden.
    if env is not None and not isinstance(env, (list, dict)):
        ret["result"] = False
        ret["comment"] = "Invalidly-formatted 'env' parameter. See " "documentation."
        return ret

    cmd_kwargs = copy.deepcopy(kwargs)
    cmd_kwargs.update(
        {
            "cwd": cwd,
            "shell": shell,
            "env": env,
            "umask": umask,
        }
    )

    if cwd and not os.path.isdir(cwd):
        ret["result"] = False
        ret["comment"] = f'Desired working directory "{cwd}" ' "is not available"
        return ret

    if ctx["test"]:
        if kwargs and kwargs.get("ignore_test", False):
            hub.log.debug(
                "Invoking cmd.run even when ctx.test is enabled due to ignore_test flag."
            )
        else:
            ret["comment"] = f"The cmd.run does not run when ctx.test is enabled"
            return ret

    cmd_ret = await hub.exec.cmd.run(
        cmd=cmd,
        timeout=timeout,
        python_shell=True,
        render_pipe=render_pipe,
        is_string_output=is_string_output,
        success_retcodes=success_retcodes,
        **cmd_kwargs,
    )

    ret["new_state"] = cmd_ret.ret
    ret["result"] = cmd_ret.result
    ret["comment"] = (
        f"stdout: {cmd_ret.ret['stdout']}",
        f"stderr: {cmd_ret.ret['stderr']}",
        f"retcode: {cmd_ret.ret['retcode']}",
    )
    if cmd_ret.comment:
        ret["comment"] = (cmd_ret.comment,) + ret["comment"]

    return ret
