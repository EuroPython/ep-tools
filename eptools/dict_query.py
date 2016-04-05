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
                  'has': operator.contains,
                 }

logic_operators = {'and': operator.and_,
                   'or': operator.or_,
                   }


def _binary_op(op_func, comps):
    """ Return a concatenation of operators `op_func` on each pair
    of conditions in `conds`.
    """
    if len(comps) == 1:
        nuop = (op_func, comps[0], True)
    elif len(comps) == 2:
        nuop = (op_func, comps[0], comps[1])
    else:
        frst = comps[0]
        rest = comps[1:]
        nuop = (op_func, frst, _binary_op(op_func, rest))

    return nuop


def _comparison_op(op_func, field_name, value):
    """Create a comparison operation or a 'or' operation if
    len(value) > 1.
    """
    if isinstance(value, (tuple, list)):
        comps = [(op_func, field_name, val) for val in value]
        return _binary_op('or', comps)
    else:
        return (op_func, field_name, value)


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
    """
    for cond in conditions:
        yield _comparison_op(op_func, cond[0], cond[1])


def _exec_comparison(talk, comp):
    return comp_operators[comp[0]](talk[comp[1]], comp[2])


def build_query(conditions, op_func='and'):
    """ Build a query tree following the list of conditions. """
    return _binary_op(op_func, tuple(_query('==', conditions)))


def exec_query(adict, query):
    """ Return True if the given query conditions apply to `adict`."""
    op = query[0]
    if op in comp_operators:
        return _exec_comparison(adict, query)

    elif op in logic_operators:
        return logic_operators[op](exec_query(adict, query[1]),
                                   exec_query(adict, query[2]))
