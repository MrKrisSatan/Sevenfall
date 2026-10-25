// Original Sevenfall game logic. Distributed under GPL-3.0-or-later, like OpenRA.
using System;

namespace OpenRA.Mods.Sevenfall
{
    public static class DreadRules
    {
        public const int ThresholdTicks = 300; // 12 seconds at 25 simulation ticks/s.
        public const int ImmunityTicks = 750;  // Prevent conversion ping-pong for 30 seconds.

        public static int Advance(int progress, int elapsed, bool exposed, bool protectedMind, bool immune)
        {
            if (protectedMind || immune)
                return 0;
            return exposed ? Math.Min(ThresholdTicks, progress + elapsed) : Math.Max(0, progress - elapsed * 2);
        }
    }
}
