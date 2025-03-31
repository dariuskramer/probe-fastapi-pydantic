# Test Ledger Project

## How to Test

Use `pytest`:

```shell
pytest
```

Or manually with `curl`:

```shell
curl --silent -X GET \
      'http://localhost:8000/hdwallet/derivation/m' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      --data '{"seed":"000102030405060708090a0b0c0d0e0f"}'
```
