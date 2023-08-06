# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pattern(Component):
    """A Pattern component.
Pane is a wrapper of Pane in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    A custom class name to assign to the pane. Empty by default.

- name (string; optional):
    The pane name.

- pane (string; optional):
    The leaflet pane of the component.

- style (dict; optional):
    The CSS style of the component (dynamic).

- type (a value equal to: "Pattern", "PatternCircle", "PatternRect", "StripePattern.js"; optional):
    The children of this component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_leaflet'
    _type = 'Pattern'
    @_explicitize_args
    def __init__(self, type=Component.UNDEFINED, name=Component.UNDEFINED, pane=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'name', 'pane', 'style', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'name', 'pane', 'style', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Pattern, self).__init__(**args)
