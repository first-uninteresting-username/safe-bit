# Usage procedure

## Important things to remember

- Use the same server for `POST /new-bit` and `POST /verify`.
- Make sure the server you are using is trusted; ideally, it should be independent and unaware of what you are doing.

## Names and symbols

P - Prover, the person who obtains a bit
V - Verifier, the person who confirms the bit

T0 - Time since which the server time is counted
T - Time at which the initial request is made
S - Created secret (MUST BE B64)
b - Generated bit
HS - SHA-512 hash of the B64 secret
H - Commitment from `POST /new-bit`

## End-to-end protocol

### Phase 0

Both P and V agree on the minute (T) when P will make the request, and on when and how P will generate the secret (I suggest `GET /secret`, because it gives the B64 secret and HS "for free").

### Phase 1

At the agreed time, P obtains the secret (S) and its hash (HS), and sends the latter to V.

HS must reach V before minute T begins. Once T has passed, the server reveals the encrypted minute, and anyone who knows it can compute the bit for any secret. V should therefore reject an HS that arrives late.

### Phase 2

At the agreed time, P generates the bit using the agreed timestamp. This is what the request JSON should look like:

```js
{
  "secret-b64": "S",
  "timestamp": T
}
```

and what the response should look like:

```js
{
  "commitment": "H",
  "bit": b,
  "timestamp": T
}
```

After obtaining the bit, P should send the commitment (H) to V.

### Phase 3

P acts on b.

### Phase 4

P reveals the secret and the bit (S and b) to V.

V can now verify HS and b, by calling `POST /verify` with this request JSON:

```js
{
  "secret-b64": "S",
  "sha512-secret-b64": "HS",
  "timestamp": T,
  "commitment": "H",
  "bit": b
}
```
