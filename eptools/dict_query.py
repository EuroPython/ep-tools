"""
Helper functions to build trees of logical
conditions to query on dictionary field values.

Example
-------
>>> talk = {'title': 'Meeting',
>>>         'duration': 60,
>>>         'admin_type': 'EPS session',
>>>        }
>>> conds = [('duration',   (30, 45, 60)),
>>>          ('language',   'English'),
>>>          ('admin_type', 'EPS session')]
>>> query = build_query(conds)
>>> assert exec_query(talk, query)

Note
----
This could be improved by adding more flexibility on the operators
being used by `conds`. For now, we only use ('==', 'and', 'or').
"""
import operator

comp_operators = {'==': operator.eq,
                  '!=': operator.ne,
                  '<': operator.lt,
                  '>': operator.gt,
                  '<=': operator.le,
                  '>=': operator.ge,
                  '_has': operator.contains,
                 }

logic_operators = {'and': operator.and_,
                   'or': operator.or_,
                   }


def _binary_op(op_func, comps):
    """ Return a concatenation of operators `op_func` on each pair
    of conditions in `conds`.
    """
    if len(comps) == 1:
        nuop = comps[0]
    elif len(comps) == 2:
        nuop = (op_func, comps[0], comps[1])
    else:
        frst = comps[0]
        rest = comps[1:]
        nuop = (op_func, frst, _binary_op(op_func, rest))

    return nuop


def _parse_comparison(comp_val, default_op='=='):
    """ Return a comparison symbol and a value parsed from `comp_val`.
    Parameters
    ----------
    comp_val: str or any value
        A comparison value, e.g.: '> 10'

    default_op: str
        A comparison operator symbol.

    Returns
    -------
    sym: str
        Comparison operator symbol

    val: str or any value
        The value to be compared to.
        Will convert str to float or int if possible.
    """
    if not isinstance(comp_val, str):
        return default_op, comp_val

    for sym in comp_operators:
        if comp_val.startswith(sym + ' '):
            val = comp_val.replace(sym + ' ', '')
            if val.strip().isdecimal() and '.' in val:
                val = float(val)
            elif val.strip().isnumeric():
                val = int(val)

            return sym, val

    return default_op, comp_val


def _comparison_op(op_func, field_name, value):
    """ Create a comparison operation or a 'or' operation if
    len(value) > 1.
    Parameters
    ----------
    op_func: str
        Comparison operation symbol.
        The default symbol if none is found in `value`.

    field_name: str
        Name of the field to extract the value from the dict.

    value: str
        Can contain a comparison operation, e.g.: '< 10'

    Returns
    -------
    comparison: 3-tuple
        Format: (operation symbol, dict field name, value)
    """
    if isinstance(value, (tuple, list)):
        ops   = [_parse_comparison(val, default_op=op_func) for val in value]
        comps = [(op, field_name, val) for op, val in ops]
        return _binary_op('or', comps)
    else:
        op, val = _parse_comparison(value, default_op=op_func)
        return (op, field_name, val)


def _query(op_func, conditions):
    """ Build a list of comparison operations given a sequence
    of conditions.
    Each condition is a triplet with the format: (op_func, field_name, value)
    Parameters
    ----------
    op_func: operator function

    conditions: list of tuples of conditions
        Each condition has the format (field_name, value).
        Where value can be only one value instance or a tuple
        of more than one possible value for the field_name.

    Returns
    -------
    generator of 3-tuples.
    """
    for cond in conditions:
        yield _comparison_op(op_func, cond[0], cond[1])


def build_query(conditions, op_func='and'):
    """ Build a query tree following the list of conditions. """
    return _binary_op(op_func, tuple(_query('==', conditions)))


def _exec_comparison(talk, comp, get=operator.itemgetter):
    return comp_operators[comp[0]](get(comp[1])(talk), comp[2])


def run_query(adict, query, get=operator.itemgetter):
    """ Return True if the given query conditions apply to `adict`."""
    op = query[0]
    if op in comp_operators:
        return _exec_comparison(adict, query)

    elif op in logic_operators:
        return logic_operators[op](run_query(adict, query[1], get=get),
                                   run_query(adict, query[2], get=get))
