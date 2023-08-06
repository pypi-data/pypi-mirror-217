from .base_backend import GitBackend
from subprocess import run
from pathlib import Path
import click
import json
import os
from making_with_code_cli.helpers import cd
from making_with_code_cli.styles import (
    confirm,
)

COMMIT_TEMPLATE = ".commit_template"

class GithubBackend(GitBackend):
    """A Github backend. Students own their own repos and grant teachers access via token.
    Note that this gives the teacher account access to the student's entire github account, 
    within scope.
    """

    # START HERE: HOW DOES GITEA DO TEMPLATE REPOS?
    def init_module(self, module, modpath):
        """Creates the named repo from a template, or clones an existing repo with. 
        """
        repo_name = self.get_repo_name_from_template_repo_url(module["repo_url"])
        url = module["repo_url"]

        if self.user_has_repo(repo_name):
            cmd = f'gh repo clone "{url}" "{modpath.name}"'
        else:
            if modpath.exists():
                self.relocate_existing_directory(modpath)
            cmd = f'gh repo create {repo_name} --clone --private --template "{url}"'
        with cd(modpath.parent):
            run(cmd, shell=True, check=True)
            run(f"mv {repo_name} {modpath.name}", shell=True, check=True) 
        if (modpath / COMMIT_TEMPLATE).exists():
            with cd(modpath):
                run(f"git config commit.template {COMMIT_TEMPLATE}")

    def get_repo_name_from_template_repo_url(self, url):
        """Parses the template repo URL and returns the name of a repo to create.
        Expects a GitHub url like "https://git.makingwithcode.org/mwc/lab_pipes.git"
        """
        parts = url.split('/')
        name, suffix = parts[-1][:-4], parts[-1][-4:]
        return name

    def relocate_existing_directory(self, path):
        """Moves an existing directory out of the way.
        """
        new_path = path.parent / path.name + '_old'
        while new_path.exists():
            new_path = new_path.parent / new_path.name + '_old'
        click.echo(confirm(f"Moving existing directory {path} to {new_path}."))
        os.rename(path, new_path)

    def user_has_repo(self, name):
        "Checks to see whether the user already has the named repo."
        cmd = f"gh repo list --json name --limit 10000"
        result = run(cmd, shell=True, capture_output=True, text=True).stdout
        repo_names = [obj['name'] for obj in json.loads(result)]
        return name in repo_names

