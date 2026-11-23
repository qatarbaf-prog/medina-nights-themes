# Medina Nights · downloadable scenes

The app reads `catalog.json` from this repository. A scene listed here appears
in the app for everyone (with a «جديد» badge) without an app update.

Photos are 1080 × 1920. Each scene has its own folder named after its `id`.

## Add a "reveal" scene (a photo that lights up place by place)

1. Make one lit photo (lamps, lanterns or windows glowing), 9:16.
2. From this folder run:

   ```powershell
   python -I -X utf8 tools/make_reveal_theme.py "C:\path\to\photo.jpg" my_scene "اسم المشهد" "سطر قصير تحت الاسم" --order top
   ```

   `--order`: `top` (top first), `near` (bottom first) or `bright` (brightest first).
   It writes `my_scene/lit.jpg`, `my_scene/night.jpg`, `my_scene/card.jpg` and
   prints the catalog entry.
3. Paste the printed entry into the `themes` list in `catalog.json`.
4. Commit and push. The app picks it up the next time it opens.

To change a scene's photos later, raise its `"version"` so phones download it again.

## Kinds the app can draw

- `reveal`: `files` {`night`, `lit`}, `points` [[x, y, r], …] (0..1), optional
  `glow` [x, y, radius px] and `anchor` (`bottom` | `center`).
- `jars`: `files` {`photo`, `glass`}, `jars` [[left, right, top, floor, mouth, neck], …]
  in photo pixels (three jars), `labelY`.

A new kind of animation needs new code in the app (an update or a code push).
