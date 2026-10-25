// Sevenfall UI asset validation without requiring a graphics device or RA content.
using System;
using System.IO;
using OpenRA.Graphics;

namespace OpenRA.Mods.Sevenfall
{
    public sealed class CheckChrome : IUtilityCommand
    {
        string IUtilityCommand.Name => "--sf-check-chrome";
        bool IUtilityCommand.ValidateArguments(string[] args) => args.Length == 1;

        [Desc("Validate merged Sevenfall UI collections and image bounds.")]
        void IUtilityCommand.Run(Utility utility, string[] args)
        {
            Game.ModData = utility.ModData;
            ChromeProvider.Initialize(utility.ModData);
            var count = 0;
            foreach (var item in ChromeProvider.Collections)
            {
                var c = item.Value;
                if (c.Image == null || !c.Image.StartsWith("sevenfall|art/ui/", StringComparison.Ordinal))
                    continue;
                var scale = 0;
                foreach (var file in new[] { c.Image, c.Image2x, c.Image3x })
                {
                    scale++;
                    if (file == null)
                        throw new InvalidDataException("Missing density image: " + item.Key);
                    using var stream = utility.ModData.DefaultFileSystem.Open(file);
                    var header = new byte[24];
                    if (stream.Read(header, 0, 24) != 24)
                        throw new InvalidDataException(file);
                    int ReadInt(int offset) => (header[offset] << 24) | (header[offset + 1] << 16)
                        | (header[offset + 2] << 8) | header[offset + 3];
                    var width = ReadInt(16) / scale;
                    var height = ReadInt(20) / scale;
                    void Check(int x, int y, int w, int h)
                    {
                        if (x < 0 || y < 0 || w < 0 || h < 0 || x + w > width || y + h > height)
                            throw new InvalidDataException("Chrome outside image: " + item.Key + " / " + file);
                    }
                    foreach (var region in c.Regions.Values)
                        Check(region.X, region.Y, region.Width, region.Height);
                    if (c.PanelRegion != null)
                    {
                        var p = c.PanelRegion;
                        if (p.Length != 8)
                            throw new InvalidDataException(item.Key);
                        Check(p[0], p[1], p[2] + p[4] + p[6], p[3] + p[5] + p[7]);
                    }
                }
                count++;
            }
            if (count < 100)
                throw new InvalidDataException("Sevenfall UI collections not loaded.");
            Console.WriteLine($"PASS: {count} merged Sevenfall chrome collections at 1x/2x/3x.");
        }
    }
}
