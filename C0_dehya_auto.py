import argparse  
from core.C0_dehya import *

def show_result(notes, detail, weapon, artifact, panel, damage, artifact_main, artifact_sub_num):
    
    result_title = f'''
    [Configuration : {notes}] {weapon} + {artifact} 
    '''

    if detail:
        # main term
        artifact_main_str = ""
        for key in artifact_main:
            if artifact_main[key] != 0 and "base" not in key:
                artifact_main_str += f"{key} {artifact_main[key]} + "
        artifact_main_str = artifact_main_str[:-2]

        # sub term
        artifact_sub_str = ""
        for key in artifact_sub_num:
            artifact_sub_str += f"{key} {artifact_sub_num[key]:.1f} + "
        artifact_sub_str = artifact_sub_str[:-2]

        result_detail = f'''
    [Artifacts] 
    - main term       : {artifact_main_str}
    - sub term number : {artifact_sub_str} 

    [Panel]
    - attack = {panel['atk']}
    - hp     = {panel['hp']} 
    - energy recharge = {panel['energy_recharge']}
    - crit rate = {panel['crit_rate']}
    - crit dmg  = {panel['crit_dmg']}
    - damage plus for e = {panel['dmg_plus_e_coff']}
    - damage plus for q = {panel['dmg_plus_q_coff']}
    - enemy defeat = {panel['enemy_defeat']}
    - enemy resistance = {panel['enemy_resistance']}

    [Damage]''' 
    else :
        result_detail = f'''
    Damage : '''

    result = result_title + result_detail + f'''
    - E = {damage['indomitable_flame_damage']} + {damage['rangeing_flame_damage']} + 4 * {damage['field_damage']} = {damage['talent_e_damage']}
    - Q = 10 * {damage['flame_manes_fist_damage']} + {damage['incineration_drive_damage']} = {damage['talent_q_damage']}
    - All = {damage['all_damage']}
    '''
    print(result)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--weapon', type=str, default='r1_beacon_of_the_reed_sea')
    parser.add_argument('--artifact', type=str, default='emblem_of_severed_fate_energy')
    parser.add_argument('--constellation', type=int, default=0)
    parser.add_argument('--detail', action="store_true")
    args = parser.parse_args()

    character_info_path = "info/characters/dehya_v3_5_52.json"
    enemy_info_path = "info/enemy.json"

    teammate_info_paths = ["info/teammates/c0_kazuha_r0.json", "info/teammates/c1_ennett_r6_sapwood.json"]
    buff_info_paths = ["info/buff/double_pyro.json"]

    weapon_info_path = f"info/weapons/{args.weapon}.json"
    artifact_info_path = f"info/artifact/{args.artifact}.json"

    detail = args.detail
    constellation = args.constellation

    dehya, weapon, artifact, enemy, teammates, buff = initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, [], [], constellation, auto=True)
    panel, damage, artifact_main, artifact_sub_num = dehya.compute(weapon, artifact, teammates, buff, enemy, auto=True,)
    show_result("single person", detail, args.weapon, args.artifact, panel, damage, artifact_main, artifact_sub_num)

    dehya, weapon, artifact, enemy, teammates, buff = initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths, constellation, auto=True)
    panel, damage, artifact_main, artifact_sub_num = dehya.compute(weapon, artifact, teammates, buff, enemy, auto=True)
    show_result("with teammates", detail, args.weapon, args.artifact, panel, damage, artifact_main, artifact_sub_num)
