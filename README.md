# FastAPI and Pydantic exploration project

A FastAPI and Pydantic exploration project. Learn by building API endpoints with type-safe data validation.

## How to run

```shell
uv run fastapi dev app/main.py
```

## How to use

Either go to the documentation of the API at `127.0.0.1:8000/docs` or use `curl` to probe the API:

```shell
curl '127.0.0.1:8000/entropy/generate/256'
```

Also, calls can be chained in a pipeline:

```shell
host='127.0.0.1:8000'

curl --silent "${host}/entropy/generate/256" |
 curl --silent -H 'Content-Type: application/json' --data '@-' "${host}/seed/from_entropy/" |
 jq --raw-output '.seed' | tr -d '\n' |
 curl --silent --variable 'seed@-' --expand-url "${host}/keypair/from_derivation/m/1'/2/3'/4?seed={{seed}}"
```

This will output something like this:

```json
{
  "pubkey": "xpub6FB74Hhw6FdRLRphxG8MPnYHUKvgEeEF2p9rBu7s2chURaxBVU7agKwtihi1PuwhT2SZvvuXqV68MVnq9zrxYh9rNSJQHbc9KSzEE6j9XLQ",
  "prvkey": "xprvA2BkenB3Ft587wkErEbM2ebYvJ6BqBWPfbEFPWiFUHAVYnd2wvoL8XdQsQEMm83xPCW6UHqAiVBeTgDngRVb11x5nsd1EHB1XNvJv7z2zqV"
}
```

## Testing

Use `pytest`:

```shell
uv run pytest
```
