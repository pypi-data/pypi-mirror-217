"""A module for running OpenAI functions"""
from __future__ import annotations
from dataclasses import dataclass
from functools import partial, update_wrapper
from typing import Callable, Generic, Protocol, TypeVar, overload
from typing_extensions import ParamSpec

from .conversation import Conversation
from .functions.wrapper import FunctionWrapper


Param = ParamSpec("Param")
Return = TypeVar("Return")
T = TypeVar("T")


@dataclass
class NaturalLanguageAnnotated(Generic[T]):
    """A natural language annotated function return value"""

    function_result: T
    annotation: str


# This is a callable protocol, thus pylint can shut up
class DecoratorProtocol(
    Protocol[Param, Return]
):  # pylint: disable=too-few-public-methods
    """A protocol for the nlp decorator"""

    def __call__(
        self,
        function: Callable[Param, Return],
        *,
        system_prompt: str | None = None,
        model: str = "gpt-3.5-turbo-0613",
    ) -> Wrapper[Param, Return]:
        ...


class Wrapper(Generic[Param, Return]):
    """A wrapper for a function that provides a natural language interface"""

    def __init__(
        self,
        origin: Callable[..., Return],
        system_prompt: str | None = None,
        model: str = "gpt-3.5-turbo-0613",
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        self.origin = origin
        self.system_prompt = system_prompt
        self.conversation = Conversation(model=model)
        self.openai_function = FunctionWrapper(
            self.origin, name=name, description=description
        )
        self.conversation.add_function(self.openai_function)

    def __call__(self, *args: Param.args, **kwds: Param.kwargs) -> Return:
        return self.origin(*args, **kwds)

    def _initialize_conversation(self) -> None:
        """Initialize the conversation"""
        self.conversation.clear_messages()
        if self.system_prompt is not None:
            self.conversation.add_message(
                {
                    "role": "system",
                    "content": self.system_prompt,
                }
            )

    def from_natural_language(self, prompt: str) -> Return:
        """Run the function with the given natural language input

        Args:
            prompt (str): The prompt to use

        Returns:
            The result of the original function
        """
        self._initialize_conversation()
        return self.conversation.run(self.openai_function.name, prompt)

    def natural_language_response(self, prompt: str) -> str:
        """Run the function and respond to the user with natural language

        Args:
            prompt (str): The prompt to use

        Returns:
            str: The response from the AI
        """
        self._initialize_conversation()
        self.conversation.add_message(prompt)
        self.conversation.generate_message(
            function_call={"name": self.openai_function.name}
        )
        response = self.conversation.run_until_response(False)
        return response.content

    def natural_language_annotated(
        self, prompt: str
    ) -> NaturalLanguageAnnotated[Return]:
        """Run the function and respond to the user with natural language as well as
        the raw function result

        Args:
            prompt (str): The prompt to use

        Returns:
            NaturalLanguageAnnotated: The response from the AI
        """
        self._initialize_conversation()
        function_result = self.conversation.run(self.openai_function.name, prompt)
        response = self.conversation.run_until_response(False)
        return NaturalLanguageAnnotated(function_result, response.content)


def _nlp(
    function: Callable[Param, Return],
    *,
    name: str | None = None,
    description: str | None = None,
    system_prompt: str | None = None,
    model: str = "gpt-3.5-turbo-0613",
) -> Wrapper[Param, Return]:
    """Add natural language input to a function

    Args:
        function (Callable): The function to add natural language input to
        system_prompt (str | None): The system prompt to use. Defaults to None.
        model (str): The model to use. Defaults to "gpt-3.5-turbo-0613".
        name (str | None): The name override for the function.
        description (str | None): The description sent to OpenAI.

    Returns:
        The function, with natural language input, or a decorator to add natural
        language input to a function
    """

    wrapped: Wrapper[Param, Return] = Wrapper(
        function,
        system_prompt=system_prompt,
        model=model,
        name=name,
        description=description,
    )
    update_wrapper(wrapped, function)

    return wrapped


@overload
def nlp(
    function: Callable[Param, Return],
    *,
    name: str | None = None,
    description: str | None = None,
    system_prompt: str | None = None,
    model: str = "gpt-3.5-turbo-0613",
) -> Wrapper[Param, Return]:
    ...


@overload
def nlp(
    *,
    name: str | None = None,
    description: str | None = None,
    system_prompt: str | None = None,
    model: str = "gpt-3.5-turbo-0613",
) -> DecoratorProtocol:
    ...


def nlp(
    function: Callable[Param, Return] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    system_prompt: str | None = None,
    model: str = "gpt-3.5-turbo-0613",
) -> Wrapper[Param, Return] | DecoratorProtocol:
    """Add natural language input to a function

    Args:
        function (Callable | None): The function
            to add natural language input to
        name (str | None): The name override for the function, will be inferred from
            the function name if not provided.
        description (str | None): The description sent to OpenAI, defaults to the short
            description from the function docstring.
        system_prompt (str | None): The system prompt to use. Defaults to None.
        model (str): The model to use. Defaults to "gpt-3.5-turbo-0613".

    Returns:
        Wrapper | DecoratorProtocol: The function, with natural language input, or a
        decorator to add natural language input to a function
    """

    if function is None:
        return partial(
            _nlp,
            name=name,
            description=description,
            system_prompt=system_prompt,
            model=model,
        )

    return _nlp(
        function,
        name=name,
        description=description,
        system_prompt=system_prompt,
        model=model,
    )
