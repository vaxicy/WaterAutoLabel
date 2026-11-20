# Water Auto Label — 水质自动标注

**English** | [简体中文](README.zh-CN.md)

A native C# mod for **Probably Stolen** (Steam App 4348910, the "Deep Space Pawn Shop" game). Water containers show their true quality automatically, so you never have to run the labeler on each one by hand.

## Features

- Every liquid container displays its **real water quality** from its actual purity — pure water, high-quality water, base water, ghost water, rust water, gutterflow, and more.
- **Manual labels are kept until the water changes.** If the purity stays the same, your label is untouched. When the water is actually purified or contaminated, the displayed label is synced to the true quality.
- Uses the game's own `WaterFeatureHelper.SetPresumedPurity`, so no custom water-quality math and no save edits.
- Works alongside **FraudDetection** (truth-in-labeling mod). Note that once the label is synced to the true quality, FraudDetection will no longer show a fake-vs-real difference for that container — that is the expected result of keeping the label honest.
- Toggle **Auto-label water quality** in the mod settings, on by default.

## Install

1. Download the latest `WaterAutoLabel` zip from the [Releases](https://github.com/vaxicy/WaterAutoLabel/releases) page and unzip it.
2. Copy the `WaterAutoLabel` folder into the game's `Mods` folder, next to `Probably Stolen.exe`. Keep `manifest.xml`, `WaterAutoLabel.dll`, `en.csv` and `zh.csv` together in that folder.
3. Start the game, open **Mods** on the main menu, enable **Water Auto Label**, and restart.
4. Load a save and hover any water container to see its true quality.

Uses the game's built-in mod loader. **MelonLoader is not required.**

## How it works

Every 0.5 seconds the mod scans all owned liquid containers and compares each container's purity with the last value it saw. Only containers whose purity changed are re-labeled through the game's own water-quality update. Nothing is written to your save.

## Troubleshooting

Search `Player.log` in your save directory for `[WaterAutoLabel]`:

- `auto-labeled N water containers` — the mod is working; N is how many containers just changed quality.
- If water never updates, make sure the mod is enabled in the Mods menu and that the four files (manifest, DLL, en.csv, zh.csv) are all directly inside `Mods\WaterAutoLabel\`.

Post the relevant log line to Issues if something still looks wrong.

## Uninstall

Close the game and delete the `Mods\WaterAutoLabel` folder. Saves are unaffected.

## About

The feature design and acceptance criteria are mine; the implementation and the reverse-engineering work were done with AI assistance.

## License

MIT. The game itself, its name, and its assets belong to Questing Goose Studio. This project contains no game assets.
