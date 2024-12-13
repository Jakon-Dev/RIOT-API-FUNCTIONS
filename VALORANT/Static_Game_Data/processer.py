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
                role = AGENTS.ROLE.all(uuid)
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
    pass

class PLAYERCARDS:
    pass

class PLAYERTITLES:
    pass

class WEAPONS:
    pass

class GEAR:
    pass

