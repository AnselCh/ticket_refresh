from typing import Dict
from bs4 import BeautifulSoup

def parse_title(soup:BeautifulSoup) -> None:
    h2s = soup.find_all('h2', {"class": "activityT title"})
    if h2s:
    	return h2s[0].text
    return None

def parse_zone_info(soup:BeautifulSoup) -> Dict[str, str]:
    """
    return zone_list/area_list format
        verbose_area_list: group_#
        e.g. "一樓站區 已售完": group_22542
    """
    zone_area_list = soup.find("div", {"class": "zone area-list"})
    zones = zone_area_list.find_all("div", {"class": "zone-label"})
    if zones:
        # Multiple zones
        zone_group_dict = {}
        for zone in zones:
            group_id = zone.attrs["data-id"]
            zone_label = zone.find("b").contents[0]
            zone_group_dict[zone_label] = group_id
        return zone_group_dict
    else:
        # 1 zone
        area_list = zone_area_list.find_all("ul", {"class": "area-list"})
        # each ul is an area
        area_group_dict = {}
        for area in area_list:
            group_id = area.attrs["id"]
            area_label = area.find("font").contents[0]
            area_group_dict[area_label] = group_id
        return area_group_dict

