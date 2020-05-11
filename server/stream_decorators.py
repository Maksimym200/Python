from contextlib import contextmanager

@contextmanager
def open_input(i):
    if i == None:
        yield stdin
    else:
        with open(i, "r") as input:
            yield input

@contextmanager
def open_output(o):
    if o == None:
        yield stdout
    else:
        with open(o, "w") as output:
            yield output

