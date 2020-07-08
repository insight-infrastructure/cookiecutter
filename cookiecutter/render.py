"""Functions to perform rendering."""
import ast
import re

import six


def render_variable(env, raw, cookiecutter_dict, context_key):
    """Render the next variable to be displayed in the user prompt.

    Inside the prompting taken from the cookiecutter.json file, this renders
    the next variable. For example, if a project_name is "Peanut Butter
    Cookie", the repo_name could be be rendered with:

        `{{ cookiecutter.project_name.replace(" ", "_") }}`.

    This is then presented to the user as the default.

    :param Environment env: A Jinja2 Environment object.
    :param raw: The next value to be prompted for by the user.
    :param dict cookiecutter_dict: The current context as it's gradually
        being populated with variables.
    :return: The rendered value for the default variable.
    """
    if raw is None:
        return None
    elif isinstance(raw, dict):
        return {
            render_variable(env, k, cookiecutter_dict, context_key): render_variable(
                env, v, cookiecutter_dict, context_key
            )
            for k, v in raw.items()
        }
    elif isinstance(raw, list):
        return [render_variable(env, v, cookiecutter_dict, context_key) for v in raw]
    elif not isinstance(raw, six.string_types):
        raw = str(raw)

    template = env.from_string(raw)

    rendered_template = template.render({context_key: cookiecutter_dict})

    LIST_REGEX = r'^\[.*\]$'
    if bool(re.search(LIST_REGEX, rendered_template)):
        """If variable looks like list, return literal list"""
        return ast.literal_eval(rendered_template)

    DICT_REGEX = r'^\{.*\}$'
    if bool(re.search(DICT_REGEX, rendered_template)):
        """If variable looks like dict, return literal dict"""
        return ast.literal_eval(rendered_template)

    return rendered_template