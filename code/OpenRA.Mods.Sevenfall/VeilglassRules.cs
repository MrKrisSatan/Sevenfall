// Original Sevenfall game logic. GPL-3.0-or-later.
using System;

namespace OpenRA.Mods.Sevenfall
{
    public static class VeilglassRules
    {
        public const int ArmingTicks = 50;
        public const int BlastRadius = 2048;
        public const int MaxBlastsPerTick = 8;
        public static int SpreadBudget(int density) => density <= 0 ? 0 : Math.Min(6, Math.Max(1, density - 1));
        public static int DamageAt(int distance) => distance > BlastRadius ? 0 :
            12000 - 6000 * Math.Max(0, distance) / BlastRadius;
    }
}
