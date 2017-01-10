it's often useful to pull an elpa repository so you can serve it from
some other location.

This code is designed to do that. 


It slurps the archive-contents from ELPA and then downloads each file
based on the information in it.

It does:

- [ELPA](http://elpa.gnu.org) 
- [MELPA](https://melpa.org)

If you want marmalade's packages you can already get them via a zip
download. But feel free to patch this code to add any repo.

## requirements

You need to:

```
pip install sexpdata
```
