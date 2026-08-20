import inspect
import warnings


def attach_legacy_names(cls, names, arguments=None):
    """ Add the old method names to a class, forwarding them to their new ones """
    arguments = arguments or {}
    for old_name, new_name in names.items():
        parameters = list(inspect.signature(getattr(cls, new_name)).parameters)[1:]  # self aside
        method = build_legacy_method(old_name, new_name, arguments.get(old_name, {}), parameters)
        setattr(cls, old_name, method)


def build_legacy_method(old_name, new_name, renamed_arguments, parameters):
    """ Build one method warning about its old name then calling the new one """
    def legacy(self, *args, **kwargs):
        warnings.warn("{}() is deprecated, use {}() instead".format(old_name, new_name),
                      DeprecationWarning, stacklevel=2)
        renamed = {}
        for name, value in kwargs.items():
            name = renamed_arguments.get(name, name)
            if name in parameters:  # arguments the new method no longer takes are left out
                renamed[name] = value
        return getattr(self, new_name)(*args[:len(parameters)], **renamed)

    legacy.__name__ = old_name
    legacy.__doc__ = " Deprecated, use {}() instead ".format(new_name)
    return legacy
