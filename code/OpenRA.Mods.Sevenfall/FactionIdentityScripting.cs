// Original native diagnostic inspection; ordinary gameplay uses normal support-power orders.
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;
namespace OpenRA.Mods.Sevenfall
{
    [ScriptPropertyGroup("Sevenfall faction identity")]
    public class SFIdentityActorProperties : ScriptActorProperties, Requires<SFFactionIdentityInfo>
    {
        public SFIdentityActorProperties(ScriptContext context, Actor self) : base(context, self) { }
        public string ActiveIdentity => Self.Trait<SFFactionIdentity>().ActiveCondition(Self) ?? "none";
        public int IdentitySpeed => Self.TraitsImplementing<ISpeedModifier>().Aggregate(100, (n, m) => n * m.GetSpeedModifier() / 100);
        public int IdentityArmor => Self.TraitsImplementing<IDamageModifier>().Aggregate(100, (n, m) => n * m.GetDamageModifier(null, new Damage(1000)) / 100);
        public void IdentityDamage(Actor target, int damage) => target.InflictDamage(Self, new Damage(damage));
    }
    [ScriptPropertyGroup("Sevenfall faction superweapon")]
    public class SFIdentityPlayerProperties : ScriptPlayerProperties, Requires<SupportPowerManagerInfo>
    {
        public SFIdentityPlayerProperties(ScriptContext context, Player player) : base(context, player) { }
        public bool FactionPowerReady => Player.PlayerActor.Trait<SupportPowerManager>().Powers.Values.Any(p => p.Info is SFFactionPowerInfo && p.Ready);
        public int FactionPowerLaunches => Player.World.WorldActor.Trait<SFFactionPowerManager>().Launches(Player);
        public bool FireFactionPower(CPos cell)
        {
            var manager = Player.PlayerActor.Trait<SupportPowerManager>();
            var power = manager.Powers.Values.FirstOrDefault(p => p.Info is SFFactionPowerInfo && p.Ready);
            if (power == null) return false;
            ((IResolveOrder)manager).ResolveOrder(manager.Self, new Order(power.Key, manager.Self, Target.FromCell(Player.World, cell), false));
            return !power.Ready;
        }
    }
}
