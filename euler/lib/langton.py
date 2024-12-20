class Ant(object):
    """An ant which belongs to a grid of black and white squares. It moves
    one square at a time, turning at each step in a direction determined
    by whether the square it's standing on is black or white."""
    DIRECTIONS = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}

    def __init__(self, G, row, column, direction='N'):
        self.G = G
        self.p = [row, column]
        if direction not in self.DIRECTIONS:
            raise ValueError('Invalid cardinal direction, use N, E, S, or W.')
        self.d = self.DIRECTIONS[direction]
        if not self.on_grid():
            raise IndexError("The ant is not on the grid.")

    def rotate(self, CW=True):
        """Change direction with clockwise or counter-clockwise rotation."""
        if CW:
            self.d[0], self.d[1] = self.d[1], -self.d[0]
        else:
            self.d[0], self.d[1] = -self.d[1], self.d[0]

    def on_grid(self):
        dim = self.G.get_dim()
        return 0 <= self.p[0] < dim and 0 <= self.p[1] < dim

    def move(self):
        self.p[0] += self.d[0]
        self.p[1] += self.d[1]
        if not self.on_grid():
            raise IndexError("The ant is not on the grid.")

    def get_p(self):
        return self.p


class Grid(object):
    """NxN grid of spaces, all initially white.
    An ant moves within this grid."""
    WHITE, BLACK = True, False

    def __init__(self, dim):
        self.dim = dim+1 if dim%2 == 0 else dim
        self.grid = [[self.WHITE for x in range(self.dim)]
            for y in range(self.dim)]
        self.W, self.B = self.dim*self.dim, 0

    def __repr__(self):
        return '\n'.join(
            [''.join(
                ['X' if sq else ' ' for sq in row]
            ) for row in self.grid]) + '\n'

    def flip(self, i, j):
        if self.grid[i][j]:
            self.W -= 1
            self.B += 1
        else:
            self.W += 1
            self.B -= 1
        self.grid[i][j] = not self.grid[i][j]
        assert(self.B+self.W == self.dim*self.dim)

    def get(self, i, j):
        return self.grid[i][j]

    def get_dim(self):
        return self.dim

    def get_center(self):
        return self.dim//2

    def get_B(self):
        return self.B


class LangtonSimulate(object):
    """Returns number of black squares in grid after n steps. This class
    exploits the fact that Langton's ant, when starting on an all-white
    grid, becomes periodic in its movement after ~10000 iterations, with
    a period of 104 moves. The cutoff value can be overriden, but if it
    is too low num_black() will not give accurate results."""
    period = 104

    def __init__(self, grid_size=100, cutoff=11000):
        """Construct B array for the number of black squares. The index of
        each value is the number of steps that have been taken."""
        self.grid_size, self.cutoff = grid_size, cutoff
        self.G = Grid(self.grid_size)
        self.A = Ant(self.G, self.G.get_center(), self.G.get_center())
        self.B = []
        for i in range(self.cutoff+1):
            self.B.append(self.G.get_B())
            self.A.rotate() if self.G.get(*self.A.get_p()) \
                else self.A.rotate(False)
            self.G.flip(*self.A.get_p())
            self.A.move()

    def __repr__(self):
        return self.G.__repr__()

    def num_black(self, n):
        """Return the number of black squares after the ant
        has taken n steps. For values greater than the cutoff,
        this value must be extrapolated."""
        if n < 0:
            raise ValueError('The number of steps must be non-negative')
        B_incr = self.B[self.cutoff] - self.B[self.cutoff-self.period]
        if n <= self.cutoff:
            return self.B[n]
        periods, remaining_steps = divmod(n-self.cutoff, self.period)
        if remaining_steps:
            periods += 1
            remaining_steps = self.period-remaining_steps
        return self.B[self.cutoff-remaining_steps] + periods*B_incr
