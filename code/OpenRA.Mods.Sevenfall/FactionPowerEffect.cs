// Original code-drawn superweapon telegraphs; no external game artwork.
using System.Collections.Generic;
using OpenRA.Effects;
using OpenRA.Graphics;
using OpenRA.Mods.Common.Graphics;
using OpenRA.Primitives;
namespace OpenRA.Mods.Sevenfall
{
    public class SFFactionPowerEffect : IEffect, IEffectAnnotation
    {
        readonly WPos center;
        readonly int radius, total;
        readonly SFUltimate kind;
        readonly bool impact;
        int remaining;
        static readonly string[] Colors = { "FFF2A8", "8DEAFF", "ED906A", "C1B4DB", "F7B25F", "78D6A6", "F2E0CF", "58D9EF", "F75B32", "E53064", "A280F0", "CF7DFF" };
        public SFFactionPowerEffect(WPos center, int radius, SFUltimate kind, int duration, bool impact)
        { this.center=center; this.radius=radius; this.kind=kind; this.impact=impact; total=remaining=duration; }
        void IEffect.Tick(World world)
        { if (--remaining<=0) world.AddFrameEndTask(w=>w.Remove(this)); }
        IEnumerable<IRenderable> IEffect.Render(WorldRenderer wr) { yield break; }
        IEnumerable<IRenderable> IEffectAnnotation.RenderAnnotation(WorldRenderer wr)
        {
            if (wr.World.FogObscures(center) || wr.World.ShroudObscures(center)) yield break;
            Color.TryParse(Colors[(int)kind],out var baseColor);
            var color=Color.FromArgb(impact ? 200 : 160,baseColor);
            // Warning boundary remains accurate; impact rings expand entirely within it.
            yield return new CircleAnnotationRenderable(center,new WDist(radius),impact ? 3 : 2,color);
            var phase=impact ? (total-remaining)*radius/total : (remaining%25)*radius/25;
            for (var i=0;i<1+(int)kind%3;i++)
                yield return new CircleAnnotationRenderable(center,new WDist((phase+i*radius/3)%radius),1,color);
        }
    }
}
