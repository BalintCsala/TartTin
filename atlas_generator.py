import json
import math
import os
from typing import Optional

from PIL import Image

ATLAS_WIDTH = 64
ATLAS_HEIGHT = 64

DEFAULT_TYPE_ID = 255

atlas = Image.new("RGBA", (ATLAS_WIDTH * 16 * 2, ATLAS_HEIGHT * 16 * 2))
texture_count = 0

replacement_block_model_template_file = open("data/replacement_block_model.json", "r")
replacement_block_model_template = replacement_block_model_template_file.read()
replacement_block_model_template_file.close()

IGNORE_LIST = [
    "button_inventory",
    "door_bottom_rh",
    "door_top_rh",
    "fence_inventory",
    "wall_inventory",
    "thin_block",
    "orientable.json",
    "cube_all.json",
    "cube_bottom_top.json",
    "cube_column.json",
    "cube_top.json",
    "orientable_vertical.json",
    "orientable_with_bottom.json",
    "cube_column_mirrored.json",
    "cube_mirrored_all.json",
    "template_command_block.json",
    "template_glazed_terracotta.json",
    "cube.json",
    "cube_directional.json",
    "template_candle.json",
    "template_four_candles.json",
    "template_three_candles.json",
    "template_two_candles.json",
    "thin_block.json",
    "button_inventory.json",
    "cube_column_horizontal.json",
    "fence_inventory.json",
    "leaves.json",
    "slab.json",
    "stairs.json",
    "template_fence_gate.json",
    "template_three_turtle_eggs.json",
    "template_turtle_egg.json",
    "template_two_turtle_eggs.json",
    "wall_inventory.json",
    "template_farmland.json",
    "template_hanging_lantern.json",
    "template_lantern.json",
    "template_seagrass.json",
    "sculk_sensor.json",
    "template_anvil.json",
    "template_azalea.json",
    "template_campfire.json",
    "template_chorus_flower.json",
    "template_four_turtle_eggs.json",
    "black_shulker_box.json",
    "blue_shulker_box.json",
    "brown_shulker_box.json",
    "cyan_shulker_box.json",
    "gray_shulker_box.json",
    "green_shulker_box.json",
    "light_blue_shulker_box.json",
    "light_gray_shulker_box.json",
    "lime_shulker_box.json",
    "magenta_shulker_box.json",
    "orange_shulker_box.json",
    "pink_shulker_box.json",
    "purple_shulker_box.json",
    "red_shulker_box.json",
    "shulker_box.json",
    "white_shulker_box.json",
    "yellow_shulker_box.json",
    "acacia_sign.json",
    "birch_sign.json",
    "crimson_sign.json",
    "dark_oak_sign.json",
    "jungle_sign.json",
    "oak_sign.json",
    "spruce_sign.json",
    "warped_sign.json",
    "banner.json",
    "barrier.json",
    "bed.json",
    "block.json",
    "button.json",
    "button_pressed.json",
    "chest.json",
    "coral_fan.json",
    "coral_wall_fan.json",
    "crop.json",
    "cross.json",
    "door_bottom.json",
    "door_top_rh.json",
    "door_bottom_rh.json",
    "door_top.json",
    "ender_chest.json",
    "end_portal.json",
    "fence_post.json",
    "fence_side.json",
    "inner_stairs.json",
    "lava.json",
    "light.json",
    "moving_piston.json",
    "outer_stairs.json",
    "pointed_dripstone.json",
    "pressure_plate_down.json",
    "rail_curved.json",
    "rail_flat.json",
    "skull.json",
    "slab_top.json",
    "stem_fruit.json",
    "stem_growth0.json",
    "stem_growth1.json",
    "stem_growth2.json",
    "stem_growth3.json",
    "stem_growth4.json",
    "stem_growth5.json",
    "stem_growth6.json",
    "stem_growth7.json",
    "structure_void.json",
    "template_fence_gate_open.json",
    "template_fence_gate_wall.json",
    "template_fence_gate_wall_open.json",
    "template_fire_floor.json",
    "template_fire_side.json",
    "template_fire_side_alt.json",
    "template_fire_up.json",
    "template_fire_up_alt.json",
    "template_glass_pane_noside.json",
    "template_glass_pane_noside_alt.json",
    "template_glass_pane_post.json",
    "template_glass_pane_side.json",
    "template_glass_pane_side_alt.json",
    "template_item_frame.json",
    "template_item_frame_map.json",
    "template_orientable_trapdoor_open.json",
    "template_orientable_trapdoor_top.json",
    "template_piston.json",
    "template_piston_head.json",
    "template_piston_head_short.json",
    "template_rail_raised_sw.json",
    "template_rail_raised_ne.json",
    "template_single_face.json",
    "template_torch.json",
    "template_torch_wall.json",
    "template_trapdoor_open.json",
    "template_trapdoor_top.json",
    "template_wall_post.json",
    "template_wall_side.json",
    "template_wall_side_tall.json",
    "tinted_cross.json",
    "cube_mirrored.json",
    "piston_extended.json",
    "water.json",
]

TYPES = {
    "cube_column": 1,
    "cube_column_horizontal": 2,
    "leaves": 3,
    "button": 4,
    "button_pressed": 5,
    "door_bottom": 6,
    "door_top": 7,
    "template_fence_gate": 8,
    "template_fence_gate_open": 9,
    "template_fence_gate_wall": 10,
    "template_fence_gate_wall_open": 11,
    "fence_post": 12,
    "fence_side": 13,
    "pressure_plate_up": 14,
    "pressure_plate_down": 15,
    "cross": 16,
    "tinted_cross": 16,
    "slab": 17,
    "slab_top": 18,
    "stairs": 19,
    "inner_stairs": 20,
    "outer_stairs": 21,
    "template_orientable_trapdoor_bottom": 22,
    "template_orientable_trapdoor_open": 23,
    "template_orientable_trapdoor_top": 24,
    "rail_flat": 25,
    "template_rail_raised_ne": 26,
    "template_rail_raised_sw": 27,
    "template_wall_post": 28,
    "template_wall_side": 29,
    "template_wall_side_tall": 30,
    "template_anvil": 31,
    "stem_fruit": 32,
    "template_azalea": 33,
    "cube_bottom_top": 34,
    "cube_mirrored_all": 35,
    "orientable_with_bottom": 36,
    "crop": 37,
    "template_cake_with_candle": 38,
    "template_four_candles": 39,
    "template_candle": 40,
    "template_three_candles": 41,
    "template_two_candles": 42,
    "carpet": 43,
    "template_glazed_terracotta": 44,
    "template_glass_pane_noside": 45,
    "template_glass_pane_noside_alt": 46,
    "template_glass_pane_post": 47,
    "template_glass_pane_side": 48,
    "template_glass_pane_side_alt": 49,
    "orientable": 50,
    "coral_fan": 51,
    "coral_wall_fan": 52,
    "template_single_face": 53,
    "template_campfire": 54,
    "cube": 55,
    "template_command_block": 56,
    "template_chorus_flower": 57,
    "template_trapdoor_bottom": 58,
    "template_trapdoor_open": 59,
    "template_trapdoor_top": 60,
    "template_daylight_detector": 61,
    "cube_column_mirrored": 62,
    "orientable_vertical": 63,
    "template_farmland": 64,
    "template_fire_floor": 65,
    "template_fire_side": 66,
    "template_fire_side_alt": 67,
    "template_fire_up": 68,
    "template_fire_up_alt": 69,
    "template_four_turtle_eggs": 70,
    "template_item_frame": 71,
    "template_item_frame_map": 72,
    "cube_directional": 73,
    "cube_top": 74,
    "template_lantern": 75,
    "template_hanging_lantern": 76,
    "template_cauldron_full": 77,
    "stem_growth0": 78,
    "stem_growth1": 78,
    "stem_growth2": 78,
    "stem_growth3": 78,
    "stem_growth4": 78,
    "stem_growth5": 78,
    "stem_growth6": 78,
    "stem_growth7": 78,
    "observer": 79,
    "template_piston": 80,
    "piston_extended": 81,
    "template_piston_head": 82,
    "template_piston_head_short": 83,
    "pointed_dripstone": 84,
    "flower_pot_cross": 85,
    "tinted_flower_pot_cross": 85,
    "template_cauldron_level1": 86,
    "template_cauldron_level2": 87,
    "rail_curved": 88,
    "redstone_dust_side": 89,
    "redstone_dust_side_alt": 90,
    "template_torch": 91,
    "template_torch_wall": 92,
    "sculk_sensor": 93,
    "template_seagrass": 94,
    "template_turtle_egg": 95,
    "template_three_turtle_eggs": 96,
    "template_two_turtle_eggs": 97,
    "beacon": 98,
    "big_dripleaf": 99,
    "big_dripleaf_full_tilt": 100,
    "big_dripleaf_partial_tilt": 101,
    "big_dripleaf_stem": 102,
    "cactus": 103,
    "campfire_off": 104,
    "chain": 105,
    "chorus_plant": 106,
    "composter": 107,
    "sea_pickle": 108,
    "dirt_path": 109,
    "dragon_egg": 110,
    "dried_kelp_block": 111,
    "enchanting_table": 112,
    "end_portal_frame": 113,
    "end_rod": 114,
    "four_dead_sea_pickles": 115,
    "four_sea_pickles": 116,
    "grass_block": 117,
    "grindstone": 118,
    "honey_block": 119,
    "lectern": 120,
    "lightning_rod": 121,
    "powder_snow": 122,
    "scaffolding": 123,
    "slime_block": 124,
    "small_dripleaf_bottom": 125,
    "small_dripleaf_top": 126,
    "spore_blossom": 127,
    "stonecutter": 128,
    "three_sea_pickles": 129,
    "two_sea_pickles": 130,
    "cube_all": 131,
    "block": 254,
}

TINTS = {
    "dark_oak_leaves":      (121, 192, 91, 255),
    "acacia_leaves":        (188, 183, 87, 255),
    "birch_leaves":         (137, 188, 102, 255),
    "jungle_leaves":        (89, 201, 59, 255),
    "oak_leaves":           (121, 192, 91, 255),
    "spruce_leaves":        (136, 183, 131, 255),
    "grass_block_top":      (121, 192, 91, 255),
    "tall_grass_bottom":    (121, 192, 91, 255),
    "tall_grass_top":       (121, 192, 91, 255),
    "grass":                (121, 192, 91, 255),
    "fern":                 (121, 192, 91, 255),
    "large_fern_bottom":    (121, 192, 91, 255),
    "large_fern_top":       (121, 192, 91, 255)
}


def print_error(msg: str) -> None:
    print(f"[ERROR]: {msg}")


def get_texture(block: str, data: any, name: str) -> Optional[str]:
    if "textures" not in data:
        print_error(f"No textures in block {block}!")
        return

    if name not in data["textures"]:
        print_error(f"Texture {name} not defined in block {block}")
        return

    texture_path: str = data["textures"][name]
    return texture_path.replace("minecraft:", "")


def get_textures(block: str, data: any, texture_names: list[str]) -> list[str]:
    result: list[str] = []
    for texture_name in texture_names:
        texture = get_texture(block, data, texture_name)
        if texture is not None:
            result.append(texture)
    return result


def encode_texture_data(texcoord: tuple[int, int], type_id: int) -> Image:
    r = ((texcoord[0] & 0b111111) << 2) | ((texcoord[1] >> 4) & 0b11)
    g = ((texcoord[1] & 0b1111) << 4) | ((type_id >> 4) & 0b1111)
    b = ((type_id & 0b1111) << 4)  # Last 4 bits are reserved for later
    return Image.new(mode="RGBA", size=(16, 16), color=(r, g, b, 255))


def put_block_into_atlas(block: str, type_id: int, textures: list[str]) -> None:
    global texture_count, replacement_block_model_template

    # If the textures required for this block don't fit into the current line, go immediately to the next line
    # We have enough space to be somewhat wasteful and this helps the GPU side
    remaining_in_row = ATLAS_WIDTH - (texture_count % ATLAS_WIDTH)
    if len(textures) > remaining_in_row:
        texture_count += remaining_in_row

    # Before we put the blocks into the atlas, we replace them with a solid block with the data texture
    block_name = block.replace('.json', '')
    start_x = texture_count % ATLAS_WIDTH
    start_y = texture_count // ATLAS_WIDTH

    replacement = encode_texture_data((start_x, start_y), type_id)
    replacement.save(f"output/assets/minecraft/textures/block/{block_name}_data.png")

    model_replacement_content = replacement_block_model_template.replace("$$BLOCK_NAME$$", block_name)
    model_replacement_file = open(f"output/assets/minecraft/models/block/{block}", "w")
    model_replacement_file.write(model_replacement_content)
    model_replacement_file.close()

    for texture_path in textures:
        main_tex = Image.open(f"data/{texture_path}.png").convert("RGBA")

        tint = TINTS.get(texture_path.replace("block/", ""))
        if tint is not None:
            main_tex_pixels = main_tex.load()
            for dx in range(16):
                for dy in range(16):
                    col = main_tex_pixels[dx, dy]
                    main_tex_pixels[dx, dy] = tuple(map(lambda d: int((d[0] / 255 * d[1] / 255) * 255), zip(col, tint)))

        normal_tex = None
        specular_tex = None
        try:
            normal_tex = Image.open(f"data/{texture_path}_n.png").convert("RGBA").crop((0, 0, 16, 16))
        except FileNotFoundError:
            print(f"[WARN]: No normal for {texture_path}")

        try:
            specular_tex = Image.open(f"data/{texture_path}_s.png").convert("RGBA").crop((0, 0, 16, 16))
        except FileNotFoundError:
            print(f"[WARN]: No specular for {texture_path}")

        x = texture_count % ATLAS_WIDTH
        y = texture_count // ATLAS_WIDTH

        main_tex = main_tex.crop((0, 0, 16, 16))
        atlas.paste(main_tex, (x * 16, y * 16))

        if specular_tex is not None:
            atlas.paste(specular_tex, ((x + ATLAS_WIDTH) * 16, y * 16))

        # _n needs some pre-processing
        normal_map = Image.new("RGBA", (16, 16))

        data_pixels = normal_tex.load() if normal_tex is not None else None

        normal_pixels = normal_map.load()
        for dx in range(16):
            for dy in range(16):
                if normal_tex is not None:
                    if (data_pixels[dx, dy][0] == 0 and data_pixels[dx, dy][1] == 0 and
                            data_pixels[dx, dy][2] == 0) or data_pixels[dx, dy][3] == 0:
                        continue
                    nx = data_pixels[dx, dy][0] / 255 * 2 - 1
                    ny = data_pixels[dx, dy][1] / 255 * 2 - 1
                    nz = math.sqrt(max(1 - nx * nx - ny * ny, 0))
                    normal_pixels[dx, dy] = (
                        int((nx / 2 + 0.5) * 255),
                        int((ny / 2 + 0.5) * 255),
                        int((nz / 2 + 0.5) * 255),
                        255
                    )
                else:
                    normal_pixels[dx, dy] = (128, 128, 255, 255)
        atlas.paste(normal_map, (x * 16, (y + ATLAS_HEIGHT) * 16))
        if normal_tex is not None:
            atlas.paste(normal_tex, ((x + ATLAS_WIDTH) * 16, (y + ATLAS_HEIGHT) * 16))

        texture_count += 1


def process_block(block: str, data: any) -> None:
    if "parent" not in data:
        print_error(f"No parent in block {block}")
        print("\tTextures: ", data["textures"] if "textures" in data else "None")
        return

    parent = data["parent"].replace("minecraft:", "").replace("block/", "")

    if parent in IGNORE_LIST:
        return

    type_id = TYPES.get(parent, DEFAULT_TYPE_ID)
    if type_id == DEFAULT_TYPE_ID:
        print_error(f"Unknown type id for parent {parent} (block: {block})")
        print("Textures: ", data["textures"] if "textures" in data else "None")
        return

    if block == "beacon.json":
        put_block_into_atlas(block, TYPES["beacon"], ["block/glass", "block/obsidian", "block/beacon"])
    elif block == "big_dripleaf.json":
        put_block_into_atlas(block, TYPES["big_dripleaf"], ["block/big_dripleaf_top", "block/big_dripleaf_stem",
                                                            "block/big_dripleaf_side",
                                                            "block/big_dripleaf_tip"])
    elif block == "big_dripleaf_full_tilt.json":
        put_block_into_atlas(block, TYPES["big_dripleaf_full_tilt"], ["block/big_dripleaf_top",
                                                                      "block/big_dripleaf_stem",
                                                                      "block/big_dripleaf_side",
                                                                      "block/big_dripleaf_tip"])
    elif block == "big_dripleaf_partial_tilt.json":
        put_block_into_atlas(block, TYPES["big_dripleaf_partial_tilt"], ["block/big_dripleaf_top",
                                                                         "block/big_dripleaf_stem",
                                                                         "block/big_dripleaf_side",
                                                                         "block/big_dripleaf_tip"])
    elif block == "big_dripleaf_stem.json":
        put_block_into_atlas(block, TYPES["big_dripleaf_stem"], ["block/big_dripleaf_stem"])
    elif block == "cactus.json":
        put_block_into_atlas(block, TYPES["cactus"], ["block/cactus_bottom", "block/cactus_top",
                                                      "block/cactus_side"])
    elif block == "campfire_off.json":
        put_block_into_atlas(block, TYPES["campfire_off"], ["block/campfire_log"])
    elif block == "chain.json":
        put_block_into_atlas(block, TYPES["chain"], ["block/chain"])
    elif block == "chorus_plant.json":
        put_block_into_atlas(block, TYPES["chorus_plant"], ["block/chorus_plant"])
    elif block == "composter.json":
        put_block_into_atlas(block, TYPES["composter"], ["block/composter_top", "block/composter_bottom",
                                                         "block/composter_side"])
    elif block == "dead_sea_pickle.json" or block == "sea_pickle.json":
        put_block_into_atlas(block, TYPES["sea_pickle"], ["block/sea_pickle"])
    elif block == "dirt_path.json":
        put_block_into_atlas(block, TYPES["dirt_path"], ["block/dirt_path_top", "block/dirt_path_side",
                                                         "block/dirt"])
    elif block == "dragon_egg.json":
        put_block_into_atlas(block, TYPES["dragon_egg"], ["block/dragon_egg"])
    elif block == "dried_kelp_block.json":
        put_block_into_atlas(block, TYPES["dried_kelp_block"],
                             ["block/dried_kelp_bottom", "block/dried_kelp_top",
                              "block/dried_kelp_side"])
    elif block == "enchanting_table.json":
        put_block_into_atlas(block, TYPES["enchanting_table"], ["block/enchanting_table_bottom",
                                                                "block/enchanting_table_top",
                                                                "block/enchanting_table_side"])
    elif block == "end_portal_frame.json":
        put_block_into_atlas(block, TYPES["end_portal_frame"], ["block/end_stone",
                                                                "block/end_portal_frame_top",
                                                                "block/end_portal_frame_side"])
    elif block == "end_rod.json":
        put_block_into_atlas(block, TYPES["end_rod"], ["block/end_rod"])
    elif block == "four_dead_sea_pickles.json":
        put_block_into_atlas(block, TYPES["four_dead_sea_pickles"], ["block/sea_pickle"])
    elif block == "four_sea_pickles.json":
        put_block_into_atlas(block, TYPES["four_sea_pickles"], ["block/sea_pickle"])
    elif block == "grass_block.json":
        put_block_into_atlas(block, TYPES["grass_block"], ["block/dirt", "block/grass_block_top",
                                                           "block/grass_block_side"])
    elif block == "grindstone.json":
        put_block_into_atlas(block, TYPES["grindstone"], ["block/grindstone_pivot", "block/grindstone_round",
                                                          "block/grindstone_side", "block/dark_oak_log"])
    elif block == "honey_block.json":
        put_block_into_atlas(block, TYPES["honey_block"], ["block/honey_block_bottom", "block/honey_block_top",
                                                           "block/honey_block_side"])
    elif block == "lectern.json":
        put_block_into_atlas(block, TYPES["lectern"], ["block/oak_planks", "block/lectern_base",
                                                       "block/lectern_front", "block/lectern_sides",
                                                       "block/lectern_top"])
    elif block == "lightning_rod.json" or block == "lightning_rod_on.json":
        put_block_into_atlas(block, TYPES["lightning_rod"], [data["textures"]["texture"]])
    elif block == "powder_snow.json":
        put_block_into_atlas(block, TYPES["powder_snow"], ["block/powder_snow"])
    elif block == "scaffolding_stable.json" or block == "scaffolding_unstable.json":
        put_block_into_atlas(block, TYPES["scaffolding"], ["block/scaffolding_top", "block/scaffolding_side",
                                                           "block/scaffolding_bottom"])
    elif block == "slime_block.json":
        put_block_into_atlas(block, TYPES["slime_block"], ["block/slime_block"])
    elif block == "small_dripleaf_bottom.json":
        put_block_into_atlas(block, TYPES["small_dripleaf_bottom"], ["block/small_dripleaf_stem_bottom"])
    elif block == "small_dripleaf_top.json":
        put_block_into_atlas(block, TYPES["small_dripleaf_top"], ["block/small_dripleaf_top",
                                                                  "block/small_dripleaf_side",
                                                                  "block/small_dripleaf_stem_top"])
    elif block == "spore_blossom.json":
        put_block_into_atlas(block, TYPES["spore_blossom"], ["block/spore_blossom",
                                                             "block/spore_blossom_base"])
    elif block == "stonecutter.json":
        put_block_into_atlas(block, TYPES["stonecutter"], ["block/stonecutter_bottom", "block/stonecutter_top",
                                                           "block/stonecutter_side", "block/stonecutter_saw"])
    elif block == "three_dead_sea_pickles.json" or block == "three_sea_pickles.json":
        put_block_into_atlas(block, TYPES["three_sea_pickles"], ["block/sea_pickle"])
    elif block == "two_dead_sea_pickles.json" or block == "two_sea_pickles.json":
        put_block_into_atlas(block, TYPES["two_sea_pickles"], ["block/sea_pickle"])
    elif parent in ["cube_all", "leaves", "cube_mirrored_all", "template_four_candles", "template_candle",
                    "template_three_candles", "template_two_candles", "template_four_turtle_eggs",
                    "template_three_turtle_eggs", "template_two_turtle_eggs", "template_turtle_egg"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["all"]))
    elif parent in ["cube_column", "cube_column_horizontal", "cube_column_mirrored"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["end", "side"]))
    elif parent in ["button", "button_pressed", "template_fence_gate", "template_fence_gate_open",
                    "template_fence_gate_wall", "template_fence_gate_wall_open", "fence_post", "fence_side",
                    "pressure_plate_up", "pressure_plate_down", "template_orientable_trapdoor_top",
                    "template_orientable_trapdoor_open", "template_orientable_trapdoor_bottom",
                    "template_single_face", "template_chorus_flower", "template_trapdoor_bottom",
                    "template_trapdoor_open", "template_trapdoor_top", "template_seagrass"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["texture"]))
    elif parent in ["door_bottom", "door_top"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["top", "bottom"]))
    elif parent in ["cross", "tinted_cross", "pointed_dripstone"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["cross"]))
    elif parent in ["slab", "slab_top", "stairs", "inner_stairs", "outer_stairs", "cube_bottom_top"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["bottom", "top", "side"]))
    elif parent in ["rail_flat", "template_rail_raised_ne", "template_rail_raised_sw", "rail_curved"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["rail"]))
    elif parent in ["template_wall_post", "template_wall_side", "template_wall_side_tall"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["wall"]))
    elif parent in ["template_anvil"]:
        put_block_into_atlas(block, type_id, ["block/anvil_top", "block/anvil"])
    elif parent in ["stem_fruit", "stem_growth0", "stem_growth1", "stem_growth2", "stem_growth3", "stem_growth4",
                    "stem_growth5", "stem_growth6", "stem_growth7"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["stem"]))
    elif parent in ["template_azalea", "template_daylight_detector", "cube_top"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["top", "side"]))
    elif parent in ["orientable_with_bottom"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["top", "bottom", "side", "front"]))
    elif parent in ["crop"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["crop"]))
    elif parent in ["template_cake_with_candle"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["candle", "bottom", "side", "top"]))
    elif parent in ["carpet"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["wool"]))
    elif parent in ["template_glazed_terracotta"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["pattern"]))
    elif parent in ["template_glass_pane_noside", "template_glass_pane_noside_alt"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["pane"]))
    elif parent in ["template_glass_pane_post", "template_glass_pane_side", "template_glass_pane_side_alt"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["pane", "edge"]))
    elif parent in ["orientable"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["top", "front", "side"]))
    elif parent in ["coral_fan", "coral_wall_fan"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["fan"]))
    elif parent in ["template_campfire"]:
        put_block_into_atlas(block, type_id, ["block/campfire_fire", "block/campfire_log_lit",
                                              "block/campfire_log"])
    elif parent in ["cube", "cube_directional"]:
        put_block_into_atlas(block, type_id,
                             get_textures(block, data, ["north", "south", "east", "west", "up", "down"]))
    elif parent in ["template_command_block"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["front", "back", "side"]))
    elif parent in ["orientable_vertical"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["front", "side"]))
    elif parent in ["template_farmland"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["dirt", "top"]))
    elif parent in ["template_fire_floor", "template_fire_side", "template_fire_side_alt", "template_fire_up",
                    "template_fire_up_alt"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["fire"]))
    elif parent in ["template_item_frame", "template_item_frame_map"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["wood", "back"]))
    elif parent in ["template_lantern", "template_hanging_lantern"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["lantern"]))
    elif parent in ["template_cauldron_full", "template_cauldron_level1", "template_cauldron_level2"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["content", "inside", "top", "bottom", "side"]))
    elif parent in ["observer"] or block == "observer.json":
        put_block_into_atlas(block, type_id,
                             [data["textures"]["bottom"], "block/observer_side", "block/observer_top",
                              "block/observer_front", "block/observer_front"])
    elif parent in ["template_piston"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["platform", "bottom", "side"]))
    elif parent in ["piston_extended"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["bottom", "side", "inside"]))
    elif parent in ["template_piston_head", "template_piston_head_short"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["platform", "side", "unsticky"]))
    elif parent in ["flower_pot_cross", "tinted_flower_pot_cross"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["plant"]))
    elif parent in ["redstone_dust_side", "redstone_dust_side_alt"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["line"]))
    elif parent in ["template_torch", "template_torch_wall"]:
        put_block_into_atlas(block, type_id, get_textures(block, data, ["torch"]))
    elif parent in ["sculk_sensor"]:
        put_block_into_atlas(block, type_id, [data["textures"]["tendrils"], "block/sculk_sensor_bottom",
                                              "block/sculk_sensor_side",
                                              "block/sculk_sensor_tendril_inactive", "block/sculk_sensor_top"])
    else:
        print_error(f"Unknown parent: {parent} (block: {block})")
        print("\tTextures: ", data["textures"] if "textures" in data else "None")


def main() -> None:
    blocks = os.listdir("data/block_models")

    for block in blocks:
        if block in IGNORE_LIST:
            continue

        with open("data/block_models/" + block) as block_file:
            block_data = json.load(block_file)
            process_block(block, block_data)

    atlas.save("output/assets/minecraft/textures/effect/atlas.png")


if __name__ == '__main__':
    main()
