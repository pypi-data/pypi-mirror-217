"""
This file includes all psychometric methods that are not questionnaires. In Polish.
That means things like the Stroop test, the Wisconsin Card Sorting Test, Alternative
Uses Task, etc. For other languages, use appropriate folder or the main file for English.

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

from velesresearch.structure import Page, Question
from velesresearch.options import QuestionOptions, PageOptions
from velesresearch import question, page, info
from anyascii import anyascii


def aut(
    label: str = "AUT",
    item: str = "cegła",
    max_answers: int = 20,
    time_limit: int = 120,
    return_type: str = "page",
    instruction: str | None = None,
) -> list[Page] | list[Question]:
    """Alternative Uses Task. The task measures creativity. The participant is given
    an item (e.g. a brick) and asked to list as many uses of it as possible. This
    function returns a a list of pages or list of questions. The first page contains
    an instruction. The second page contains the item and the task itself.
    You probably want to add a time limit to the second page.

    Args:
        label (str, optional): Defaults to "AUT". An item will be added to the label.
        item (str, optional): the item to be used, lowercase. Defaults to "Cegła".
        max_answers (int, optional): max. number of input fields to generate. Defaults to 20.
        time_limit (int, optional): time limit in seconds. Works only for return_type="page". Defaults to 120.
        return_type (str, optional): should the function return pages ("page") or list of questions ("question"). Defaults to "page".
        instruction (str | None, optional): If None, defaults to the default instruction.
    """
    if instruction is None:
        instruction_info = info(
            f"{label}_instruction",
            "Za chwilę zostaniesz poproszony(-a) o wymyślenie jak największej liczby **zastosowań** dla pewnego przedmiotu. Postaraj się, żeby Twoje odpowiedzi były jak najbardziej **oryginalne, kreatywne, twórcze, pomysłowe**. Każdą odpowiedź wpisz w osobne pole. **Odpowiedzi wpisuj po kolei.** Będziesz widział(a) tylko trzy okienka do wpisywania odpowiedzi na raz.",
        )
    else:
        instruction_info = info(f"{label}_instruction", instruction)

    item_ascii = anyascii(item)
    question_text = f"Twórcze zastosowanie: {item}"
    placeholder = "Następny pomysł..."

    initial_items = []
    for i in range(1, 4):
        initial_items.append(
            Question(
                label=f"{label}_{item_ascii}_{i}",
                question_text=f"{i}. {question_text}",
                question_type="text",
                options=QuestionOptions(
                    visible_if=f"{{{label}_{item_ascii}_{i+1}}} empty",
                    placeholder=placeholder,
                    hide_number=True,
                ),
            )
        )
    middle_items = []
    for i in range(4, max_answers):
        middle_items.append(
            Question(
                label=f"{label}_{item_ascii}_{i}",
                question_text=f"{i}. {question_text}",
                question_type="text",
                options=QuestionOptions(
                    visible_if=f"{{{label}_{item_ascii}_{i-2}}} notempty and {{{label}_{item_ascii}_{i+1}}} empty",
                    placeholder=placeholder,
                    hide_number=True,
                ),
            )
        )

    last_item = Question(
        label=f"{label}_{item_ascii}_{max_answers}",
        question_text=f"{max_answers}. {question_text}",
        question_type="text",
        options=QuestionOptions(
            visible_if=f"{{{label}_{item_ascii}_{max_answers-2}}} notempty",
            placeholder=placeholder,
            hide_number=True,
        ),
    )

    question_list = initial_items + middle_items + [last_item]

    if return_type == "question":
        return [instruction_info] + question_list
    elif return_type == "page":
        return [Page(label=f"{label}_instruction", questions=instruction_info)] + [
            Page(
                label=f"{label}_{item_ascii}",
                questions=question_list,
                options=PageOptions(
                    time_limit=time_limit, navigation_visibility="hide"
                ),
            )
        ]
    else:
        raise ValueError("return_type must be either 'page' or 'question'")
