/*
 * The Freedom Filled® Pathway Audit · scoring engine v2
 * Base truth: projects/ffb-strategy/pathway-audit/SCORING-MATRIX.md (tracy-harris-co repo)
 * v2 delta (Karl, 2026-06-10): dedicated 5-question FRESH block (Q25-29, one
 * per letter) so FRESH gets a MEASURED health indicator alongside BUILD /
 * SELL / LEAD, with per-letter detail. The 24 business questions, area
 * scoring, bands and the BUILD tie-break are unchanged from v1.
 * FRESH-first routing fires on measured FRESH health (< 45) OR the legacy
 * depletion flags (>= 4). Calibration open until real completions.
 * Nothing numeric is ever shown to the respondent.
 */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) { module.exports = factory(); }
  else { root.AuditEngineV2 = factory(); }
}(typeof self !== 'undefined' ? self : this, function () {

  /* ---------- 9 focus areas ---------- */
  var AREAS = {
    B1: { code: 'B1', domain: 'BUILD', name: 'Clarify your offer' },
    B2: { code: 'B2', domain: 'BUILD', name: 'Tighten your message' },
    B3: { code: 'B3', domain: 'BUILD', name: 'Simplify your business model' },
    S1: { code: 'S1', domain: 'SELL', name: 'Attract the right people' },
    S2: { code: 'S2', domain: 'SELL', name: 'Create a cleaner sales pathway' },
    S3: { code: 'S3', domain: 'SELL', name: 'Improve what is already working' },
    L1: { code: 'L1', domain: 'LEAD', name: 'Strengthen client experience' },
    L2: { code: 'L2', domain: 'LEAD', name: 'Facilitate without overgiving' },
    L3: { code: 'L3', domain: 'LEAD', name: 'Lead with clearer boundaries' }
  };
  var AREA_ORDER = ['B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'L1', 'L2', 'L3'];
  var CLASS_ORDER_BUILD = ['B1', 'B2', 'B3']; // exact-tie order inside BUILD

  /* ---------- 24 scored questions ----------
   * o = options in order a,b,c,d. r = readiness. f = F.R.E.S.H flag.
   * dep = true when the flag is a depletion flag (F/R/S); E and H are support-only.
   */
  var QUESTIONS = [
    { id: 'Q1', area: 'B1', text: 'When someone new lands on your page or profile, how quickly could she tell exactly what you sell and who it’s for?', o: [
      { t: 'She’d have to piece it together. Honestly, I describe it differently almost every time.', r: 0, tags: ['offer_unclear'] },
      { t: 'She’d get the general idea, but I still get “so what exactly do you do?” questions.', r: 1, tags: ['offer_unclear'] },
      { t: 'She’d get it, but the next step after understanding it isn’t obvious.', r: 2, tags: [] },
      { t: 'Fast. The promise, the woman it’s for, and the next step are all right there.', r: 3, tags: ['offer_clear'] }
    ]},
    { id: 'Q2', area: 'B1', text: 'When you explain your offer out loud, what do you find yourself doing?', o: [
      { t: 'Talking about my method, my modules, my process. People nod politely.', r: 0, tags: ['selling_the_method'] },
      { t: 'Listing everything that’s included so it feels like enough.', r: 1, tags: ['inclusion_stacking'] },
      { t: 'Naming the outcome, but still adding a lot of extras to the explanation.', r: 2, tags: [] },
      { t: 'Naming the transformation in a sentence, and then stopping talking.', r: 3, tags: [] }
    ]},
    { id: 'Q3', area: 'B1', text: 'What happens when it’s time to say your price?', o: [
      { t: 'I discount before she even asks, or add bonuses to soften it.', r: 0, tags: ['price_softening'] },
      { t: 'I say it, then talk too much straight after.', r: 1, tags: ['price_softening'] },
      { t: 'I say it cleanly, but I quietly wonder if it’s too much.', r: 2, tags: [] },
      { t: 'I say it plainly. The price matches the depth of the work, and I know it.', r: 3, tags: [] }
    ]},
    { id: 'Q4', area: 'B2', text: 'A stranger at a dinner party asks what you do. What actually comes out?', o: [
      { t: 'A different answer every time, and never as clear as I want it to be.', r: 0, tags: ['one_sentence_fail'] },
      { t: 'The long version. People understand it eventually, with effort.', r: 1, tags: ['one_sentence_fail'] },
      { t: 'A decent sentence, but it doesn’t make the right person lean in yet.', r: 2, tags: [] },
      { t: 'One sentence, the same one every time, and the right woman always wants to know more.', r: 3, tags: [] }
    ]},
    { id: 'Q5', area: 'B2', text: 'Where does your content actually start each time you create?', o: [
      { t: 'A blank page. I re-decide what to say, who it’s for, and how to say it, every single time.', r: 0, tags: ['blank_page_content', 'content_treadmill'] },
      { t: 'Themes I circle back to, but no real message I’m known for.', r: 1, tags: [] },
      { t: 'A core message I mostly hold, though I drift from it when I’m tired.', r: 2, tags: [] },
      { t: 'One clear message my content keeps repeating in fresh ways, on purpose.', r: 3, tags: [] }
    ]},
    { id: 'Q6', area: 'B2', text: 'When it’s time to actually sell, on a call, in the DMs, or on a sales page, what happens?', o: [
      { t: 'I freeze, soften it, or find a reason to avoid the moment altogether.', r: 0, tags: ['selling_freeze'] },
      { t: 'I get the invitation out, but it sounds apologetic, even to me.', r: 1, tags: ['selling_freeze'] },
      { t: 'I can sell, but I lean on discounts or extras to get to yes.', r: 2, tags: ['price_softening'] },
      { t: 'I invite clearly and warmly, and I’m comfortable in the pause that follows.', r: 3, tags: [] }
    ]},
    { id: 'Q7', area: 'B3', text: 'Be honest: how many things are you selling and delivering right now?', o: [
      { t: 'Too many. Different offers, custom versions, one-off projects, all needing me.', r: 0, tags: ['too_many_offers'] },
      { t: 'A main offer plus several side things that each want their own attention.', r: 1, tags: ['too_many_offers'] },
      { t: 'One or two core offers, but the delivery still has too many moving parts.', r: 2, tags: [] },
      { t: 'A simple model. One core pathway, and everything else feeds it.', r: 3, tags: [] }
    ]},
    { id: 'Q8', area: 'B3', text: 'If you mapped how your money arrives against the hours it costs you, what would you see?', o: [
      { t: 'Almost everything is tied to my live hours. More income means more of me.', r: 0, tags: ['time_for_money'] },
      { t: 'Some of it is packaged, but the biggest income still needs me in the room.', r: 1, tags: ['time_for_money'] },
      { t: 'The model mostly works, but a few offers quietly eat more time than they pay for.', r: 2, tags: [] },
      { t: 'The model gives me margin and time. My income isn’t chained to my calendar.', r: 3, tags: [] }
    ]},
    { id: 'Q9', area: 'S1', text: 'Who is actually arriving in your world right now: your DMs, your enquiries, your list?', o: [
      { t: 'Mostly crickets. Not many new people are finding me at all.', r: 0, tags: ['visibility_crickets'] },
      { t: 'People arrive, but they’re often not the right fit, or not ready to invest.', r: 1, tags: ['wrong_fit_leads'] },
      { t: 'Right-fit women show up, but not consistently enough to count on.', r: 2, tags: [] },
      { t: 'Right-fit women arrive steadily, and they often quote my message back to me.', r: 3, tags: [] }
    ]},
    { id: 'Q10', area: 'S1', text: 'What would happen to your business if you stopped posting for two weeks?', o: [
      { t: 'It would go quiet. The business only moves when I’m posting, daily.', r: 0, tags: ['content_treadmill'] },
      { t: 'Things would slow right down. Most of my visibility is me, live, every day.', r: 1, tags: ['content_treadmill'] },
      { t: 'It would dip, but email, referrals or evergreen content would keep things moving.', r: 2, tags: [] },
      { t: 'Honestly, not much. Demand doesn’t depend on me posting every day.', r: 3, tags: [] }
    ]},
    { id: 'Q11', area: 'S1', text: 'How would you describe where your new people come from?', o: [
      { t: 'I’m a bit of everywhere, doing all the platforms, and none of it feels strategic.', r: 0, tags: ['spread_thin'], f: 'H', dep: false },
      { t: 'Mostly one platform, but I show up reactively, usually when the guilt kicks in.', r: 1, tags: [] },
      { t: 'One or two channels I work on purpose, though the rhythm slips.', r: 2, tags: [] },
      { t: 'Focused channels with a repeatable rhythm, and I know which one converts.', r: 3, tags: [] }
    ]},
    { id: 'Q12', area: 'S2', text: 'When a woman is interested but not ready to buy, what happens to her?', o: [
      { t: 'She usually drifts away, unless she happens to keep following me.', r: 0, tags: ['no_capture'] },
      { t: 'I sometimes invite her to my list or a freebie, but it’s ad hoc.', r: 1, tags: [] },
      { t: 'There’s a next step for her, but it needs tightening.', r: 2, tags: [] },
      { t: 'She lands somewhere on purpose, and I can follow up with context later.', r: 3, tags: [] }
    ]},
    { id: 'Q13', area: 'S2', text: 'Someone raises her hand: a reply, a DM, a “tell me more.” What does your follow-up actually look like?', o: [
      { t: 'I often don’t follow up. It feels pushy, so the moment passes.', r: 0, tags: ['followup_avoidance'] },
      { t: 'I follow up when I remember, or when I feel brave that day.', r: 1, tags: ['followup_avoidance'] },
      { t: 'There’s a loose rhythm, but warm conversations still slip through.', r: 2, tags: [] },
      { t: 'There’s a clear, kind follow-up path, and I lead it without apology.', r: 3, tags: [] }
    ]},
    { id: 'Q14', area: 'S2', text: 'If a ready-to-buy woman appeared today, how obvious is her next step?', o: [
      { t: 'She’d have to DM me and ask. There’s no visible doorway.', r: 0, tags: ['no_visible_doorway'] },
      { t: 'There’s a way in, but she’d have to hunt for it.', r: 1, tags: [] },
      { t: 'The step exists and works, but it could be more direct.', r: 2, tags: [] },
      { t: 'It’s obvious. She could move from interested to enrolled without confusion.', r: 3, tags: [] }
    ]},
    { id: 'Q15', area: 'S3', text: 'How well do you know what’s actually working in your business right now?', o: [
      { t: 'I honestly couldn’t say. I’m going off feel, and hope.', r: 0, tags: ['flying_blind'] },
      { t: 'I check things occasionally, usually after something disappoints me.', r: 1, tags: [] },
      { t: 'I watch a few numbers, but I don’t always act on what they’re telling me.', r: 2, tags: [] },
      { t: 'I know my handful of numbers, and they shape what I do next.', r: 3, tags: [] }
    ]},
    { id: 'Q16', area: 'S3', text: 'After a launch or a promotion, what do you usually do next?', o: [
      { t: 'Scrap it and try something completely different. Clearly that one didn’t work.', r: 0, tags: ['reinvention_loop'] },
      { t: 'Take a long recovery break, then start mostly from scratch.', r: 1, tags: [], f: 'F', dep: true },
      { t: 'Repeat the parts I remember working, but I don’t review it properly.', r: 2, tags: [] },
      { t: 'Review it, keep what worked, fix one thing, and run it again better.', r: 3, tags: [] }
    ]},
    { id: 'Q17', area: 'L1', text: 'How consistent is the experience your clients get, from their first yes to the finish?', o: [
      { t: 'It depends on my week. Every client gets a slightly different version of me.', r: 0, tags: ['inconsistent_delivery'], f: 'E', dep: false },
      { t: 'The big pieces are there, but a lot of it still lives in my head.', r: 1, tags: [] },
      { t: 'It’s documented and mostly consistent, with a few gaps I keep meaning to fix.', r: 2, tags: [] },
      { t: 'It’s a designed experience. Any client, any month, gets the same quality.', r: 3, tags: [] }
    ]},
    { id: 'Q18', area: 'L1', text: 'When your clients get results, what happens to those wins?', o: [
      { t: 'They mostly live in my DMs and my memory.', r: 0, tags: ['proof_invisible'] },
      { t: 'I screenshot them and mean to use them, but rarely do.', r: 1, tags: ['proof_invisible'] },
      { t: 'I share them sometimes, but not in a way that helps a buyer decide.', r: 2, tags: [] },
      { t: 'Wins are captured and woven into my content, my pages, and my invitations.', r: 3, tags: [] }
    ]},
    { id: 'Q19', area: 'L2', text: 'Look honestly at everything you give your clients. How much of it was actually part of the offer?', o: [
      { t: 'There’s a lot of unpaid extra in there: voice notes, extensions, just-this-once favours.', r: 0, tags: ['overgiving'], f: 'S', dep: true },
      { t: 'I add extras whenever someone seems wobbly. It’s how I keep them happy.', r: 1, tags: ['overgiving'] },
      { t: 'Mostly contained, though scope creeps in busy seasons.', r: 2, tags: [] },
      { t: 'The offer has clear edges. Generosity happens inside them, by design.', r: 3, tags: [] }
    ]},
    { id: 'Q20', area: 'L2', text: 'How do you feel at the end of a delivery-heavy week?', o: [
      { t: 'Emptied out. It takes most of the weekend to recover, and Monday comes anyway.', r: 0, tags: ['under_supported'], f: 'F', dep: true },
      { t: 'Proud but flattened. The cost is higher than anyone around me realises.', r: 1, tags: ['under_supported'], f: 'F', dep: true },
      { t: 'Tired in a normal way. A few parts drain me more than they should.', r: 2, tags: [] },
      { t: 'Satisfied. The way I deliver protects my energy as well as their results.', r: 3, tags: [] }
    ]},
    { id: 'Q21', area: 'L2', text: 'If you stepped right back for two full weeks, no laptop, what would happen?', o: [
      { t: 'Things would break. Everything routes through me: delivery, decisions, replies, rescues.', r: 0, tags: ['under_supported', 'business_depends_on_me'] },
      { t: 'Clients would cope, but I’d come back to a mess and a guilty inbox.', r: 1, tags: [] },
      { t: 'Most things would hold. A few founder-only knots would wait for me.', r: 2, tags: [] },
      { t: 'The business would hold. Support and systems carry it while I’m gone.', r: 3, tags: [] }
    ]},
    { id: 'Q22', area: 'L3', text: 'Where does your business currently spill into your life?', o: [
      { t: 'Evenings, weekends, holidays, my head at the dinner table. It’s always on.', r: 0, tags: ['always_on'], f: 'R', dep: true },
      { t: 'I hold the line until pressure rises, then family time is the first thing traded.', r: 1, tags: [], f: 'R', dep: true },
      { t: 'Mostly contained, with predictable busy-season spills I’d like to close.', r: 2, tags: [] },
      { t: 'Work lives inside its hours. My family gets me, not what’s left of me.', r: 3, tags: [] }
    ]},
    { id: 'Q23', area: 'L3', text: 'How do decisions actually get made in your business?', o: [
      { t: 'They pile up until pressure forces them, usually late, usually under stress.', r: 0, tags: ['decision_fatigue'], f: 'S', dep: true },
      { t: 'Reactively. Whatever is loudest gets decided first.', r: 1, tags: ['decision_fatigue'] },
      { t: 'I have a loose weekly rhythm for priorities, though it slips.', r: 2, tags: [] },
      { t: 'There’s a clear rhythm: numbers, priorities and capacity, reviewed on purpose.', r: 3, tags: [] }
    ]},
    { id: 'Q24', area: 'RG', text: 'Last one, and it’s the honest one. If the right support and a clear plan were in front of you, what would you actually do?', o: [
      { t: 'I’d hesitate. Between money, time and energy, this isn’t a season where I can take something on.', r: 0, tags: ['not_ready_season'], f: 'F', dep: true },
      { t: 'I’d want it, but I’d probably talk myself out of it. I’ve bought things before and not finished them.', r: 1, tags: ['course_graveyard'] },
      { t: 'I’d take it seriously. I’m done trying to piece this together on my own.', r: 2, tags: ['ready_for_support'] },
      { t: 'I’d move. I’ve been waiting for the clear next step, not for motivation.', r: 3, tags: ['ready_now'] }
    ]}
  ];

  /* ---------- v2: the FRESH block (Q25-29, one per letter) ----------
   * Same observable-behaviour format. Scored into a FRESH domain health
   * indicator + per-letter detail. Never feeds the 9 business areas,
   * never competes for the primary focus.
   */
  var FRESH_QUESTIONS = [
    { id: 'Q25', letter: 'F', text: 'Your energy, honestly. What’s the pattern most weeks?', o: [
      { t: 'I’m running on fumes. Coffee in, willpower out, flat by Friday.', r: 0 },
      { t: 'I get through, but the tank never quite refills before Monday asks again.', r: 1 },
      { t: 'Mostly okay, with rough patches I can usually see coming.', r: 2 },
      { t: 'I treat my energy like it matters. Sleep, movement and rest are part of the plan.', r: 3 }
    ]},
    { id: 'Q26', letter: 'R', text: 'When you’re with the people you love, where are you really?', o: [
      { t: 'Half there. The business is always running in my head, and they can tell.', r: 0 },
      { t: 'Present until something pings. Then I’m gone, even if I’m still in the room.', r: 1 },
      { t: 'Mostly there. Busy seasons pull me away more than I’d like.', r: 2 },
      { t: 'There. When I close the laptop it stays closed, and they get all of me.', r: 3 }
    ]},
    { id: 'Q27', letter: 'E', text: 'The space you work in, physical and digital. What does it feel like?', o: [
      { t: 'Chaos. Piles, tabs, notifications, and nowhere that feels calm to sit.', r: 0 },
      { t: 'Functional but cluttered. I work around the mess more than in a system.', r: 1 },
      { t: 'Decent. A few corners need sorting, but it mostly supports me.', r: 2 },
      { t: 'Calm and set up on purpose. My space makes the work easier, not harder.', r: 3 }
    ]},
    { id: 'Q28', letter: 'S', text: 'Look at your calendar for the next two weeks. Where are YOU in it?', o: [
      { t: 'Nowhere. Every block belongs to clients, kids or the business.', r: 0 },
      { t: 'Pencilled in, and always the first thing traded when something comes up.', r: 1 },
      { t: 'There in small ways: a walk, a coffee, the odd morning off.', r: 2 },
      { t: 'Booked like it’s non-negotiable, because it is. My rhythm holds.', r: 3 }
    ]},
    { id: 'Q29', letter: 'H', text: 'When you sit down to work, what does that time actually look like?', o: [
      { t: 'Scattered. A bit of everything, lots of switching, not much finished.', r: 0 },
      { t: 'Busy all day, but the needle-moving work keeps sliding to tomorrow.', r: 1 },
      { t: 'Focused in bursts. Good days and scattered days about even.', r: 2 },
      { t: 'Focused hours on the few things that matter. Busy isn’t the goal, progress is.', r: 3 }
    ]}
  ];

  var FRESH_LABELS = {
    F: 'Protect your energy and health',
    R: 'Protect the relationships your business is meant to support',
    E: 'Create a calmer working environment',
    S: 'Put yourself back into the rhythm',
    H: 'Focus your hustle'
  };

  /* ---------- health states ---------- */
  function healthState(norm) {
    if (norm >= 75) return 'strong';
    if (norm >= 45) return 'steady';
    return 'attention';
  }

  /* ---------- primary selection + BUILD tie-break (matrix section 5) ---------- */
  function selectPrimary(scores) {
    // scores: { areaCode: normalised 0-100 }
    var ranked = AREA_ORDER.slice().sort(function (a, b) {
      if (scores[a] !== scores[b]) return scores[a] - scores[b];
      return AREA_ORDER.indexOf(a) - AREA_ORDER.indexOf(b); // stable: class order
    });
    var lowest = ranked[0];
    var primary = lowest;
    if (AREAS[lowest].domain !== 'BUILD') {
      // any BUILD area within 5 internal points of the lowest takes primary;
      // if several qualify, the lowest of them; exact tie inside BUILD = class order
      var candidates = CLASS_ORDER_BUILD.filter(function (b) {
        return scores[b] - scores[lowest] <= 5;
      });
      if (candidates.length) {
        candidates.sort(function (a, b) {
          if (scores[a] !== scores[b]) return scores[a] - scores[b];
          return CLASS_ORDER_BUILD.indexOf(a) - CLASS_ORDER_BUILD.indexOf(b);
        });
        primary = candidates[0];
      }
    }
    var secondaries = ranked.filter(function (a) { return a !== primary; }).slice(0, 2);
    return { primary: primary, secondaries: secondaries, ranked: ranked };
  }

  /* ---------- route logic (matrix section 7, priority order, first match wins)
   * v2: FRESH-first now fires on measured FRESH health (< 45, i.e. the
   * Needs-attention threshold) OR the legacy depletion flags (>= 4). ---------- */
  function selectRoute(R, NA, q24, DF, q1IsA, q7IsA, freshScore) {
    if (freshScore < 45 || DF >= 4) return 'fresh';
    if (R < 35 || (q1IsA && q7IsA && R < 45)) return 'nurture';
    if (R >= 60 && q24 >= 2 && NA <= 4) return 'ffb';
    return 'workshop';
  }

  /* ---------- band ---------- */
  function selectBand(R) {
    if (R >= 80) return 'leadership';
    if (R >= 60) return 'refinement';
    if (R >= 35) return 'momentum';
    return 'foundation';
  }

  /* ---------- F.R.E.S.H dominant letter (tie: F > R > S > E > H) ---------- */
  var LETTER_PRIORITY = ['F', 'R', 'S', 'E', 'H'];
  function dominantLetter(counts) {
    var best = null;
    LETTER_PRIORITY.forEach(function (L) {
      if (!counts[L]) return;
      if (best === null || counts[L] > counts[best]) best = L;
    });
    return best;
  }

  /* ---------- full computation ----------
   * answers: array of 29 option indices (0-3): 24 business questions in
   * matrix order, then the 5 FRESH questions (F, R, E, S, H).
   */
  function compute(answers) {
    var raw = {}, max = {}, tags = [], letters = {}, DF = 0;
    AREA_ORDER.forEach(function (a) { raw[a] = 0; max[a] = 0; });

    var rTotal = 0;
    QUESTIONS.forEach(function (q, i) {
      var opt = q.o[answers[i]];
      rTotal += opt.r;
      if (q.area !== 'RG') { raw[q.area] += opt.r; max[q.area] += 3; }
      opt.tags.forEach(function (t) { tags.push(t); });
      if (opt.f) {
        letters[opt.f] = (letters[opt.f] || 0) + 1;
        if (opt.dep) DF += 1;
      }
    });

    var scores = {}, states = {};
    AREA_ORDER.forEach(function (a) {
      scores[a] = Math.round(raw[a] / max[a] * 100);
      states[a] = healthState(scores[a]);
    });

    // v2: measured FRESH block (per-letter 0-3 + domain health 0-100)
    var letterScores = {}, freshRaw = 0;
    FRESH_QUESTIONS.forEach(function (q, i) {
      var r = q.o[answers[24 + i]].r;
      letterScores[q.letter] = r;
      freshRaw += r;
    });
    var freshScore = Math.round(freshRaw / 15 * 100);
    var freshState = healthState(freshScore);
    // support label = the letter she scored lowest on (tie: F > R > S > E > H)
    var supportLetter = LETTER_PRIORITY.slice().sort(function (a, b) {
      if (letterScores[a] !== letterScores[b]) return letterScores[a] - letterScores[b];
      return LETTER_PRIORITY.indexOf(a) - LETTER_PRIORITY.indexOf(b);
    })[0];

    // v2: domain health indicators (BUILD / SELL / LEAD from their questions, FRESH measured)
    var domainScores = { BUILD: 0, SELL: 0, LEAD: 0, FRESH: freshScore };
    var domRaw = { BUILD: 0, SELL: 0, LEAD: 0 }, domMax = { BUILD: 0, SELL: 0, LEAD: 0 };
    AREA_ORDER.forEach(function (a) {
      domRaw[AREAS[a].domain] += raw[a];
      domMax[AREAS[a].domain] += max[a];
    });
    ['BUILD', 'SELL', 'LEAD'].forEach(function (d) {
      domainScores[d] = Math.round(domRaw[d] / domMax[d] * 100);
    });
    var domainStates = {};
    Object.keys(domainScores).forEach(function (d) { domainStates[d] = healthState(domainScores[d]); });

    var R = Math.round(rTotal / 72 * 100);
    var NA = AREA_ORDER.filter(function (a) { return states[a] === 'attention'; }).length;
    var sel = selectPrimary(scores);
    var q24 = QUESTIONS[23].o[answers[23]].r;
    var route = selectRoute(R, NA, q24, DF, answers[0] === 0, answers[6] === 0, freshScore);
    var band = selectBand(R);

    // F.R.E.S.H signal level: measured health first, legacy flags as backstop
    var freshLevel = (freshScore < 45 || DF >= 4) ? 'first'
      : ((freshScore < 75 || DF >= 2) ? 'elevated' : 'quiet');

    // MDM trigger: B2 in Needs attention AND >= 2 distinct of the 3 messaging tags fired
    var mdmTags = ['one_sentence_fail', 'selling_freeze', 'blank_page_content'].filter(function (t) {
      return tags.indexOf(t) !== -1;
    });
    var mdmFit = states.B2 === 'attention' && mdmTags.length >= 2;

    var strengths = AREA_ORDER.filter(function (a) { return states[a] === 'strong'; });
    var allStrong = strengths.length === 9;

    // AC tags this result would write (matrix section 9)
    var slug = function (code) { return AREAS[code].name.toLowerCase().replace(/[^a-z0-9]+/g, '_'); };
    var acTags = ['quiz_audit_completed', 'quiz_audit_band_' + band, 'quiz_audit_route_' + route,
      'quiz_audit_area_primary_' + slug(sel.primary)];
    if (DF >= 2) acTags.push('quiz_audit_fresh_support');
    if (mdmFit) acTags.push('quiz_audit_mdm_fit');
    tags.filter(function (t, i) { return tags.indexOf(t) === i; }).forEach(function (t) {
      acTags.push('quiz_audit_tag_' + t);
    });

    return {
      scores: scores, states: states, R: R, NA: NA, band: band, route: route,
      primary: sel.primary, secondaries: sel.secondaries, ranked: sel.ranked,
      strengths: strengths, allStrong: allStrong,
      domainScores: domainScores, domainStates: domainStates,
      freshScore: freshScore, freshState: freshState,
      letterScores: letterScores, supportLetter: supportLetter,
      supportLabel: FRESH_LABELS[supportLetter],
      freshLevel: freshLevel, depletionCount: DF, letters: letters,
      dominantLetter: dominantLetter(letters), q24: q24,
      tags: tags.filter(function (t, i) { return tags.indexOf(t) === i; }),
      mdmFit: mdmFit, acTags: acTags
    };
  }

  return {
    AREAS: AREAS, AREA_ORDER: AREA_ORDER, QUESTIONS: QUESTIONS,
    FRESH_QUESTIONS: FRESH_QUESTIONS, FRESH_LABELS: FRESH_LABELS,
    compute: compute, healthState: healthState,
    selectPrimary: selectPrimary, selectRoute: selectRoute, selectBand: selectBand
  };
}));
