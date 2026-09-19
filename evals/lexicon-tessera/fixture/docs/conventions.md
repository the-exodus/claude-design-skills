# Code conventions

Short, and meant to be followed. If a rule here gets in the way, raise it in a pull request rather than quietly ignoring it.

## Naming

- Take identifiers from the [lexicon](lexicon.md). If the lexicon says tile, the code says `tile`, not `cell` or `slot`; if it says send, the method is `SendTo`, not `Push`.
- When a pull request adds a class, add a lexicon entry for the class in the same pull request.
- The stack is `SecondaryArea` in code, never `Stack`. Everyone says "the stack" when talking about the main-stack layout, but in C# the word already means `System.Collections.Generic.Stack<T>` and the call stack, and a type called `Stack` in a layout namespace confused every newcomer who met it.
- Command names in the config file are lower-case with hyphens (`move-to-workspace`). The method that carries one out is the same words in Pascal case where that reads well.
- No Hungarian prefixes, no `I` on anything but interfaces, `_camelCase` for private fields.

## Structure

- Every command and every service method that acts on the running system takes `WmContext ctx` as its first parameter. Do not reach for statics, and do not cache anything from `ctx` in a field.
- Layouts are pure ([ADR 0001](adr/0001-layouts-are-pure-functions.md)). A layout never sees a window handle and never takes `ctx`.
- Win32 calls live in `Tessera.Native`. Code under `src/Tessera` talks to the platform only through the interfaces on `WmContext`.
- Nothing under `src/Tessera` starts a thread. Window events and hotkeys arrive on the message loop; handle them and return.

## Doc comments

- Every public type and member has a `/// <summary>`.
- Where a comment leans on a word from the lexicon, cite it once as `(lexicon: term)` so a reader knows the word is being used in its defined sense.
- Say what and why. The code already says how.

## Errors

- A bad config file never takes Tessera down: `TesseraConfig.Load` throws `ConfigException`, and the caller keeps the old settings.
- A window that vanishes halfway through a command is normal on Windows. Treat a failed native call on a window as "the window is gone" and carry on.
