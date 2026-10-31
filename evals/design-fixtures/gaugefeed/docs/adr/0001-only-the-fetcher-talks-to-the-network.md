# ADR-0001 — Only the fetcher talks to the network

**Status:** Accepted (2025-03-10)

## Context

Every station is reached over HTTP, and stations fail in the ways remote hosts do: they time out, refuse connections, or answer slowly. Each new place that opens a connection has to handle all of that again, and every test that reaches it needs a station or a patch standing in for one.

## Decision

`gaugefeed/fetcher.py` is the only module that talks to the network. It asks each station for its reading and hands the rest of gaugefeed plain data; a station that does not answer is dealt with there. The architecture test forbids every other module from importing `urllib`, `http` or `socket`, so a second network path fails the build rather than slipping in.

Letting each module fetch what it needs was rejected because the timeout and the handling of a station that does not answer would be repeated, and would drift apart. Wrapping the network in a client object passed around the program was rejected as more structure than one module of two functions needs.

## Consequences

Timeouts and failed stations are handled in one place, and the other modules are tested without patching the network. A feature that needs something from a station goes through the fetcher, even when it would be shorter to open a connection where it is used.
