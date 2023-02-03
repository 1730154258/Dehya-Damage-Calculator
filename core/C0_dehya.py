import json

term_atk = 0.0498
term_hp = 0.0498
term_crit_rate = 0.033
term_crit_dmg = 0.066
term_energy_recharge = 0.055

class Weapon:

    def __init__(self, weapon_info_path):

        with open(weapon_info_path,'r') as load_f:
            self.weapon_info = json.load(load_f)
            
        # weapon
        self.weapon_atk = self.weapon_info["weapon_atk"]
        self.weapon_sub = self.weapon_info["weapon_sub"]
        self.weapon_bonus = self.weapon_info["weapon_bonus"]


class Artifact:

    def __init__(self, artifact_info_path, auto):

        self.auto = auto
        with open(artifact_info_path,'r') as load_f:
            self.artifact_info = json.load(load_f)
            
        # artifact
        self.artifact_main = self.artifact_info["artifact_main"]
        if not auto:
            self.artifact_sub_num = self.artifact_info["artifact_sub_num"]
        else:
            self.artifact_sub_info = self.artifact_info["artifact_sub_info"]
    

class Teammates:
    
    def __init__(self, teammate_info_paths):

        self.teammate_infos = []
        for teammate_info_path in teammate_info_paths:
            with open(teammate_info_path,'r') as load_f:
                self.teammate_infos.append(json.load(load_f))


class Buff:
    
    def __init__(self, buff_info_paths):

        self.buff_infos = []
        for buff_info_path in buff_info_paths:
            with open(buff_info_path,'r') as load_f:
                self.buff_infos.append(json.load(load_f))


class Enemy:
    
    def __init__(self, enemy_info_path):

        with open(enemy_info_path,'r') as load_f:
            self.enemy_info = json.load(load_f)
        
        # enemy
        self.enemy_defeat = self.enemy_info["defeat"] 
        self.enemy_resistance = self.enemy_info["resistance"]


class Dehya:

    def __init__(self, character_info_path, constellation):

        with open(character_info_path,'r') as load_f:
            character_info = json.load(load_f)
 
        # character
        self.version = character_info["version"]
        self.profile = character_info["profile"]
        self.talent = character_info["talent"]
        self.constellation = constellation

        self.base_hp = self.profile["base_hp"]
        self.base_atk = self.profile["base_atk"]
        self.base_def = self.profile["base_def"]
        self.breakout_hp = self.profile["breakout_hp"]

        talent_e = self.talent["e"]
        talent_q = self.talent["q"]
        
        self.talent_e_level = int(talent_e["level"])
        self.talent_q_level = int(talent_q["level"])

        if self.constellation >= 3:
            self.talent_q_level += 3
        if self.constellation >= 5:
            self.talent_e_level += 3

        self.talent_e = talent_e[str(self.talent_e_level)]
        self.talent_q = talent_q[str(self.talent_q_level)]
        
        self.c1 = True if self.constellation >= 1 else False
        self.c2 = True if self.constellation >= 2 else False
        self.c6 = True if self.constellation >= 6 else False

    def compute_panel_basic(self, weapon, artifact):
        
        self.atk = (self.base_atk + weapon.weapon_atk) * (1 + weapon.weapon_sub['atk'] + weapon.weapon_bonus['atk'] + artifact.artifact_main["atk"] + artifact.artifact_sub_num["atk"] * term_atk) + artifact.artifact_main['base_atk']

        self.hp = self.base_hp * (1 + weapon.weapon_sub['hp'] + weapon.weapon_bonus['hp'] + artifact.artifact_main["hp"] + artifact.artifact_sub_num["hp"] * term_hp + self.breakout_hp) + artifact.artifact_main['base_hp']

        self.energy_recharge = 1 + weapon.weapon_sub['energy_recharge'] + weapon.weapon_bonus['energy_recharge'] + artifact.artifact_main["energy_recharge"] + artifact.artifact_sub_num["energy_recharge"] * term_energy_recharge
        self.energy_recharge += (0.2 if artifact.artifact_info["name"] == "emblem_of_severed_fate" else 0.0) 

        self.crit_rate = 0.05 + weapon.weapon_sub['crit_rate'] + weapon.weapon_bonus['crit_rate'] + artifact.artifact_main["crit_rate"] + artifact.artifact_sub_num["crit_rate"] * term_crit_rate

        self.crit_dmg = 0.5 + weapon.weapon_sub['crit_dmg'] + weapon.weapon_bonus['crit_dmg'] + artifact.artifact_main["crit_dmg"] + artifact.artifact_sub_num["crit_dmg"] * term_crit_dmg

        self.dmg_plus_e_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + artifact.artifact_main['dmg_plus']
        self.dmg_plus_q_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + weapon.weapon_bonus['dmg_plus_q'] + artifact.artifact_main['dmg_plus'] 
    
    def compute_panel_basic_auto(self, weapon, artifact):
        
        miminum_energy_recharge = artifact.artifact_info["miminum_energy_recharge"]
        term_number_crit = artifact.artifact_sub_info["crit"]
        term_number = artifact.artifact_sub_info["term_number"]

        # auto : main term
        self.energy_recharge = 1 + weapon.weapon_sub['energy_recharge'] + weapon.weapon_bonus['energy_recharge']

        if self.energy_recharge + 0.466 > miminum_energy_recharge and self.energy_recharge + (term_number - term_number_crit) * term_energy_recharge > miminum_energy_recharge:
            artifact.artifact_main["atk"] = 0.466
            artifact.artifact_main["energy_recharge"] = 0
        else:
            artifact.artifact_main["atk"] = 0
            artifact.artifact_main["energy_recharge"] = 0.466

        self.crit_rate = 0.05 + weapon.weapon_sub['crit_rate'] + weapon.weapon_bonus['crit_rate']
        self.crit_dmg = 0.5 + weapon.weapon_sub['crit_dmg'] + weapon.weapon_bonus['crit_dmg']

        if self.crit_dmg >= 2 * self.crit_rate:
            artifact.artifact_main["crit_rate"] = 0.311
            artifact.artifact_main["crit_dmg"] = 0
        else :
            artifact.artifact_main["crit_rate"] = 0
            artifact.artifact_main["crit_dmg"] = 0.622


        # auto : sub term
        artifact.artifact_sub_num = {}

        self.energy_recharge += artifact.artifact_main["energy_recharge"] + (0.2 if artifact.artifact_info["name"] == "emblem_of_severed_fate" else 0.0) 
        artifact.artifact_sub_num["energy_recharge"] = max(0, miminum_energy_recharge - self.energy_recharge) / term_energy_recharge

        if artifact.artifact_sub_num["energy_recharge"] > term_number:
            assert False
        elif artifact.artifact_sub_num["energy_recharge"] > term_number - term_number_crit:
            term_number_crit = term_number - artifact.artifact_sub_num["energy_recharge"]
            artifact.artifact_sub_num["atk"] = 0
            artifact.artifact_sub_num["hp"] = 0
        else:
            artifact.artifact_sub_num["atk"] = term_number - term_number_crit - artifact.artifact_sub_num["energy_recharge"]
            artifact.artifact_sub_num["hp"] = 0

        self.crit_rate += artifact.artifact_main["crit_rate"]
        self.crit_dmg += artifact.artifact_main["crit_dmg"]

        if self.crit_dmg >= 2 * self.crit_rate:
            term_num_crit_rate_diff = (self.crit_dmg / 2 - self.crit_rate) / term_crit_rate
            if term_num_crit_rate_diff > term_number_crit:
                artifact.artifact_sub_num["crit_rate"] = term_number_crit
                artifact.artifact_sub_num["crit_dmg"] = 0
            else:
                artifact.artifact_sub_num["crit_rate"] =  term_num_crit_rate_diff + (term_number_crit - term_num_crit_rate_diff) / 2
                artifact.artifact_sub_num["crit_dmg"] = (term_number_crit - term_num_crit_rate_diff) / 2
        else :
            term_num_crit_rate_diff = (self.crit_rate - self.crit_dmg / 2) / term_crit_rate
            if term_num_crit_rate_diff > term_number_crit:
                artifact.artifact_sub_num["crit_rate"] = 0
                artifact.artifact_sub_num["crit_dmg"] = term_number_crit
            else:
                artifact.artifact_sub_num["crit_rate"] = (term_number_crit - term_num_crit_rate_diff) / 2
                artifact.artifact_sub_num["crit_dmg"] = term_num_crit_rate_diff + (term_number_crit - term_num_crit_rate_diff) / 2


        self.atk = (self.base_atk + weapon.weapon_atk) * (1 + weapon.weapon_sub['atk'] + weapon.weapon_bonus['atk'] + artifact.artifact_main["atk"] + artifact.artifact_sub_num["atk"] * term_atk) + artifact.artifact_main['base_atk']

        self.hp = self.base_hp * (1 + weapon.weapon_sub['hp'] + weapon.weapon_bonus['hp'] + artifact.artifact_main["hp"] + artifact.artifact_sub_num["hp"] * term_hp + self.breakout_hp) + artifact.artifact_main['base_hp']

        self.energy_recharge += artifact.artifact_sub_num["energy_recharge"] * term_energy_recharge
        self.crit_rate += artifact.artifact_sub_num["crit_rate"] * term_crit_rate
        self.crit_dmg += artifact.artifact_sub_num["crit_dmg"] * term_crit_dmg

        self.dmg_plus_e_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + artifact.artifact_main['dmg_plus']
        self.dmg_plus_q_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + weapon.weapon_bonus['dmg_plus_q'] + artifact.artifact_main['dmg_plus']

    def compute_panel_basic_auto_c6_part1(self, weapon, artifact):
        
        miminum_energy_recharge = artifact.artifact_info["miminum_energy_recharge"]
        term_number_crit = artifact.artifact_sub_info["crit"]
        term_number = artifact.artifact_sub_info["term_number"]

        # auto : main term
        self.energy_recharge = 1 + weapon.weapon_sub['energy_recharge'] + weapon.weapon_bonus['energy_recharge']

        if self.energy_recharge + 0.466 > miminum_energy_recharge and self.energy_recharge + (term_number - term_number_crit) * term_energy_recharge > miminum_energy_recharge:
            artifact.artifact_main["atk"] = 0.466
            artifact.artifact_main["energy_recharge"] = 0
        else:
            artifact.artifact_main["atk"] = 0
            artifact.artifact_main["energy_recharge"] = 0.466

        self.crit_rate = 0.05 + weapon.weapon_sub['crit_rate'] + weapon.weapon_bonus['crit_rate']
        self.crit_dmg = 0.5 + weapon.weapon_sub['crit_dmg'] + weapon.weapon_bonus['crit_dmg']

        # auto : sub term
        artifact.artifact_sub_num = {}

        self.energy_recharge += artifact.artifact_main["energy_recharge"] + (0.2 if artifact.artifact_info["name"] == "emblem_of_severed_fate" else 0.0) 
        artifact.artifact_sub_num["energy_recharge"] = max(0, miminum_energy_recharge - self.energy_recharge) / term_energy_recharge

        if artifact.artifact_sub_num["energy_recharge"] > term_number:
            assert False
        elif artifact.artifact_sub_num["energy_recharge"] > term_number - term_number_crit:
            term_number_crit = term_number - artifact.artifact_sub_num["energy_recharge"]
            artifact.artifact_sub_num["atk"] = 0
            artifact.artifact_sub_num["hp"] = 0
        else:
            artifact.artifact_sub_num["atk"] = term_number - term_number_crit - artifact.artifact_sub_num["energy_recharge"]
            artifact.artifact_sub_num["hp"] = 0

        self.atk = (self.base_atk + weapon.weapon_atk) * (1 + weapon.weapon_sub['atk'] + weapon.weapon_bonus['atk'] + artifact.artifact_main["atk"] + artifact.artifact_sub_num["atk"] * term_atk) + artifact.artifact_main['base_atk']

        self.hp = self.base_hp * (1 + weapon.weapon_sub['hp'] + weapon.weapon_bonus['hp'] + artifact.artifact_main["hp"] + artifact.artifact_sub_num["hp"] * term_hp + self.breakout_hp) + artifact.artifact_main['base_hp']

        self.energy_recharge += artifact.artifact_sub_num["energy_recharge"] * term_energy_recharge

        self.dmg_plus_e_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + artifact.artifact_main['dmg_plus']
        self.dmg_plus_q_coff = 1 + weapon.weapon_sub['dmg_plus'] + weapon.weapon_bonus['dmg_plus'] + weapon.weapon_bonus['dmg_plus_q'] + artifact.artifact_main['dmg_plus']

        return term_number_crit

    def compute_panel_basic_auto_c6_part2(self, weapon, artifact, term_number_crit):

        # compute magnification

        indomitable_flame_mag = self.talent_e["indomitable_flame"] * self.atk + self.talent_e["c1"] * self.hp
        rangeing_flame_mag = self.talent_e["rangeing_flame"] * self.atk + self.talent_e["c1"] * self.hp
        field_damage_single_mag = self.talent_e["field"] * self.atk + self.talent_e["c1"] * self.hp

        e_mag = indomitable_flame_mag + rangeing_flame_mag + 5 * field_damage_single_mag

        flame_manes_fist_damage_base_mag = self.talent_q["flame_manes_fist"] * self.atk + self.talent_q["c1"] * self.hp
        incineration_drive_damage_mag = self.talent_q["incineration_drive"] * self.atk + self.talent_q["c1"] * self.hp
            
        q_mag_p1 = flame_manes_fist_damage_base_mag * 15
        q_mag_p2 = incineration_drive_damage_mag

        k = 0.15
        a, b, c = e_mag, q_mag_p1, q_mag_p2
        A, B, C = a + b + c, 0.1 * (b + c), k * (10. / 3 * b + 4 * c)
        k1, k2 = B / A, C / A

        r, d = self.crit_rate, self.crit_dmg
        rm, dm = r + 0.331, d + 0.662
        L_main_crit_rate = rm * d + k1 * d + k2 * rm 
        L_main_crit_dmg = r * dm + k1 * dm + k2 * r 

        # auto : main
        if L_main_crit_rate >= L_main_crit_dmg:
            artifact.artifact_main["crit_rate"] = 0.311
            artifact.artifact_main["crit_dmg"] = 0
        else :
            artifact.artifact_main["crit_rate"] = 0
            artifact.artifact_main["crit_dmg"] = 0.622

        # auto : sub term
        self.crit_rate += artifact.artifact_main["crit_rate"]
        self.crit_dmg += artifact.artifact_main["crit_dmg"]

        term_num_crit_rate_diff = (self.crit_rate - self.crit_dmg / 2 + k1 - k2 / 2) / term_crit_rate

        if term_num_crit_rate_diff < 0:
            if -term_num_crit_rate_diff > term_number_crit:
                artifact.artifact_sub_num["crit_rate"] = term_number_crit
                artifact.artifact_sub_num["crit_dmg"] = 0
            else:
                artifact.artifact_sub_num["crit_rate"] =  (term_number_crit - term_num_crit_rate_diff) / 2
                artifact.artifact_sub_num["crit_dmg"] = (term_number_crit + term_num_crit_rate_diff) / 2
        else :
            if term_num_crit_rate_diff > term_number_crit:
                artifact.artifact_sub_num["crit_rate"] = 0
                artifact.artifact_sub_num["crit_dmg"] = term_number_crit
            else:
                artifact.artifact_sub_num["crit_rate"] = (term_number_crit + term_num_crit_rate_diff) / 2
                artifact.artifact_sub_num["crit_dmg"] = (term_number_crit - term_num_crit_rate_diff) / 2

        self.crit_rate += artifact.artifact_sub_num["crit_rate"] * term_crit_rate
        self.crit_dmg += artifact.artifact_sub_num["crit_dmg"] * term_crit_dmg
        
    def compute_artifact_bonus(self, weapon, artifact):

        if artifact.artifact_info["name"] == "emblem_of_severed_fate":
            self.dmg_plus_q_coff += self.energy_recharge * 0.25
        elif artifact.artifact_info["name"] == "atk_atk":
            self.atk += (self.base_atk + weapon.weapon_atk) * 0.18 * 2
        elif artifact.artifact_info["name"] == "atk_hp":
            self.atk += (self.base_atk + weapon.weapon_atk) * 0.18
            self.hp += self.base_atk * 0.20
        elif artifact.artifact_info["name"] == "atk_pyro":
            self.atk += (self.base_atk + weapon.weapon_atk) * 0.18
            self.dmg_plus_e_coff += 0.15
            self.dmg_plus_q_coff += 0.15
        elif artifact.artifact_info["name"] == "atk_burst":
            self.atk += (self.base_atk + weapon.weapon_atk) * 0.18
            self.dmg_plus_q_coff += 0.20
        elif artifact.artifact_info["name"] == "pyro_burst":
            self.dmg_plus_e_coff += 0.15
            self.dmg_plus_q_coff += 0.15
            self.dmg_plus_q_coff += 0.20
        else:
            assert artifact.artifact_info["name"] == "empty"

    def compute_teammates(self, weapon, artifact, teammates, enemy):
    
        for teammate_info in teammates.teammate_infos:
            teammate_info = teammate_info["character"]
            self.atk += teammate_info["base_atk"]
            self.atk += (self.base_atk + weapon.weapon_atk) * teammate_info["atk"]
            self.hp += self.base_hp * teammate_info["hp"]
            self.crit_rate += teammate_info["crit_rate"]
            self.crit_dmg += teammate_info["crit_dmg"]
            self.dmg_plus_e_coff += teammate_info["dmg_plus"]
            self.dmg_plus_q_coff += teammate_info["dmg_plus"]
            self.energy_recharge += teammate_info["energy_recharge"]
            enemy.enemy_defeat += teammate_info["defeat_reduce"]

            resistance_reduce = teammate_info["resistance_reduce"]
            resistance_reduce_part1 = min(max(0, 1 - enemy.enemy_resistance), resistance_reduce)
            resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
            enemy.enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2

    def compute_buff(self, weapon, artifact, buff, enemy):
        
        for buff_info in buff.buff_infos:
            self.atk += (self.base_atk + weapon.weapon_atk) * buff_info["atk"]
            self.hp += self.base_hp * buff_info["hp"]
            self.crit_rate += buff_info["crit_rate"]
            self.crit_dmg += buff_info["crit_dmg"]
            self.dmg_plus_e_coff += buff_info["dmg_plus"]
            self.dmg_plus_q_coff += buff_info["dmg_plus"]
            self.energy_recharge += buff_info["energy_recharge"]
            enemy.enemy_defeat += buff_info["defeat_reduce"]

            resistance_reduce = buff_info["resistance_reduce"]
            resistance_reduce_part1 = min(max(0, 1 - enemy.enemy_resistance), resistance_reduce)
            resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
            enemy.enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2

    def compute_constellation(self):

        if self.c1 >= 1:
            self.hp += self.base_hp * 0.2
        if self.c2 >= 2:
            self.dmg_plus_e_coff += 0.5

    def compute_panel(self, enemy):
        
        panel = {
            "atk" : self.atk,
            "hp" : self.hp,
            "energy_recharge" : self.energy_recharge,
            "crit_rate" : self.crit_rate,
            "crit_dmg" : self.crit_dmg,
            "dmg_plus_e_coff" : self.dmg_plus_e_coff,
            "dmg_plus_q_coff" : self.dmg_plus_q_coff,
            "enemy_defeat" : enemy.enemy_defeat,
            "enemy_resistance" : enemy.enemy_resistance,
        }

        return panel

    def compute_damamge(self, weapon, artifact, buff, enemy):

        # coff
        enemy_coff = enemy.enemy_defeat * enemy.enemy_resistance

        # e
        e_crit_coff = 1 + self.crit_rate * self.crit_dmg
        e_coff = e_crit_coff * self.dmg_plus_e_coff * enemy_coff

        indomitable_flame_damage = (self.talent_e["indomitable_flame"] * self.atk + (self.talent_e["c1"] * self.hp if self.c1 else 0)) * e_coff
        rangeing_flame_damage = (self.talent_e["rangeing_flame"] * self.atk + (self.talent_e["c1"] * self.hp if self.c1 else 0)) * e_coff
        field_damage_single = (self.talent_e["field"] * self.atk + (self.talent_e["c1"] * self.hp if self.c1 else 0)) * e_coff
        field_damage = [field_damage_single for _ in range(4 if not self.c2 else 5)]

        talent_e_damage = indomitable_flame_damage + rangeing_flame_damage + sum(field_damage)

        # q
        if not self.c6:
            q_crit_coff = 1 + self.crit_rate * self.crit_dmg
            q_coff = q_crit_coff * self.dmg_plus_q_coff * enemy_coff
            flame_manes_fist_damage_single = (self.talent_q["flame_manes_fist"] * self.atk + (self.talent_q["c1"] * self.hp if self.c1 else 0)) * q_coff
            flame_manes_fist_damage = [flame_manes_fist_damage_single for _ in range(10)]
            incineration_drive_damage = (self.talent_q["incineration_drive"] * self.atk + (self.talent_q["c1"] * self.hp if self.c1 else 0)) * q_coff
        else:
            q_crit_rate = self.crit_rate + 0.1
            q_coff = self.dmg_plus_q_coff * enemy_coff
            flame_manes_fist_damage_base = (self.talent_q["flame_manes_fist"] * self.atk + self.talent_q["c1"] * self.hp) * q_coff 
            flame_manes_fist_damage = [flame_manes_fist_damage_base * (1 + q_crit_rate * (self.crit_dmg + (i * 0.15 if i <= 4 else 0.6))) for i in range(15)]
            incineration_drive_damage = (self.talent_q["incineration_drive"] * self.atk + self.talent_q["c1"] * self.hp) * q_coff * (1 + q_crit_rate * (self.crit_dmg + 0.6))
            
        talent_q_damage = sum(flame_manes_fist_damage) + incineration_drive_damage

        damage = {
            "indomitable_flame_damage" : indomitable_flame_damage,
            "rangeing_flame_damage" : rangeing_flame_damage,
            "field_damage" : field_damage,
            "talent_e_damage" : talent_e_damage,
            "flame_manes_fist_damage" : flame_manes_fist_damage,
            "incineration_drive_damage" : incineration_drive_damage,
            "talent_q_damage" : talent_q_damage,
            "all_damage" : talent_e_damage + talent_q_damage
        }

        return damage

    def compute(self, weapon, artifact, teammates, buff, enemy, auto):

        if not auto:
            self.compute_panel_basic(weapon, artifact)
        else:
            # self.compute_panel_basic_auto(weapon, artifact)
            if not self.c6:
                self.compute_panel_basic_auto(weapon, artifact)
            else:
                term_number_crit = self.compute_panel_basic_auto_c6_part1(weapon, artifact)


        self.compute_artifact_bonus(weapon, artifact)
        self.compute_teammates(weapon, artifact, teammates, enemy)
        self.compute_buff(weapon, artifact, buff, enemy)
        self.compute_constellation()

        if auto and self.c6:
            self.compute_panel_basic_auto_c6_part2(weapon, artifact, term_number_crit)

        panel = self.compute_panel(enemy)
        damage = self.compute_damamge(weapon, artifact, buff, enemy)


        if not auto:
            return panel, damage
        else:
            return panel, damage, artifact.artifact_main, artifact.artifact_sub_num


def initialize(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths, constellation, auto):
    dehya = Dehya(character_info_path, constellation)
    weapon = Weapon(weapon_info_path)
    artifact = Artifact(artifact_info_path, auto)
    enemy = Enemy(enemy_info_path)
    teammates = Teammates(teammate_info_paths)
    buff = Buff(buff_info_paths)
    return dehya, weapon, artifact, enemy, teammates, buff

