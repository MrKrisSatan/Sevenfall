// Original Sevenfall game logic. Distributed under GPL-3.0-or-later, like OpenRA.
using System;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Primitives;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    public enum SFDefenseKind { Light, Flesh, Wire, Thorns, Sanctuary }

    [Desc("A Sevenfall defensive field, controlled by the world's deterministic defense manager.")]
    public class SFDefenseSourceInfo : ConditionalTraitInfo
    {
        public readonly SFDefenseKind Kind = SFDefenseKind.Flesh;
        public readonly WDist Range = WDist.FromCells(3);
        public readonly int Damage = 0;
        public readonly int Heal = 0;
        public override object Create(ActorInitializer init) => new SFDefenseSource(init.Self, this);
    }

    public class SFDefenseSource : ConditionalTrait<SFDefenseSourceInfo>
    {
        public readonly Actor Actor;
        public SFDefenseSource(Actor actor, SFDefenseSourceInfo info) : base(info) { Actor = actor; }
        public bool Active => !IsTraitDisabled && Actor.IsInWorld && !Actor.IsDead && !Actor.Disposed && (Info.Kind == SFDefenseKind.Wire || Info.Kind == SFDefenseKind.Thorns
            || !(Actor.World.WorldActor.TraitOrDefault<SFDoctrineManager>()?.Suppressed(Actor) ?? false));
        public bool Contains(Actor actor) => (actor.CenterPosition - Actor.CenterPosition).HorizontalLengthSquared <= (long)Info.Range.Length * Info.Range.Length;
    }

    [TraitLocation(SystemActors.World)]
    [Desc("Updates light curtains, obstacles, sanctuary healing and non-stacking dread exposure on all maps.")]
    public class SFDefenseManagerInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFDefenseManager();
    }

    public class SFDefenseManager : ITick, ISync
    {
        const int Interval = 5;
        sealed class Mind
        {
            public Player VictimOwner;
            public Player SourceOwner;
            public int Progress;
            public int ImmuneUntil;
        }

        readonly Dictionary<Actor, Mind> minds = new Dictionary<Actor, Mind>();
        [Sync] int countdown;

        // Dictionary order is never used to choose an owner or a target. Include
        // exposure and immunity in sync checking, not merely the resulting owner.
        [Sync]
        public int ExposureHash
        {
            get
            {
                unchecked
                {
                    var hash = 17;
                    foreach (var pair in minds.OrderBy(p => p.Key.ActorID))
                    {
                        hash = hash * 31 + (int)pair.Key.ActorID;
                        hash = hash * 31 + pair.Value.Progress;
                        hash = hash * 31 + pair.Value.ImmuneUntil;
                        hash = hash * 31 + (int)(pair.Value.VictimOwner?.PlayerActor.ActorID ?? 0);
                        hash = hash * 31 + (int)(pair.Value.SourceOwner?.PlayerActor.ActorID ?? 0);
                    }
                    return hash;
                }
            }
        }

        public int Progress(Actor actor) => minds.TryGetValue(actor, out var mind) ? mind.Progress : 0;
        static bool Living(Actor a) => a.IsInWorld && !a.IsDead && !a.Disposed;
        static bool Infantry(Actor a) => a.Info.TraitInfoOrDefault<MobileInfo>()?.Locomotor == "foot";
        static bool Enemy(Actor source, Actor target) => source.Owner.RelationshipWith(target.Owner) == PlayerRelationship.Enemy;
        static bool Allied(Actor source, Actor target) => source.Owner.IsAlliedWith(target.Owner);

        static void Condition(Actor actor, object source, string name)
        {
            var external = actor.TraitsImplementing<ExternalCondition>().FirstOrDefault(e => e.Info.Condition == name);
            if (external != null && external.CanGrantCondition(source))
                external.GrantCondition(actor, source, Interval + 1);
        }

        void ITick.Tick(Actor self)
        {
            if (--countdown > 0)
                return;
            countdown = Interval;
            var world = self.World;
            var tick = world.WorldTick;
            var sources = world.Actors.Where(Living).Select(a => a.TraitOrDefault<SFDefenseSource>())
                .Where(s => s != null && s.Active).OrderBy(s => s.Actor.ActorID).ToArray();
            foreach (var dead in minds.Keys.Where(a => !Living(a)).ToArray())
                minds.Remove(dead);
            if (sources.Length == 0 && minds.Count == 0)
                return;
            var units = world.Actors.Where(a => Living(a) && a.Info.HasTraitInfo<MobileInfo>() && a.Info.HasTraitInfo<HealthInfo>())
                .OrderBy(a => a.ActorID).ToArray();

            // Passable entanglements are crushed by hostile ground vehicles.
            foreach (var obstacle in sources.Where(s => s.Info.Kind == SFDefenseKind.Wire || s.Info.Kind == SFDefenseKind.Thorns))
            {
                var crusher = units.FirstOrDefault(a => !Infantry(a) && Enemy(obstacle.Actor, a) && obstacle.Contains(a));
                if (crusher != null)
                    obstacle.Actor.Kill(crusher);
            }

            foreach (var actor in units)
            {
                var infantry = Infantry(actor);
                var sanctuary = infantry ? sources.FirstOrDefault(s => s.Active && s.Info.Kind == SFDefenseKind.Sanctuary && Allied(s.Actor, actor) && s.Contains(actor)) : null;
                SFDefenseSource dread = null;
                foreach (var source in sources)
                {
                    if (!source.Active || !Enemy(source.Actor, actor) || !source.Contains(actor))
                        continue;
                    if (source.Info.Kind == SFDefenseKind.Light)
                        actor.InflictDamage(source.Actor, new Damage(source.Info.Damage, new BitSet<DamageType>(new[] { "FireDeath" })));
                    else if (infantry && (source.Info.Kind == SFDefenseKind.Wire || source.Info.Kind == SFDefenseKind.Thorns))
                    {
                        Condition(actor, this, source.Info.Kind == SFDefenseKind.Wire ? "sf-wire" : "sf-thorns");
                        actor.InflictDamage(source.Actor, new Damage(source.Info.Damage));
                    }
                    else if (infantry && source.Info.Kind == SFDefenseKind.Flesh && dread == null)
                        dread = source; // One owner, one rate: overlapping walls never accelerate conversion.
                    if (!Living(actor))
                        break;
                }
                if (!infantry || !Living(actor))
                    continue;
                if (sanctuary != null)
                    actor.InflictDamage(sanctuary.Actor, new Damage(-sanctuary.Info.Heal));
                if (!minds.TryGetValue(actor, out var mind))
                {
                    if (dread == null)
                        continue;
                    mind = new Mind { VictimOwner = actor.Owner };
                    minds.Add(actor, mind);
                }
                if (mind.VictimOwner != actor.Owner)
                {
                    mind.VictimOwner = actor.Owner;
                    mind.Progress = 0;
                    mind.ImmuneUntil = Math.Max(mind.ImmuneUntil, tick + DreadRules.ImmunityTicks);
                }
                var elapsed = Interval;
                if (dread != null && mind.SourceOwner != dread.Actor.Owner)
                {
                    mind.SourceOwner = dread.Actor.Owner;
                    mind.Progress = 0;
                    elapsed = 0; // Start timing at first contact, never five ticks before it.
                }
                mind.Progress = DreadRules.Advance(mind.Progress, elapsed, dread != null, sanctuary != null || (world.WorldActor.TraitOrDefault<SFDoctrineManager>()?.Convicted(actor) ?? false), tick < mind.ImmuneUntil);
                if (mind.Progress > 0)
                    Condition(actor, this, "sf-dread");
                if (mind.Progress < DreadRules.ThresholdTicks || dread == null)
                    continue;
                var victim = actor;
                var wall = dread;
                var owner = wall.Actor.Owner;
                mind.Progress = 0;
                mind.ImmuneUntil = tick + DreadRules.ImmunityTicks;
                world.AddFrameEndTask(w =>
                {
                    // Destruction, power loss or diplomacy changes cancel a pending conversion.
                    if (!Living(victim) || !wall.Active || wall.Actor.Owner != owner || !Enemy(wall.Actor, victim) || !wall.Contains(victim))
                        return;
                    if (w.Actors.Where(Living).Select(a => a.TraitOrDefault<SFDefenseSource>()).Any(s => s != null && s.Active && s.Info.Kind == SFDefenseKind.Sanctuary && Allied(s.Actor, victim) && s.Contains(victim)))
                        return;
                    if (w.WorldActor.TraitOrDefault<SFDoctrineManager>()?.Convicted(victim) ?? false)
                        return;
                    victim.CancelActivity();
                    victim.ChangeOwner(owner);
                });
            }
        }
    }

    [Desc("Displays the unit's rising dread as a purple selection bar.")]
    public class SFDreadBarInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFDreadBar(init.Self);
    }

    public class SFDreadBar : ISelectionBar
    {
        readonly Actor actor;
        public SFDreadBar(Actor actor) { this.actor = actor; }
        float ISelectionBar.GetValue() => (actor.World.WorldActor.TraitOrDefault<SFDefenseManager>()?.Progress(actor) ?? 0) / (float)DreadRules.ThresholdTicks;
        Color ISelectionBar.GetColor() => Color.FromArgb(255, 190, 60, 230);
        bool ISelectionBar.DisplayWhenEmpty => false;
    }
}
