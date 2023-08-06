from __future__ import annotations

from typing import List, Optional, Tuple, Union
import warnings

from typeguard import typechecked

from jijmodeling.deprecation.deprecation import (
    deprecated_name,
    JijFutureWarning
)
import jijmodeling.expression.condition as _condition
import jijmodeling.expression.expression as _expression
import jijmodeling.expression.sum as _sum

# type validation
import jijmodeling.expression.variables.variable as _variable


class ProdOperator(_sum.ReductionOperator):
    pass


INDEXWITHCOND = Union[_variable.Element, Tuple[_variable.Element, _condition.Condition]]


@deprecated_name("Prod", "prod", kind="function")
def Prod(
    indices: Union[INDEXWITHCOND, List[INDEXWITHCOND]],
    term: _expression.Expression,
) -> ProdOperator:
    """
    Prod function.

    Args:
        indices: product index dict or list of index.
        term (Expression): operand

    Returns:
        ProdOperator: ProdOperator object.

    Example:
        Create $\\prod_{i=0}^n d_i x_i$

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', dim=1)
        n = d.shape[0]
        x = jm.Binary('x', shape=n)
        i = jm.Element('i', n)
        jm.Prod(i, d[i]*x[i])
        ```

        Create $\\prod_{i}\\sum_j d_{ij}x_i x_j$

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', dim = 2)
        n = d.shape[0]
        x = jm.Binary('x', shape=n)
        i = jm.Element('i', n)
        j = jm.Element('j', n)
        jm.Prod([i, j], d[i, j]*x[i]*x[j])
        ```

        Conditional production

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', dim = 2)
        n = d.shape[0]
        i, j = jm.Element("i", n), jm._variable.Element("j", n)
        x = jm.Binary('x', shape=n)
        jm.Prod([i, (j, i < j)], d[i, j]*x[i]*x[j])
        ```
    """

    # convert indices and condition to list-type object
    # ex. i -> [i]
    indices_list = indices if isinstance(indices, list) else [indices]  # type: ignore

    @typechecked
    def convert_to_element(
        index: Union[
            _variable.Element, Tuple[_variable.Element, Optional[_condition.Condition]]
        ],
    ) -> Tuple[_variable.Element, Optional[_condition.Condition]]:
        if isinstance(
            index, tuple
        ):  # Tuple[_variable.ElementType, Optional[Condition]]
            elem, cond = index
            return (elem, cond)
        else:  # _variable.ElementType
            return (index, None)

    elems_and_conds: List[Tuple[_variable.Element, Optional[_condition.Condition]]] = [
        convert_to_element(index) for index in indices_list
    ]
    elements = [elem for elem, _ in elems_and_conds]
    condition_list = [cond for _, cond in elems_and_conds]

    # list length validation
    import jijmodeling.utils.utils as _utils

    _utils.validate_value("len(indices) > 0", len(elements) > 0)
    _utils.validate_value("len(condition_list) > 0", len(condition_list) > 0)
    _utils.validate_value(
        "len(indices_list)  == len(condition_list)",
        len(indices_list) == len(condition_list),
    )
    sum_term = term
    for sum_index, cond in zip(elements[::-1], condition_list[::-1]):
        sum_term = ProdOperator(
            sum_index=sum_index,
            operand=sum_term,
            condition=cond if cond is not None else _condition.NoneCondition(),
        )
    return sum_term  # type: ignore


def prod(
    index: Union[INDEXWITHCOND, List[INDEXWITHCOND]],
    operand: _expression.Expression,
) -> ProdOperator:
    """
    Prod function.

    Args:
        indices: product index dict or list of index.
        operand (Expression): operand

    Returns:
        ProdOperator: ProdOperator object.

    Example:
        Create $\\prod_{i=0}^n d_i x_i$

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', ndim=1)
        n = d.shape[0]
        x = jm.BinaryVar('x', shape=n)
        i = jm.Element('i', n)
        jm.prod(i, d[i]*x[i])
        ```

        Create $\\prod_{i}\\sum_j d_{ij}x_i x_j$

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', ndim=2)
        n = d.shape[0]
        x = jm.BinaryVar('x', shape=n)
        i = jm.Element('i', n)
        j = jm.Element('j', n)
        jm.prod([i, j], d[i, j]*x[i]*x[j])
        ```

        Conditional production

        ```python
        import jijmodeling as jm
        d = jm.Placeholder('d', ndim=2)
        n = d.shape[0]
        i, j = jm.Element("i", n), jm._variable.Element("j", n)
        x = jm.BinaryVar('x', shape=n)
        jm.prod([i, (j, i < j)], d[i, j]*x[i]*x[j])
        ```
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=JijFutureWarning)
        return Prod(index, operand)