# Motivation

## The problem

Imagine a medical researcher running an experiment in which each patient is
randomly assigned to receive either a placebo or an experimental medication.

The patients, for whatever reason, don't trust the researcher to assign the
groups fairly.

## How `safe-bit` helps

With `safe-bit`, the patients can verify for themselves, after the fact, that
the assignment was fair.

In the terms used in [usage.md](usage.md):

- the researcher is the **Prover (P)**, who obtains the random bit and acts on
  it;
- the patients are the **Verifiers (V)**, who later confirm the bit was not
  manipulated.

See [usage.md](usage.md) for the full protocol.

> [!IMPORTANT]
> The `safe-bit` server used for the procedure must be operated independently
> of both parties. If either the researcher or the patients control the server,
> the verification proves nothing.
