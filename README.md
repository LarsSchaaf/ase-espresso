# GapAlysis

Python package to investigate the use of GAP on catalytic systems. 

- Also included as a submodule in `PhD_Code`
 

## Creating Commit Alias

Saved in `~/.gitconfig`

```bash
scommit = "!f() { git submodule foreach \"git add . \" ; echo $1; git submodule foreach \"git commit -a -m 'PhD-Code: $1' \" ; git add .; git commit -a -m \"$1\"; }; f"

spush = "!f() {git submodule foreach \"git push\"; git push --recurse-submodules=on-demand ;}; f"
```
