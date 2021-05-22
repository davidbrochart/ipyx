from .x import X, make_x


class F:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        inputs = [make_x(i) for i in args]
        operation = "self.v = self._function(*[i.v for i in self._inputs])"
        x = X(_inputs=inputs, _operation=operation, _function=self.f)
        x._compute()
        for i in inputs:
            i._outputs.append(x)
        return x
