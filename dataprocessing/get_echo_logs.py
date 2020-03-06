#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import re
import sys
from bl3data.bl3data import BL3Data
from bl3hotfixmod.bl3hotfixmod import LVL_TO_ENG_LOWER

# Just getting a list of ECHO logs so I could compare to see if I'd gotten
# all of them.

data = BL3Data()

# Globs for non-mission-related ECHOs
globs_rando = [
        '/Game/InteractiveObjects/EchoLog_NonMission/Data/EchoLogData/EchoLogData_*',
        '/Game/PatchDLC/Dandelion/InteractiveObjects/EchoLogs/DataAssets/EchoLogData_*',
        ]
objects_rando = []
for glob in globs_rando:
    objects_rando.extend(list(data.glob_data(glob)))

# Globs for mission-related ECHOs
# (eh, turns out these don't show up in the list anyway)
#globs_mission = [
#        '/Game/Missions/*/*/*/*/EchoLogData_*',
#        '/Game/PatchDLC/Dandelion/Missions/*/*/EchoLogData_*',
#        ]
#objects_mission = []
#for glob in globs_mission:
#    objects_mission.extend(list(data.glob_data(glob)))

# Some level transforms we may need to do
level_transforms = {
        'sanctuary': 'sanctuary3',
        'casino': 'casinointro',
        'tower': 'towerlair',
        }

# There are a few ECHOs which we find this way which legit cannot
# appear in the game
name_additions = {
        '/Game/PatchDLC/Dandelion/InteractiveObjects/EchoLogs/DataAssets/EchoLogData_DLC1_Impound3': '(does not appear in game)',
        '/Game/PatchDLC/Dandelion/InteractiveObjects/EchoLogs/DataAssets/EchoLogData_DLC1_Core2': '(does not appear to be in game)',
        '/Game/PatchDLC/Dandelion/InteractiveObjects/EchoLogs/DataAssets/EchoLogData_DLC1_Core3': '(does not appear in game)',
        '/Game/PatchDLC/Dandelion/InteractiveObjects/EchoLogs/DataAssets/EchoLogData_DLC1_Core4': '(does not appear in game)',
        }

# Loop through randos
echoes = []
lvl_re = re.compile(r'^.*_([a-zA-Z]+?)\d+$')
for (obj_name, obj) in objects_rando:
    match = lvl_re.match(obj_name)
    if not match:
        raise Exception('No match: {}'.format(obj_name))
    lvl_name_base = match.group(1).lower()
    if lvl_name_base in level_transforms:
        lvl_name_base = level_transforms[lvl_name_base]
    lvl_name = '{}_p'.format(lvl_name_base)
    if lvl_name not in LVL_TO_ENG_LOWER:
        raise Exception('No level mapping: {} ({})'.format(lvl_name, obj_name))

    name = obj[0]['InventoryName']['string']
    if obj_name in name_additions:
        name = '{} {}'.format(name, name_additions[obj_name])
    echoes.append((name, LVL_TO_ENG_LOWER[lvl_name]))

# Loop through Missions
#for (obj_name, obj) in objects_mission:
#    if 'InventoryName' in obj[0]:
#        echoes.append((obj[0]['InventoryName']['string'], '(mission ECHO)'))
#    else:
#        # Turns out this happens for a lot of side mission ones.
#        pass
#        #raise Exception('Inventory Name not found: {}'.format(obj_name))

# Report
for name, level in sorted(echoes):
    print('{} - {}'.format(name, level))

