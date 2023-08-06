import sys
import os
from impose_cli import impose
from subprocess import run


def get_index_url():
    pip = "pip" + str(sys.version_info[0])
    return run(args=f"{pip} config get global.index-url", shell=True, capture_output=True).stdout.decode("utf-8").strip()


def set_index_url(body, extra: bool=False):
    pip = "pip" + str(sys.version_info[0])
    index_url = "extra-index-url" if extra else "index-url"
    response = os.execvp(pip, [pip] + ["config", "set", f"global.{index_url}", body])


@impose
def pip_for_codeartifact(domain: str = None, repo: str = None, region: str = None):
    if domain is None or repo is None:
        raise Exception("A domain and a repo must be defined for CodeArtifact.")
    region = "" if region is None else f"--region {region}"
    index_url = get_index_url()
    # First we authenticate using code artifact
    res = run(args=f"aws codeartifact login --tool pip --domain {domain} --repository {repo} {region}", shell=True, capture_output=True)

    new_index_url = get_index_url()
    set_index_url(index_url)
    set_index_url(new_index_url, extra=True)
