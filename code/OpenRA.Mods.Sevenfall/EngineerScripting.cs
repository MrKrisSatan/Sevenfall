// Original Sevenfall game logic. GPL-3.0-or-later.
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [ScriptPropertyGroup("Sevenfall engineering")]
    public class SFBridgePostProperties : ScriptActorProperties, Requires<BridgeHutInfo>
    {
        public SFBridgePostProperties(ScriptContext context, Actor self) : base(context, self) { }
        [Desc("Current damage state of the bridge connected to this repair post.")]
        public string BridgeDamageState => Self.Trait<BridgeHut>().BridgeDamageState.ToString();
    }

    [ScriptPropertyGroup("Sevenfall engineering")]
    public class SFEngineerProperties : ScriptActorProperties, Requires<RepairsBridgesInfo>
    {
        public SFEngineerProperties(ScriptContext context, Actor self) : base(context, self) { }

        [Desc("Issue the normal bridge repair order to a bankside repair post.")]
        public void RepairBridge(Actor target)
        {
            ((IResolveOrder)Self.Trait<RepairsBridges>()).ResolveOrder(Self,
                new Order("RepairBridge", Self, Target.FromActor(target), false));
        }
    }
}
