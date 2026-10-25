// Developer-map normal save/load round-trip checks. GPL-3.0-or-later.
using System;
using System.Collections.Generic;
using System.Reflection;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [TraitLocation(SystemActors.World)]
    public class SFSaveProbeInfo : TraitInfo
    {
        public readonly int SaveTick = 300;
        public readonly int FinalTick = 1000;
        public readonly bool DetailedSnapshots = false;
        public override object Create(ActorInitializer init) => new SFSaveProbe(this);
    }
    public class SFSaveProbe : ITick, INotifyGameSaved, INotifyGameLoaded
    {
        int ticks;
        bool acknowledged;
        readonly SFSaveProbeInfo info;
        public SFSaveProbe(SFSaveProbeInfo info) { this.info=info; }
        public void GameLoaded(World world)
        {
            // Normal loading opens the options menu and pauses singleplayer.
            // The automated scenario must issue the same unpause order as Resume.
            Game.RunAfterTick(() => world.SetPauseState(false));
            Console.WriteLine("SAVE_TEST RESUME_AFTER_LOAD");
        }
        public void GameSaved(World world)
        {
            acknowledged = true;
            Console.WriteLine("SAVE_TEST ACKNOWLEDGED");
        }
        public void Tick(Actor self)
        {
            ticks++;
            if (ticks == info.SaveTick && !SFAcceptanceLoadScreen.LoadingSaveAcceptance)
                self.World.RequestGameSave("sevenfall-acceptance.orasav");
            if (ticks == 375 || ticks == 500 || ticks == 875 || ticks == 1000)
                Console.WriteLine("SAVE_TEST SNAPSHOT tick=" + ticks + " hash=" + self.World.SyncHash());
            if (ticks==875 && info.DetailedSnapshots)
            {
                var values=new SortedDictionary<string,string>();
                values["random"]=self.World.SharedRandom.Last+"/"+self.World.SharedRandom.TotalCount;
                foreach (var actor in self.World.Actors)
                {
                    var index=0;
                    foreach (var trait in actor.TraitsImplementing<ISync>())
                    {
                        var prefix=actor.ActorID+"/"+actor.Info.Name+"/"+trait.GetType().Name+"/"+(index++)+"/";
                        foreach (var field in trait.GetType().GetFields(BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance))
                            if (field.IsDefined(typeof(SyncAttribute))) values[prefix+field.Name]=field.GetValue(trait)?.ToString();
                        foreach (var property in trait.GetType().GetProperties(BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance))
                            if (property.IsDefined(typeof(SyncAttribute))) values[prefix+property.Name]=property.GetValue(trait)?.ToString();
                    }
                }
                Console.WriteLine("SAVE_DETAIL "+System.Text.Json.JsonSerializer.Serialize(values));
            }
            if (ticks != info.FinalTick) return;
            if (self.World.IsLoadingGameSave || (!SFAcceptanceLoadScreen.LoadingSaveAcceptance && !acknowledged))
                Console.WriteLine("SAVE_TEST FAIL: save acknowledgement or load restoration missing");
            else
                Console.WriteLine("SAVE_TEST COMPLETE restored=" + SFAcceptanceLoadScreen.LoadingSaveAcceptance);
            Game.RunAfterDelay(500, Game.Exit);
        }
    }
}
