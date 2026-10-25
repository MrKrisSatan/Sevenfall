// Native renderer regression diagnostics. GPL-3.0-or-later.
using System.Linq;
using OpenRA.Graphics;
using OpenRA.Primitives;
using OpenRA.Scripting;

namespace OpenRA.Mods.Sevenfall
{
    [ScriptGlobal("GraphicsCheck")]
    public class SFGraphicsCheckGlobal : ScriptGlobal
    {
        public SFGraphicsCheckGlobal(ScriptContext context) : base(context) { }

        [Desc("Diagnostic: upload an empty sheet, release its CPU buffer, and read back initialized zero pixels.")]
        public bool EmptySheetReadback()
        {
            using var sheet = new Sheet(SheetType.BGRA, new Size(32, 32));
            sheet.GetTexture();
            sheet.ReleaseBuffer();
            var pixels = sheet.GetData();
            return pixels.Length == 4096 && pixels.All(p => p == 0);
        }

        [Desc("Diagnostic: verify nonempty pixel data survives GPU upload, buffer release and texture readback.")]
        public bool PixelRoundTrip()
        {
            using var sheet = new Sheet(SheetType.BGRA, new Size(32, 32));
            var pixels = sheet.GetData();
            pixels[0] = 23; pixels[1] = 67; pixels[2] = 123; pixels[3] = 255;
            sheet.CommitBufferedData();
            sheet.ReleaseBuffer();
            var restored = sheet.GetData();
            return restored.Length == 4096 && restored[0] == 23 && restored[1] == 67
                && restored[2] == 123 && restored[3] == 255;
        }
    }
}
