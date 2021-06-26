# Tart Tin

Resourcepack generator for https://github.com/BalintCsala/VanillaPuddingTart

Supports all LabPBR format resource packs

## Usage

Requires python 3.5 or later. [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Automatic/Magic installation (recommended)

The automatic installer only works if you have Minecraft in the default install location. It can download VanillaPuddingTart and apply a resourcepack for you:

 1. If you want to apply a resourcepack, download it first (You can find some at [https://github.com/rre36/lab-pbr/wiki/Resource-Packs](https://github.com/rre36/lab-pbr/wiki/Resource-Packs) or in the ShaderLABS discord)
 2. Either clone the project or download through the `Code` -> `Download as ZIP` button and extract it somewhere
 3. Open a command line and navigate to the project directory
 4. Install the requirements  (`pip install -r requirements.txt`)
 5. Run `py automatic_setup.py` or `python automatic_setup.py` or `python3 automatic_setup.py`
 6. When the installer asks for the resourcepack you want to apply, either enter "none" for no resourcepack (This won't allow for any PBR features) or enter the path to the resourcepack you downloaded. If you give it a path to a ZIP file, make sure the zip contains the assets folder at the root directory, otherwise you'll need to extract it somewhere. If you give it a directory path, the same needs to apply. E.g. If the resourcepack is at `C:\MyResourcePack`, there should be a folder with the path `C:\MyResourcePack\assets`
 7. Do as best as you can to ignore the warnings
 8. When the installer asks you if you want to autoinstall VanillaPuddingTart, say `yes` to let it download it and apply the resourcepack or `no`, if you want to apply it yourself (not recommended)
 9. Launch the game and activate the resourcepack

### Manual installation

The instructions are for Windows users, I don't know Macs, so can't check that and Linux users should be able to guess

 1. Either clone the project or download through the `Code` -> `Download as ZIP` button and extract it somewhere
 2. Put the default assets into the data folder
    1. Go into the minecraft folder (By default `C:\Users\<Name>\AppData\Roaming\.minecraft`)
    2. Find the jar file for the current version `versions\<version>\<version>.jar`
    3. Open it with an archive manager (I recommend https://www.7-zip.org/)
    4. Take the assets folder and put it into the data folder
 3. Open the resource pack you want to convert and place the assets folder into the data folder (The os should merge the folder automatically). If it asks about conflicting files, make sure to choose "replace"
 4. Open a command line and navigate to the project directory
 5. Install the requirements  (`pip install -r requirements.txt`)
 6. Run `py atlas_generator.py`. Ignore the errors and warnings
 7. Take the `assets` folder and put it inside the VanillaPudingTart folder in your resourcepacks folder (If it asks you about conflicting files, tell it to replace them)
    1. The folder you put the assets folder into should already contain one, the OS will automatically merge them for you
 8. Launch the game and activate the resource pack    


## Caveats

VanillaPuddingTart doesn't support block tints (and might never be able to), so the current version pre-multiplies the tintable assets. I chose the most appropriate colors, but most biomes won't work correctly

Animations also don't work, the animated blocks will be static
