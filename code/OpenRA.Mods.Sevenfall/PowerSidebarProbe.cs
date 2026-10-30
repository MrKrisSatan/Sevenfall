// Diagnostic-map-only UI acceptance. GPL-3.0-or-later.
using System;
using OpenRA.Mods.Common.Widgets;
using OpenRA.Traits;
using OpenRA.Widgets;

namespace OpenRA.Mods.Sevenfall
{
    [TraitLocation(SystemActors.World)]
    public class SFPowerSidebarProbeInfo : TraitInfo
    {
        public override object Create(ActorInitializer init) => new SFPowerSidebarProbe();
    }

    public class SFPowerSidebarProbe : ITick
    {
        void Check(bool ok, string name) => Console.WriteLine("POWERLIFECYCLE_TEST " + (ok ? "PASS: " : "FAIL: ") + name);
        void ITick.Tick(Actor self)
        {
            var tick = self.World.WorldTick;
            if (self.World.LocalPlayer == null || tick % 25 != 0) return;
            var sidebar = Ui.Root.GetOrNull<ContainerWidget>("SIDEBAR_PRODUCTION");
            if (sidebar == null) return;
            var powers = sidebar.Get<SFDefensePowersWidget>("DEFENSE_POWERS");
            var palette = sidebar.Get<ProductionPaletteWidget>("PRODUCTION_PALETTE");
            var defense = sidebar.Get<ProductionTypeButtonWidget>("DEFENSE");
            var building = sidebar.Get<ProductionTypeButtonWidget>("BUILDING");
            switch (tick / 25)
            {
                case 5: building.OnClick(); break;
                case 6:
                    Check(!powers.IsVisible(), "powers hidden on Buildings tab");
                    defense.OnClick();
                    break;
                case 7:
                    Check(powers.IsVisible() && powers.IconCount == 1, "power appears on Defences tab");
                    Check(palette.Bounds.Y >= powers.Bounds.Y + 47, "defense icons clear the power row");
                    Check(Ui.Root.GetOrNull("SUPPORT_POWERS") == null, "old detached support palette removed");
                    break;
                case 12:
                    Check(!defense.IsDisabled(), "Defences remains selectable without Construction Yard");
                    defense.OnClick();
                    break;
                case 13:
                    Check(powers.IsVisible() && powers.IconCount == 1, "rebuilt installation restores sidebar icon without yard");
                    break;
                case 34: defense.OnClick(); break;
                case 36:
                    Check(powers.IconCount == 17, "captured power icons wrap into six rows");
                    Check(palette.Bounds.Y >= powers.Bounds.Y + 6 * 47, "wrapped powers do not overlap defenses");
                    Check(powers.EventBounds.Bottom < Game.Renderer.Resolution.Height, "all seventeen powers fit viewport");
                    break;
            }
        }
    }
}
