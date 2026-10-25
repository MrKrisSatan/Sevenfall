// Original Sevenfall game logic. GPL-3.0-or-later.
using System;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Effects;
using OpenRA.Graphics;
using OpenRA.Mods.Common.Graphics;
using OpenRA.Mods.Common.Traits;
using OpenRA.Primitives;
using OpenRA.Scripting;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [ScriptGlobal("Veilglass")]
    public class SFVeilglassGlobal : ScriptGlobal
    {
        readonly IResourceLayer resources;
        public SFVeilglassGlobal(ScriptContext context) : base(context)
        {
            resources = context.World.WorldActor.Trait<IResourceLayer>();
        }
        [Desc("Current resource density at a map cell, or zero when empty.")]
        public int DensityAt(CPos cell) => resources.GetResource(cell).Density;
    }

    [TraitLocation(SystemActors.World)]
    [Desc("Non-harvester ground contact detonates Veilglass and scatters a finite amount of mineral.")]
    public class SFVeilglassHazardInfo : TraitInfo, Requires<ResourceLayerInfo>
    {
        public override object Create(ActorInitializer init) => new SFVeilglassHazard();
    }

    public class SFVeilglassHazard : ITick, ISync
    {
        readonly Dictionary<CPos, int> armedAt = new Dictionary<CPos, int>();
        static readonly CVec[] Scatter = { new CVec(3, 0), new CVec(2, 2), new CVec(0, 3),
            new CVec(-2, 2), new CVec(-3, 0), new CVec(-2, -2), new CVec(0, -3), new CVec(2, -2) };

        [Sync] public int ArmingHash
        {
            get
            {
                unchecked
                {
                    var hash = 17;
                    foreach (var entry in armedAt.OrderBy(p => p.Key.X).ThenBy(p => p.Key.Y))
                        hash = ((hash * 31 + entry.Key.X) * 31 + entry.Key.Y) * 31 + entry.Value;
                    return hash;
                }
            }
        }

        static bool GroundActor(Actor actor) => actor.IsInWorld && !actor.IsDead && !actor.Disposed
            && actor.OccupiesSpace != null && actor.Info.HasTraitInfo<HealthInfo>()
            && actor.World.Map.DistanceAboveTerrain(actor.CenterPosition).Length <= 128;

        void ITick.Tick(Actor self)
        {
            var world = self.World;
            var resources = world.WorldActor.Trait<IResourceLayer>();
            foreach (var cell in armedAt.Where(p => p.Value <= world.WorldTick).Select(p => p.Key).ToArray())
                armedAt.Remove(cell);
            var actors = world.Actors.Where(GroundActor).OrderBy(a => a.ActorID).ToArray();
            var blasts = 0;
            foreach (var actor in actors)
            {
                if (!GroundActor(actor) || actor.Info.HasTraitInfo<HarvesterInfo>())
                    continue;
                // Full footprint catches structure edges and large vehicles.
                foreach (var cell in actor.OccupiesSpace.OccupiedCells().Select(p => p.Cell).Distinct()
                    .OrderBy(c => c.X).ThenBy(c => c.Y).ToArray())
                {
                    if (!GroundActor(actor))
                        break;
                    var deposit = resources.GetResource(cell);
                    if ((deposit.Type != "Ore" && deposit.Type != "Gems") || armedAt.ContainsKey(cell))
                        continue;
                    resources.ClearResources(cell);
                    var center = world.Map.CenterOfCell(cell);
                    foreach (var victim in actors.Where(GroundActor))
                    {
                        var distance = victim.OccupiesSpace.OccupiedCells().Select(p =>
                            (world.Map.CenterOfCell(p.Cell) - center).HorizontalLength).DefaultIfEmpty(int.MaxValue).Min();
                        var damage = VeilglassRules.DamageAt(distance);
                        if (damage > 0)
                            victim.InflictDamage(self, new Damage(damage,
                                new BitSet<DamageType>(new[] { "FireDeath" })));
                    }
                    var budget = VeilglassRules.SpreadBudget(deposit.Density);
                    var rotation = (cell.X + cell.Y) & 7;
                    for (var i = 0; i < Scatter.Length && budget > 0; i++)
                    {
                        var destination = cell + Scatter[(i + rotation) & 7];
                        var amount = Math.Min(2, budget);
                        if (resources.GetResource(destination).Type != null ||
                            !resources.CanAddResource(deposit.Type, destination, amount))
                            continue;
                        var added = resources.AddResource(deposit.Type, destination, amount);
                        if (added > 0)
                        {
                            budget -= added;
                            armedAt[destination] = world.WorldTick + VeilglassRules.ArmingTicks;
                        }
                    }
                    world.AddFrameEndTask(w => w.Add(new SFVeilglassBlast(center)));
                    if (++blasts >= VeilglassRules.MaxBlastsPerTick)
                        return;
                }
            }
        }
    }

    // Asset-independent placeholder shockwave: no inherited RA explosion sprites.
    public class SFVeilglassBlast : IEffect
    {
        readonly WPos position;
        int age;
        public SFVeilglassBlast(WPos position) { this.position = position; }
        public void Tick(World world)
        {
            if (++age >= 16)
                world.AddFrameEndTask(w => w.Remove(this));
        }
        public IEnumerable<IRenderable> Render(WorldRenderer wr)
        {
            if (wr.World.FogObscures(position))
                yield break;
            yield return new CircleAnnotationRenderable(position, new WDist(128 + age * 128), 3,
                Color.FromArgb(Math.Max(0, 255 - age * 15), 195, 100, 255));
            if (age < 5)
                yield return new CircleAnnotationRenderable(position, new WDist(600), 1,
                    Color.FromArgb(160 - age * 30, 245, 215, 255), true);
        }
    }
}
