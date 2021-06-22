# Tart Tin

Resourcepack generator for https://github.com/BalintCsala/TartTin

Supports all LabPBR format resource packs

## Usage

This requires Python 3.6 or later
The instructions are for Windows users, I don't know Macs, so can't check that and Linux users should be able to guess

 1. Either clone the project or download through the `Code` -> `Download as ZIP` button and extract it somewhere
 2. Put the default block textures and models into data/block and data/block_models respectively
    1. Go into the minecraft folder (By default `C:\Users\<Name>\AppData\Roaming\.minecraft`)
    2. Find the jar file for the current version `versions\<version>\<version>.jar`
    3. Open it with an archive manager (I recommend https://www.7-zip.org/)
    4. Inside the jar file the textures are in `assets\minecraft\textures\block` and the models are in `assets\minecraft\models\block`. Dump the contents of these into `data\block` and `data\block_models` respectively
    5. Safety check: When sorted by name, the file `acacia_door_bottom.png` should be the first in block and `acacia_button.json` the first in block_models
 3. Open the resource pack you want to convert and find the folder `assets\minecraft\textures\block` and dump the content of it into `data/block`. If it asks you what you want to do with conflicting files, then choose "replace"
 4. Open a command line and navigate to the project directory
 5. Install the requirements  (`pip install -r requirements.txt`)
 6. Run `py atlas_generator.py`. Ignore the errors and warnings
 7. Take the `assets` folder and put it inside the VanillaPudingTart folder in your resourcepacks folder (If it asks you about conflicting files, tell it to replace them)
    1. The folder you put the assets folder into should already contain one, the OS will automatically merge them for you
 8. Launch the game and choose the resource pack    


## Caveats

VanillaPuddingTart doesn't support block tints (and might never be able to), so the current version pre-multiplies the tintable assets. I chose the most appropriate colors, but most biomes won't work correctly

Animations also don't work, the animated blocks will be static