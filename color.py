class Color(object):
    def __init__(self, r)

def rgb(r, g, b, **kwargs):
    return (r, g, b)

def red(r, **kwargs):
    return rgb(r, 0, 0, **kwargs)

if __name__ == "__main__":
    for x in range(2):
        for t in range(2):
            print(red(r=t, x=x, t=t))

