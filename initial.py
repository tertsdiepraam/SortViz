import random
import math

def randomized(n, m):
    return [random.randint(1, n+1) for _ in range(m)]

def shuffled(n, m):
    listy = ascending(n, m)
    random.shuffle(listy)
    return listy

def ascending(n, m):
    return [i*n//m for i in range(1,m+1)]

def descending(n, m):
    listy = ascending(n, m)
    listy.reverse()
    return listy

def perlin(n, m):
    def interpolate(pa, pb, px):
        ft = px * math.pi
        f = (1 - math.cos(ft)) * 0.5
        return pa * (1 - f) + pb * f
    
    def octave(amp, wl):
        a = random.random() - 0.5
        b = random.random() - 0.5
        for x in range(m):
            if x % wl == 0:
                a = b
                b = random.random() - 0.5
                yield a * amp
            else:
                yield interpolate(a, b, (x % wl) / wl) * amp
    
    def bound(x, min, max):
        if x < min:
            return min
        elif x > max:
            return max
        else:
            return x

    amp = n*0.8
    wl  = 128
    octaves = zip(*(octave(amp//2**i, wl//2**i) for i in range(8)))
    return [bound(n//2 + int(sum(x)), 0, n) for x in octaves]
    