using System;
using System.IO;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using OpenRA.Mods.Common.Widgets;
using OpenRA.Mods.Common.Widgets.Logic;
using OpenRA.Widgets;

namespace OpenRA.Mods.Sevenfall
{
	public sealed class SevenfallMainMenuLogic : MainMenuLogic
	{
		const string ChangelogUrl = "https://raw.githubusercontent.com/MrKrisSatan/Sevenfall/main/CHANGELOG.md";
		readonly ScrollPanelWidget panel;
		readonly Widget template;
		readonly int maxHeight;
		bool disposed;

		[ObjectCreator.UseCtor]
		public SevenfallMainMenuLogic(Widget widget, World world, ModData modData)
			: base(widget, world, modData)
		{
			var background = widget.Get("SF_CHANGELOG_BG");
			background.IsVisible = () => menuType != MenuType.None && menuType != MenuType.StartupPrompts;
			var button = background.Get<DropDownButtonWidget>("SF_CHANGELOG_BUTTON");
			button.GetText = () => "Sevenfall Changelog";
			panel = Ui.LoadWidget<ScrollPanelWidget>("NEWS_PANEL", null, new WidgetArgs());
			maxHeight = panel.Bounds.Height;
			template = panel.Get("NEWS_ITEM_TEMPLATE");
			using (var reader = new StreamReader(modData.DefaultFileSystem.Open("sevenfall|CHANGELOG.md")))
				Display(reader.ReadToEnd(), "Included with this build");
			button.OnClick = () => button.AttachPanel(panel, () => { });
			if (Game.Settings.Game.FetchNews)
				_ = Refresh();
		}

		async Task Refresh()
		{
			try
			{
				using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(10), MaxResponseContentBufferSize = 262144 };
				var markdown = await client.GetStringAsync(ChangelogUrl);
				// Validate before replacing the bundled, always-available entry.
				LatestEntry(markdown);
				Game.RunAfterTick(() => { if (!disposed) Display(markdown, "Latest from Sevenfall on GitHub"); });
			}
			catch (Exception)
			{
				// Offline launches retain the bundled entry without an error dialog.
			}
		}

		public static (string Title, string Content) LatestEntry(string markdown)
		{
			var match = Regex.Match(markdown.Replace("\r", ""), @"(?m)^## ([^\n]+)\n([\s\S]*?)(?=^## |\z)");
			if (!match.Success || string.IsNullOrWhiteSpace(match.Groups[2].Value))
				throw new FormatException("No changelog entry found.");
			var body = match.Groups[2].Value.Trim();
			body = Regex.Replace(body, @"\n[ \t]+", " ");
			body = Regex.Replace(body, @"\[([^\]]+)\]\([^)]+\)", "$1");
			body = body.Replace("**", "").Replace("`", "");
			return (match.Groups[1].Value.Trim(), body);
		}

		void Display(string markdown, string source)
		{
			var entry = LatestEntry(markdown);
			panel.RemoveChildren();
			var item = template.Clone();
			var title = item.Get<LabelWidget>("TITLE");
			var heading = WidgetUtils.WrapText(entry.Title, title.Bounds.Width, Game.Renderer.Fonts[title.Font]);
			title.GetText = () => heading;
			var extra = Math.Max(0, Game.Renderer.Fonts[title.Font].Measure(heading).Y - title.Bounds.Height);
			title.Bounds.Height += extra;
			var author = item.Get<LabelWidget>("AUTHOR_DATETIME");
			author.Bounds.Y += extra;
			author.GetText = () => source;
			var label = item.Get<LabelWidget>("CONTENT");
			label.Bounds.Y += extra;
			var content = WidgetUtils.WrapText(entry.Content, label.Bounds.Width, Game.Renderer.Fonts[label.Font]);
			label.GetText = () => content;
			label.Bounds.Height = Game.Renderer.Fonts[label.Font].Measure(content).Y;
			item.Bounds.Height += label.Bounds.Height + extra;
			panel.AddChild(item);
			panel.Layout.AdjustChildren();
			panel.Bounds.Height = Math.Min(panel.ContentHeight, maxHeight);
		}

		protected override void Dispose(bool disposing)
		{
			disposed = true;
			base.Dispose(disposing);
		}
	}
}
