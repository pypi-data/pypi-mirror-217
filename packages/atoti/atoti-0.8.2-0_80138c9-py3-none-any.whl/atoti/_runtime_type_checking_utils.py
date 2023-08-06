import copy
import functools
import inspect
from collections.abc import Callable, Collection
from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)

import typeguard

from ._api_utils import ContainerType, walk_api

PercentileInterpolation = Literal["linear", "higher", "lower", "nearest", "midpoint"]
PercentileIndexInterpolation = Literal["higher", "lower", "nearest"]
PercentileMode = Literal["simple", "centered", "inc", "exc"]
VarianceMode = Literal["sample", "population"]

F = TypeVar("F", bound=Callable[..., Any])


def _instrument_typechecking(
    container: ContainerType,
    include_attribute: Optional[Callable[[ContainerType, str], bool]] = None,
) -> None:
    def callback(container: ContainerType, attribute_name: str) -> None:
        func = getattr(container, attribute_name)

        # Bound methods cannot be instrumented.
        assert not inspect.ismethod(func) or _is_typechecked(
            func
        ), f"Missing type checking for bound method {func}"

        new_func = typecheck()(func)
        if new_func is not func:
            setattr(container, attribute_name, new_func)

    walk_api(container, callback=callback, include_attribute=include_attribute)


def _is_typechecked(func: Callable[..., Any]) -> bool:
    return getattr(func, "_typechecked", False)


def _mark_typechecked(func: Callable[..., Any]) -> None:
    setattr(func, "_typechecked", True)  # noqa: B010


@overload
def typecheck(func: F) -> F:
    ...


@overload
def typecheck(
    *,
    ignored_params: Optional[Collection[str]] = ...,
) -> Callable[[F], F]:
    ...


@overload
def typecheck(clazz: type) -> type:
    ...


def typecheck(  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
    target: Optional[Union[F, type]] = None,
    *,
    ignored_params: Optional[Collection[str]] = None,
) -> Union[F, Callable[[F], F], type]:
    """Decorate the target to perform dynamic type checking.

    Use the more specific overloaded functions depending on the decorated argument.
    """
    if not target:
        return _typecheck_function(ignored_params=ignored_params)
    if inspect.isfunction(target) or inspect.ismethod(target):
        return _typecheck_function()(target)
    if isinstance(target, type):
        return _typecheck_class(target)

    raise TypeError(f"Unexpected type {type(target)} of {target}")


def _typecheck_function(
    *, ignored_params: Optional[Collection[str]] = None
) -> Callable[[F], F]:
    """Perform runtime type checking on the parameters of the decorated function.

    Args:
        ignored_params: A collection of parameter names that will not be type checked.
    """

    def decorator(func: F) -> F:
        # Verify whether we need to perform type checking.
        if not getattr(func, "__annotations__", None):
            # No type annotations. Ignore this method.
            return func
        if _is_typechecked(func):
            # Already typechecked.
            return func

        # Create and return the wrapper.
        return cast(F, _TypecheckWrapperFactory(func, ignored_params).create_wrapper())

    return decorator


def _typecheck_class(clazz: type) -> type:
    """Perform runtime type checking on the public API of the decorated class."""

    # Consider all public symbols of the class.
    def include_attribute(  # pylint: disable=too-many-positional-parameters
        container: ContainerType, attribute_name: str
    ) -> bool:
        assert container is clazz, f"Unexpected container for {clazz}: {container}"

        # Only consider public functions / methods.
        element = getattr(container, attribute_name)
        if inspect.isfunction(element) or inspect.ismethod(element):
            return not attribute_name.startswith("_")

        return False

    # Instrument the class and return it.
    _instrument_typechecking(clazz, include_attribute)
    return clazz


class _TypecheckWrapperFactory(Generic[F]):
    def __init__(self, func: F, ignored_params: Optional[Collection[str]]):
        self._func = func

        # Unwrap the function for type checking.
        # Make sure that the function is not already typed checked.
        self._ts_func = inspect.unwrap(func, stop=_is_typechecked)
        assert not _is_typechecked(self._ts_func), f"{func} is already typed checked."

        # Create a copy of the function for typechecking if necessary.
        if ignored_params:
            self._ts_func = copy.copy(self._ts_func)
            setattr(  # noqa: B010
                self._ts_func,
                "__annotations__",
                {
                    param: annotation
                    for param, annotation in self._ts_func.__annotations__.items()
                    if param not in ignored_params
                },
            )

    def create_wrapper(self) -> Any:
        # Create the wrapper function.
        @functools.wraps(self._func)
        def typechecked_func_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Perform typechecking on the input arguments.
            memo = typeguard._CallMemo(func=self._ts_func, args=args, kwargs=kwargs)
            typeguard.check_argument_types(memo)

            # Call the actual function.
            return self._func(*args, **kwargs)

        # Mark the function as typechecked and return it.
        _mark_typechecked(typechecked_func_wrapper)
        return typechecked_func_wrapper
