// Original Sevenfall game logic. GPL-3.0-or-later.
using System;
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [TraitLocation(SystemActors.Player | SystemActors.EditorPlayer)]
    [Desc("Counts accepted refinery income independently of spending or cash grants.")]
    public class SFHarvestAccountingInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFHarvestAccounting();
    }

    public class SFHarvestAccounting : INotifyResourceAccepted, ISync
    {
        [Sync] public int RefinedCredits;

        void INotifyResourceAccepted.OnResourceAccepted(Actor self, Actor refinery,
            string resourceType, int count, int value)
        {
            // Refinery dispatches only to its current owner's actors, after
            // storage limits and value modifiers have been applied.
            if (refinery.Owner == self.Owner && (resourceType == "Ore" || resourceType == "Gems") && value > 0)
                RefinedCredits = (int)Math.Min(int.MaxValue, (long)RefinedCredits + value);
        }
    }

    [ScriptPropertyGroup("Sevenfall economy")]
    public class SFHarvestProperties : ScriptPlayerProperties, Requires<SFHarvestAccountingInfo>
    {
        readonly SFHarvestAccounting accounting;

        public SFHarvestProperties(ScriptContext context, Player player) : base(context, player)
        {
            accounting = player.PlayerActor.Trait<SFHarvestAccounting>();
        }

        [Desc("Cumulative accepted Veilglass refinery income; excludes cash grants and spending.")]
        public int RefinedCredits => accounting.RefinedCredits;
    }
}
