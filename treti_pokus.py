from config import board_size, moves
from random import shuffle


def generate_moves(pos, obstacles, random=False):
    if random:  # aby se nezačínalo vždy krokem doprava, ale krokem náhodným směrem - heuristika
        shuffle(moves)

    posx, posy = pos[0]
    for x, y in moves:
        nextposx = posx + x
        nextposy = posy + y
        if 0 <= nextposx < board_size and 0 <= nextposy < board_size:  # ošetření aby nova pozice nebyla mimo šachovnici
            if (nextposx, nextposy) not in pos[1]:  # aby se nemohl byt další krok na již navštívené políčko
                if not obstacles[nextposy][nextposx]:  # pokud neni obstacle
                    yield nextposx, nextposy  # TADY JSEM POUZIL GENERATOR MEGA KUL


def find_path(obstacles, start_pos, end_pos, break_at_first=False, random=False):
    done = False

    """tady ta funkce vygeneruje vsechny mozne dalsi pohyby do dalsiho listu
     a ten pak cely zkontroluje a while cyklus pripadne skonci az potom takze to najde vsechny cesty ktere jsou stejne
      kratke jako cesta, 
    ktera, protoze vime, ze tohle je BFS, vime, ze je nejkratsi
    jestli je break at first true tak to moc casu neusetri protoze stejne prohledavame do sirky ale 
    jakmile to najde jednu cestu tak uz se neobtezuje"""

    states = [(start_pos, [])]  # state je vzdycky tupl aktualni pozice a listu minulych pozic (cesty)
    finalstates = []
    while not done:
        newstates = []
        for state in states:
            for newpos in generate_moves(state, obstacles, random=random):
                if newpos not in state[1]:
                    path = state[1][:]
                    path.append(state[0])
                    if break_at_first:
                        if newpos == end_pos:
                            return [[newpos, path]]
                    newstates.append((newpos, path))

        states = newstates[:]
        for state in states:
            if state[0] == end_pos:
                finalstates.append(state)
                done = True

    print(f"found {len(finalstates)}")
    return finalstates

