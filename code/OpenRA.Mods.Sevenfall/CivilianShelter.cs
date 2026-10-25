// Original Sevenfall game logic. GPL-3.0-or-later.
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [Desc("Nearby uncontested infantry claim an empty civilian shelter. Occupied shelters cannot change hands.")]
    public class SFCivilianShelterInfo : TraitInfo, Requires<CargoInfo>
    {
        public readonly WDist ClaimRange = new WDist(2560);
        public override object Create(ActorInitializer init) => new SFCivilianShelter(init.Self, this);
    }

    public class SFCivilianShelter : ITick, ISync
    {
        readonly SFCivilianShelterInfo info;
        readonly Player originalOwner;
        [Sync] int countdown;
        public SFCivilianShelter(Actor actor, SFCivilianShelterInfo info)
        {
            this.info = info;
            originalOwner = actor.Owner;
        }

        Player Claimant(Actor self)
        {
            if (self.Trait<Cargo>().PassengerCount != 0)
                return self.Owner;
            var units = self.World.FindActorsInCircle(self.CenterPosition, info.ClaimRange)
                .Where(a => a.IsInWorld && !a.IsDead && !a.Disposed && !a.Owner.NonCombatant
                    && a.Info.HasTraitInfo<MobileInfo>()
                    && a.TraitOrDefault<Passenger>()?.Info.CargoType == "Infantry")
                .OrderBy(a => a.ActorID).ToArray();
            if (units.Length == 0)
                return originalOwner;
            var claimant = units[0].Owner;
            return units.All(a => claimant.IsAlliedWith(a.Owner)) ? claimant : self.Owner;
        }

        void ITick.Tick(Actor self)
        {
            if (--countdown > 0 || !self.IsInWorld || self.IsDead)
                return;
            countdown = 5;
            if (Claimant(self) == self.Owner)
                return;
            self.World.AddFrameEndTask(w =>
            {
                if (self.Disposed || self.IsDead || !self.IsInWorld)
                    return;
                var owner = Claimant(self);
                if (owner != self.Owner)
                    self.ChangeOwner(owner);
            });
        }
    }
}
