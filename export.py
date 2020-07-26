#! python

import sys
import os
import xml.etree.ElementTree as ET
import ctypes.wintypes

def parse_mods(slots, lines):
    r = []
    for line in (lines.split('\n\n')[slots].split('\n')):
        if '[Empty' in line:
            continue
        else:
            r.append(line)
    return(r)

def parse_other(lines):
    drone_types = [
        'Warrior', 'Acolyte', 'Hornet', 'Hobgoblin',
        'Valkyrie', 'Infiltrator', 'Vespa', 'Hammerhead',
        'Berserker', 'Praetor', 'Wasp', 'Ogre', 'Gecko'
        'Bouncer', 'Curator', 'Warden', 'Garde',
        'Armor Maintenance Bot', 'Shield Maintenance Bot',
        'Hull Maintenance Bot'
        ]
    other = lines.split('\n\n\n')[1:]
    cargo, drones = [], []
    if len(other) == 0:
        return(cargo, drones)
    if len(other) == 2:
        drones, cargo = handle_drone_bullshit(other[0].split('\n')), other[1].split('\n')
    else:
        is_this_drones = True
        for item in other[0].split('\n'):
            is_this_a_drone = False
            for drone in drone_types:
                if drone in item:
                    is_this_a_drone = True
                    break
            if not is_this_a_drone:
                is_this_drones = False
                break
        if is_this_drones:
            drones = handle_drone_bullshit(other[0].split('\n'))
        else:
            cargo = other[0].split('\n')
    return(drones, cargo)

def handle_drone_bullshit(d_list):
    drones = {}
    for item in d_list:
        drone, count = item.split(' x')
        if drone in drones.keys():
            drones[drone] += int(count)
        else:
            drones[drone] = int(count)
    ret = []
    for k,v in drones.items():
        ret.append(k+' x'+str(v))
    return(ret)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('specify a directory to generate a fittings import file for')
        sys.exit(0)

    if sys.argv[1][-1] != '/':
        sys.argv[1] = sys.argv[1]+'/'
    fit_files = []
    for entry in os.listdir(os.path.join(os.getcwd(), sys.argv[1])):
        if entry == 'template' or entry == 'out.txt':
            continue
        fit_files.append(os.path.join(sys.argv[1], entry))
    parsed_fits = []
    #read in and parse fits from file
    for fit in fit_files:
        with open(fit, 'r') as f:
            parsed_fit = {}
            lines = f.read()
            split = lines.split('\n')[0].rstrip()[1:-1].split(', ')
            parsed_fit['name'] = split[1]
            parsed_fit['shipType'] = split[0]
            for name, slot in {'lows': 1, 'mids': 2, 'highs': 3, 'rigs': 4}.items():
                parsed_fit[name] = parse_mods(slot, lines)
            parsed_fit['drones'], parsed_fit['cargo'] = parse_other(lines)
            parsed_fits.append(parsed_fit)

    #write out to xml
    xml_lines = ['<?xml version="1.0" ?>\n', '<fittings>\n']
    for fit in parsed_fits:
        xml_lines.append(f"<fitting name='{fit['name']} {fit['shipType']}'>\n")
        xml_lines.append('<description value=""/>\n')
        xml_lines.append(f"<shipType value='{fit['shipType']}'/>\n")
        for slot, module in enumerate(fit['lows']):
            xml_lines.append(f'<hardware slot="low slot {slot}" type="{module}"/>\n')
        for slot, module in enumerate(fit['mids']):
            xml_lines.append('<hardware slot="med slot {}" type="{}"/>\n'.format(slot, module))
        for slot, module in enumerate(fit['highs']):
            xml_lines.append('<hardware slot="hi slot {}" type="{}"/>\n'.format(slot, module))
        for slot, module in enumerate(fit['rigs']):
            xml_lines.append('<hardware slot="rig slot {}" type="{}"/>\n'.format(slot, module))
        if len(fit['drones']) > 0:
            for drone in fit['drones']:
                t, c = drone.split(' x')
                xml_lines.append('<hardware qty="{}" slot="drone bay" type="{}"/>\n'.format(c, t))


        if len(fit['cargo']) > 0:

            for item in fit['cargo']:
                if item != '':
                    t, c = item.split(' x')
                    xml_lines.append('<hardware qty="{}" slot="cargo" type="{}"/>\n'.format(c,t))
        xml_lines.append('</fitting>\n')
    xml_lines.append('</fittings>')

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
    p = os.path.join(buf.value, 'EVE\\fittings', sys.argv[1][0:-1]+'.xml')

    with open(p, 'w') as f:
        f.writelines(xml_lines)
    print('fitting file written to {}'.format(p))