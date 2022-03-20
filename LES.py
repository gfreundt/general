from tqdm import tqdm


def solve(*equations):
    terms = [aggregate_terms(break_terms(i)) for i in equations]
    vars = list(set([k for j in [get_unique_variables(i) for i in terms] for k in j]))
    vars = {i: 0 for i in vars if i != ""}
    print(vars)

    response = iterate_options(
        terms, n=30, vars=vars, depth=0, max_depth=len(vars), response=[]
    )
    """
    if not response:
        response = iterate_options(
            terms, n=1000, vars=vars, depth=0, max_depth=len(vars), response=[]
        )
    """
    return terms, response


def break_terms(equation):
    def split_terms(equation):
        term_split_pos = (
            [0]
            + [k for k, i in enumerate(equation) if i in "+-" and k > 0]
            + [len(equation) + 1]
        )
        terms = [
            equation[term_split_pos[k] : term_split_pos[k + 1]]
            for k in range(0, len(term_split_pos) - 1)
        ]
        terms = [i if ("-" in i or "+" in i) else "+" + i for i in terms]
        return terms

    def invert_signs(terms):
        inverted = []
        for term in terms:
            term = term.replace("+", "@")
            term = term.replace("-", "+")
            term = term.replace("@", "-")
            inverted.append(term)
        return inverted

    def to_dict(term):
        p = 0
        while True and p < len(term):
            if not (term[p].isdigit() or term[p] in "+-"):
                break
            else:
                p += 1
        if p == 1:  # no coefficient (implicit 1)
            term = term[0] + "1" + term[1:]
            p = 2
        return {"coefficient": int(term[:p]), "variable": term[p:]}

    left, right = equation.split("=")
    terms = split_terms(left) + invert_signs(split_terms(right))
    terms = [to_dict(term) for term in terms]

    return terms


def aggregate_terms(term):
    result = []
    for var in get_unique_variables(term):
        agg = sum([i["coefficient"] for i in term if i["variable"] == var])
        result.append({"coefficient": agg, "variable": var})
    return result


def get_unique_variables(terms):
    d = [i["variable"] for i in terms]
    return sorted(list(set(d)))


def iterate_options(terms, n, vars, depth, max_depth, response):

    # print(f"{vars=}")

    if depth >= max_depth:
        return response

    for next in range(-n, n):
        vars.update({[i for i in vars.keys()][depth]: next})
        if evaluate_for_zero(terms, vars):
            print("*********", vars)
            response.append(vars)
        else:
            iterate_options(terms, n, vars, depth + 1, max_depth, response)


def evaluate_for_zero(terms, varvals):
    varvals.update({"": 1})
    for term in terms:
        evaluation = 0
        for t in term:
            evaluation += t["coefficient"] * varvals[t["variable"]]
        if evaluation != 0:
            return False
    return True


print(solve("2beta+8y=4", "-7beta+4y-9p=14"))  # , {"x": -6.0, "y": 2.0})

"""   
    @test.it('Long variable names')
    def b():
        tester(solve("2alpha+8beta=4", "-alpha+4beta=14"), {'alpha':-6.0, 'beta':2.0})
        
        
    @test.it('Right hand variable')
    def b():
        tester(solve("2x=8y", "x+y=5"), {'x':4.0, 'y':1.0})
        
        
    @test.it('Solvable with repeated equations')
    def b():
        tester(solve("x=4y", "2x=8y", "x+y=5"), {'x':4.0, 'y':1.0})
        
        
    @test.it('Zero as solution')
    def b():
        tester(solve("x+y=7z-1", "6x+z=-3y", "4y+10z=-8x"), {'x':1, 'y':-2, 'z': 0})

a = solve("2x+4y+6z=18", "3y+3z=6", "x+2y=z-3")

for i in a:
    print(i)
"""
