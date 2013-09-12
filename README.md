vuforia-utils
=============

Some scripts and memos on Vuforia framefork. obj2h.py to start with.

obj2h.py
--------
This script is just a simple utility and it *does not* (not even remotely) implement [OBJ.spec](http://www.martinreddy.net/gfx/3d/OBJ.spec) to its full extend. MTL files are ignored completely. The only things you get are static arrays of properly arranged vertices, normals, texture coordinates and indices, which is actually what worked for me e.g. on this nice model of [Cacodemon](http://www.blendswap.com/blends/view/58584).

Warning: This simple script expects a one mesh in a one group, in another words: vertices, text coords, normals, faces respectively. You might either select and join the groups in Blender or do a simple fix in the script :-)

I would like to give a credit to **Ahl** from [gamedev](http://www.gamedev.net/topic/600614-creating-vbo-data-from-obj-files/)
and to **jctjct3** on [stackoverflow](http://stackoverflow.com/questions/15933908/android-obj-to-vbo-loader-garbage-collection-loop-how-to-improve). Last but not least, one might find [Modern_OpenGL_Tutorial](http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Load_OBJ
) useful.
