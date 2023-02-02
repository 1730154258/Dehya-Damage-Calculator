# 迪希雅伤害计算器

> 最后更新时间：2023/02/01
> 测试服版本：3.5.52 （迪希雅v3）
> 项目版本：v0.1
> 联系作者：1730154258@qq.com 邮箱或qq均可联系，欢迎指正bug、优化意见或希望的更多功能
> - 本项目预计于原神3.5更新后 / ysin 更新迪希雅伤害计算后停止维护与更新，仅用于临时数据计算
> - 鸣谢：nga用户 @开罗尔物质 帮助进行了部分数据核验，特此鸣谢！

本项目使用 python3 进行测试服迪希雅的伤害计算，预计功能：
- [x] 迪希雅 面板计算
- [x] 迪希雅 元素战绩(e)与元素爆发(q) 伤害计算
- [x] 主流武器、圣遗物、队友模板
- [x] **指定充能需求下，自动分配圣遗物词条** 并进行伤害计算
- [x] 不同武器、圣遗物类型伤害对比
- [x] C0 命座
- [ ] C1-C6 命座
- [ ] GUI界面 / 网站

### 使用说明

#### 0. 快速尝试

**1) 对比 28 词条 绝缘套 零命迪希雅 佩戴不同武器的单人伤害，要求保证200充能，圣遗物主副词条自动分配**

```bash
python C0_dehya_auto_compare.py --weapon r1_beacon_of_the_reed_sea r1_redhorn_stonethresher r1_skyward_pride r1_wolfs_gravestone --artifact auto_emblem_of_severed_fate auto_emblem_of_severed_fate auto_emblem_of_severed_fate auto_emblem_of_severed_fate
```

得到计算结果：

```
# [单人] [精炼一 苇海信标 + 绝缘四件套]
# 面板：攻击 / 生命 / 充能/ 暴击 / 暴伤
[single person] [r1_beacon_of_the_reed_sea + auto_emblem_of_severed_fate] Damage = 99171.8
Panel : attack / hp / energy recharge / crit rate / crit dmg = 1705 / 29985 / 200.0% / 76.8% / 153.6%

# [单人] [精炼一 赤角石溃杵 + 绝缘四件套]
[single person] [r1_redhorn_stonethresher + auto_emblem_of_severed_fate] Damage = 80225.0
Panel : attack / hp / energy recharge / crit rate / crit dmg = 1277 / 24969 / 200.0% / 82.3% / 164.6%

# [单人] [精炼一 天空之傲 + 绝缘四件套]
[single person] [r1_skyward_pride + auto_emblem_of_severed_fate] Damage = 82955.8
Panel : attack / hp / energy recharge / crit rate / crit dmg = 1720 / 24969 / 203.4% / 60.2% / 120.5%

# [单人] [精炼一 狼的末路 + 绝缘四件套]
[single person] [r1_wolfs_gravestone + auto_emblem_of_severed_fate] Damage = 90437.9
Panel : attack / hp / energy recharge / crit rate / crit dmg = 1964 / 24969 / 200.0% / 60.2% / 120.5%
```

可以得到规定充能下的伤害对比。如果在命令后添加 `--with_teammates`运行，可以得到吃万班（c1班尼特r5原木刀 + 800精通 c0万叶无专武）的伤害。

**2) 计算 28 指定词条（4充能 + 6攻击 + 12暴击 + 6爆伤）充火暴伤 绝缘套 0+1 迪希雅的伤害【队友：c1班尼特r5原木刀 + 800精通 c0万叶无专武】**

```bash
python C0_dehya.py --weapon r1_beacon_of_the_reed_sea --artifact emblem_of_severed_fate_energy --detail
```

得到计算结果：

```
# [配置：单人] 精炼一 苇海信标 + 绝缘四件套
[Configuration : single person] r1_beacon_of_the_reed_sea + emblem_of_severed_fate_energy 

# [面板] 从上而下依次为：攻击、生命、充能、暴击、暴伤、E总增伤、Q总增伤、敌人防御区、敌人抗性区
[Panel]
- attack = 1795.95
- hp     = 29985.4
- energy recharge = 1.938
- crit rate = 0.777
- crit dmg  = 1.5179999999999998
- damage plus for e = 1.466
- damage plus for q = 1.9505
- enemy defeat = 0.5
- enemy resistance = 0.9

# [伤害]：展示了E、Q的每一段伤害与一轮循环（二段E+4次协同+Q10拳+Q1脚）总伤害
[Damage]
- E = 5247.089993596819 + 6171.5280928624015 + 4 * 3196.7999075161724 = 24205.81771652391
- Q = 10 * 6974.335440589219 + 9846.52481415207 = 79589.87922004425
- All = 103795.69693656816

# [配置：包含队友] 精炼一 苇海信标 + 绝缘四件套
[Configuration : with teammates] r1_beacon_of_the_reed_sea + emblem_of_severed_fate_energy

# [面板] 从上而下依次为：攻击、生命、充能、暴击、暴伤、E总增伤、Q总增伤、敌人防御区、敌人抗性区
[Panel]
- attack = 3103.825
- hp     = 29985.4
- energy recharge = 1.938
- crit rate = 0.777
- crit dmg  = 1.5179999999999998
- damage plus for e = 1.786
- damage plus for q = 2.2704999999999997
- enemy defeat = 0.5
- enemy resistance = 1.15

# [伤害]：展示了E、Q的每一段伤害与一轮循环（二段E+E的4次协同+Q10拳+Q1脚）总伤害
[Damage]
- E = 14116.41161758502 + 16603.456577769783 + 4 * 8600.451566225518 = 65121.67446025687
- Q = 10 * 17928.200453655667 + 25311.439655259677 = 204593.44419181635
- All = 269715.1186520732
```

可以看到详细的面板数据和每一段的伤害。


#### 1. 人物、武器、圣遗物、队友配置方法

本项目使用 json 文件配置各种数据，配置文件保存于 `./info` 文件夹下。

- `./info/characters/` 人物基础属性与倍率配置
- `./info/weapons/` 武器配置
- `./info/artifact/` 圣遗物配置，其中以 "auto" 为前缀的是自动分配主副词条的配置文件，其余为人工指定词条的配置文件
- `./info/teammate/` 队友配置
- `./info/buff/` 非队友直接影响的buff配置（如元素共鸣增益）
- `./info/enemy.json` 敌人配置

项目默认使用配置为：迪希雅v3.5.53 + 万班 + 双火
- 人物：`dehya_v3_5_52`
- 队友：`c1_ennett_r6_sapwood` + `c0_kazuha_r0`
- buff：`double_pyro`

可以使用的武器有 精炼一 苇海信标、精炼一 赤角石溃杵 等 11 件常用武器，可以使用的圣遗物为 绝缘四件套、游戏中可以组合出的 攻击/生命/火伤/宗室 二件套的 2+2 套装。

- 如果需要测试项目中不默认包含的武器 / 圣遗物，可以根据已有的示例文件新建配置文件，填写需要的数据并放置于对应文件夹下。

- 如果需要使用非默认的人物数据、队友、buff，可以编写好配置文件后修改主脚本文件（如 `C0_dehya.py`）中的对应路径位置。


#### 2. 指定武器、指定圣遗物词条的伤害计算

```bash
python C0_dehya.py --weapon [武器配置文件名称] --artifact [圣遗物配置文件名称] [--detail]
```
- weapon：武器配置文件名称，如 `r1_beacon_of_the_reed_sea`
- artifact：圣遗物配置文件名称，如 `emblem_of_severed_fate_energy`
- detail：可选，显示面板计算结果

运行后，将会显示指定武器、圣遗物词条下迪希雅的面板与伤害。

#### 3. 指定武器、自动分配圣遗物词条的伤害计算

规定圣遗物**副词条总数、双爆词条数量、充能需求**，根据不同武器自动分配圣遗主/副词条并计算伤害。

```bash
python C0_dehya_auto.py --weapon [武器配置文件名称] --artifact [圣遗物配置文件名称] [--detail]
```
- weapon：武器配置文件名称，如 `r1_beacon_of_the_reed_sea`
- artifact：圣遗物配置文件名称，如 `auto_emblem_of_severed_fate_energy`
- detail：可选，显示圣遗物词条分配结果、面板计算结果

运行后，将会显示指定武器下，迪希雅的圣遗物词条的分配结果、面板与伤害。

> 注：圣遗物词条自动分配规则
> 1. 若使用攻击沙时，副词条可以满足充能需求，则使用攻击沙；否则，使用充能沙
> 2. 使用火伤杯
> 3. 使用暴击/暴伤头，具体使用哪个取决于双暴配平中哪个更低
> 4. 副词条首先满足充能需求
> 5. 副词条尽量使得双暴满足 1:2 配平
> 6. 剩余副词条分配给大攻击

#### 3. 自动分配圣遗物词条，对比不同武器或圣遗物的伤害计算

```bash
python C0_dehya_auto_compare.py --weapon [多个武器配置文件名称] --artifact auto_emblem_of_severed_fate [多个圣遗物配置文件名称] [--with_teammates]
```
- weapon：多个武器配置文件名称，如 `r1_beacon_of_the_reed_sea r1_wolfs_gravestone`
- artifact：对应的多个圣遗物配置文件名称，如 `emblem_of_severed_fate_energy emblem_of_severed_fate_energy`
- with_teammates：可选，显示吃队友拐的伤害对比

`weapon` 和 `artifact` 参数数量应一致切一一对应，如上述实例中对比为 [精炼一 苇海信标 + 绝缘四件套] 对比 [精炼一 狼的末路 + 绝缘四件套]

运行后，将会对比不同武器下，迪希雅的面板与伤害。
