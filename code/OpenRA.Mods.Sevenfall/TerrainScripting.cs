// Original Sevenfall scripting inspection. GPL-3.0-or-later.
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;
namespace OpenRA.Mods.Sevenfall
{
    [ScriptPropertyGroup("Sevenfall terrain inspection")]
    public class SFTerrainMovementProperties : ScriptActorProperties, Requires<MobileInfo>
    {
        public SFTerrainMovementProperties(ScriptContext context, Actor self) : base(context, self) { }
        [Desc("Whether this locomotor permits a terrain cell, ignoring temporary actor occupancy.")]
        public bool CanEnterTerrainCell(CPos cell) => Self.Trait<Mobile>().CanEnterCell(cell, check: BlockedByActor.None);
    }
}
