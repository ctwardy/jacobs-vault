# README
> jacobs-vault / nbs

Toplevel notebooks for Jacobs' VAULT submission. Note that some pieces are in other folders which might not use nbdev.

## Symlinks
The following soft links are required:

### ../data
> data -> ../data 

which itself should contain or point to your VAULT data. E.g.
```bash
ln -s ../data ./
```


### ../jacobs_vault
The code here needs to be able to find the Python modules.  Either symlink  jacobs_vault -> ../jacobs_vault/, e.g.
```bash
ln -s ../jacobs_vault ./
```
or ensure ../jacobs_vault is on the PYTHONPATH.
