#!/usr/bin/env python
import re
import sys
import os
import gitlab
from gitlab.v4.objects import GitlabCreateError
from git import Repo
from github import Github
from github import GithubException


def check_role_name(role):
        ROLE_REGEX = r'^[a-zA-Z][\.\-a-zA-Z0-9]+$'
        if not re.match(ROLE_REGEX, role):
                print('ERROR: %s is not an approved role name!' % role)
                sys.exit(1)


def create_local_repo(repo_path, git_url):
        os_repo_path = os.path.expanduser(repo_path)
        new_repo = Repo.init(os_repo_path)
        assert not new_repo.bare
        origin = new_repo.create_remote('origin', git_url)
        assert origin.exists()
        assert origin == new_repo.remotes.origin == new_repo.remotes['origin']
        origin.fetch()


def create_github_repo(git_remote, git_token, role):
        git = Github(git_token)
        user = git.get_user()
        try:
                repo = user.create_repo('ansible-role-%s' % (role))
        except GithubException as e:
                print "Failed to create repository"
                print "The error was: %s" % e.data['message']
                sys.exit(1)
        return(git_remote + repo.full_name)


def create_gitlab_repo(git_project, git_remote, git_token, role):
        print git_project
        gl = gitlab.Gitlab(git_remote, private_token=git_token)
        gitlab_group = gl.groups.get(git_project)
        print gitlab_group.id
        try:
                gl.projects.create({
                        'name': 'ansible-role-%s' % role,
                        'namespace_id': '%s' % gitlab_group.id
                        })
        except GitlabCreateError as e:
                print "Failed to create repository"
                print "The error was: %s" % e
                sys.exit(1)
        repo = gl.projects.get('%s/ansible-role-%s' % (git_project, role))
        print 'gitlab repo url : %s' % repo.ssh_url_to_repo
        return(repo.ssh_url_to_repo)


def create_remote_repo(git_project, git_remote, git_token, role, git_service):
        if git_service == 'GitHub':
                remote_repo = create_github_repo(
                                                git_remote,
                                                git_token,
                                                role
                                                )
        elif git_service == 'GitLab':
                remote_repo = create_gitlab_repo(
                                                git_project,
                                                git_remote,
                                                git_token,
                                                role,
                                                )
        else:
                print "unsupport git service: %s" % git_service
        return (remote_repo)


def main():

        cwd = os.getcwd()
        check_role_name(cookiecutter['role'])
        git_url = create_remote_repo(
                        cookiecutter['git_project'],
                        cookiecutter['git_remote'],
                        cookiecutter['git_token'],
                        cookiecutter['role'],
                        cookiecutter['git_service']
                        )
        print 'git_url : %s' % git_url
        create_local_repo(cwd, git_url)


if __name__ == "__main__":
        main()
