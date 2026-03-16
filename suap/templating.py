import re
import logging
from pathlib import Path
from dataclasses import dataclass

__all__ = ()

logger = logging.getLogger(__name__)

@dataclass
class Key:
    name: str
    value: str

class TemplateKeysRemainingError(Exception):
    def __init__(self, remaining_keys: set[str]):
        super().__init__(
            "There are keys defined in the template " \
                f"that were not formatted! Remaining Keys: {remaining_keys}"
        )

class Template():
    def __init__(self, template_name: str):
        self.__template_string = self.__get_template_contents(template_name)

        # NOTE: Help improving this would be cool, I'm not good at regex
        defined_suap_keys_list = re.findall(
            "{suap-(.*?)}", self.__template_string, re.DOTALL
        )

        self.__defined_suap_keys: set[str] = set(defined_suap_keys_list)

        print(f"--> {self.__defined_suap_keys}")

    def format(self, keys: tuple[Key, ...]) -> str:
        formatted_string = self.__template_string

        remaining_keys = self.__defined_suap_keys

        for key in keys:
            key_name = key.name

            if key_name in remaining_keys:
                logger.debug(f"Formatting template key '{key_name}'...")

                remaining_keys.remove(key_name)

                formatted_string = formatted_string.replace(
                    f"{{suap-{key_name}}}", str(key.value)
                )

        if len(remaining_keys) > 0:
            raise TemplateKeysRemainingError(remaining_keys)

        return formatted_string

    def __get_template_contents(self, template_name: str) -> str:
        specific_template_path = Path(__file__).parent.joinpath("templates", template_name)

        logger.debug(
            f"Opening and reading '{template_name}' template at '{specific_template_path}'..."
        )

        with open(specific_template_path, mode = "r") as file:
            template_contents = file.read()

        return template_contents