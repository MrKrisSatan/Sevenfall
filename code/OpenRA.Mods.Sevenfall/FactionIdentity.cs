// Original Sevenfall game logic. GPL-3.0-or-later.
using System;
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Mods.Common.Traits.Render;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    public class SFSuppressionStateInfo : ConditionalTraitInfo
    {
        public override object Create(ActorInitializer init) => new SFSuppressionState(this);
    }
    public class SFSuppressionState : ConditionalTrait<SFSuppressionStateInfo>
    {
        public SFSuppressionState(SFSuppressionStateInfo info) : base(info) { }
        public bool Active => !IsTraitDisabled;
    }
    public class SFFactionIdentityInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFFactionIdentity();
    }

    // Local timers belong to the actor: ownership changes cannot carry a prepared volley.
    public class SFFactionIdentity : ITick, INotifyAttack, INotifyKilled, ISync
    {
        [Sync] int stillTicks;
        [Sync] int feedingUntil;
        [Sync] int lastOwner = -1;
        [Sync] CPos previous;
        public static bool Living(Actor a) => SFDoctrineManager.Living(a);
        public static bool Near(Actor a, Actor b, int cells) =>
            (a.CenterPosition - b.CenterPosition).HorizontalLengthSquared <= (long)cells * cells * 1024 * 1024;
        public static void Grant(Actor actor, object source, string name, int duration)
        {
            if (!Living(actor)) return;
            var condition = actor.TraitsImplementing<ExternalCondition>().FirstOrDefault(c => c.Info.Condition == name);
            if (condition != null && condition.CanGrantCondition(source)) condition.GrantCondition(actor, source, duration);
        }
        static bool Suppressed(Actor actor) => actor.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.Suppressed(actor) ?? false;
        public string ActiveCondition(Actor self)
        {
            var health = self.TraitOrDefault<Health>();
            if (health == null || self.OccupiesSpace == null) return null;
            var faction = self.Owner.Faction.InternalName;
            // New realm doctrines are combat-only: collectors and engineers do not
            // acquire combat/escape bonuses. Fallen miracles obey null suppression.
            if ((faction.StartsWith("i_") || faction.StartsWith("f_")) && !self.Info.HasTraitInfo<ArmamentInfo>()) return null;
            if (faction != "h_bastion" && faction != "h_union" && Suppressed(self)) return null;
            var friends = self.World.FindActorsInCircle(self.CenterPosition,new WDist(6144))
                .Where(a => Living(a) && a.Owner == self.Owner && a != self && a.OccupiesSpace != null);
            switch (self.Owner.Faction.InternalName)
            {
                case "i_echo": return stillTicks >= 75 ? "sf-focus" : null;
                case "i_iron": return "sf-machine-iron";
                case "i_grid": return friends.Any(a => a.Info.Name == "i_relay" && Near(a, self, 4)) ? "sf-machine-grid" : null;
                case "i_paradox": return health.HP * 2 < health.MaxHP ? "sf-machine-paradox" : null;
                case "f_thrones": return stillTicks >= 100 ? "sf-fallen-throne" : null;
                case "f_choir": return friends.Any(a => a.Info.Name == "f_lamentor" && Near(a, self, 4)) ? "sf-fallen-choir" : null;
                case "f_scars": return health.HP * 2 < health.MaxHP ? "sf-fallen-scars" : null;
                case "f_wings": return !friends.Any(a => a.Info.HasTraitInfo<ArmamentInfo>() && Near(a, self, 4)) ? "sf-fallen-wings" : null;
                case "a_seraph": return stillTicks >= 75 ? "sf-focus" : null;
                case "a_warden": return friends.Any(a => (a.Info.Name == "a_gatekeeper" || a.Info.Name == "a_wardbearer") && Near(a, self, 4)) ? "sf-aegis" : null;
                case "a_exile": return health.HP * 2 < health.MaxHP ? "sf-defiance" : null;
                case "h_bastion": return stillTicks >= 100 ? "sf-entrenched" : null;
                case "h_union": return friends.Any(a => (a.Info.Name == "h_harvester" || a.Info.Name == "h_pathfinder") && Near(a, self, 6)) ? "sf-logistics" : null;
                case "h_covenant": return friends.Any(a => (a.Info.Name == "h_templar" || a.Info.Name == "h_confessor") && Near(a, self, 4)) ? "sf-oath" : null;
                case "d_legion": return friends.Any(a => (a.Info.Name == "d_hellreaver" || a.Info.Name == "d_taskmaster") && Near(a, self, 4)) ? "sf-iron" : null;
                case "d_brood": return feedingUntil > self.World.WorldTick ? "sf-fed" : null;
                default: return null;
            }
        }
        void ITick.Tick(Actor self)
        {
            if (self.OccupiesSpace == null) return;
            var owner = (int)self.Owner.PlayerActor.ActorID;
            if (lastOwner != owner) { stillTicks = 0; feedingUntil = 0; lastOwner = owner; previous = self.Location; }
            stillTicks = self.Location == previous ? Math.Min(100, stillTicks + 1) : 0;
            previous = self.Location;
            if (self.World.WorldTick % 5 != 0) return;
            var condition = ActiveCondition(self);
            if (condition != null) Grant(self, this, condition, 6);
            // Oath heals infantry only, at 200 HP/second. Multiple confessors never stack.
            if (condition == "sf-oath" && self.Info.HasTraitInfo<WithInfantryBodyInfo>() && self.World.WorldTick % 25 == 0)
                self.InflictDamage(self, new Damage(-200));
        }
        void INotifyAttack.PreparingAttack(Actor self, in Target target, Armament armament, Barrel barrel) { }
        void INotifyAttack.Attacking(Actor self, in Target target, Armament armament, Barrel barrel)
        {
            if (target.Type != TargetType.Actor || !Living(target.Actor) || self.Owner.RelationshipWith(target.Actor.Owner) != PlayerRelationship.Enemy || Suppressed(self)) return;
            if (self.Owner.Faction.InternalName == "d_court" && (self.Info.Name == "d_hexer" || self.Info.Name == "d_silencer"))
                Grant(target.Actor, self, "sf-whisper", 100);
        }
        void INotifyKilled.Killed(Actor self, AttackInfo attack)
        {
            var killer = attack.Attacker;
            if (killer == null || killer.Disposed || killer.Owner.Faction.InternalName != "d_brood" || killer.Owner.RelationshipWith(self.Owner) != PlayerRelationship.Enemy || Suppressed(killer)) return;
            var identity = killer.TraitOrDefault<SFFactionIdentity>();
            if (identity == null || !self.Info.HasTraitInfo<MobileInfo>()) return;
            identity.feedingUntil = self.World.WorldTick + 150;
            var health = killer.TraitOrDefault<Health>();
            if (health != null) killer.InflictDamage(killer, new Damage(-Math.Min(5000, health.MaxHP / 10)));
        }
    }
}
