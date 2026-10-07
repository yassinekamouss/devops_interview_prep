# Git 08 - Cheatsheet and Interview Questions

## Module Objective

Quickly consolidate commands and classic DevOps interview answers.

## Summary Table

| Command               | Description                            |
| --------------------- | -------------------------------------- |
| git init              | Initialize a Git repository            |
| git status            | Show repository status                 |
| git add               | Add files to staging                   |
| git diff              | Show modifications                     |
| git commit            | Create a commit                        |
| git log               | Show history                           |
| git show              | Detail of a commit                     |
| git branch            | List branches                          |
| git switch            | Switch branch                          |
| git merge             | Merge a branch                         |
| git merge --abort     | Abort a merge                          |
| git rebase            | Rewrite history                        |
| git rebase -i         | Interactive rebase                     |
| git rebase --continue | Continue a rebase                      |
| git rebase --abort    | Abort a rebase                         |
| git reset             | Move HEAD                              |
| git reset --soft      | Undo commit only                       |
| git reset --mixed     | Remove from staging                    |
| git reset --hard      | Return exactly to a previous state     |
| git commit --amend    | Modify the last commit                 |
| git stash             | Temporarily save work                  |
| git stash pop         | Restore and delete the stash           |
| git stash apply       | Restore without deleting               |
| git stash list        | List stashes                           |
| git stash clear       | Delete all stashes                     |

## Classic Interview Questions

### Difference Between Merge and Rebase

Merge preserves real history and may create a merge commit.
Rebase rewrites history to make it linear.

### Difference Between Reset and Revert

Reset rewrites history.
Revert creates a new commit that undoes an old one.

### When to Use Stash?

When work is not finished but you need to quickly switch branches.

### When to Use Amend?

To fix the last commit (message or content) before sharing.

### When to Use Rebase?

To update a working branch or clean history before Pull Request.

## Interview Revision Tips

1. Replay commands on a test repository.
2. Explain each scenario out loud (merge, rebase, reset, revert).
3. Practice reading commit graphs quickly.
