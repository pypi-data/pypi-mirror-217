# Custom importing library

### Importing a function from n different code files depending on the running operating system.
Let's say this is our project structure:
```
main/
  -> main.py
  -> linux.py
  -> windows/
    -> windows.py
```

And you want to import a function named `product` from linux.py if you are running Linux and from windows.py if you are running Windows.

```python
import customimport

product = customimport.import_by_os({
    customimport.WINDOWS: 'windows.windows',
    customimport.LINUX: 'linux'
}, 'product')
```

And you can use your product function, and its backend will be the code from the file chosen by the os.
> The function name has to be the same in all these code files.

> `customimport` supports these opearting systems:
>  - Windows
>  - Linux
>  - MacOS
>  - FreeBSD
>  - NetBSD
>  - OpenBSD
>  - SunOS
>  - AIX


### Importing a function from n different code files based on the value of a variable.
Let's say this is our project structure:
```
main/
  -> main.py
  -> hey.py
  -> rututu/
    -> there.py
```

And you want to import a function named `product` from hey.py if variable `alala` is 'hey' and from there.py if it is 'there'.

```python
import customimport

alala = 'hey'

product = customimport.import_by_variable({
    'there': 'rututu.there',
    'hey': 'hey'
}, alala, 'product')
```

And you can use your product function, and its backend will be the code from the file determined by the variable outcome.
> The function name has to be the same in all these code files.

You can also set default return if the variable value did not match any of those:
```python
import customimport

alala = 'hello'

product = customimport.import_by_variable({
    'there': 'rututu.there',
    'hey': 'hey'
}, alala, 'product', 'not_found')
```
### Importing a function from n different code files based on the active python version.
Let's say this is our project structure:
```
main/
  -> main.py
  -> v37.py
  -> rututu/
    -> v38.py
```

And you want to import a function named `product` from v37.py if python version is `3.7` and from v38.py if it is `3.8`.

```python
import customimport

product = customimport.import_by_version({
    '3.8': 'rututu.v38',
    '3.7': 'v37'
}, 'product')
```

And you can use your product function, and its backend will be the code from the file determined by the active python version.
> The function name has to be the same in all these code files.


### Support os.py
You can buy me a coffee if you enjoy my work [Buy me a coffee ☕](https://www.buymeacoffee.com/Bamboooz)


### License

This project is licensed under the [BSD-3 Clause License](https://opensource.org/license/bsd-3-clause/).