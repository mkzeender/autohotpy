import sys

from autohotpy import ahk_run

sys.modules[__name__] = ahk_run.run_str()  # type: ignore
