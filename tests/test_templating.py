from suap.templating import Template, Key
from suap.errors import TemplateKeysRemainingError

def test_keys_remaining():
    template = Template("test_template.txt")

    try:
        template.format(
            keys = (
                Key("some-weird-format-2", "this should work!"),
            )
        )

    except Exception as error:
        assert isinstance(error, TemplateKeysRemainingError) == True
        return

    assert False, "Unreadable! The 'TemplateKeysRemainingError' exception did not occur!"

def test_correct_formatting():
    template = Template("test_template.txt")

    formatted_template = template.format(
        keys = (
            Key("insert-meow", "MEOW"),
            Key("some-weird-format-1", "some weird format"),
            Key("some-weird-format-2", "this should work!"),
        )
    )

    expected_result = """The kitty goes... MEOW! Some weird formatting... {some weird format" {some weird format}} {this should work!} suap-umm"""

    assert formatted_template == expected_result