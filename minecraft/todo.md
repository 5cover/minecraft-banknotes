i think design package goes too far into a professional projection? i ran it on v4, and well, it created monochrome renders, unreproducible pngs from flattened layers, created artificial frames that don't exist in the export file. i think the prompt is just trying to do too much at once. it created a 237mb archive.

what i actually want is more simple than this. separate elements.

- so we can turn into assets what can be turned into an asset
- layer composition so the final arrangment becomes tweakable
- separate AI generation from the final, deterministic composition

the idea is this : the package should contain intermediates and the finished notes built deterministically from it. it should prefer vector images when possible. it should be self contained, and include all provided assets.
so the final result can be seen without spending 30 minutes reconstructing everything in paint.net

markdown files contain documentation with the reproducible construction procedure.
python scripts used for construction are also provided

layers:

- generated: the scene plate
- generated: the ore label shape, decorations and field, but it is empty : the isometric block is an asset
- generated: the frame, details and decorations
- asset: each isometric ore block
- asset: eu map
- asset: eu flag
- asset: EURO / EYPO / EBPO lettering
(and anything else i'm forgetting)

i have also acquried the minecraft typeface i want to use for the value and EURO lettering. how should we use it? should we refer to it in svg text elements hoping the renderer knows the font, or use the ttf file directly?

design work can compose these layers into a PDN files, maybe with python package pypdn. I don't know if you have the ability to work with Paint.NET, but this is what i use.

one thing that matters, and i think the workflow file needs to emphasize on this, is maintain a consistent style and visual grammar between scene plates of different denominations. use broadly the same level of detail. i've had instances where the AI imagines another style, smooths blocks, or changes texture between denominations.
