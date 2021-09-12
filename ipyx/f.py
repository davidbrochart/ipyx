from .x import X, make_x


class F:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        inputs = [make_x(i) for i in args]
        kwinputs = {k: make_x(i) for k, i in kwargs.items()}
        operation = (
            "self.v = self._function(*(i.v for i in self._inputs), "
            "**{k: i.v for k, i in self._kwinputs.items()})"
        )
        x = X(
            _inputs=inputs, _kwinputs=kwinputs, _operation=operation, _function=self.f
        )
        x._compute()
        for i in inputs:
            i._outputs.append(x)
        for i in kwinputs.values():
            i._outputs.append(x)
        return x
