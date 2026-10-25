// Developer-map normal save/load round-trip checks. GPL-3.0-or-later.
using System;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [TraitLocation(SystemActors.World)]
    public class SFSaveProbeInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFSaveProbe();
    }
    public class SFSaveProbe : ITick, INotifyGameSaved
    {
        int ticks;
        bool acknowledged;
        public void GameSaved(World world)
        {
            acknowledged = true;
            Console.WriteLine("SAVE_TEST ACKNOWLEDGED");
        }
        public void Tick(Actor self)
        {
            ticks++;
            if (ticks == 300 && !SFAcceptanceLoadScreen.LoadingSaveAcceptance)
                self.World.RequestGameSave("sevenfall-acceptance.orasav");
            if (ticks == 375 || ticks == 500 || ticks == 875 || ticks == 1000)
                Console.WriteLine("SAVE_TEST SNAPSHOT tick=" + ticks + " hash=" + self.World.SyncHash());
            if (ticks != 1000) return;
            if (self.World.IsLoadingGameSave || (!SFAcceptanceLoadScreen.LoadingSaveAcceptance && !acknowledged))
                Console.WriteLine("SAVE_TEST FAIL: save acknowledgement or load restoration missing");
            else
                Console.WriteLine("SAVE_TEST COMPLETE restored=" + SFAcceptanceLoadScreen.LoadingSaveAcceptance);
            Game.RunAfterDelay(500, Game.Exit);
        }
    }
}
