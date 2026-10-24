# Usage procedure

## Important things to remember

- Use the same server for `POST /new-bit` and `POST /verify`
- Make sure the server you are using is trusted, it should be ideally independent and unknowing of what you are doing

## Names and symbols

P - Prover, the person who obtains a bit
V - Verifier, the person who confirms the bit

T0 - Time since which the server time is counted
T - Time at which initial request is made
S - Created secret (MUST BE B64)
b - Generated bit
HS - SHA512 of secret b64
H - Commitment from `POST /new-bit`

## End-to-end protocol

### Phase 0

Both P and V agree on the minute (T) when P will made the request, time when P will generate the secret and how (I suggest `GET /secret`, because it gives B64 secret and HS "for free").

### Phase 1

On agreed time, P obtains the secret (S) and hash (HS), and sends latter to V.

### Phase 2

On agreed time, P generates the bit, with agreed timestamp. This is how the request json should look like:

```js
{
  "secret-b64": "S",
  "timestamp": T
}
```

and how response should look like:

```js
{
  "commitment": "H",
  "bit": b,
  "timestamp": T
}
```

After obtaining the bit, P should send commitment (H) to V

### Phase 3

P acts on b.

### Phase 4

P reveals secret and bit (S and b) to V.

V can now verify HS and b, by calling `POST /verify` with that request json:

```js
{
  "secret-b64": "S",
  "sha512-secret-b64": "HS",
  "timestamp": T,
  "commitment": "H",
  "bit": b
}
```
