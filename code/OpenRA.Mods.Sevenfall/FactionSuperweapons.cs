// Original Sevenfall game logic. GPL-3.0-or-later.
using System;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Mods.Common.Effects;
using OpenRA.Mods.Common.Traits;
using OpenRA.Mods.Common.Traits.Render;
using OpenRA.Graphics;
using OpenRA.Mods.Common.Graphics;
using OpenRA.Primitives;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    public enum SFUltimate { Dawn, Sanctuary, Rebellion, Requiem, Barrage, Relief, Covenant, Singularity, Furnace, Bloodtide, Silence, Verdict, Nuclear, Petrification, Hellrift, Extinction, Rapture }
    public class SFFactionPowerInfo : SupportPowerInfo
    {
        public readonly SFUltimate Kind;
        public readonly int Radius = 5;
        public readonly int WarningTicks = 75;
        public override object Create(ActorInitializer init) => new SFFactionPower(init.Self, this);
    }
    public class SFFactionPower : SupportPower
    {
        readonly SFFactionPowerInfo data;
        public SFFactionPower(Actor self, SFFactionPowerInfo info) : base(self, info) { data = info; }
        public override void SelectTarget(Actor self,string order,SupportPowerManager manager) =>
            self.World.OrderGenerator=new FactionTarget(order,manager,data);
        sealed class FactionTarget : SelectGenericPowerTarget
        {
            readonly SupportPowerManager manager;
            readonly SFFactionPowerInfo data;
            CPos? hover;
            public FactionTarget(string order,SupportPowerManager manager,SFFactionPowerInfo data) : base(order,manager,data,MouseButton.Left)
            { this.manager=manager; this.data=data; }
            bool Valid(World world,CPos cell)=>world.Map.Contains(cell)&&manager.Self.Owner.Shroud.IsExplored(cell);
            protected override string GetCursor(World world,CPos cell,int2 pixel,MouseInput mi)
            { hover=cell; return Valid(world,cell) ? data.Cursor : data.BlockedCursor; }
            protected override IEnumerable<Order> OrderInner(World world,CPos cell,int2 pixel,MouseInput mi)
            {
                if (!Valid(world,cell)) { world.CancelInputMode(); yield break; }
                foreach (var order in base.OrderInner(world,cell,pixel,mi)) yield return order;
            }
            protected override IEnumerable<IRenderable> RenderAnnotations(WorldRenderer wr,World world)
            {
                if (!hover.HasValue || !Valid(world,hover.Value)) yield break;
                var center=world.Map.CenterOfCell(hover.Value);
                var first=data.Kind==SFUltimate.Barrage ? -1 : 0;
                var last=data.Kind==SFUltimate.Barrage ? 1 : 0;
                for (var i=first;i<=last;i++)
                    yield return new CircleAnnotationRenderable(center+new WVec(i*2048,0,0),new WDist(data.Radius*1024),2,manager.Self.Owner.Color);
            }
        }
        public override void Activate(Actor self, Order order, SupportPowerManager manager)
        {
            var cell = self.World.Map.CellContaining(order.Target.CenterPosition);
            if (!self.World.Map.Contains(cell) || !self.Owner.Shroud.IsExplored(cell) || IsTraitDisabled || IsTraitPaused) return;
            base.Activate(self, order, manager);
            PlayLaunchSounds();
            self.World.WorldActor.Trait<SFFactionPowerManager>().Launch(self, data, cell);
        }
    }
    [TraitLocation(SystemActors.World)]
    public class SFFactionPowerManagerInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFFactionPowerManager();
    }
    public class SFFactionPowerManager : ITick, ISync
    {
        sealed class Strike
        {
            public Actor Source;
            public Player Owner;
            public SFFactionPowerInfo Info;
            public CPos Cell;
            public int At, Pulse;
        }
        readonly List<Strike> pending = new List<Strike>();
        readonly Dictionary<Player,int> launches = new Dictionary<Player,int>();
        public int Launches(Player player) => launches.TryGetValue(player,out var count) ? count : 0;
        [Sync] public int PendingHash
        {
            get
            {
                unchecked
                {
                    var h = 17;
                    foreach (var p in launches.OrderBy(p=>p.Key.PlayerActor.ActorID)) { h=h*31+(int)p.Key.PlayerActor.ActorID; h=h*31+p.Value; }
                    foreach (var s in pending)
                        foreach (var n in new[] { (int)s.Source.ActorID, (int)s.Owner.PlayerActor.ActorID, (int)s.Info.Kind, s.Cell.X, s.Cell.Y, s.At, s.Pulse }) h = h * 31 + n;
                    return h;
                }
            }
        }
        public void Launch(Actor source, SFFactionPowerInfo info, CPos cell)
        {
            launches[source.Owner]=Launches(source.Owner)+1;
            if (info.Kind==SFUltimate.Petrification)
                source.World.AddFrameEndTask(w=>w.Add(new SpriteEffect(w.Map.CenterOfCell(cell)+new WVec(0,0,2048),w,"sf_witness","warning","sf_rgba")));
            if (info.Kind==SFUltimate.Nuclear)
            {
                var launchedAt=source.World.WorldTick;
                source.World.AddFrameEndTask(w=>w.Add(new SpriteEffect(
                    ()=>w.Map.CenterOfCell(cell)+new WVec(0,0,12000*System.Math.Max(0,info.WarningTicks-(w.WorldTick-launchedAt))/System.Math.Max(1,info.WarningTicks)),
                    ()=>WAngle.Zero,w,"sf_nuclear","warning","sf_rgba")));
            }
            pending.Add(new Strike { Source = source, Owner = source.Owner, Info = info, Cell = cell, At = source.World.WorldTick + info.WarningTicks });
            // Visible to everyone with vision at the target; no hidden-information leak.
            source.World.AddFrameEndTask(w => w.Add(new FloatingText(w.Map.CenterOfCell(cell), source.Owner.Color,
                info.Kind + " — " + (info.WarningTicks / 25) + "s", Math.Max(25, info.WarningTicks))));
            source.World.AddFrameEndTask(w =>
            {
                var first=info.Kind==SFUltimate.Barrage ? -1 : 0;
                var last=info.Kind==SFUltimate.Barrage ? 1 : 0;
                for (var i=first;i<=last;i++)
                    w.Add(new SFFactionPowerEffect(w.Map.CenterOfCell(cell)+new WVec(i*2048,0,0),info.Radius*1024,info.Kind,
                        Math.Max(1,info.WarningTicks+(info.Kind==SFUltimate.Barrage ? (i+1)*25 : 0)),false));
            });
        }
        public static int DamageFor(SFUltimate kind, bool building, int hp, int max)
        {
            switch (kind)
            {
                case SFUltimate.Dawn: return building ? 25000 : 15000;
                case SFUltimate.Nuclear: return building ? 120000 : 60000;
                case SFUltimate.Hellrift: return building ? 50000 : 30000;
                case SFUltimate.Extinction: return building ? 18000 : 10000;
                case SFUltimate.Rapture: return building ? 45000 : 35000;
                case SFUltimate.Barrage: return building ? 18000 : 9000;
                case SFUltimate.Singularity: return 12000;
                case SFUltimate.Furnace: return building ? 65000 : 10000;
                case SFUltimate.Verdict: return building ? 15000 : hp * 2 < max ? 25000 : 8000;
                default: return 0;
            }
        }
        void Impact(Actor worldActor, Strike strike)
        {
            var world = worldActor.World;
            var center = world.Map.CenterOfCell(strike.Cell);
            // Barrage walks east across three separately warned impact circles.
            if (strike.Info.Kind == SFUltimate.Barrage) center += new WVec((strike.Pulse - 1) * 2048, 0, 0);
            var radius = strike.Info.Radius * 1024;
            var impactCenter=center;
            world.AddFrameEndTask(w=>w.Add(new SFFactionPowerEffect(impactCenter,radius,strike.Info.Kind,45,true)));
            if (strike.Info.Kind==SFUltimate.Petrification || strike.Info.Kind==SFUltimate.Nuclear)
                world.AddFrameEndTask(w=>w.Add(new SpriteEffect(impactCenter,w,strike.Info.Kind==SFUltimate.Petrification?"sf_witness":"sf_nuclear","impact","sf_rgba")));
            foreach (var target in world.FindActorsInCircle(center, new WDist(radius)).Where(SFFactionIdentity.Living).OrderBy(a => a.ActorID).ToArray())
            {
                var health = target.TraitOrDefault<Health>();
                if (health == null || target.OccupiesSpace == null) continue;
                var relation = strike.Owner.RelationshipWith(target.Owner);
                var ally = relation == PlayerRelationship.Ally;
                var enemy = relation == PlayerRelationship.Enemy;
                var mobile = target.Info.HasTraitInfo<MobileInfo>() || target.Info.HasTraitInfo<AircraftInfo>();
                var infantry = target.Info.HasTraitInfo<WithInfantryBodyInfo>();
                void Grant(string name, int ticks) => SFFactionIdentity.Grant(target, this, name, ticks);
                if (strike.Info.Kind==SFUltimate.Petrification)
                {
                    target.TraitOrDefault<SFPetrifiable>()?.Petrify(target,strike.Source,100);
                    continue;
                }
                var damage = (enemy || strike.Info.Kind==SFUltimate.Nuclear) ? DamageFor(strike.Info.Kind, !mobile, health.HP, health.MaxHP) : 0;
                if (damage > 0) target.InflictDamage(strike.Source, new Damage(damage));
                if (!SFFactionIdentity.Living(target)) continue;
                switch (strike.Info.Kind)
                {
                    case SFUltimate.Extinction: if (enemy) Grant("sf-lockdown",75); break;
                    case SFUltimate.Hellrift: if (enemy) Grant("sf-scorched",250); break;
                    case SFUltimate.Rapture: if (enemy) Grant("sf-null",750); break;
                    case SFUltimate.Sanctuary: if (ally && mobile) Grant("sf-sanctum", 375); break;
                    case SFUltimate.Rebellion: if (ally && mobile) Grant("sf-rebellion", 500); break;
                    case SFUltimate.Requiem:
                        if (ally && mobile) Grant("sf-requiem", 500);
                        if (enemy && infantry) Grant("sf-whisper", 300);
                        break;
                    case SFUltimate.Relief:
                        if (ally && mobile) { target.InflictDamage(worldActor, new Damage(-health.MaxHP * 30 / 100)); Grant("sf-relief", 500); }
                        break;
                    case SFUltimate.Covenant:
                        if (ally && infantry) { target.InflictDamage(worldActor, new Damage(-health.MaxHP)); Grant("sf-martyrguard", 300); }
                        break;
                    case SFUltimate.Singularity:
                        // Experimental implosion also locks friendly troops: a deliberate friendly-fire tradeoff.
                        if ((enemy || ally) && mobile) { Grant("sf-lockdown", 150); Grant("sf-null", 750); }
                        break;
                    case SFUltimate.Furnace: if (enemy && mobile) Grant("sf-scorched", 250); break;
                    case SFUltimate.Bloodtide:
                        if (ally && infantry) { target.InflictDamage(worldActor, new Damage(-health.MaxHP / 4)); Grant("sf-bloodtide", 750); }
                        break;
                    case SFUltimate.Silence: if (enemy) Grant("sf-lockdown", 300); break;
                    case SFUltimate.Verdict: if (ally && mobile) Grant("sf-requiem", 300); break;
                }
            }
        }
        void ITick.Tick(Actor self)
        {
            foreach (var strike in pending.Where(s => s.At <= self.World.WorldTick).ToArray())
            {
                // The firing installation must survive, retain ownership and power through the warning.
                var power = SFFactionIdentity.Living(strike.Source) && strike.Source.Owner == strike.Owner
                    ? strike.Source.TraitsImplementing<SFFactionPower>().FirstOrDefault(p => p.Info == strike.Info) : null;
                if (power == null || power.IsTraitDisabled || power.IsTraitPaused) { pending.Remove(strike); continue; }
                Impact(self, strike);
                if ((strike.Info.Kind == SFUltimate.Barrage || strike.Info.Kind == SFUltimate.Extinction) && ++strike.Pulse < 3) strike.At += 25;
                else pending.Remove(strike);
            }
        }
    }
}
