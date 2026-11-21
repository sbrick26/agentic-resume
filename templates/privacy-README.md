# privacy (keep this folder private)

- client-names.txt: one per line, `Real Name | generic wording`. These names
  never appear in public output; the generic wording is used instead.
- blocklist.txt: any other term that must never appear in public output.
- public-paths.txt: folders that are public or feed something public
  (for example resume/ and site/).

`ar-guard` reads these files. The plugin ships no names of its own.
