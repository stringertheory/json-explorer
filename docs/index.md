[![Build status](https://img.shields.io/github/actions/workflow/status/stringertheory/json-explorer/main.yml?branch=main)](https://github.com/stringertheory/json-explorer/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/stringertheory/json-explorer/branch/main/graph/badge.svg)](https://codecov.io/gh/stringertheory/json-explorer)

# JSON Explorer

Explore the structure and contents of a group of JSONs, like responses
from an API.

### Installation

```
pip install json-explorer
```

JSON Explorer is a small tool with no dependencies and is tested in
Python 3.7+.

### Getting started

Get started by writing a few JSONs you want to explore to a file, one
per line. Then run `json-explorer` from the command line:

```
json-explorer data_from_an_undocumented_API.jsonl
```

If you just want to try it out but don't have JSONs in a file, you can
run `json-explorer --example` to see how it works with example data.

This will pop up a web page that helps you explore the properties of
the objects, what data types are in there, what values are unique, and
more.

From there, you might use `jq` or `jmespath` to write something to
more read the data that you're interested in using.

