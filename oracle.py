import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def pattern_plan(throwsArr):
    n = len(throwsArr)
    if n == 0:
        return {"error": "the pattern needs at least one throw"}
    for t in throwsArr:
        if not (t >= 1) or t != math.floor(t) or t > 9:
            return {"error": "every throw must be a whole number from 1 to 9"}
    avg = sum(throwsArr) / n
    if avg != math.floor(avg):
        return {"error": "the throws average " + fmt(round1(avg)) + ", not a whole ball count"}
    seen = set()
    for i, t in enumerate(throwsArr):
        land = (t + i) % n
        if land in seen:
            return {"error": "two throws share a landing beat - this pattern collides"}
        seen.add(land)
    avg = int(avg)
    if avg <= 3: verdict = "a starting pattern"
    elif avg <= 5: verdict = "a working pattern"
    else: verdict = "a numbers act"
    return {"balls": avg, "beats": n, "verdict": verdict}

def throw_plan(throwVal, beatMs):
    if not (throwVal >= 1) or throwVal != math.floor(throwVal) or throwVal > 9:
        return {"error": "the throw must be a whole number from 1 to 9"}
    if not (beatMs > 0):
        return {"error": "the labeled beat must be positive"}
    airS = round1(throwVal * beatMs / 1000)
    apexCm = math.floor(9.81 * ((throwVal * beatMs / 1000) / 2) ** 2 / 2 * 100 + 0.5)
    if apexCm < 60: verdict = "a knee-high toss"
    elif apexCm < 250: verdict = "a head-high arc"
    else: verdict = "a ceiling tester"
    return {"airS": airS, "apexCm": apexCm, "verdict": verdict}

def tempo_plan(beatMs, hands):
    if not (beatMs > 0):
        return {"error": "the labeled beat must be positive"}
    if not (hands >= 1) or hands != math.floor(hands):
        return {"error": "the hands must be a whole number, one or more"}
    throwsPerMin = round1(60000 / beatMs)
    perHand = round1(60000 / beatMs / hands)
    if beatMs >= 600: verdict = "a lazy tempo"
    elif beatMs >= 350: verdict = "a working tempo"
    else: verdict = "a blur"
    return {"throwsPerMin": throwsPerMin, "perHand": perHand, "verdict": verdict}

def render_pattern(r, throwsArr):
    return ("A pattern " + " ".join(fmt(t) for t in throwsArr) + " over " + plural(r["beats"], "beat") + " juggles "
            + plural(r["balls"], "ball") + ", every throw landing on its own beat - " + r["verdict"] + ".")

def render_throw(r, throwVal, beatMs):
    return ("A " + fmt(throwVal) + "-throw at a labeled " + fmt(beatMs) + " ms beat stays up " + fmt(r["airS"])
            + " s and tops out at " + fmt(r["apexCm"]) + " cm - " + r["verdict"] + ".")

def render_tempo(r, beatMs, hands):
    return ("A labeled " + fmt(beatMs) + " ms beat runs " + plural(r["throwsPerMin"], "throw") + " a minute, "
            + fmt(r["perHand"]) + " a hand - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[[3]],[[5,3,1]],[[4,4,1]],[[7,4,4]],[[9,9,9,9]],[[4,4]],[[7,3]],[[1,2,3]],[[5,1,3]],[[4,4,2]],[[]],[[5,0,1]],[[5,10,1]]]:
    add("patternPlan", pattern_plan, render_pattern, a)
for a in [[5,400],[3,400],[1,400],[7,500],[0,400],[3,0],[10,400],[5,350],[2,600]]:
    add("throwPlan", throw_plan, render_throw, a)
for a in [[400,2],[600,2],[250,2],[0,2],[500,1],[350,2],[700,1],[450,2]]:
    add("tempoPlan", tempo_plan, render_tempo, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
