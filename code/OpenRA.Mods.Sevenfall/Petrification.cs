// Original Sevenfall salt judgement. GPL-3.0-or-later.
using OpenRA.Mods.Common.Effects;
using OpenRA.Scripting;
using OpenRA.Traits;
namespace OpenRA.Mods.Sevenfall
{
    public class SFPetrifiableInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFPetrifiable();
    }
    public class SFPetrifiable : ITick, ISync
    {
        [Sync] int crumbleAt;
        Actor attacker;
        [Sync] public int AttackerId => unchecked((int)(attacker?.ActorID ?? 0));
        public bool IsPetrified => crumbleAt != 0;
        public void Petrify(Actor self, Actor source, int duration)
        {
            if (IsPetrified || !SFFactionIdentity.Living(self)) return;
            attacker=source;
            crumbleAt=self.World.WorldTick+duration;
            SFFactionIdentity.Grant(self,this,"sf-petrified",duration+25);
            self.CancelActivity();
        }
        void ITick.Tick(Actor self)
        {
            if (!IsPetrified || self.World.WorldTick<crumbleAt) return;
            var pos=self.CenterPosition;
            self.World.AddFrameEndTask(w=>w.Add(new SpriteEffect(pos,w,"sf_witness","crumble","sf_rgba")));
            self.Kill(attacker);
            crumbleAt=0;
        }
    }
    [ScriptPropertyGroup("Sevenfall petrification")]
    public class SFPetrificationProperties : ScriptActorProperties, Requires<SFPetrifiableInfo>
    {
        public SFPetrificationProperties(ScriptContext context,Actor self):base(context,self){}
        public bool IsPetrified => Self.Trait<SFPetrifiable>().IsPetrified;
    }
}
