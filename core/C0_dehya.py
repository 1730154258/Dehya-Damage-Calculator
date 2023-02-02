import json

def compute(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths):
    ## Calculate the panel and damage

    #################
    ##  read info  ##
    #################
    with open(character_info_path,'r') as load_f:
        character_info = json.load(load_f)
    with open(weapon_info_path,'r') as load_f:
        weapon_info = json.load(load_f)
    with open(artifact_info_path,'r') as load_f:
        artifact_info = json.load(load_f)
    with open(enemy_info_path,'r') as load_f:
        enemy_info = json.load(load_f)
    teammate_infos = []
    for teammate_info_path in teammate_info_paths:
        with open(teammate_info_path,'r') as load_f:
            teammate_infos.append(json.load(load_f))
    buff_infos = []
    for buff_info_path in buff_info_paths:
        with open(buff_info_path,'r') as load_f:
            buff_infos.append(json.load(load_f))

    # enemy
    enemy_defeat = enemy_info["defeat"] 
    enemy_resistance = enemy_info["resistance"] 

    # character
    version = character_info["version"]
    profile = character_info["profile"]
    talent = character_info["talent"]

    base_hp = profile["base_hp"]
    base_atk = profile["base_atk"]
    base_def = profile["base_def"]
    breakout_hp = profile["breakout_hp"]

    talent_e = talent["e"]
    talent_e = talent_e[str(int(talent_e["level"]))]
    talent_q = talent["q"]
    talent_q = talent_q[str(int(talent_q["level"]))]

    # weapon
    weapon_atk = weapon_info["weapon_atk"]
    weapon_sub = weapon_info["weapon_sub"]
    weapon_bonus = weapon_info["weapon_bonus"]

    # artifact
    artifact_main = artifact_info["artifact_main"]
    artifact_sub_num = artifact_info["artifact_sub_num"]

    term_atk = 0.0498
    term_hp = 0.0498
    term_crit_rate = 0.033
    term_crit_dmg = 0.066
    term_energy_recharge = 0.055

    #################
    ##   panel     ##
    #################

    atk = (base_atk + weapon_atk) * (1 + weapon_sub['atk'] + weapon_bonus['atk'] + artifact_main["atk"] + artifact_sub_num["atk"] * term_atk) + artifact_main['base_atk']

    hp = base_hp * (1 + weapon_sub['hp'] + weapon_bonus['hp'] + artifact_main["hp"] + artifact_sub_num["hp"] * term_hp + breakout_hp) + artifact_main['base_hp']

    energy_recharge = 1 + weapon_sub['energy_recharge'] + weapon_bonus['energy_recharge'] + artifact_main["energy_recharge"] + artifact_sub_num["energy_recharge"] * term_energy_recharge

    crit_rate = 0.05 + weapon_sub['crit_rate'] + weapon_bonus['crit_rate'] + artifact_main["crit_rate"] + artifact_sub_num["crit_rate"] * term_crit_rate

    crit_dmg = 0.5 + weapon_sub['crit_dmg'] + weapon_bonus['crit_dmg'] + artifact_main["crit_dmg"] + artifact_sub_num["crit_dmg"] * term_crit_dmg

    dmg_plus_e_coff = 1 + weapon_sub['dmg_plus'] + weapon_bonus['dmg_plus'] + artifact_main['dmg_plus']
    dmg_plus_q_coff = 1 + weapon_sub['dmg_plus'] + weapon_bonus['dmg_plus']+ artifact_main['dmg_plus'] + weapon_bonus['dmg_plus_q']


    ######################
    ##  artifact bonus  ##
    ######################

    if artifact_info["name"] == "emblem_of_severed_fate":
        energy_recharge += 0.2
        dmg_plus_q_coff += energy_recharge * 0.25
    elif artifact_info["name"] == "atk_atk":
        atk += (base_atk + weapon_atk) * 0.18 * 2
    elif artifact_info["name"] == "atk_hp":
        atk += (base_atk + weapon_atk) * 0.18
        hp += base_atk * 0.20
    elif artifact_info["name"] == "atk_pyro":
        atk += (base_atk + weapon_atk) * 0.18
        dmg_plus_e_coff += 0.15
        dmg_plus_q_coff += 0.15
    elif artifact_info["name"] == "atk_burst":
        atk += (base_atk + weapon_atk) * 0.18
        dmg_plus_q_coff += 0.20
    elif artifact_info["name"] == "pyro_burst":
        dmg_plus_e_coff += 0.15
        dmg_plus_q_coff += 0.15
        dmg_plus_q_coff += 0.20
    else:
        assert False

    #################
    ##  teammates  ##
    #################
    for teammate_info in teammate_infos:
        teammate_info = teammate_info["character"]
        atk += teammate_info["base_atk"]
        atk += (base_atk + weapon_atk) * teammate_info["atk"]
        hp += base_hp * teammate_info["hp"]
        crit_rate += teammate_info["crit_rate"]
        crit_dmg += teammate_info["crit_dmg"]
        dmg_plus_e_coff += teammate_info["dmg_plus"]
        dmg_plus_q_coff += teammate_info["dmg_plus"]
        energy_recharge += teammate_info["energy_recharge"]
        enemy_defeat += teammate_info["defeat_reduce"]

        resistance_reduce = teammate_info["resistance_reduce"]
        resistance_reduce_part1 = min(max(0, 1 - enemy_resistance), resistance_reduce)
        resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
        enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2

    #############
    ##  buffs  ##
    #############
    for buff_info in buff_infos:
        atk += (base_atk + weapon_atk) * buff_info["atk"]
        hp += base_hp * buff_info["hp"]
        crit_rate += buff_info["crit_rate"]
        crit_dmg += buff_info["crit_dmg"]
        dmg_plus_e_coff += buff_info["dmg_plus"]
        dmg_plus_q_coff += buff_info["dmg_plus"]
        energy_recharge += buff_info["energy_recharge"]
        enemy_defeat += buff_info["defeat_reduce"]

        resistance_reduce = buff_info["resistance_reduce"]
        resistance_reduce_part1 = min(max(0, 1 - enemy_resistance), resistance_reduce)
        resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
        enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2


    ###############
    ##  compute  ##
    ###############

    # coff
    crit_coff = 1 + crit_rate * crit_dmg
    enemy_coff = enemy_defeat * enemy_resistance

    # e
    e_coff = crit_coff * dmg_plus_e_coff * enemy_coff
    indomitable_flame_damage = talent_e["indomitable_flame"] * atk * e_coff
    rangeing_flame_damage = talent_e["rangeing_flame"] * atk * e_coff
    field_damage = talent_e["field"] * atk * e_coff

    talent_e_damage = indomitable_flame_damage + rangeing_flame_damage + 4 * field_damage

    # q
    q_coff = crit_coff * dmg_plus_q_coff * enemy_coff
    flame_manes_fist_damage = talent_q["flame_manes_fist"] * atk * q_coff
    incineration_drive_damage = talent_q["incineration_drive"] * atk * q_coff

    talent_q_damage = 10 * flame_manes_fist_damage + incineration_drive_damage

    # results
    panel = {
        "atk" : atk,
        "hp" : hp,
        "energy_recharge" : energy_recharge,
        "crit_rate" : crit_rate,
        "crit_dmg" : crit_dmg,
        "dmg_plus_e_coff" : dmg_plus_e_coff,
        "dmg_plus_q_coff" : dmg_plus_q_coff,
        "enemy_defeat" : enemy_defeat,
        "enemy_resistance" : enemy_resistance,
    }

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

    return panel, damage

def compute_auto(character_info_path, weapon_info_path, artifact_info_path, enemy_info_path, teammate_info_paths, buff_info_paths):
    ## Given the artifact's sub term num, mininum energy recharge and crit term number, calculate the panel and damage

    #################
    ##  read info  ##
    #################
    with open(character_info_path,'r') as load_f:
        character_info = json.load(load_f)
    with open(weapon_info_path,'r') as load_f:
        weapon_info = json.load(load_f)
    with open(artifact_info_path,'r') as load_f:
        artifact_info = json.load(load_f)
    with open(enemy_info_path,'r') as load_f:
        enemy_info = json.load(load_f)
    teammate_infos = []
    for teammate_info_path in teammate_info_paths:
        with open(teammate_info_path,'r') as load_f:
            teammate_infos.append(json.load(load_f))
    buff_infos = []
    for buff_info_path in buff_info_paths:
        with open(buff_info_path,'r') as load_f:
            buff_infos.append(json.load(load_f))

    # enemy
    enemy_defeat = enemy_info["defeat"] 
    enemy_resistance = enemy_info["resistance"] 

    # character
    version = character_info["version"]
    profile = character_info["profile"]
    talent = character_info["talent"]

    base_hp = profile["base_hp"]
    base_atk = profile["base_atk"]
    base_def = profile["base_def"]
    breakout_hp = profile["breakout_hp"]

    talent_e = talent["e"]
    talent_e = talent_e[str(int(talent_e["level"]))]
    talent_q = talent["q"]
    talent_q = talent_q[str(int(talent_q["level"]))]

    # weapon
    weapon_atk = weapon_info["weapon_atk"]
    weapon_sub = weapon_info["weapon_sub"]
    weapon_bonus = weapon_info["weapon_bonus"]

    # artifact
    artifact_main = artifact_info["artifact_main"]
    artifact_sub_info = artifact_info["artifact_sub_info"]

    term_atk = 0.05
    term_hp = 0.05
    term_crit_rate = 0.033
    term_crit_dmg = 0.066
    term_energy_recharge = 0.055

    miminum_energy_recharge = artifact_info["miminum_energy_recharge"]
    term_number_crit = artifact_sub_info["crit"]
    term_number = artifact_sub_info["term_number"]

    # auto : main term
    energy_recharge = 1 + weapon_sub['energy_recharge'] + weapon_bonus['energy_recharge']

    if energy_recharge + 0.466 > miminum_energy_recharge and energy_recharge + (term_number - term_number_crit) * term_energy_recharge > miminum_energy_recharge:
        artifact_main["atk"] = 0.466
        artifact_main["energy_recharge"] = 0
    else:
        artifact_main["atk"] = 0
        artifact_main["energy_recharge"] = 0.466

    crit_rate = 0.05 + weapon_sub['crit_rate'] + weapon_bonus['crit_rate']
    crit_dmg = 0.5 + weapon_sub['crit_dmg'] + weapon_bonus['crit_dmg']

    if crit_dmg >= 2 * crit_rate:
        artifact_main["crit_rate"] = 0.311
        artifact_main["crit_dmg"] = 0
    else :
        artifact_main["crit_rate"] = 0
        artifact_main["crit_dmg"] = 0.622


    # auto : sub term
    artifact_sub_num = {}

    energy_recharge += artifact_main["energy_recharge"] + (0.2 if artifact_info["name"] == "emblem_of_severed_fate" else 0.0) 
    artifact_sub_num["energy_recharge"] = max(0, miminum_energy_recharge - energy_recharge) / term_energy_recharge

    if artifact_sub_num["energy_recharge"] > term_number:
        assert False
    elif artifact_sub_num["energy_recharge"] > term_number - term_number_crit:
        term_number_crit = term_number - artifact_sub_num["energy_recharge"]
        artifact_sub_num["atk"] = 0
        artifact_sub_num["hp"] = 0
    else:
        artifact_sub_num["atk"] = term_number - term_number_crit - artifact_sub_num["energy_recharge"]
        artifact_sub_num["hp"] = 0

    crit_rate += artifact_main["crit_rate"]
    crit_dmg += artifact_main["crit_dmg"]

    if crit_dmg >= 2 * crit_rate:
        term_num_crit_rate_diff = (crit_dmg / 2 - crit_rate) / term_crit_rate
        if term_num_crit_rate_diff > term_number_crit:
            artifact_sub_num["crit_rate"] = term_number_crit
            artifact_sub_num["crit_dmg"] = 0
        else:
            artifact_sub_num["crit_rate"] =  term_num_crit_rate_diff + (term_number_crit - term_num_crit_rate_diff) / 2
            artifact_sub_num["crit_dmg"] = (term_number_crit - term_num_crit_rate_diff) / 2
    else :
        term_num_crit_rate_diff = (crit_rate - crit_dmg / 2) / term_crit_rate
        if term_num_crit_rate_diff > term_number_crit:
            artifact_sub_num["crit_rate"] = 0
            artifact_sub_num["crit_dmg"] = term_number_crit
        else:
            artifact_sub_num["crit_rate"] = (term_number_crit - term_num_crit_rate_diff) / 2
            artifact_sub_num["crit_dmg"] = term_num_crit_rate_diff + (term_number_crit - term_num_crit_rate_diff) / 2


    #################
    ##   panel     ##
    #################

    atk = (base_atk + weapon_atk) * (1 + weapon_sub['atk'] + weapon_bonus['atk'] + artifact_main["atk"] + artifact_sub_num["atk"] * term_atk) + artifact_main['base_atk']

    hp = base_hp * (1 + weapon_sub['hp'] + weapon_bonus['hp'] + artifact_main["hp"] + artifact_sub_num["hp"] * term_hp + breakout_hp) + artifact_main['base_hp']

    energy_recharge += artifact_sub_num["energy_recharge"] * term_energy_recharge
    crit_rate += artifact_sub_num["crit_rate"] * term_crit_rate
    crit_dmg += artifact_sub_num["crit_dmg"] * term_crit_dmg

    dmg_plus_e_coff = 1 + weapon_sub['dmg_plus'] + weapon_bonus['dmg_plus'] + artifact_main['dmg_plus']
    dmg_plus_q_coff = 1 + weapon_sub['dmg_plus'] + weapon_bonus['dmg_plus']+ artifact_main['dmg_plus'] + weapon_bonus['dmg_plus_q']

    ######################
    ##  artifact bonus  ##
    ######################

    if artifact_info["name"] == "emblem_of_severed_fate":
        dmg_plus_q_coff += energy_recharge * 0.25
    elif artifact_info["name"] == "atk_atk":
        atk += (base_atk + weapon_atk) * 0.18 * 2
    elif artifact_info["name"] == "atk_hp":
        atk += (base_atk + weapon_atk) * 0.18
        hp += base_atk * 0.20
    elif artifact_info["name"] == "atk_pyro":
        atk += (base_atk + weapon_atk) * 0.18
        dmg_plus_e_coff += 0.15
        dmg_plus_q_coff += 0.15
    elif artifact_info["name"] == "atk_burst":
        atk += (base_atk + weapon_atk) * 0.18
        dmg_plus_q_coff += 0.20
    elif artifact_info["name"] == "pyro_burst":
        dmg_plus_e_coff += 0.15
        dmg_plus_q_coff += 0.15
        dmg_plus_q_coff += 0.20
    else:
        assert False


    #################
    ##  teammates  ##
    #################
    for teammate_info in teammate_infos:
        teammate_info = teammate_info["character"]
        atk += teammate_info["base_atk"]
        atk += (base_atk + weapon_atk) * teammate_info["atk"]
        hp += base_hp * teammate_info["hp"]
        crit_rate += teammate_info["crit_rate"]
        crit_dmg += teammate_info["crit_dmg"]
        dmg_plus_e_coff += teammate_info["dmg_plus"]
        dmg_plus_q_coff += teammate_info["dmg_plus"]
        energy_recharge += teammate_info["energy_recharge"]
        enemy_defeat += teammate_info["defeat_reduce"]

        resistance_reduce = teammate_info["resistance_reduce"]
        resistance_reduce_part1 = min(max(0, 1 - enemy_resistance), resistance_reduce)
        resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
        enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2

    #############
    ##  buffs  ##
    #############
    for buff_info in buff_infos:
        atk += (base_atk + weapon_atk) * buff_info["atk"]
        hp += base_hp * buff_info["hp"]
        crit_rate += buff_info["crit_rate"]
        crit_dmg += buff_info["crit_dmg"]
        dmg_plus_e_coff += buff_info["dmg_plus"]
        dmg_plus_q_coff += buff_info["dmg_plus"]
        energy_recharge += buff_info["energy_recharge"]
        enemy_defeat += buff_info["defeat_reduce"]

        resistance_reduce = buff_info["resistance_reduce"]
        resistance_reduce_part1 = min(max(0, 1 - enemy_resistance), resistance_reduce)
        resistance_reduce_part2 = resistance_reduce - resistance_reduce_part1
        enemy_resistance += resistance_reduce_part1 + resistance_reduce_part2 / 2


    ###############
    ##  compute  ##
    ###############

    # coff
    crit_coff = 1 + crit_rate * crit_dmg
    enemy_coff = enemy_defeat * enemy_resistance

    # e
    e_coff = crit_coff * dmg_plus_e_coff * enemy_coff
    indomitable_flame_damage = talent_e["indomitable_flame"] * atk * e_coff
    rangeing_flame_damage = talent_e["rangeing_flame"] * atk * e_coff
    field_damage = talent_e["field"] * atk * e_coff

    talent_e_damage = indomitable_flame_damage + rangeing_flame_damage + 4 * field_damage

    # q
    q_coff = crit_coff * dmg_plus_q_coff * enemy_coff
    flame_manes_fist_damage = talent_q["flame_manes_fist"] * atk * q_coff
    incineration_drive_damage = talent_q["incineration_drive"] * atk * q_coff

    talent_q_damage = 10 * flame_manes_fist_damage + incineration_drive_damage


    # results
    panel = {
        "atk" : atk,
        "hp" : hp,
        "energy_recharge" : energy_recharge,
        "crit_rate" : crit_rate,
        "crit_dmg" : crit_dmg,
        "dmg_plus_e_coff" : dmg_plus_e_coff,
        "dmg_plus_q_coff" : dmg_plus_q_coff,
        "enemy_defeat" : enemy_defeat,
        "enemy_resistance" : enemy_resistance,
    }

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

    return panel, damage, artifact_main, artifact_sub_num
