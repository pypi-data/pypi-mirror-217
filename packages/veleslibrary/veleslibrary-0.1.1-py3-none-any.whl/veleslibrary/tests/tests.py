"""
This file includes all psychometric methods that are not questionnaires. In English.
That means things like the Stroop test, the Wisconsin Card Sorting Test, Alternative
Uses Task, etc. For other languages, use appropriate folder.

Every test should be a function returning the lowest possible type of structural
element. For example if it has to be a page, so be it, but if it can be a list of
questions, it should be that. Use type hints to indicate what the function returns.

Names of the functions should be lowercase abbrieviations of the test name (if possible).
The default label should be an uppercase abbrieviation of the test name (if possible).
If there's a standard instruction, it should be included.

Every function should have a docstring explaining what the test is, what it measures,
and possibly APA-style citation. Feel free to include any other information you think
might be useful.

I'd be grateful if you could also add a page in the documentation:
https://github.com/jakub-jedrusiak/VelesLibrary
"""
