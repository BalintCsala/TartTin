import math
import platform
import os
from pathlib import Path
import shutil
from zipfile import ZipFile
import sys
import time
import atlas_generator
import requests

RESOLUTION_FILES = [
    os.path.join("assets", "minecraft", "shaders", "include", "utils.glsl"),
    os.path.join("assets", "minecraft", "shaders", "program", "raytracer.fsh"),
    os.path.join("assets", "minecraft", "shaders", "program", "raytracer.vsh"),
]


def extract_assets(file_path):
    file = ZipFile(file_path)
    extracted_count = 0

    for i, content in enumerate(file.namelist()):
        # Loading spinning animation
        loading_char = "\\|/-"[int(time.time() * 4) % 4]
        sys.stdout.write(f"\rExtracting required files, this might take a while {loading_char}")
        sys.stdout.flush()
        if content.startswith("assets/minecraft/"):
            file.extract(content, "data")
            extracted_count += 1
    print()
    return extracted_count


def main():
    if platform.system() == "Windows":
        # Windows
        minecraft_folder = os.path.join(os.getenv("APPDATA"), ".minecraft")
    elif platform.system() == "Linux":
        # Linux
        minecraft_folder = os.path.join(str(Path.home()), ".minecraft")
    elif platform.system() == "Darwin":
        # MacOS
        minecraft_folder = os.path.join(str(Path.home()), "Library", "Application Support", "minecraft")
    else:
        print("Unknown or misdetected OS, please use the manual installation method!")
        return

    if not os.path.exists(minecraft_folder):
        print("Couldn't find the Minecraft folder in the default location, please use the manual installation method!")
        return

    version_dir = os.path.join(minecraft_folder, "versions")
    versions = [ver for ver in os.listdir(version_dir) if os.path.isdir(os.path.join(version_dir, ver))]

    if len(versions) == 0:
        print("Couldn't find any downloaded Minecraft versions. Please download one using the launcher or use the "
              "manual installation method!")
        return

    print("Please select a version (make sure it's an unmodified version and is at least 1.17):")
    for i, version in enumerate(versions):
        print(f"  ({i}) {version}")

    while True:
        try:
            index = int(input(f"Enter the selected index (0-{len(versions) - 1}): "))
            if index < 0 or index >= len(versions):
                print("Index out of range!")
            break
        except ValueError:
            print("Please enter a number!")

    jar_path = os.path.join(version_dir, versions[index], versions[index] + ".jar")

    assets_path = os.path.join("data", "assets")
    if os.path.exists(assets_path):
        shutil.rmtree(assets_path)
    os.mkdir(assets_path)

    extract_assets(jar_path)

    print("Finished extracting base game files")
    while True:
        resourcepack_path = input("Please enter the path to the resourcepack zip or folder. "
                                  "It should contain the assets folder inside. If you don't want to use a resourcepack,"
                                  " please enter \"none\": ")
        if "none" in resourcepack_path or os.path.exists(resourcepack_path):
            break
        print("Can't find specified file or folder, try again")

    if "none" not in resourcepack_path:
        if os.path.isfile(resourcepack_path):
            # ZIP file
            extracted_count = extract_assets(resourcepack_path)
            if extracted_count == 0:
                print("The specified zip file didn't have an assets folder at the root level. "
                      "Make sure you don't need to extract it first")
                return
        else:
            # Folder
            print("Copying data from resourcepack...")
            shutil.copytree(os.path.join(resourcepack_path, "assets"), os.path.join("data", "assets"),
                            dirs_exist_ok=True)

        # Copy textures to the appropriate folders to make sure everything works, even if it isn't supported by the
        # shader
        print("Copying textures to the output folder...")
        shutil.copytree(
            os.path.join("data", "assets", "minecraft", "textures"),
            os.path.join("output", "assets", "minecraft", "textures"),
            dirs_exist_ok=True
        )

    atlas_generator.generate()

    print("Successfully generated files!")
    answer = input("Should VanillaPuddingTart be autoinstalled? (y)es / (n)o: ")
    if "y" in answer:
        resourcepack_folder = os.path.join(minecraft_folder, "resourcepacks")
        final_path = os.path.join(resourcepack_folder, "VanillaPuddingTart-main")
        if os.path.exists(final_path):
            shutil.rmtree(final_path)

        print("Downloading VanillaPuddingTart...")
        vpt = requests.get("https://github.com/BalintCsala/VanillaPuddingTart/archive/refs/heads/main.zip")
        vpt_file_path = os.path.join("data", "vpt.zip")
        with open(vpt_file_path, "wb") as vpt_file:
            vpt_file.write(vpt.content)
        print("Successfully downloaded VanillaPuddingTart!")
        vpt_zip = ZipFile(vpt_file_path)
        print("Placing VanillaPuddingTart into the resourcepacks folder...")
        vpt_zip.extractall(resourcepack_folder)

        edit = input("Do you want to edit the default view distance? (y)es / (n)o: ")
        if "y" in edit:
            print("Please enter your game resolution, this isn't always equal to you screen resolution, "
                  "please refer to the GitHub page, to find the required value")
            width = int(input("Horizontal resolution: "))
            height = int(input("Vertical resolution: "))

            max_size = math.floor(pow(width * height, 1 / 3))  # Max possible size, we go down from here
            for i in range(max_size, 0, -1):
                if (width // i) * (height // i) > i and i % 2 == 0:
                    size = i
                    break

            for file_path in RESOLUTION_FILES:
                with open(os.path.join(resourcepack_folder, "VanillaPuddingTart-main", file_path), "r+") as code_file:
                    content = code_file.read()
                    content = content.replace(
                        "VOXEL_STORAGE_RESOLUTION = vec2(1024, 705)",
                        f"VOXEL_STORAGE_RESOLUTION = vec2({width}, {height})"
                    )
                    content = content.replace(
                        "LAYER_SIZE = 88",
                        f"LAYER_SIZE = {size}"
                    )
                    content = content.replace(
                        "MAX_STEPS = 100",
                        f"MAX_STEPS = {int(size * 2.5)}"
                    )
                    code_file.seek(0)
                    code_file.write(content)

        print("Applying generated resourcepack...")
        shutil.copytree(
            os.path.join("output", "assets"),
            os.path.join(final_path, "assets"),
            dirs_exist_ok=True
        )
        print("Finished")


if __name__ == '__main__':
    main()
