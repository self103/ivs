#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pgoapi - Pokemon Go API
Copyright (c) 2016 tjado <https://github.com/tejado>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

Author: tjado <https://github.com/tejado>
"""

import os
import sys
import json
import time
import pprint
import logging
import getpass
import argparse

pokemon_list = [
'Bulbasaur',
'Ivysaur',
'Venusaur',
'Charmander',
'Charmeleon',
'Charizard',
'Squirtle',
'Wartortle',
'Blastoise',
'Caterpie',
'Metapod',
'Butterfree',
'Weedle',
'Kakuna',
'Beedrill',
'Pidgey',
'Pidgeotto',
'Pidgeot',
'Rattata',
'Raticate',
'Spearow',
'Fearow',
'Ekans',
'Arbok',
'Pikachu',
'Raichu',
'Sandshrew',
'Sandslash',
'Nidoran ♀',
'Nidorina',
'Nidoqueen',
'Nidoran ♂',
'Nidorino',
'Nidoking',
'Clefairy',
'Clefable',
'Vulpix',
'Ninetales',
'Jigglypuff',
'Wigglytuff',
'Zubat',
'Golbat',
'Oddish',
'Gloom',
'Vileplume',
'Paras',
'Parasect',
'Venonat',
'Venomoth',
'Diglett',
'Dugtrio',
'Meowth',
'Persian',
'Psyduck',
'Golduck',
'Mankey',
'Primeape',
'Growlithe',
'Arcanine',
'Poliwag',
'Poliwhirl',
'Poliwrath',
'Abra',
'Kadabra',
'Alakazam',
'Machop',
'Machoke',
'Machamp',
'Bellsprout',
'Weepinbell',
'Victreebel',
'Tentacool',
'Tentacruel',
'Geodude',
'Graveler',
'Golem',
'Ponyta',
'Rapidash',
'Slowpoke',
'Slowbro',
'Magnemite',
'Magneton',
'Farfetch\'d',
'Doduo',
'Dodrio',
'Seel',
'Dewgong',
'Grimer',
'Muk',
'Shellder',
'Cloyster',
'Gastly',
'Haunter',
'Gengar',
'Onix',
'Drowzee',
'Hypno',
'Krabby',
'Kingler',
'Voltorb',
'Electrode',
'Exeggcute',
'Exeggcutor',
'Cubone',
'Marowak',
'Hitmonlee',
'Hitmonchan',
'Lickitung',
'Koffing',
'Weezing',
'Rhyhorn',
'Rhydon',
'Chansey',
'Tangela',
'Kangaskhan',
'Horsea',
'Seadra',
'Goldeen',
'Seaking',
'Staryu',
'Starmie',
'Mr Mime',
'Scyther',
'Jynx',
'Electabuzz',
'Magmar',
'Pinsir',
'Tauros',
'Magikarp',
'Gyarados',
'Lapras',
'Ditto',
'Eevee',
'Vaporeon',
'Jolteon',
'Flareon',
'Porygon',
'Omanyte',
'Omastar',
'Kabuto',
'Kabutops',
'Aerodactyl',
'Snorlax',
'Articuno',
'Zapdos',
'Moltres',
'Dratini',
'Dragonair',
'Dragonite',
'Mewtwo',
'Mew'
]


# add directory of this file to PATH, so that the package will be found
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import Pokemon Go API lib
from pgoapi import pgoapi
from pgoapi import utilities as util



log = logging.getLogger(__name__)


def prettyTable(dictionary, cssClass=''):
    ''' pretty prints a dictionary into an HTML table(s) '''
    if isinstance(dictionary, str):
        return '<td>' + dictionary + '</td>'
    s = ['<table ']
    if cssClass != '':
        s.append('class="%s"' % (cssClass))
    s.append('>\n')
    for key, value in dictionary.iteritems():
        if key != 'picture' or key != 'icon':
            s.append('<tr>\n  <td valign="top"><strong>%s</strong></td>\n' % str(key))
        if isinstance(value, dict):
            if key == 'picture' or key == 'icon':
                s.insert(0,'  <td valign="top"><img src="%s"></td>\n' % Page.prettyTable(value, cssClass))
            else:
                s.append('  <td valign="top">%s</td>\n' % Page.prettyTable(value, cssClass))
        elif isinstance(value, list):
            s.append("<td><table>")
            for i in value:
                s.append('<tr><td valign="top">%s</td></tr>\n' % Page.prettyTable(i, cssClass))
            s.append('</table>')
        else:
            if key == 'picture' or key == 'icon':
                s.insert(0,'  <td valign="top"><img src="%s"></td>\n' % value)
            else:
                s.append('  <td valign="top">%s</td>\n' % value)
        s.append('</tr>\n')
    s.append('</table>')
    return '\n'.join(s)

def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"

    # If config file exists, load variables from json
    load   = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))

    # Read passed in Arguments
    required = lambda x: not x in load
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
        required=required("auth_service"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
    parser.set_defaults(DEBUG=False, TEST=False)
    config = parser.parse_args()

    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = str(load[key])

    if config.__dict__["password"] is None:
        log.info("Secure Password Input (if there is no password prompt, use --password <pw>):")
        config.__dict__["password"] = getpass.getpass()

    if config.auth_service not in ['ptc', 'google']:
      log.error("Invalid Auth service specified! ('ptc' or 'google')")
      return None

    return config


def main():
    # log settings
    # log format
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')
    # log level for http request class
    logging.getLogger("requests").setLevel(logging.WARNING)
    # log level for main pgoapi class
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    # log level for internal pgoapi class
    logging.getLogger("rpc_api").setLevel(logging.INFO)

    config = init_config()
    if not config:
        return

    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)


    # instantiate pgoapi
    api = pgoapi.PGoApi()

    # parse position
    position = util.get_pos_by_name(config.location)
    if not position:
        log.error('Your given location could not be found by name')
        return
    elif config.test:
        return

    # set player position on the earth
    api.set_position(*position)

    if not api.login(config.auth_service, config.username, config.password, app_simulation = True):
        return

    # get player profile call (single command example)
    # ----------------------
    response_dict = api.get_player()
    print('Response dictionary (get_player): \n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
    
    # sleep 200ms due to server-side throttling
    time.sleep(0.2)

    # get player profile + inventory call (thread-safe/chaining example)
    # ----------------------
    req = api.create_request()
    req.get_player()
    req.get_inventory()
    response_dict = req.call()
    #print('Response dictionary (get_player + get_inventory): \n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
    #print response_dict


    all_my_pokemon = {}
    with open('myPokemon.txt', 'w') as file:
        for i in response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']:#['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']['inventory_item_data']['pokemon_data']:
            try:
                stats = {}
                unique_id = int(i['inventory_item_data']['pokemon_data']['id'])

                number = int(i['inventory_item_data']['pokemon_data']['pokemon_id'])
                #stats.update({'number' : number})

                name = pokemon_list[number - 1]
                stats.update({'name' : name})

                cp = int(i['inventory_item_data']['pokemon_data']['cp'])
                stats.update({'cp' : cp})

                attack = int(i['inventory_item_data']['pokemon_data']['individual_attack'])
                stats.update({'attack' : attack})

                defense = int(i['inventory_item_data']['pokemon_data']['individual_defense'])
                stats.update({'defense' : defense})

                stamina = int(i['inventory_item_data']['pokemon_data']['individual_stamina'])
                stats.update({'stamina' : stamina})

                if number<10:
                    elong_num = str("00{}".format(str(number)))
                elif number<100:
                    elong_num = str("0{}".format(str(number)))

                #picture = str("eternia.fr/public/media/go/sprites/{0}.png".format(elong_num))
                picture = str("/sprites/{0}.png".format(elong_num))
                stats.update({'picture' : picture})


                pocket_mon = {unique_id : stats}
                all_my_pokemon.update(pocket_mon)


            except:
                pass



        for j in all_my_pokemon:
            file.write(prettyTable(all_my_pokemon[j]))
            #file.write(all_my_pokemon[j]['name'])
            #file.write('\n')

            #file.write(str(all_my_pokemon[j]['image']))
            #file.write('\n\n')

    #print all_my_pokemon


    file.close()


    #sudo python pokecli.py -a google -u runawayturtl@gmail.com -p 13794693ds -l 37.336992,-121.939896






























if __name__ == '__main__':
    main()
