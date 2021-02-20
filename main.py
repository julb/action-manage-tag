#!/usr/bin/python3
import os
from github import Github


def main():
    """ The main method executed. """

    # Github  variables
    github_token = os.environ.get('GITHUB_TOKEN')
    github_repository = os.environ.get('GITHUB_REPOSITORY')
    github_sha = os.environ.get('GITHUB_SHA')

    # Input variables
    input_tag_name = os.environ.get('INPUT_NAME')
    input_tag_state = os.environ.get('INPUT_STATE', 'create')
    input_tag_from = os.environ.get('INPUT_FROM', '')

    # Post-process date-time.
    tag_name = input_tag_name
    tag_git_ref_name = f'refs/tags/{tag_name}'
    tag_state = input_tag_state
    tag_from = github_sha
    if input_tag_from != '':
        tag_from = input_tag_from

    # Get repository.
    github = Github(github_token)
    github_repo = github.get_repo(github_repository)

    # Check if already exists.
    existing_github_ref = None
    for github_ref in github_repo.get_git_refs():
        # Check if the target tag exists.
        if github_ref.ref.lower() == tag_git_ref_name.lower():
            existing_github_ref = github_ref

        # Determine if the source is a tag, a tag or a ref.
        if tag_from and github_ref.ref.lower() in (f'refs/heads/{tag_from}'.lower(), f'refs/tags/{tag_from}'.lower(), tag_from.lower()):
            tag_from = github_ref.object.sha

    # Manage state.
    if tag_state in ('create', 'present'):
        # Source sha.
        if not existing_github_ref:
            print('::debug::Creating the tag.')
            existing_github_ref = github_repo.create_git_ref(ref=tag_git_ref_name, sha=tag_from)
        else:
            print('::debug::Updating the tag with the given SHA.')
            existing_github_ref.edit(sha=tag_from, force=True)

        # Return milestone number.
        print(f'::set-output name=ref::{existing_github_ref.ref}')
        print(f'::set-output name=name::{tag_name}')
        print(f'::set-output name=sha::{existing_github_ref.object.sha}')
    elif tag_state in ('deleted', 'absent'):
        # Delete if repo exists.
        if existing_github_ref is not None:
            print('::debug::Deleting the tag.')
            existing_github_ref.delete()
        else:
            print('::debug::Skipping tag deletion as it does not exist.')

        # Return 0 as number.
        print('::set-output name=ref::none')
        print('::set-output name=name::none')
        print('::set-output name=sha::none')


if __name__ == '__main__':
    main()
