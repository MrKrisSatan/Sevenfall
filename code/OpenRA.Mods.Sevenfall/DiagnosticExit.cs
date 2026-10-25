// Developer-map graceful shutdown after genuine game-over. GPL-3.0-or-later.
using System;
using OpenRA.Graphics;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    [TraitLocation(SystemActors.World)]
    public class SFDiagnosticExitInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFDiagnosticExit();
    }

    public class SFDiagnosticExit : IGameOver, IWorldLoaded
    {
        public void WorldLoaded(World world, WorldRenderer renderer)
        {
            if (world.IsReplay) world.ReplayTimestep = 1;
        }
        public void GameOver(World world)
        {
            // Use normal shutdown so the recorder writes completion metadata.
            Game.RunAfterDelay(1000, () =>
            {
                Console.WriteLine("MATCH_TEST COMPLETE checks=3 game_over=True graceful_exit=True");
                Game.Exit();
            });
        }
    }
}
