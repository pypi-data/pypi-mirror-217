import os
import shutil
import subprocess
import sys

import click
from spin import util
from spin.cmds import meson


def get_git_revision_hash(submodule) -> str:
    return subprocess.check_output(["git", "rev-parse", f"@:{submodule}"]).decode("ascii").strip()


@click.command()
@click.option("--build-dir", default="build", help="Build directory; default is `$PWD/build`")
@click.option("--clean", is_flag=True, help="Clean previously built docs before building")
@click.option("--noplot", is_flag=True, help="Build docs without plots")
def docs(build_dir, clean=False, noplot=False):
    """📖 Build documentation"""
    if clean:
        doc_dir = "./docs/_build"
        if os.path.isdir(doc_dir):
            print(f"Removing `{doc_dir}`")
            shutil.rmtree(doc_dir)

    site_path = meson._get_site_packages()
    if site_path is None:
        print("No built scikit-tree found; run `./spin build` first.")
        sys.exit(1)

    util.run(["pip", "install", "-q", "-r", "doc_requirements.txt"])

    os.environ["SPHINXOPTS"] = "-W"
    os.environ["PYTHONPATH"] = f'{site_path}{os.sep}:{os.environ.get("PYTHONPATH", "")}'
    if noplot:
        util.run(["make", "-C", "docs", "clean", "html-noplot"], replace=True)
    else:
        util.run(["make", "-C", "docs", "clean", "html"], replace=True)


@click.command()
@click.pass_context
def coverage(ctx):
    """📊 Generate coverage report"""
    pytest_args = ("-o", "python_functions=test_*", "sktree", "--cov=sktree", "--cov-report=xml")
    ctx.invoke(meson.test, pytest_args=pytest_args)


@click.command()
@click.option("--forcesubmodule", is_flag=True, help="Force submodule pull.")
def setup_submodule(forcesubmodule=False):
    """Build scikit-tree using submodules.

    git submodule update --recursive --remote

    To update submodule wrt latest commits:

        git submodule update --init --recursive --remote
        git add -A
        git commit

    This will update the submodule, which then must be commited so that
    git knows the submodule needs to be at a certain commit hash.
    """
    commit_fpath = "./sktree/_lib/sklearn/commit.txt"
    submodule = "./sktree/_lib/sklearn_fork"
    commit = ""
    current_hash = ""

    # if the forked folder does not exist, we will need to force update the submodule
    if not os.path.exists("./sktree/_lib/sklearn/") or forcesubmodule:
        # update git submodule
        util.run(["git", "submodule", "update", "--init", "--force"])
    else:
        # update git submodule
        util.run(
            [
                "git",
                "submodule",
                "update",
                "--init",
                "--force",
            ]
        )

    # get the commit hash if the commmit file exists
    if os.path.exists(commit_fpath):
        with open(commit_fpath, "r") as f:
            commit = f.read().strip()

    # get revision hash
    current_hash = get_git_revision_hash(submodule)

    print(current_hash)
    print(commit)

    # if the commit file doesn't exist or the commit hash is different, we need
    # to update our sklearn repository
    if current_hash == "" or current_hash != commit:
        util.run(
            [
                "mkdir",
                "-p",
                "./sktree/_lib/sklearn/",
            ],
        )
        util.run(
            [
                "touch",
                commit_fpath,
            ],
        )
        print(commit_fpath)
        with open(commit_fpath, "w") as f:
            f.write(current_hash)

        util.run(
            [
                "rm",
                "-rf",
                "sktree/_lib/sklearn",
            ]
        )

        if os.path.exists("sktree/_lib/sklearn_fork/sklearn"):
            util.run(
                [
                    "mv",
                    "sktree/_lib/sklearn_fork/sklearn",
                    "sktree/_lib/sklearn",
                ]
            )


@click.command()
@click.option("-j", "--jobs", help="Number of parallel tasks to launch", type=int)
@click.option("--clean", is_flag=True, help="Clean build directory before build")
@click.option(
    "--forcesubmodule", is_flag=True, help="Force submodule pull.", envvar="FORCE_SUBMODULE"
)
@click.option("-v", "--verbose", is_flag=True, help="Print all build output, even installation")
@click.argument("meson_args", nargs=-1)
@click.pass_context
def build(ctx, meson_args, jobs=None, clean=False, forcesubmodule=False, verbose=False):
    """Build scikit-tree using submodules.

    git submodule update --recursive --remote

    To update submodule wrt latest commits:

        git submodule update --init --recursive --remote
        git add -A
        git commit

    This will update the submodule, which then must be commited so that
    git knows the submodule needs to be at a certain commit hash.
    """
    ctx.invoke(setup_submodule, forcesubmodule=forcesubmodule)

    # run build as normal
    ctx.invoke(meson.build, meson_args=meson_args, jobs=jobs, clean=clean, verbose=verbose)




@click.command()
def sdist():
    """📦 Build a source distribution in `dist/`"""
    util.run(["python", "-m", "build", ".", "--sdist"])