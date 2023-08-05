"""
`git_knapsack.py`

Knapsack untracked files in a git repository in many commits, so that each commit does not exceed 30 MB.
Currently the knapsacking algorithm is extremely naive, and it does not expose any custom git features.
Effectively, this scripts performs git add, git commit and git push.

Note that it also will commit and push any untracked file.
If you run git status before this command and see anything you don't want committed,
either delete it or add it to the .gitignore file.

If any single file exceeds the git server's file limit or commit size limit, this script will not be able to help you.

The dependencies of this script are gitpython and tqdm.
"""
import os

from git import Repo
from tqdm import tqdm

def main():
    repository = Repo(os.path.curdir)
    untracked_files = repository.untracked_files

    commit_size = 0
    untracked_file_batch = []
    for untracked_file in tqdm(untracked_files):
        current_file_size = os.stat(untracked_file).st_size
        if commit_size + current_file_size > 1024 ** 2 * 30:  # keep commits below 30 MB
            repository.index.add(untracked_file_batch)
            repository.index.commit("Knapsack into multiple commits")
            # For many hosts, pushing after each commit is required.
            # Not only the commit and file size can be limited,
            # but often also the size of a push over HTTPS has a size limit
            origin = repository.remote('origin')
            origin.push()
            untracked_file_batch = [untracked_file]  # reset the batch
            commit_size = current_file_size  # reset the commit size
        else:
            untracked_file_batch.append(untracked_file)
            commit_size += current_file_size

    # Clean up any files in the queue
    repository.index.add(untracked_file_batch)
    repository.index.commit("Knapsack into multiple commits")
    origin = repository.remote('origin')
    origin.push()


if __name__ == '__main__':
    main()
