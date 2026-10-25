using OpenRA.Mods.Sevenfall;

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
