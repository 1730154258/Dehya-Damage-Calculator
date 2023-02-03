import argparse  
from core.C0_dehya import *

def show_result(notes, weapon, artifact, panel, damage):
    
    result = f'''
    [{notes}] [{weapon} + {artifact}] Damage = {damage['talent_e_damage']:.1f} + {damage['talent_q_damage']:.1f} = {damage['all_damage']:.1f}
    Panel : attack / hp / energy recharge / crit rate / crit dmg = {panel['atk']:.0f} / {panel['hp']:.0f} / {10 ** 2 * panel['energy_recharge']:.1f}% / {10 ** 2 * panel['crit_rate']:.1f}% / {10 ** 2 * panel['crit_dmg']:.1f}% '''

    print(result)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--weapon', type=str, nargs='+', default=['r1_beacon_of_the_reed_sea'])
    parser.add_argument('--artifact', type=str, nargs='+', default=['emblem_of_severed_fate_energy'])
    parser.add_argument('--constellation', type=int, nargs='+', default=[0])
    parser.add_argument('--with_teammates', action="store_true")
    args = parser.parse_args()

    character_info_path = "info/characters/dehya_v3_5_52.json"
    enemy_info_path = "info/enemy.json"

    # teammate_info_paths = ["info/teammates/c0_kazuha_r0.json", "info/teammates/c1_ennett_r6_sapwood.json"] 
    teammate_info_paths = ["info/teammates/c0_kazuha_r1_freedom_sworn.json", "info/teammates/c6_ennett_r1_aquila_favonia.json"] if args.with_teammates else []
    buff_info_paths = ["info/buff/double_pyro.json"] if args.with_teammates else []

    assert len(args.weapon) == len(args.artifact) == len(args.constellation), "The number of weapons and artifacts should be the same"

    for i in range(len(args.weapon)):
        
        weapon_name, artifact_name, constellation = args.weapon[i], args.artifact[i], args.constellation[i]

        weapon_info_path = f"info/weapons/{weapon_name}.json"
        artifact_info_path = f"info/artifact/{artifact_name}.json"
        
        dehya, weapon, artifact, enemy, teammates, buff = initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths, constellation, auto=True)
        panel, damage, artifact_main, artifact_sub_num = dehya.compute(weapon, artifact, teammates, buff, enemy, auto=True)
        show_result(f"C{constellation} " + ("with teammates" if args.with_teammates else "single person"), weapon_name, artifact_name,  panel, damage)