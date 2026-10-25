using OpenRA.Mods.Sevenfall;
using AI.Fuzzy.Library;

static void Check(bool condition, string message) { if (!condition) throw new Exception(message); }
var progress = 0;
for (var i = 0; i < 59; i++) progress = DreadRules.Advance(progress, 5, true, false, false);
Check(progress == 295, "Infantry must not convert before twelve seconds.");
progress = DreadRules.Advance(progress, 5, true, false, false);
Check(progress == 300, "Sustained exposure must reach the conversion threshold.");
Check(DreadRules.Advance(300, 5, true, false, false) == 300, "Exposure must be capped.");
Check(DreadRules.Advance(200, 5, false, false, false) == 190, "Retreat must decay dread at twice its growth rate.");
Check(DreadRules.Advance(5, 5, false, false, false) == 0, "Dread cannot become negative.");
Check(DreadRules.Advance(295, 5, true, true, false) == 0, "Sanctuary must prevent and clear conversion.");
Check(DreadRules.Advance(295, 5, true, false, true) == 0, "Recent conversion must prevent ping-pong ownership.");
Console.WriteLine("PASS: 7 Sevenfall dread timing and counterplay assertions.");
Check(VeilglassRules.DamageAt(0) == 12000, "Contact takes full blast damage.");
Check(VeilglassRules.DamageAt(2048) == 6000, "Blast edge damage is half strength.");
Check(VeilglassRules.DamageAt(2049) == 0, "Outside blast radius is safe.");
for (var density = 1; density <= 100; density++)
    Check(VeilglassRules.SpreadBudget(density) <= density && VeilglassRules.SpreadBudget(density) <= 6,
        "Detonations cannot create extra mineral and must cap spread.");
Check(VeilglassRules.SpreadBudget(0) == 0, "Empty deposits cannot spread.");
Console.WriteLine("PASS: 104 Veilglass blast-radius and finite-spread assertions.");

var shoulder = new TrapezoidMembershipFunction(0, 0, 20, 40);
Check(shoulder.Evaluate(0) == 1 && shoulder.Evaluate(20) == 1, "A left shoulder includes its closed endpoint.");
Check(shoulder.Evaluate(30) == 0.5 && shoulder.Evaluate(40) == 0, "Trapezoid membership slopes continuously to zero.");
Check(shoulder.Evaluate(-1) == 0 && shoulder.Evaluate(double.NaN) == 0, "Out-of-domain inputs do not fire rules.");
var fuzzy = new MamdaniFuzzySystem();
var health = new FuzzyVariable("Health", 0, 100);
health.Terms.Add(new FuzzyTerm("Low", new TrapezoidMembershipFunction(0, 0, 20, 40)));
health.Terms.Add(new FuzzyTerm("High", new TrapezoidMembershipFunction(60, 80, 100, 100)));
var power = new FuzzyVariable("Power", 0, 100);
power.Terms.Add(new FuzzyTerm("Strong", new TrapezoidMembershipFunction(60, 80, 100, 100)));
fuzzy.Input.Add(health); fuzzy.Input.Add(power);
var action = new FuzzyVariable("Action", 0, 50);
action.Terms.Add(new FuzzyTerm("Attack", new TrapezoidMembershipFunction(0, 15, 15, 30)));
action.Terms.Add(new FuzzyTerm("Flee", new TrapezoidMembershipFunction(25, 35, 35, 50)));
fuzzy.Output.Add(action);
fuzzy.Rules.Add(fuzzy.ParseRule("if ((Health is High) or ((Health is Low) and (Power is Strong))) then Action is Attack"));
fuzzy.Rules.Add(fuzzy.ParseRule("if (Health is Low) then Action is Flee"));
Check(Math.Abs(fuzzy.Calculate(new() {{health,100},{power,0}})[action] - 15) < 0.01, "Healthy forces choose the attack centroid.");
Check(fuzzy.Calculate(new() {{health,10},{power,0}})[action] > 30, "Weak wounded forces choose retreat.");
Check(fuzzy.Calculate(new() {{health,10},{power,100}})[action] < 30, "Strong wounded forces aggregate attack and retreat rules.");
Check(double.IsNaN(fuzzy.Calculate(new() {{health,50},{power,0}})[action]), "No matching rules produce no invented decision.");
var malformedRejected = false;
try { fuzzy.ParseRule("if Health is High then Action is Attack trailing"); } catch (ArgumentException) { malformedRejected = true; }
Check(malformedRejected, "Malformed rules must not silently truncate.");
var missingRejected = false;
try { fuzzy.Calculate(new() {{health,100}}); } catch (ArgumentException) { missingRejected = true; }
Check(missingRejected, "Missing inputs must be rejected.");
Console.WriteLine("PASS: 9 original Mamdani inference and rule-validation assertions.");
