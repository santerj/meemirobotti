# virtual keyboard and typoer

keyboard_upper = (
    ('§','1','2','3','4','5','6','7','8','9','+'),
    ('Q','W','E','R','T','Y','U','I','O','P','Å'),
    ('A','S','D','F','G','H','J','K','L','Ö','Ä'),
    ('<','Z','X','C','V','B','N','M',',','.','-')
)

keyboard_lower = (
    ('§','1','2','3','4','5','6','7','8','9','+'),
    ('q','w','e','r','t','y','u','i','o','p','å'),
    ('a','s','d','f','g','h','j','k','l','ö','ä'),
    ('<','z','x','c','v','b','n','m',',','.','-')
)

def neigboring_keys(kb):
    # from https://github.com/MaxRudometkin/2d_kbay_neighbours
    neighbors = {}

    for i in range(len(kb)):
        for j, value in enumerate(kb[i]):

            if i == 0 or i == len(kb) - 1 or j == 0 or j == len(kb[i]) - 1:
                # corners
                new_neighbors = []
                if i != 0:
                    new_neighbors.append(kb[i - 1][j])  # top neighbor
                if j != len(kb[i]) - 1:
                    new_neighbors.append(kb[i][j + 1])  # right neighbor
                if i != len(kb) - 1:
                    new_neighbors.append(kb[i + 1][j])  # bottom neighbor
                if j != 0:
                    new_neighbors.append(kb[i][j - 1])  # left neighbor

            else:
                # add neighbors
                new_neighbors = [
                    kb[i - 1][j],  # top neighbor
                    kb[i][j + 1],  # right neighbor
                    kb[i + 1][j],  # bottom neighbor
                    kb[i][j - 1]   # left neighbor
                ]

            neighbors[value] = new_neighbors
                #"value": value,
                #"neighbors": new_neighbors})

    return neighbors