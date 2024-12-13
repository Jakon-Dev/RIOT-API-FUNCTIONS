from tkinter import ALL
import utils
import Static_Game_Data.StaticGameData as StaticGameData
import json




class AGENTS:
    ALL_AGENTS = StaticGameData.getAgents()
    
    class GET_UUID:
        def by_name(displayName: str) -> str:
            for agent in AGENTS.ALL_AGENTS:
                if agent["displayName"] == displayName and agent["isPlayableCharacter"] == True:
                    return agent["uuid"]
            return None
        
        def by_path(assetPath: str) -> str:
            for agent in AGENTS.ALL_AGENTS:
                if agent["assetPath"] == assetPath and agent["isPlayableCharacter"] == True:
                    return agent["uuid"]
            return None

        def by_dev_name(developerName: str) -> str:
            for agent in AGENTS.ALL_AGENTS:
                if agent["developerName"] == developerName and agent["isPlayableCharacter"] == True:
                    return agent["uuid"]
            return None

    class GET_BY_UUID:
        def agent(uuid: str) -> json:
            for agent in AGENTS.ALL_AGENTS:
                if agent["uuid"] == uuid:
                    return agent
            return None
        
        def name(uuid: str) -> str:
            agent = AGENTS.GET_BY_UUID.agent(uuid)
            if agent is not None:
                return agent["displayName"]
            return None

        def images_and_colors(uuid: str) -> dict:
            agent = AGENTS.GET_BY_UUID.agent(uuid)
            if agent is not None:
                images_and_colors = {
                    "displayIcon": agent["displayIcon"],
                    "displayIconSmall": agent["displayIconSmall"],
                    "bustPortrait": agent["bustPortrait"],
                    "fullPortrait": agent["fullPortrait"],
                    "fullPortraitV2": agent["fullPortraitV2"],
                    "killfeedPortrait": agent["killfeedPortrait"],
                    "background": agent["background"],
                    "backgroundGradientColors": agent["backgroundGradientColors"],
                }
                return images_and_colors
            return None

        def description(uuid: str) -> str:
            agent = AGENTS.GET_BY_UUID.agent(uuid)
            if agent is not None:
                return agent["description"]
            return None
        
        class ABILITIES:
            def all(uuid: str) -> list:
                agent = AGENTS.GET_BY_UUID.agent(uuid)
                if agent is not None:
                    return agent["abilities"]
                return None
            
            def ability1(uuid: str) -> dict:
                abilities = AGENTS.ABILITIES.all(uuid)
                for ability in abilities:
                    if ability["slot"] == "Ability1":
                        return ability
                return None
            
            def ability2(uuid: str) -> dict:
                abilities = AGENTS.ABILITIES.all(uuid)
                for ability in abilities:
                    if ability["slot"] == "Ability2":
                        return ability
                return None
            
            def grenade(uuid: str) -> dict:
                abilities = AGENTS.ABILITIES.all(uuid)
                for ability in abilities:
                    if ability["slot"] == "Grenade":
                        return ability
                return None
            
            def ultimate(uuid: str) -> dict:
                abilities = AGENTS.ABILITIES.all(uuid)
                for ability in abilities:
                    if ability["slot"] == "Ultimate":
                        return ability
                return None
            
            def passive(uuid: str) -> dict:
                abilities = AGENTS.ABILITIES.all(uuid)
                for ability in abilities:
                    if ability["slot"] == "Passive":
                        return ability
                return None
        
        class ROLE:
            def all(uuid: str) -> dict:
                agent = AGENTS.GET_BY_UUID.agent(uuid)
                if agent is not None:
                    return agent["role"]
                return None
            
            def uuid(uuid: str) -> str:
                role = AGENTS.ROLE.all(uuid)
                if role is not None:
                    return role["uuid"]
                return None

            def displayName(uuid: str) -> str:
                role = AGENTS.ROLE.all(uuid)
                if role is not None:
                    return role["displayName"]
                return None
            
            def description(uuid: str) -> str:
                role = AGENTS.ROLE.all(uuid)
                if role is not None:
                    return role["description"]
                return None
            
            def displayIcon(uuid: str) -> str:
                role = AGENTS.GET_BY_UUID.ROLE.all(uuid)
                if role is not None:
                    return role["displayIcon"]
                return None
            
            def assetPath(uuid: str) -> str:
                role = AGENTS.ROLE.all(uuid)
                if role is not None:
                    return role["assetPath"]
                return None
        
    class GET_BY_ROLE_UUID:
        
        ROLES = {
            "dbe8757e-9e92-4ed4-b39f-9dfc589691d4": {"name": "Duelist", "image": "https://media.valorant-api.com/agents/roles/dbe8757e-9e92-4ed4-b39f-9dfc589691d4/displayicon.png"},
            "5fc02f99-4091-4486-a531-98459a3e95e9": {"name": "Sentinel", "image": "https://media.valorant-api.com/agents/roles/5fc02f99-4091-4486-a531-98459a3e95e9/displayicon.png"},
            "1b47567f-8f7b-444b-aae3-b0c634622d10": {"name": "Initiator", "image": "https://media.valorant-api.com/agents/roles/1b47567f-8f7b-444b-aae3-b0c634622d10/displayicon.png"},
            "4ee40330-ecdd-4f2f-98a8-eb1243428373": {"name": "Controller", "image": "https://media.valorant-api.com/agents/roles/4ee40330-ecdd-4f2f-98a8-eb1243428373/displayicon.png"}
        }

        def valid(role_uuid: str) -> bool:
            return role_uuid in AGENTS.GET_BY_ROLE_UUID.ROLES

        def name(role_uuid: str) -> str:
            return AGENTS.GET_BY_ROLE_UUID.ROLES[role_uuid]["name"] if AGENTS.GET_BY_ROLE_UUID.valid(role_uuid) else None

        def image(role_uuid: str) -> str:
            return AGENTS.GET_BY_ROLE_UUID.ROLES[role_uuid]["image"] if AGENTS.GET_BY_ROLE_UUID.valid(role_uuid) else None
        
        def agents(role_uuid: str) -> list:
            if not AGENTS.GET_BY_ROLE_UUID.valid(role_uuid):
                return None
            agents = []
            for agent in AGENTS.ALL_AGENTS:
                if agent["role"]["uuid"] == role_uuid:
                    agents.append(agent)
            return agents
        
        def agents_uuids(role_uuid: str) -> list:
            if not AGENTS.GET_BY_ROLE_UUID.valid(role_uuid):
                return None
            agents_uuids = []
            for agent in AGENTS.GET_BY_ROLE_UUID.agents(role_uuid):
                agents_uuids.append(agent["uuid"])
            return agents_uuids
        
        def agents_names(role_uuid: str) -> list:
            if not AGENTS.GET_BY_ROLE_UUID.valid(role_uuid):
                return None
            agents_names = []
            for uuid in AGENTS.GET_BY_ROLE_UUID.agents_uuids(role_uuid):
                agents_names.append(AGENTS.GET_BY_UUID.name(uuid))
            return agents_names
        
        
    def isPlayable(uuid: str) -> bool:
        agent = AGENTS.GET_BY_UUID.agent(uuid)
        if agent is None:
            return False
        if agent.get("isPlayableCharacter") == True:
            return True
        return False

class MAPS:
    ALL_MAPS = StaticGameData.getMaps()
    
    class GET_UUID:
        def by_name(name: str) -> str:
            for map in MAPS.ALL_MAPS:
                if map["displayName"] == name:
                    return map["uuid"]
            return None

        def by_path(path: str) -> str:
            for map in MAPS.ALL_MAPS:
                if map["assetPath"] == path:
                    return map["uuid"]
            return None
        
        def by_url(url: str) -> str:
            for map in MAPS.ALL_MAPS:
                if map["mapUrl"] == url:
                    return map["uuid"]
            return None

    class GET_BY_UUID:
        def map(uuid: str) -> json:
            for map in MAPS.ALL_MAPS:
                if map["uuid"] == uuid:
                    return map
            return None
        
        def name(uuid: str) -> str:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                return map["displayName"]
            return None

        def images(uuid: str) -> dict:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                images = {
                    "displayIcon": map["displayIcon"],
                    "listViewIcon": map["listViewIcon"],
                    "listViewIconTall": map["listViewIconTall"],
                    "splash": map["splash"],
                    "stylizedBackgroundImage": map["stylizedBackgroundImage"],
                    "premierBackgroundImage": map["premierBackgroundImage"]
                }
                return images
            return None

        def description(uuid: str) -> str:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                return map["tacticalDescription"]
            return None

        def mapUrl(uuid: str) -> str:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                return map["mapUrl"]
            return None

        def assetPath(uuid: str) -> str:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                return map["assetPath"]
            return None

        def callouts(uuid: str) -> json:
            map = MAPS.GET_BY_UUID.map(uuid)
            if map is not None:
                return map["callouts"]
            return None
        
        class DISPLAY:
            def all_variables(uuid: str) -> list:
                map = MAPS.GET_BY_UUID.map(uuid)
                if map is not None:
                    variables = {
                        "xMultiplier": map.get("xMultiplier"),
                        "yMultiplier": map.get("yMultiplier"),
                        "xScalarToAdd": map.get("xScalarToAdd"),
                        "yScalarToAdd": map.get("yScalarToAdd")
                    }
                    return variables
                return None

            def xMultiplier(uuid: str) -> float:
                variables = MAPS.GET_BY_UUID.DISPLAY.all_variables(uuid)
                if variables is not None:
                    return variables["xMultiplier"]
                return None
            
            def yMultiplier(uuid: str) -> float:
                variables = MAPS.GET_BY_UUID.DISPLAY.all_variables(uuid)
                if variables is not None:
                    return variables["yMultiplier"]
                return None
            
            def xScalarToAdd(uuid: str) -> float:
                variables = MAPS.GET_BY_UUID.DISPLAY.all_variables(uuid)
                if variables is not None:
                    return variables["xScalarToAdd"]
                return None
            
            def yScalarToAdd(uuid: str) -> float:
                variables = MAPS.GET_BY_UUID.DISPLAY.all_variables(uuid)
                if variables is not None:
                    return variables["yScalarToAdd"]
                return None

            def displayImage(uuid: str) -> str:
                images = MAPS.GET_BY_UUID.images(uuid)
                if images is not None:
                    return images["displayIcon"]
                return None

class PLAYERCARDS:
    ALL_PLAYER_CARDS = StaticGameData.getPlayerCards()

    class GET_UUID:
        def by_name(name: str) -> str:
            for card in PLAYERCARDS.ALL_PLAYER_CARDS:
                if card["displayName"] == name:
                    return card["uuid"]
            return None

        def by_path(path: str) -> str:
            for card in PLAYERCARDS.ALL_PLAYER_CARDS:
                if card["assetPath"] == path:
                    return card["uuid"]
            return None

    class GET_BY_UUID:
        def card(uuid: str) -> json:
            for card in PLAYERCARDS.ALL_PLAYER_CARDS:
                if card["uuid"] == uuid:
                    return card
            return None
        
        def name(uuid: str) -> str:
            card = PLAYERCARDS.GET_BY_UUID.card(uuid)
            if card is not None:
                return card["displayName"]
            return None

        def images(uuid: str) -> dict:
            card = PLAYERCARDS.GET_BY_UUID.card(uuid)
            if card is not None:
                images = {
                    "displayIcon": card["displayIcon"],
                    "smallArt": card["smallArt"],
                    "wideArt": card["wideArt"],
                    "largeArt": card["largeArt"]
                }
                return images
            return None

        def assetPath(uuid: str) -> str:
            card = PLAYERCARDS.GET_BY_UUID.card(uuid)
            if card is not None:
                return card["assetPath"]
            return None

class PLAYERTITLES:
    ALL_PLAYER_TITLES = StaticGameData.getPlayerTitles()

    class GET_UUID:
        def by_name(name: str) -> str:
            for title in PLAYERTITLES.ALL_PLAYER_TITLES:
                if title["displayName"] == name:
                    return title["uuid"]
            return None

        def by_path(path: str) -> str:
            for title in PLAYERTITLES.ALL_PLAYER_TITLES:
                if title["assetPath"] == path:
                    return title["uuid"]
            return None
        
        def by_title(title: str) -> str:
            for title in PLAYERTITLES.ALL_PLAYER_TITLES:
                if title["titleText"] == title:
                    return title["uuid"]
            return None

    class GET_BY_UUID:
        def player_title(uuid: str) -> json:
            for title in PLAYERTITLES.ALL_PLAYER_TITLES:
                if title["uuid"] == uuid:
                    return title
            return None
        
        def name(uuid: str) -> str:
            title = PLAYERTITLES.GET_BY_UUID.title(uuid)
            if title is not None:
                return title["displayName"]
            return None

        def title(uuid: str) -> str:
            title = PLAYERTITLES.GET_BY_UUID.title(uuid)
            if title is not None:
                return title["titleText"]
            return None

        def path(uuid: str) -> str:
            title = PLAYERTITLES.GET_BY_UUID.title(uuid)
            if title is not None:
                return title["assetPath"]
            return None

class WEAPONS:
    ALL_WEAPONS = StaticGameData.getWeapons()
    
    class GET_UUID:
        def by_name(name: str) -> str:
            for weapon in WEAPONS.ALL_WEAPONS:
                if weapon["displayName"] == name:
                    return weapon["uuid"]
            return None
        
        def by_default_skin_uuid(uuid: str) -> str:
            for weapon in WEAPONS.ALL_WEAPONS:
                if weapon["defaultSkinUuid"] == uuid:
                    return weapon["uuid"]
            return None

    class GET_BY_UUID:
        def weapon(uuid: str) -> json:
            for weapon in WEAPONS.ALL_WEAPONS:
                if weapon["uuid"] == uuid:
                    return weapon
            return None
        
        def name(uuid: str) -> str:
            weapon = WEAPONS.GET_BY_UUID.weapon(uuid)
            if weapon is not None:
                return weapon["displayName"]
            return None
        
        def images(uuid: str) -> dict:
            weapon = WEAPONS.GET_BY_UUID.weapon(uuid)
            if weapon is not None:
                images = {
                    "displayIcon": weapon["displayIcon"],
                    "killStreamIcon": weapon["killfeedIcon"],
                    "shopImage": weapon["shopData"]["newImage"]
                }
                return images
            return None
        
        def stats(uuid: str) -> json:
            weapon = WEAPONS.GET_BY_UUID.weapon(uuid)
            if weapon is not None:
                return weapon["weaponStats"]
            return None
        
        def shopData(uuid: str) -> json:
            weapon = WEAPONS.GET_BY_UUID.weapon(uuid)
            if weapon is not None:
                return weapon["shopData"]
            return None
        
        def skins(uuid: str) -> json:
            weapon = WEAPONS.GET_BY_UUID.shopData(uuid)
            if weapon is not None:
                return weapon["skins"]
            return None

class GEAR:
    ALL_GEAR = StaticGameData.getGear()
    
    class GET_UUID:
        def by_name(name: str) -> str:
            for gear in GEAR.ALL_GEAR:
                if gear["displayName"] == name:
                    return gear["uuid"]
            return None
        
        def by_path(path: str) -> str:
            for gear in GEAR.ALL_GEAR:
                if gear["assetPath"] == path:
                    return gear["uuid"]
            return None
        
        def by_cost(cost: int) -> str:
            for gear in GEAR.ALL_GEAR:
                if gear["shopData"]["cost"] == cost:
                    return gear["uuid"]
            return None
        
    class GET_BY_UUID:
        def gear(uuid: str) -> json:
            for gear in GEAR.ALL_GEAR:
                if gear["uuid"] == uuid:
                    return gear
            return None
        
        def name(uuid: str) -> str:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["displayName"]
            return None
        
        def image(uuid: str) -> str:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["displayIcon"]
            return None
        
        def description(uuid: str) -> str:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["description"]
            return None
        
        def shopData(uuid: str) -> json:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["shopData"]
            return None

        def details(uuid: str) -> json:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["details"]
            return None
        
        def path(uuid: str) -> str:
            gear = GEAR.GET_BY_UUID.gear(uuid)
            if gear is not None:
                return gear["assetPath"]
            return None



