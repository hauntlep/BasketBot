# the list of reactions used in the game

import random
import math
import dataManager as dm
from settings import settingsTable as settings


reactions = [
    ":smile:",
    ":frowning:",
    ":angry:",
    ":sunglasses:",
    ":scream:",
    ":smirk:",
    ":flushed:",
    ":sweat_smile:",
    ":cry:",
    ":joy:",
    ":sob:",
    ":heart:",
    ":broken_heart:",
    ":sparkling_heart:",
    ":star:",
    ":star2:",
    ":dizzy:",
    ":boom:",
    ":fire:",
    ":sparkles:",
    ":sunny:",
    ":cloud:",
    ":snowflake:",
    ":zap:",
    ":cyclone:",
    ":rainbow:",
    ":ocean:",
    ":cat:",
    ":dog:",
    ":mouse:",
    ":hamster:",
    ":rabbit:",
    ":fox:",
    ":bear:",
    ":panda_face:",
    ":koala:",
    ":tiger:",
    ":lion:",
    ":cow:",
    ":pig:",
    ":frog:",
    ":monkey:",
    ":chicken:",
    ":penguin:",
    ":bird:",
    ":baby_chick:",
    ":hatching_chick:",
    ":hatched_chick:",
    ":wolf:",
    ":boar:",
    ":horse:",
    ":unicorn:",
    ":bee:",
    ":bug:",
    ":snail:",
    ":beetle:",
    ":ant:",
    ":spider:",
    ":scorpion:",
    ":crab:",
    ":snake:",
    ":turtle:",
    ":tropical_fish:",
    ":fish:",
    ":blowfish:",
    ":dolphin:",
    ":whale:",
    ":whale2:",
    ":crocodile:",
    ":leopard:",
    ":tiger2:",
    ":water_buffalo:",
    ":ox:",
    ":cow2:",
    ":dromedary_camel:",
    ":camel:",
    ":elephant:",
    ":goat:",
    ":transgender_flag:",
    ":rat:",
    ":rooster:",
    ":turkey:",
    ":dove:",
    ":speaking_head:",
    ":100:",
    ":x:",
    ":o:",  
     ":money_mouth:",
    ":nerd:",
    ":face_with_rolling_eyes:",
    ":thinking:",
    ":zipper_mouth:",
    ":raised_hands:",
    ":vulcan_salute:",
    ":muscle:",
    ":clap:",
    ":wave:",
    ":point_up:",
    ":point_down:",
    ":point_left:",
    ":point_right:",
    ":raised_hand:",
    ":ok_hand:",
    ":thumbsup:",
    ":thumbsdown:",
    ":pray:",
    ":medal:",
    ":trophy:",
    ":checkered_flag:",
    ":fireworks:",
    ":rainbow_flag:",
    ":balloon:",
    ":gift:",
    ":confetti_ball:",
    ":tada:",
    ":clipboard:",
    ":mag:",
    ":bulb:",
    ":lock:",
    ":key:",
    ":bell:",
    ":no_bell:",
    ":mute:",
    ":speaker:",
    ":loud_sound:",
    ":hourglass:",
    ":watch:",
    ":alarm_clock:",
    ":stopwatch:",
    ":hourglass_flowing_sand:",
    ":new_moon:",
    ":waxing_crescent_moon:",
    ":first_quarter_moon:",
    ":waxing_gibbous_moon:",
    ":full_moon:",
    ":waning_gibbous_moon:",
    ":last_quarter_moon:",
    ":waning_crescent_moon:",
    ":crescent_moon:",
    ":star_and_crescent:",
    ":hammer_and_wrench:",
    ":gear:",
    ":atom_symbol:",
    ":biohazard:",
    ":recycle:",
    ":chart_with_upwards_trend:",
    ":chart_with_downwards_trend:",
    ":bar_chart:",
    ":clipboard:",
    ":file_folder:",
    ":open_file_folder:",
    ":page_with_curl:",
    ":page_facing_up:",
    ":bookmark_tabs:",
    ":link:",
    ":paperclip:",
    ":scissors:",
    ":memo:",
    ":pencil2:",
    ":paintbrush:",
    ":crayon:",
    ":triangular_ruler:",
    ":straight_ruler:",
    ":pushpin:",
    ":round_pushpin:",
    ":scissors:",
    ":paperclip:",
    ":file_folder:",
    ":open_file_folder:",
    ":bookmark_tabs:",
    ":page_facing_up:",
    ":page_with_curl:",
    ":calendar:",
    ":date:",
    ":spiral_calendar:",
    ":card_index:",
    ":card_file_box:",
    ":ballot_box:",
    ":ballot_box_with_check:",
    ":file_cabinet:",
    ":money_with_wings:",
    ":credit_card:",
    ":gem:",
    ":hammer:",
    ":pick:",
    ":nut_and_bolt:",
    ":wrench:",
    ":gear:",
    ":chains:",
    ":gun:",
    ":bomb:",
    ":hocho:",
    ":smoking:",
    ":skull_and_crossbones:",
    ":coffin:",
    ":funeral_urn:",
    ":amphora:",
    ":crystal_ball:",
    ":pray:",
    ":thermometer:",
    ":label:",
    ":bookmark:",
    ":toilet:",
    ":shower:",
    ":bathtub:",
    ":razor:",
    ":lotion_bottle:",
    ":microbe:",
    ":petri_dish:",
    ":test_tube:",
    ":syringe:",
    ":dna:",
    ":pill:",
    ":medical_symbol:",
    ":stethoscope:",
    ":door:",
    ":bed:",
    ":couch_and_lamp:",
    ":tooth:",
    ":bricks:",
    ":moneybag:",
    ":yen:",
    ":dollar:",
    ":euro:",
    ":pound:",
    ":money_with_wings:",
    ":credit_card:",
    ":chart_with_upwards_trend:",
    ":chart_with_downwards_trend:",
    ":alarm_clock:",
    ":stopwatch:",
    ":timer_clock:",
    ":mantelpiece_clock:",
    ":hourglass:",
    ":hourglass_flowing_sand:",
    ":camera:",
    ":video_camera:",
    ":film_projector:",
    ":film_frames:",
    ":telephone_receiver:",
    ":telephone:",
    ":pager:",
    ":fax:",
    ":tv:",
    ":radio:",
    ":studio_microphone:",
    ":level_slider:",
    ":control_knobs:",
    ":stop_button:",
    ":record_button:",
    ":eject_button:",
    ":bell:",
    ":musical_note:",
    ":headphones:",
    ":musical_score:",
    ":man_dancing:",
    ":woman_dancing:",
    ":man_in_tuxedo:",
    ":bride_with_veil:",
    ":pregnant_woman:",
    ":breast_feeding:",
    ":angel:",
    ":santa:",
    ":superhero:",
    ":supervillain:",
    ":mage:",
    ":fairy:",
    ":vampire:",
    ":merperson:",
    ":elf:",
    ":genie:",
    ":zombie:",
    ":clown:",
    ":juggling:",
    ":person_in_lotus_position:",
    ":bath:",
    ":person_climbing:",
    ":horse_racing:",
    ":skier:",
    ":snowboarder:",
    ":golfer:",
    ":surfer:",
    ":rowboat:",
    ":swimmer:",
    ":basketball_player:",
    ":weight_lifter:",
    ":bicyclist:",
    ":mountain_bicyclist:",
    ":cartwheeling:",
    ":wrestlers:",
    ":water_polo:",
    ":handball_person:",
    ":juggling_person:",
    ":people_with_bunny_ears_partying:",
    ":man_bowing:",
    ":woman_bowing:",
    ":man_tipping_hand:",
    ":woman_tipping_hand:",
    ":man_gesturing_no:",
    ":woman_gesturing_no:",
    ":man_gesturing_ok:",
    ":woman_gesturing_ok:",
    ":man_raising_hand:",
    ":woman_raising_hand:",
    ":man_facepalming:",
    ":woman_facepalming:",
    ":man_shrugging:",
    ":woman_shrugging:",
    ":man_health_worker:",
    ":woman_health_worker:",
    ":man_student:",
    ":woman_student:",
    ":man_teacher:",
    ":woman_teacher:",
    ":man_judge:",
    ":woman_judge:",
    ":man_farmer:",
    ":woman_farmer:",
    ":man_cook:",
    ":woman_cook:",
    ":man_mechanic:",
    ":woman_mechanic:",
    ":man_factory_worker:",
    ":woman_factory_worker:",
    ":man_office_worker:",
    ":woman_office_worker:",
    ":man_scientist:",
    ":woman_scientist:",
    ":man_technologist:",
    ":woman_technologist:",
    ":man_singer:",
    ":woman_singer:",
    ":man_artist:",
    ":woman_artist:",
    ":man_pilot:",
    ":woman_pilot:",
    ":man_astronaut:",
    ":woman_astronaut:",
    ":man_firefighter:",
    ":woman_firefighter:",
    ":man_police_officer:",
    ":woman_police_officer:",
    ":man_detective:",
    ":woman_detective:",
    ":man_guard:",
    ":woman_guard:",
    ":man_construction_worker:",
]

def calculate_rarity(reaction):
    # get the index of the reaction in the list
    index = reactions.index(reaction)


    chance = math.floor(1 + (len(reactions) - index) * (math.pow(random.random(), 1.5)))

    # cannot use chance because of the randomness for the percentage, so we need to calculate it again
    percentageOutOf100 = math.floor(1 + (len(reactions) - index) * (math.pow(1, 1.5)))

    return chance, percentageOutOf100

def get_reaction():
    # get a random reaction
    yup = random.randint(1, 100)

    if yup <= 16:
        return False, None, None
    
    reaction = random.choice(reactions)

    # calculate the chance of getting the reaction
    chance, _ = calculate_rarity(reaction)

    # get a random number between 1 and 100
    roll = random.randint(random.randint(1,20), 100)

    # if the roll is less than or equal to the chance, return the reaction
    if roll <= chance:
        return True, reaction, chance
    else:
        return False, None, chance
    
def get_reaction_index(reaction):
    return reactions.index(reaction)

def list_reactions_with_price():
    reactionsWithPrice = []
    for reaction in reactions:
        this = []

        this.append(reaction)
        index = get_reaction_index(reaction)
        
        if index == 0:
            index += 1

        this.append(index * 10)
        this.append(index * 25)

        reactionsWithPrice.append(this)

    return reactionsWithPrice

def calculate_inventory_value(user_id):
    reactions = dm.obtained_reactions(user_id)
    doubleCredits = settings["doubleCredits"]
    value = 0

    for reaction in reactions:
        index = get_reaction_index(reaction)
        if index == 0:
            index += 1

        value += index * 3

    if doubleCredits:
        print("Double credits is active, doubling inventory value.")
        value = value * 2

    return value

def random_reaction():
    return random.choice(reactions)

inf = float("inf")

def rarest_reaction():
    # by rarest we mean MOST RARE, so lower percentage
    highest = inf
    highest_reaction = None
    top10 = []
    
    for reaction in reactions:
        _, percentage = calculate_rarity(reaction)
        # is this percentage lower than the current highest?
        if percentage < highest:
            highest = percentage
            highest_reaction = reaction
        
        top10.append([reaction, percentage])

    top10.sort(key=lambda x: x[1])

    return highest_reaction, top10[:10]
