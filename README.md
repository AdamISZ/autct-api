### autct-api

This allows a Python application to make RPC calls to an [autct](https://github.com/AdamISZ/aut-ct) server, without any dependencies or cryptographic library calls. Read there for me details on what autct is.

The RPC calls provided are:

* prove

* verify

* createkeys

## Install

```
pip install autctapi
```

Projected published [on PyPI](https://pypi.org/project/autctapi/). A very small library that only relies on [websockets](https://github.com/python-websockets/websockets).

## Examples

To try it out, you need to run the [autct rust binary](https://github.com/AdamISZ/aut-ct/releases) **as a server**. The syntax for that is shown in the Worked Example section of that repo's readme. Then, run here:

```
python src/example.py
```

... although obviously the purpose here is for a Python developer to actually *read* that file, and look at the way that RPC calls are done. Individual scenarios will require different config settings, that can easily be modified as shown in that file.



