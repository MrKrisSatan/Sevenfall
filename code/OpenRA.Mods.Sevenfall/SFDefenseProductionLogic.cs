#region Copyright & License Information
/*
 * Copyright (c) The OpenRA Developers and Contributors
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

// Adapted from the pinned OpenRA RA sidebar for Sevenfall building-bound powers.

using System;
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Widgets;
using OpenRA.Mods.Common.Widgets;

namespace OpenRA.Mods.Sevenfall
{
	public class SFDefenseProductionLogic : ChromeLogic
	{
		readonly ProductionPaletteWidget palette;
		readonly World world;
		readonly SFDefensePowersWidget powers;
		bool HasPowers => powers.IconCount > 0;
		bool DefenseSelected => palette.CurrentQueue != null && (palette.CurrentQueue.Info.Group ?? palette.CurrentQueue.Info.Type) == "Defense";
		public bool PowersVisible => DefenseSelected && HasPowers;

		void SetupProductionGroupButton(ProductionTypeButtonWidget button)
		{
			if (button == null)
				return;

			// Classic production queues are initialized at game start, and then never change.
			var queues = world.LocalPlayer.PlayerActor.TraitsImplementing<ProductionQueue>()
				.Where(q => (q.Info.Group ?? q.Info.Type) == button.ProductionGroup)
				.ToArray();

			void SelectTab(bool reverse)
			{
				palette.CurrentQueue = queues.FirstOrDefault(q => q.Enabled) ?? (button.ProductionGroup == "Defense" && HasPowers ? queues.FirstOrDefault() : null);

				// When a tab is selected, scroll to the top because the current row position may be invalid for the new tab
				palette.ScrollToTop();

				// Attempt to pick up a completed building (if there is one) so it can be placed
				palette.PickUpCompletedBuilding();
			}

			button.IsDisabled = () => !queues.Any(q => q.AnyItemsToBuild()) && !(button.ProductionGroup == "Defense" && HasPowers);
			button.OnMouseUp = mi => SelectTab(mi.Modifiers.HasModifier(Modifiers.Shift));
			button.OnKeyPress = e => SelectTab(e.Modifiers.HasModifier(Modifiers.Shift));
			button.OnClick = () => SelectTab(false);
			button.IsHighlighted = () => queues.Contains(palette.CurrentQueue);

			var chromeName = button.ProductionGroup.ToLowerInvariant();
			var icon = button.Get<ImageWidget>("ICON");
			icon.GetImageName = () => button.IsDisabled() ? chromeName + "-disabled" :
				(queues.Any(q => q.AllQueued().Any(i => i.Done)) || (button.ProductionGroup == "Defense" && world.LocalPlayer.PlayerActor.Trait<SupportPowerManager>().Powers.Values.Any(p => p.Ready))) ? chromeName + "-alert" : chromeName;
		}

		[ObjectCreator.UseCtor]
		public SFDefenseProductionLogic(Widget widget, World world)
		{
			this.world = world;
			palette = widget.Get<ProductionPaletteWidget>("PRODUCTION_PALETTE");
			powers = widget.Get<SFDefensePowersWidget>("DEFENSE_POWERS");
			powers.IsVisible = () => PowersVisible;
			var baseY = palette.Bounds.Y;
			var totalRows = Math.Max(2, (Game.Renderer.Resolution.Height - widget.Bounds.Y - 40) / 47);
			Action refreshLayout = () => { };

			var background = widget.GetOrNull("PALETTE_BACKGROUND");
			var foreground = widget.GetOrNull("PALETTE_FOREGROUND");
			if (background != null || foreground != null)
			{
				Widget backgroundTemplate = null;
				Widget backgroundBottom = null;
				Widget foregroundTemplate = null;

				if (background != null)
				{
					backgroundTemplate = background.Get("ROW_TEMPLATE");
					backgroundBottom = background.GetOrNull("BOTTOM_CAP");
				}

				if (foreground != null)
					foregroundTemplate = foreground.Get("ROW_TEMPLATE");

				var lastRows = -1;
				var lastPowerRows = -1;
				var updating = false;
				void UpdateBackground(int _, int icons)
				{
					if (updating) return;
					updating = true;
					var powerRows = PowersVisible ? (powers.IconCount + powers.Columns - 1) / powers.Columns : 0;
					palette.MaxIconRowOffset = Math.Max(1, totalRows - powerRows);
					palette.MinimumRows = Math.Max(1, 4 - powerRows);
					palette.Bounds.Y = baseY + powerRows * 47;
					if (lastPowerRows != powerRows)
					{
						palette.ScrollToTop();
						palette.RefreshIcons();
						icons = palette.DisplayedIconCount;
					}
					var rows = Math.Max(palette.MinimumRows, (icons + palette.Columns - 1) / palette.Columns);
					rows = Math.Min(rows, palette.MaxIconRowOffset) + powerRows;
					updating = false;
					if (rows == lastRows && powerRows == lastPowerRows) return;
					lastRows = rows;
					lastPowerRows = powerRows;

					if (background != null)
					{
						background.RemoveChildren();

						var rowHeight = backgroundTemplate.Bounds.Height;
						for (var i = 0; i < rows; i++)
						{
							var row = backgroundTemplate.Clone();
							row.Bounds.Y = i * rowHeight;
							background.AddChild(row);
						}

						if (backgroundBottom == null)
							return;

						backgroundBottom.Bounds.Y = rows * rowHeight;
						background.AddChild(backgroundBottom);
					}

					if (foreground != null)
					{
						foreground.RemoveChildren();

						var rowHeight = foregroundTemplate.Bounds.Height;
						for (var i = 0; i < rows; i++)
						{
							var row = foregroundTemplate.Clone();
							row.Bounds.Y = i * rowHeight;
							foreground.AddChild(row);
						}
					}
				}

				palette.OnIconCountChanged += UpdateBackground;
				powers.OnIconCountChanged += (_, __) => UpdateBackground(0, palette.DisplayedIconCount);
				refreshLayout = () => UpdateBackground(0, palette.DisplayedIconCount);

				// Set the initial palette state
				UpdateBackground(0, 0);
			}

			var typesContainer = widget.Get("PRODUCTION_TYPES");
			foreach (var i in typesContainer.Children)
				SetupProductionGroupButton(i as ProductionTypeButtonWidget);

			var ticker = widget.Get<LogicTickerWidget>("PRODUCTION_TICKER");
			ticker.OnTick = () =>
			{
				powers.RefreshIcons();
				refreshLayout();
				if (palette.CurrentQueue == null || (palette.DisplayedIconCount == 0 && !PowersVisible))
				{
					// Select the first active tab
					foreach (var b in typesContainer.Children)
					{
						if (b is not ProductionTypeButtonWidget button || button.IsDisabled())
							continue;

						button.OnClick();
						break;
					}
				}
			};

			// Hook up scroll up and down buttons on the palette
			var scrollDown = widget.GetOrNull<ButtonWidget>("SCROLL_DOWN_BUTTON");

			if (scrollDown != null)
			{
				scrollDown.OnClick = palette.ScrollDown;
				scrollDown.IsVisible = () => palette.TotalIconCount > palette.MaxIconRowOffset * palette.Columns;
				scrollDown.IsDisabled = () => !palette.CanScrollDown;
			}

			var scrollUp = widget.GetOrNull<ButtonWidget>("SCROLL_UP_BUTTON");

			if (scrollUp != null)
			{
				scrollUp.OnClick = palette.ScrollUp;
				scrollUp.IsVisible = () => palette.TotalIconCount > palette.MaxIconRowOffset * palette.Columns;
				scrollUp.IsDisabled = () => !palette.CanScrollUp;
			}

			refreshLayout();
		}

	}
}
