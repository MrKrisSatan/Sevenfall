"""Adapt the pinned RA sidebar to building-bound, automatic Defences powers."""
def integrate(text):
    start = text.index("\t\tContainer@SUPPORT_POWERS:\n")
    end = text.index("\t\tSupportPowerTimer@SUPPORT_POWER_TIMER:", start)
    text = text[:start] + text[end:]
    text = text.replace("Logic: ClassicProductionLogic", "Logic: SFDefenseProductionLogic")
    needle = "\t\t\t\tLogicTicker@PRODUCTION_TICKER:\n"
    assert text.count(needle) == 1, "Unexpected upstream production sidebar"
    powers = """\t\t\t\tSFDefensePowers@DEFENSE_POWERS:
\t\t\t\t\tX: 42
\t\t\t\t\tY: 1
\t\t\t\t\tColumns: 3
\t\t\t\t\tIconSize: 62, 46
\t\t\t\t\tIconMargin: 1
\t\t\t\t\tIconSpriteOffset: -1, -1
\t\t\t\t\tTooltipContainer: TOOLTIP_CONTAINER
\t\t\t\t\tReadyText: supportpowers-support-powers-palette.ready
\t\t\t\t\tHoldText: supportpowers-support-powers-palette.hold
\t\t\t\t\tHotkeyPrefix: SupportPower
\t\t\t\t\tHotkeyCount: 6
"""
    return text.replace(needle, powers + needle)
