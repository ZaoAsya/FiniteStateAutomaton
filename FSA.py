from itertools import product


ways = {}


def get_conditions_set(v: set):
    """Генерирует множество состояний, в которое перейдет множество v по буквам 0 и 1"""
    return {ways[t][0] for t in v}, {ways[t][1] for t in v}


def create_result(word: str):
    """Вывод синхронизируемых автоматов с их синхрословами"""
    print("\nSuccess!")
    res = 'length:' + str(len(word)) + ' word:' + word + ' config:' + str(ways) + '\n'
    print(res)
    if len(word) >= 10:
        with open("big_words.txt", 'a') as f:
            f.write(res)


def get_automaton_config():
    """Генератор всевозможных автоматов с 0 |Q|=6 |Alf|=2"""
    print("Creating automaton configurations...\n")
    v1 = [a for a in product([1], [0, 1, 2, 3, 4, 5])]
    v1 = [a for a in product(v1, [0, 1, 2, 3, 4, 5])]
    v2 = [a for a in product([2], [0, 1, 2, 3, 4, 5])]
    v2 = [a for a in product(v2, [0, 1, 2, 3, 4, 5])]
    v3 = [a for a in product([3], [0, 1, 2, 3, 4, 5])]
    v3 = [a for a in product(v3, [0, 1, 2, 3, 4, 5])]
    v4 = [a for a in product([4], [0, 1, 2, 3, 4, 5])]
    v4 = [a for a in product(v4, [0, 1, 2, 3, 4, 5])]
    v5 = [a for a in product([5], [0, 1, 2, 3, 4, 5])]
    v5 = [a for a in product(v5, [0, 1, 2, 3, 4, 5])]
    vars = []
    for t1 in v1:
        for t2 in v2:
            for t3 in v3:
                for t4 in v4:
                    for t5 in v5:
                        var = get_var_config([((0, 0), 0), t1, t2, t3, t4, t5])
                        if is_coherent(var):
                            vars.append(var)
    print("\nPossible automaton configurations created!\n")
    return vars


def get_var_config(points):
    """Из списка ((*,*),*) делает словарь переходов"""
    return {c[0][0]: {0: c[0][1], 1: c[1]} for c in points}


def is_coherent(var: dict):
    """Нет ли петель, достижима ли каждая из вершин откуда-либо
    var = {cond1: {0: cond10, 1: cond11}, ...}"""
    pred = set()
    for k, v in var.items():
        if v[0] == v[1] == k != 0:
            return False
        if k != 0:
            pred.add(v[0])
            pred.add(v[1])
    return pred == {0, 1, 2, 3, 4, 5}


def find_synchronising_automatons():

    def bfs(cond_word, finish: bool):
        """cond_word = (cond: set, word: str)"""
        if finish:
            return
        if cond_word[0] in cond_set:
            return
        cond_set.append(cond_word[0])
        new_cond_0, new_cond_1 = get_conditions_set(cond_word[0])
        if new_cond_0 == {0}:
            finish = True
            create_result(cond_word[1] + '0')
        elif new_cond_0 not in cond_set:
            queue.append((new_cond_0, cond_word[1] + '0'))
        if new_cond_1 == {0}:
            finish = True
            create_result(cond_word[1] + '1')
        elif new_cond_1 not in cond_set:
            queue.append((new_cond_1, cond_word[1] + '1'))
        while queue:
            bfs(queue.pop(0), finish)

    vars = get_automaton_config()
    for var in vars:
        global ways
        ways = var
        cond_set = []
        queue = []
        bfs(({0, 1, 2, 3, 4, 5}, ""), False)


if __name__ == "__main__":
    find_synchronising_automatons()
