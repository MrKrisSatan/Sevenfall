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
