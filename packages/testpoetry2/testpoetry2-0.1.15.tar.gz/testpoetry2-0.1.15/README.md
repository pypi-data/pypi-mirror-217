## Task description

The main goal is to implement a password generator that returns whether a randomly generated password or password generated based on the passed template.

## Detailed conditions

Write a utility for generating passwords according to a given template that supports the CLI interface,
be able to work in PIPE and logging (-vvv – show detailed information during processing).

#### Generation Based on Character Sets

This password generation app should be implements two ways to generate random passwords:
- the random method (a password of a given length is randomly generated from a set of
  characters);
- the pattern-based generation method is used if passwords follow special rules or fulfill certain
  conditions.

Generation based on a character set is very simple. You simply let Password Gen know which characters
can be used (e.g. upper-case letters, digits, ...) and Password Gen will randomly pick characters out of the
set.

###### Defining a character set:

The character set can be defined directly in the argument line. For convenience, PasswordGen offers to add
commonly used ranges of characters to the set. This is done by chouse the appropriate optional in the
argument line. Additionally, to these predefined character ranges, you can specify characters manually: all
characters that you enter in the value of the -S option will be directly added to the character set.
