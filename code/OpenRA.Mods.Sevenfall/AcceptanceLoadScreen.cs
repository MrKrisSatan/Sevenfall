// Original Sevenfall developer acceptance hooks. GPL-3.0-or-later.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using OpenRA.Mods.Common.LoadScreens;
using OpenRA.Network;
using OpenRA.Traits;

namespace OpenRA.Mods.Sevenfall
{
    public class SFAcceptanceLoadScreen : ILoadScreen
    {
        readonly LogoStripeLoadScreen screen = new LogoStripeLoadScreen();
        OrderManager manager;
        bool startIssued;
        public static bool LoadingSaveAcceptance { get; private set; }
        public void Init(ModData modData, Dictionary<string, string> info) => screen.Init(modData, info);
        public void Display() => screen.Display();
        public bool BeforeLoad() => screen.BeforeLoad();
        public void Dispose()
        {
            Game.LobbyInfoChanged -= Ready;
            Game.ConnectionStateChanged -= ConnectionChanged;
            screen.Dispose();
        }
        public void StartGame(Arguments args)
        {
            var save = args.GetValue("Sevenfall.LoadAcceptance", "");
            LoadingSaveAcceptance = save == "sevenfall-acceptance.orasav";
            if (LoadingSaveAcceptance)
            {
                var path = Path.Combine(Platform.SupportDir, "Saves", Game.ModData.Manifest.Id,
                    Game.ModData.Manifest.Metadata.Version, save);
                var state = new GameSave(path);
                var map = Game.ModData.MapCache[state.GlobalSettings.Map];
                if (Path.GetFileName(map.PackageName) != "save-test" && Path.GetFileName(map.PackageName) != "identitysave-test")
                    throw new InvalidOperationException("Save acceptance is limited to the developer map");
                Game.CreateAndStartLocalServer(map.Uid, new[]
                {
                    Order.FromTargetString("LoadGameSave", save, true),
                    Order.Command("state Ready")
                });
                return;
            }
            if (args.GetValue("Sevenfall.NetworkAcceptance", "") == "2")
            {
                Game.LobbyInfoChanged += Ready;
                Game.ConnectionStateChanged += ConnectionChanged;
            }
            screen.StartGame(args);
        }
        void ConnectionChanged(OrderManager value, string password, NetworkConnection connection) => manager = value;
        void Ready()
        {
            if (manager == null || string.IsNullOrEmpty(manager.LobbyInfo.GlobalSettings.Map)) return;
            var lobby = manager.LobbyInfo;
            var map = Game.ModData.MapCache[lobby.GlobalSettings.Map];
            // This automation is impossible on the published skirmish map list.
            if (map == null || (Path.GetFileName(map.PackageName) != "network-test" && Path.GetFileName(map.PackageName) != "identitynetwork-test")) return;
            var local = lobby.ClientWithIndex(manager.Connection.LocalClientId);
            if (local == null) return;
            if (local.State == Session.ClientState.NotReady)
                manager.IssueOrder(Order.Command("state Ready"));
            else if (!startIssued && local.IsAdmin && lobby.NonBotClients.Count(c => c.Slot != null) == 2
                && lobby.NonBotClients.Where(c => c.Slot != null).All(c => c.IsReady))
            {
                startIssued = true;
                manager.IssueOrder(Order.Command("startgame"));
            }
        }
    }

    [TraitLocation(SystemActors.World)]
    public class SFNetworkProbeInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFNetworkProbe();
    }
    public class SFNetworkProbe : ITick
    {
        int ticks;
        public void Tick(Actor self)
        {
            ticks++;
            if (ticks % 250 == 0)
                Console.WriteLine("NETWORK_TEST SNAPSHOT tick=" + ticks + " hash=" + self.World.SyncHash());
            if (ticks == 1250)
            {
                Console.WriteLine("NETWORK_TEST COMPLETE ticks=1250");
                Game.RunAfterDelay(500, Game.Exit);
            }
        }
    }
}
