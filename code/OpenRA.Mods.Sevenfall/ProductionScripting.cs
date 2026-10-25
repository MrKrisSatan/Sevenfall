// Original Sevenfall game logic. GPL-3.0-or-later.
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Scripting;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [ScriptPropertyGroup("Sevenfall construction")]
    public class SFConstructionProperties : ScriptPlayerProperties, Requires<PlaceBuildingInfo>
    {
        public SFConstructionProperties(ScriptContext context, Player player) : base(context, player) { }

        [Desc("Whether a paid building is complete in a production queue and awaits placement.")]
        public bool BuildingReady(string type) => Player.PlayerActor.TraitsImplementing<ProductionQueue>()
            .Any(q => q.AllQueued().Any(i => i.Item == type && i.Done));

        [Desc("Queue one buildable item using the normal paid production order; returns false if prerequisites or a busy queue prevent it.")]
        public bool QueueProduction(string type)
        {
            var actor = Player.PlayerActor;
            var info = actor.World.Map.Rules.Actors[type];
            var queue = actor.TraitsImplementing<ProductionQueue>()
                .FirstOrDefault(q => q.Enabled && q.CanBuild(info) && q.BuildableItems().Contains(info) && !q.AllQueued().Any());
            if (queue == null)
                return false;
            queue.ResolveOrder(actor, Order.StartProduction(actor, type, 1));
            return queue.AllQueued().Any(i => i.Item == type);
        }

        [Desc("Place a completed building through the normal placement order, including terrain and base-distance validation.")]
        public void PlaceCompletedBuilding(string type, CPos location)
        {
            var actor = Player.PlayerActor;
            var queue = actor.TraitsImplementing<ProductionQueue>()
                .FirstOrDefault(q => q.AllQueued().Any(i => i.Item == type && i.Done));
            if (queue == null)
                return;
            ((IResolveOrder)actor.Trait<PlaceBuilding>()).ResolveOrder(actor,
                new Order("PlaceBuilding", actor, Target.FromCell(actor.World, location), false)
                {
                    TargetString = type,
                    ExtraData = queue.Actor.ActorID
                });
        }
    }
}
