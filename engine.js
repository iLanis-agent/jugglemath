(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function patternPlan(throwsArr) {
    var n = throwsArr.length;
    if (n === 0) return { error: "the pattern needs at least one throw" };
    for (var i = 0; i < n; i++) {
      var t = throwsArr[i];
      if (!(t >= 1) || t !== Math.floor(t) || t > 9) return { error: "every throw must be a whole number from 1 to 9" };
    }
    var sum = 0;
    for (i = 0; i < n; i++) sum += throwsArr[i];
    var avg = sum / n;
    if (avg !== Math.floor(avg)) return { error: "the throws average " + round1(avg) + ", not a whole ball count" };
    var seen = {};
    for (i = 0; i < n; i++) {
      var land = (throwsArr[i] + i) % n;
      if (seen[land]) return { error: "two throws share a landing beat - this pattern collides" };
      seen[land] = true;
    }
    var verdict;
    if (avg <= 3) verdict = "a starting pattern";
    else if (avg <= 5) verdict = "a working pattern";
    else verdict = "a numbers act";
    return { balls: avg, beats: n, verdict: verdict };
  }

  function throwPlan(throwVal, beatMs) {
    if (!(throwVal >= 1) || throwVal !== Math.floor(throwVal) || throwVal > 9) return { error: "the throw must be a whole number from 1 to 9" };
    if (!(beatMs > 0)) return { error: "the labeled beat must be positive" };
    var airS = round1(throwVal * beatMs / 1000);
    var apexCm = Math.round(9.81 * Math.pow(throwVal * beatMs / 1000 / 2, 2) / 2 * 100);
    var verdict;
    if (apexCm < 60) verdict = "a knee-high toss";
    else if (apexCm < 250) verdict = "a head-high arc";
    else verdict = "a ceiling tester";
    return { airS: airS, apexCm: apexCm, verdict: verdict };
  }

  function tempoPlan(beatMs, hands) {
    if (!(beatMs > 0)) return { error: "the labeled beat must be positive" };
    if (!(hands >= 1) || hands !== Math.floor(hands)) return { error: "the hands must be a whole number, one or more" };
    var throwsPerMin = round1(60000 / beatMs);
    var perHand = round1(60000 / beatMs / hands);
    var verdict;
    if (beatMs >= 600) verdict = "a lazy tempo";
    else if (beatMs >= 350) verdict = "a working tempo";
    else verdict = "a blur";
    return { throwsPerMin: throwsPerMin, perHand: perHand, verdict: verdict };
  }

  function renderPattern(r, throwsArr) {
    return "A pattern " + throwsArr.join(" ") + " over " + plural(r.beats, "beat") + " juggles " + plural(r.balls, "ball") + ", every throw landing on its own beat - " + r.verdict + ".";
  }

  function renderThrow(r, throwVal, beatMs) {
    return "A " + throwVal + "-throw at a labeled " + beatMs + " ms beat stays up " + r.airS + " s and tops out at " + r.apexCm + " cm - " + r.verdict + ".";
  }

  function renderTempo(r, beatMs, hands) {
    return "A labeled " + beatMs + " ms beat runs " + plural(r.throwsPerMin, "throw") + " a minute, " + r.perHand + " a hand - " + r.verdict + ".";
  }

  var api = { patternPlan: patternPlan, throwPlan: throwPlan, tempoPlan: tempoPlan, renderPattern: renderPattern, renderThrow: renderThrow, renderTempo: renderTempo };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.JuggleMath = api;
})(this);
