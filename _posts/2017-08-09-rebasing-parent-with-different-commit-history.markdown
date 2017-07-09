---
title:  "Rebasing a child branch with parent when parent has different commit history"
date:   2017-07-08 15:04:23
categories: [blog]
tags: [git]
---
In git we usually `rebase` a child branch with parent to keep the child branch up to date with parents. This is easy as running `git rebase [your parent branchname]` from child branch when all the past commits in child branch are same as parent's.

For example, let's say you have below commit history in parent branch `master`

``` ruby
> git log --oneline
d0d2cc9 second line
9926ae0 first commit
```

Now you create a child branch `child-branch` from `master` and do a commit after changing something.

``` ruby
> git checkout -b child-branch
> git add --all
> git commit -m 'changes from child'
> git log --oneline
1764e47 changes from child # commit from child
d0d2cc9 second line # commit from parent
9926ae0 first commit # commit from parent
```

Let's checkout parent branch and add another file and commit so that we can easily rebase the child branch with master.


``` ruby
> git checkout master
> touch test2.txt
> echo 'hello world' > test2.txt
> git add --all
> git commit -m 'added test2'
6e96fa0 added test2 #new commit in master branch which isnt available in 'child-branch'
d0d2cc9 second line
9926ae0 first commit
```

So, now if we checkout `child-branch`, We notice we are one commit behind parent branch.

``` ruby
> git log child-branch..master --oneline
6e96fa0 added test2 # the new commit that created in parent.
```

What it means is, that git tells you that, when you checked out `child-branch` from parent branch `master`, the below commits have been added to master and you are behind those. So how it compares? Git finds out the commit which started your `child-branch` and lists the commit you have added in your child branch after that. we can also find that by doing,

``` ruby
> git merge-base child-branch master
d0d2cc97aa53d95e1bdd00a638d968e7e0fe12e2
```

If we notice we'll see that the first few character matches the second commit in our `child-branch`, as we had this one as the lastest commit in this branch and after that we added a new commit.

Now if we do a `git rebase` in our `child-branch` will receive all the commits that are in `master`, behind its new commit
<pre>
 1764e47 changes from child # commit from child
</pre>

So let's do this,

``` ruby
> git checkout child-branch
> git rebase master
> git log --oneline
391883d changes from child  # child's latest commit
6e96fa0 added test2         # the new commit from parent
d0d2cc9 second line         # commit from parent
9926ae0 first commit        # commit from parent
```

As we can see, this is how we got up to date with parent.

But situation changes when the parent tree's commit histry changes. Let's compare the parent and child's commit history side by side.
<pre>
    Parent                          Child
                                    391883d changes from child
    6e96fa0 added test2             6e96fa0 added test2
    d0d2cc9 second line             d0d2cc9 second line
    9926ae0 first commit            9926ae0 first commit
</pre>
As seen in the diff, all the past commits of child and parent are identical which makes it possible to rebase the child with parent. However, what if the parent's latest commit ID changes. Let's do this.

``` ruby
> git checkout master
> git commit --amend -m 'added file2 and changing commit'
> git log --oneline
52ea860 added file2 and changing commit # new commit id which we dont have in child, instead of 6e96fa0 
d0d2cc9 second line  # old commit id we have in child
9926ae0 first commit # old commit id we have in child
```

The diff now becomes a bit different.
<pre>
    Parent                                      Child
                                                391883d changes from child [not found]
    52ea860 added file2 and changing commit     6e96fa0 added test2  [not found]
    d0d2cc9 second line                         d0d2cc9 second line  [identical]
    9926ae0 first commit                        9926ae0 first commit [identical]
</pre>

So, what happens now is Parent branch rewrote the history and we also want the history to be re-written in child branch. Means we want the commit history in child branch to look like below in order to make it up to date with `master`.
<pre>
    391883d changes from child
    52ea860 added file2 and changing commit (instead of `6e96fa0 added test2`)
    d0d2cc9 second line
    9926ae0 first commit
</pre>

Git's Interactive rebase can come to help in achieving that. If we do an interactive rebase with last 3 commits and if we drop the commit that we do not want in our branch then our branch becomes ready to receive fresh new commits from `master` and it won't complain the rebase.

``` ruby
> git rebase -i HEAD~3
pick d0d2cc9 second line
pick 6e96fa0 added test2
pick 391883d changes from child
```

It gives us option to pick all three comit but we just want to drop the commit that was changed in the parent branch, in this case this is the second one `pick 6e96fa0 added test2` so we remove it and complete the commit like below 

``` ruby
pick d0d2cc9 second line
pick 391883d changes from child
```

And now our commit history in child branch becomes below,

``` ruby
> git log --oneline
3304d15 changes from child
d0d2cc9 second line
9926ae0 first commit
```

As you have seen the removed commit (6e96fa0 added test2) is no longer in our child branch. We can now easily rebase our child branch with parent to keep it up to date with parent. While being in `child-branch` 

``` ruby
> git rebase master
> git log
2172d09 changes from child
52ea860 added file2 and changing commit
d0d2cc9 second line
9926ae0 first commit
```

As you can see, We have received the changed commit from parent. We are now up to date in child-branch with master.

Please note that, this is not a suggested workflow and I do not recommend the workflow. But I came into a situation where I had to update a feature branch constantly without increasing number of commit and ammending the same commit each time, However, this branch also had few child branches and in the case I had to keep those child branches up to date with the feature, I followed this procedure and was easy for me to do the job.
