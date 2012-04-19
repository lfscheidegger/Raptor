# Raptor

Raptor is a python utility that wraps around common git commands to
provide slightly better hooks.

git hooks have two main drawbacks:

1 - they can't take user input. Because they run from within git, it's
impossible to write a hook that, for instance, runs a linter (or unit
tests), and prompts the user to continue or abort. Git hooks can only
return a zero- or non-zero exit status to signify success or failure,
without user interaction.

2 - there is no pre-push hook. I don't know why this is the case, but
it is.

### Usage ###

Raptor captures some common git commands and wraps them around extra
functionality. You can configure a linter for your files using the
.raptorconfig file, for instance, and Raptor will run that linter
whenever you commit or push code that matches the rules. Any git
command that Raptor doesn't recognize simply gets passed on to git
without changes.

tl;dr - just replace 'git' by 'raptor' wherever you want to use
raptor. So for instance, you can

$ raptor checkout master

$ raptor rebase origin/master

$ raptor diff

instead of using vanilla git.

### Installation ###

Assuming you're running on a machine with setuptools,

$ sudo python setup.py install

After this you should just be able to run

$ raptor

in your bash.

### Contact info ###

Questions, suggestions, harshly worded criticisms and the like should
be sent to luiz.scheidegger@gmail.com.
