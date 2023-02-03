import argparse  
from core.C0_dehya import *

def show_result(notes, detail, weapon, artifact, panel, damage):
    
    result_title = f'''
    [Configuration : {notes}] {weapon} + {artifact} 
    '''

    if detail:
        result_detail = f'''
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

    dehya, weapon, artifact, enemy, teammates, buff = initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, [], [], constellation, auto=False)
    panel, damage = dehya.compute(weapon, artifact, teammates, buff, enemy, auto=False)
    show_result("single person", detail, args.weapon, args.artifact,  panel, damage)

    dehya, weapon, artifact, enemy, teammates, buff = initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths, constellation, auto=False)
    panel, damage = dehya.compute(weapon, artifact, teammates, buff, enemy, auto=False)
    show_result("with teammates", detail, args.weapon, args.artifact,  panel, damage)
