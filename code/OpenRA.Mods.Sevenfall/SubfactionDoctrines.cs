// Original Sevenfall game logic. GPL-3.0-or-later.
using System;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    public enum SFDoctrineRole { Follower, Cantor, Shrine, Retrieval, Janus, Pylon, Magistrate, Contemptor, Throne }

    public class SFDoctrineMemberInfo : ConditionalTraitInfo
    {
        public readonly SFDoctrineRole Role;
        public override object Create(ActorInitializer init) => new SFDoctrineMember(init.Self, this);
    }

    public class SFDoctrineMember : ConditionalTrait<SFDoctrineMemberInfo>, INotifyKilled, INotifyAttack
    {
        public readonly Actor Actor;
        public SFDoctrineMember(Actor actor, SFDoctrineMemberInfo info) : base(info) { Actor = actor; }
        public bool Active => !IsTraitDisabled && SFDoctrineManager.Living(Actor);
        void INotifyKilled.Killed(Actor self, AttackInfo attack) =>
            self.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.FollowerKilled(self, Info.Role, attack.Attacker);
        void INotifyAttack.PreparingAttack(Actor self, in Target target, Armament armament, Barrel barrel) { }
        void INotifyAttack.Attacking(Actor self, in Target target, Armament armament, Barrel barrel)
        {
            if (Active && Info.Role == SFDoctrineRole.Magistrate && target.Type == TargetType.Actor)
                self.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.Condemn(self, target.Actor);
        }
    }

    [TraitLocation(SystemActors.World)]
    public class SFDoctrineManagerInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFDoctrineManager();
    }

    public class SFDoctrineManager : ITick, ISync
    {
        sealed class State
        {
            public int Resonance, ResonanceUntil, MarkUntil, NextMark, AscendancyUntil, SwitchAt;
            public Actor Target, Magistrate;
            public bool Abyss, DesiredAbyss;
        }
        readonly Dictionary<Player, State> states = new Dictionary<Player, State>();
        SFDoctrineMember[] members = Array.Empty<SFDoctrineMember>();
        [Sync] int countdown;
        [Sync] public int DoctrineHash
        {
            get
            {
                unchecked
                {
                    var h = 17;
                    foreach (var pair in states.OrderBy(p => p.Key.PlayerActor.ActorID))
                    {
                        var s = pair.Value;
                        foreach (var v in new[] { (int)pair.Key.PlayerActor.ActorID, s.Resonance, s.ResonanceUntil,
                            s.MarkUntil, s.NextMark, s.AscendancyUntil, s.SwitchAt, (int)(s.Target?.ActorID ?? 0),
                            (int)(s.Magistrate?.ActorID ?? 0), s.Abyss ? 1 : 0, s.DesiredAbyss ? 1 : 0 })
                            h = h * 31 + v;
                    }
                    return h;
                }
            }
        }
        State For(Player player)
        {
            if (!states.TryGetValue(player, out var state))
                states.Add(player, state = new State());
            return state;
        }
        public static bool Living(Actor a) => a != null && a.IsInWorld && !a.IsDead && !a.Disposed;
        static bool Near(Actor a, Actor b, int radius) =>
            (a.CenterPosition - b.CenterPosition).HorizontalLengthSquared <= (long)radius * radius;
        static bool Enemy(Actor a, Actor b) => a.Owner.RelationshipWith(b.Owner) == PlayerRelationship.Enemy;
        IEnumerable<SFDoctrineMember> Current(World world) => world.Actors.Where(Living)
            .Select(a => a.TraitOrDefault<SFDoctrineMember>()).Where(m => m != null && m.Active).OrderBy(m => m.Actor.ActorID);
        public bool Suppressed(Actor actor) => actor.OccupiesSpace != null && members.Any(m => m.Active && m.Info.Role == SFDoctrineRole.Pylon
            && m.Actor.Owner.Faction.InternalName == "h_area52" && Near(actor, m.Actor, 4096));
        public bool Convicted(Actor actor) => actor.Owner.Faction.InternalName == "a_desolation" && !Suppressed(actor)
            && members.Any(m => m.Active && m.Actor.Owner == actor.Owner &&
                (m.Info.Role == SFDoctrineRole.Cantor || m.Info.Role == SFDoctrineRole.Shrine) && !Suppressed(m.Actor) && Near(actor, m.Actor, 5120));
        public int Resonance(Player player) => states.TryGetValue(player, out var s) ? s.Resonance : 0;
        public bool Ascendancy(Player player) => states.TryGetValue(player, out var s) && s.AscendancyUntil > player.World.WorldTick;
        public Actor Condemned(Player player) => states.TryGetValue(player, out var s) && Living(s.Target) && Marked(s.Target, player) ? s.Target : null;
        public bool Abyss(Player player) => states.TryGetValue(player, out var s) && s.Abyss;
        public bool Marked(Actor actor, Player player) => states.TryGetValue(player, out var s)
            && s.Target == actor && s.MarkUntil > actor.World.WorldTick && Living(s.Magistrate)
            && s.Magistrate.Owner == player && Enemy(s.Magistrate, actor) && !Suppressed(s.Magistrate);

        public void FollowerKilled(Actor follower, SFDoctrineRole role, Actor killer)
        {
            if (role != SFDoctrineRole.Follower || follower.Owner.Faction.InternalName != "a_desolation"
                || killer == null || !Enemy(follower, killer) || Suppressed(follower))
                return;
            // Query live sources here: kill notifications run before the next field update.
            if (!Current(follower.World).Any(m => m.Actor.Owner == follower.Owner &&
                (m.Info.Role == SFDoctrineRole.Cantor || m.Info.Role == SFDoctrineRole.Shrine)
                && !Suppressed(m.Actor) && Near(follower, m.Actor, 5120)))
                return;
            var s = For(follower.Owner);
            s.Resonance = Math.Min(3, (s.ResonanceUntil > follower.World.WorldTick ? s.Resonance : 0) + 1);
            s.ResonanceUntil = follower.World.WorldTick + 150;
        }
        public void Condemn(Actor magistrate, Actor target)
        {
            if (magistrate.Owner.Faction.InternalName != "d_contempt" || !Living(target)
                || !Enemy(magistrate, target) || Suppressed(magistrate))
                return;
            var s = For(magistrate.Owner);
            if (magistrate.World.WorldTick < s.NextMark)
                return;
            s.Target = target;
            s.Magistrate = magistrate;
            s.MarkUntil = magistrate.World.WorldTick + 250;
            s.NextMark = magistrate.World.WorldTick + 200;
        }
        public void TargetKilled(Actor target, Actor killer)
        {
            if (killer == null)
                return;
            foreach (var pair in states)
                if (pair.Key == killer.Owner && Marked(target, pair.Key))
                {
                    pair.Value.Target = null;
                    pair.Value.AscendancyUntil = target.World.WorldTick + 150;
                }
        }
        public int MarkDamage(Actor target, Actor attacker)
        {
            // Projectiles retain their firing actor after it is disposed. Its
            // traits are no longer accessible; the base impact still applies.
            if (attacker == null || attacker.Disposed || target.Disposed)
                return 100;
            var health = target.TraitOrDefault<Health>();
            var execution = attacker?.TraitOrDefault<SFDoctrineMember>()?.Info.Role == SFDoctrineRole.Contemptor
                && health != null && health.HP < health.MaxHP / 2 ? 130 : 100;
            if (attacker == null || !Marked(target, attacker.Owner) || Suppressed(attacker))
                return execution;
            return execution * (members.Any(m => m.Active && m.Info.Role == SFDoctrineRole.Throne
                && m.Actor.Owner == attacker.Owner && Near(attacker, m.Actor, 5120)
                && Near(states[attacker.Owner].Magistrate, m.Actor, 5120)) ? 130 : 115) / 100;
        }
        void Grant(Actor actor, string condition, int count = 1)
        {
            var external = actor.TraitsImplementing<ExternalCondition>().FirstOrDefault(e => e.Info.Condition == condition);
            if (external != null)
                for (var i = 0; i < count; i++)
                    if (external.CanGrantCondition(this)) external.GrantCondition(actor, this, 6);
        }
        void ITick.Tick(Actor self)
        {
            if (--countdown > 0) return;
            countdown = 5;
            var tick = self.World.WorldTick;
            members = Current(self.World).ToArray();
            foreach (var player in self.World.Players)
            {
                var s = For(player);
                if (s.ResonanceUntil <= tick) s.Resonance = 0;
                if (s.Target != null && (!Living(s.Target) || s.MarkUntil <= tick || !Living(s.Magistrate)
                    || s.Magistrate.Owner != player || !Enemy(s.Magistrate, s.Target))) s.Target = null;
                var pylon = members.FirstOrDefault(m => m.Info.Role == SFDoctrineRole.Pylon && m.Actor.Owner == player);
                var desired = pylon?.Actor.Trait<GrantConditionOnDeploy>().DeployState == DeployState.Deployed;
                if (s.DesiredAbyss != desired) { s.DesiredAbyss = desired; s.SwitchAt = tick + 75; }
                if (tick >= s.SwitchAt) s.Abyss = s.DesiredAbyss;
            }
            foreach (var actor in self.World.Actors.Where(a => Living(a) && a.OccupiesSpace != null).OrderBy(a => a.ActorID))
            {
                var s = For(actor.Owner);
                var role = actor.TraitOrDefault<SFDoctrineMember>()?.Info.Role;
                if (Suppressed(actor)) Grant(actor, "sf-null");
                if (role == SFDoctrineRole.Follower && Convicted(actor)) Grant(actor, "sf-conviction");
                if (actor.Owner.Faction.InternalName == "a_desolation" && actor.Info.Name.StartsWith("a_")
                    && role != SFDoctrineRole.Follower && s.Resonance > 0 && Convicted(actor))
                    Grant(actor, "sf-resonance", s.Resonance);
                if (actor.Owner.Faction.InternalName == "d_contempt" && s.AscendancyUntil > tick
                    && !Suppressed(actor) && members.Any(m => m.Active && m.Actor.Owner == actor.Owner
                        && (m.Info.Role == SFDoctrineRole.Magistrate || m.Info.Role == SFDoctrineRole.Throne)
                        && !Suppressed(m.Actor) && Near(actor, m.Actor, 6144))) Grant(actor, "sf-ascendancy");
                if (role == SFDoctrineRole.Janus)
                {
                    if (s.Abyss) Grant(actor, "sf-abyss");
                    if (s.SwitchAt > tick || !members.Any(m => m.Info.Role == SFDoctrineRole.Pylon
                        && m.Actor.Owner == actor.Owner)) Grant(actor, "sf-protocol-offline");
                }
                if (states.Any(p => Marked(actor, p.Key))) Grant(actor, "sf-condemned");
            }
        }
    }

    public class SFDoctrineTargetInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFDoctrineTarget(init.Self);
    }
    public class SFDoctrineTarget : IDamageModifier, INotifyKilled
    {
        readonly Actor actor;
        public SFDoctrineTarget(Actor self) { actor = self; }
        int IDamageModifier.GetDamageModifier(Actor attacker, Damage damage) => damage.Value <= 0 ? 100 :
            actor.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.MarkDamage(actor, attacker) ?? 100;
        void INotifyKilled.Killed(Actor self, AttackInfo attack) =>
            self.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.TargetKilled(self, attack.Attacker);
    }
    [ScriptPropertyGroup("Sevenfall containment")]
    public class SFProtocolProperties : ScriptActorProperties, Requires<GrantConditionOnDeployInfo>
    {
        public SFProtocolProperties(ScriptContext context, Actor self) : base(context, self) { }
        public void ToggleProtocol() => Self.Trait<GrantConditionOnDeploy>().ResolveOrder(Self,
            new Order("GrantConditionOnDeploy", Self, false));
    }
    [ScriptPropertyGroup("Sevenfall doctrine inspection")]
    public class SFDoctrineActorProperties : ScriptActorProperties, Requires<SFDoctrineTargetInfo>
    {
        public SFDoctrineActorProperties(ScriptContext context, Actor self) : base(context, self) { }
        public int DoctrineFirepower => Self.TraitsImplementing<IFirepowerModifier>().Aggregate(100, (value, modifier) => value * modifier.GetFirepowerModifier() / 100);
        public bool NullSuppressed => Self.World.WorldActor.Trait<SFDoctrineManager>().Suppressed(Self);
        public bool ConvictionProtected => Self.World.WorldActor.Trait<SFDoctrineManager>().Convicted(Self);
        public int DoctrineDamageFrom(Actor attacker) => Self.World.WorldActor.Trait<SFDoctrineManager>().MarkDamage(Self, attacker);
    }
    [ScriptPropertyGroup("Sevenfall doctrines")]
    public class SFDoctrineProperties : ScriptPlayerProperties
    {
        public SFDoctrineProperties(ScriptContext context, Player player) : base(context, player) { }
        public int Resonance => Player.World.WorldActor.Trait<SFDoctrineManager>().Resonance(Player);
        public bool Ascendancy => Player.World.WorldActor.Trait<SFDoctrineManager>().Ascendancy(Player);
        public Actor CondemnedTarget => Player.World.WorldActor.Trait<SFDoctrineManager>().Condemned(Player);
        public bool AbyssProtocol => Player.World.WorldActor.Trait<SFDoctrineManager>().Abyss(Player);
    }
}
