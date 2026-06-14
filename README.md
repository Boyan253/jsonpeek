# jsonpeek

> Print the inferred schema of a JSON or JSONL file so you can see its shape without reading it.

## Why

You get handed a 40 MB API dump and need to know what is in it. `jq` can show
you values; `jsonpeek` shows you the *shape* — every key, its type, and which
keys are only sometimes there.

## Usage

```
python jsonpeek.py response.json
python jsonpeek.py events.jsonl --lines
curl -s https://api.example.com/things | python jsonpeek.py -
```

## Output

```
{
  items: [
    {
      id: int
      name: str
      deleted_at: null|str  (optional)
    }
  ]
  total: int
}
```

- Arrays are collapsed to a single merged element type.
- A key missing from some elements is marked `(optional)`.
- Conflicting types are unioned, e.g. `int|str`.

## Sampling

Large arrays are sampled (`--sample`, default 50 items) so the tool stays fast
on big files. Raise it if the tail of your data looks different from the head.

## Tests

```
pip install pytest
pytest
```
