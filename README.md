# jsonpeek

> Print the inferred schema of a JSON or JSONL file so you can see its shape without reading it.

## Why

You get handed a 40 MB API dump and need to know what is in it. `jq` can show
you values; `jsonpeek` shows you the *shape* — every key, its type, and which
keys are only sometimes there.
