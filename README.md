it's often useful to pull an elpa repository so you can serve it from
some other location.

This code is designed to do that. 


It slurps the archive-contents from ELPA and then downloads each file
based on the information in it.

It only does [ELPA](http://elpa.gnu.org) right now but it could do any
repository (marmalade or MELPA) easily.

## requirements

You need to:

```
pip install sexpdata
```
