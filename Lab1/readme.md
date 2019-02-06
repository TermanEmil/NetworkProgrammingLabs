# Introduction to git...
In this laboratory work I used the following commands
  * git init
  * git add
  * git commit
  * git push
  * git branch
  * git checkout
  * git merge

## Steps
    1. `git init` Create an empty Git repo
    2. `touch f1 f2`
    3. `git remote add origin <link to my repo>`
    4. `git add -A && git commit -m "First commit" && git push -u origin master` Add all changes, commit them with "First commit" message and push on `master`
    5. `git branch dev` Create a new branch `dev`
    6. `git checkout dev` Goto `dev`
    7. `touch f3_dev`
    8. `git add -A && git commit -m "added more files" && git push -u origin dev`
    9. `git checkout master` Goto `master`
    10. `git merge dev` Merge dev into master
    11. `git push` Push the changes
