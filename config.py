import json
from typing import Dict, List, Tuple

import questionary

from requests_operations import validate_line_token, validate_url
from requests_operations import request
import html_parser as parser

def pretty_print_config(config):
    config = validate_config(config)
    notification_type = "通知方式： "
    if config["notification_type"]["window"]:
        notification_type += "跳出視窗通知 "
    if config["notification_type"]["line"]:
        notification_type += "傳送Line通知 (權杖已驗證)"
    questionary.print(notification_type, style="bold fg:lightgreen")

    title = config["target"].get("title")
    if title:
        questionary.print(f"監控活動：{title}", style="bold fg:lightgreen")
    zone_verboses = config["target"].get("zone_verboses")
    if zone_verboses:
        questionary.print(f"監控票區：{zone_verboses}", style="bold fg:lightgreen")

def validate_config(config):
    """
    {
        "notification_type": {
            "window": false,
            "line": true
        },
        "token": {
            "line": ""
        },
        "target": {
            "url": "",
            "group_ids": []
        }
    }
    """
    # Existance Check
    if "notification_type" not in config.keys():
        config["notification_type"] = ask_for_notification_type()
    if "token" not in config.keys():
        config["token"] = {}
    if "target" not in config.keys():
        config["target"] = ask_for_target()
    if "url" not in config["target"]:
        config["target"] = ask_for_target()
    if "group_ids" not in config["target"]:
        config["target"] = ask_for_target(config["target"]["url"])

    # Value Check
    if config["notification_type"]["line"] and not config["token"].get("line"):
        notification_type, line_token = ask_for_line_token(config["notification_type"], True)
        config["notification_type"] = notification_type
        config["token"]["line"] = line_token
    if not config["target"].get("url"):
        config["target"] = ask_for_target()
    if not len(config["target"].get("group_ids")):
        config["target"] = ask_for_target(config["target"]["url"])

    # Validate
    if config["notification_type"]["line"]:
        valid, reason = validate_line_token(config["token"]["line"])
        if not valid:
            questionary.print(
                "設定的權杖無效，請從 https://notify-bot.line.me/my/ 申請或是稍後修改config.json檔",
                style="bold italic fg:red")
            notification_type, line_token = ask_for_line_token(config["notification_type"], True)
            config["notification_type"] = notification_type
            config["token"]["line"] = line_token
    valid, reason = validate_url(config["target"]["url"])
    if not valid:
        questionary.print(
            "設定的網址無效，請重新輸入",
            style="bold italic fg:red")
        config["target"] = ask_for_target()
    return config

def ask_for_notification_type() -> dict:
    answer = questionary.checkbox(
        '選擇通知方式 (上下鍵移動｜按空白鍵勾選(可複選)｜Enter確認)',
        choices = [
            "跳出視窗通知",
            "傳送Line通知"
        ]
    ).ask()
    return {
        "window": "跳出視窗通知" in answer,
        "line": "傳送Line通知" in answer
    }

def ask_for_line_token(notification_type, required=False) -> Tuple[dict, str]:

    while True:
        line_token = questionary.password(
            "輸入Line權杖（可從 https://notify-bot.line.me/my/ 申請或是按Enter跳過）："
        ).skip_if(not notification_type.get("line")).ask() or ""

        line_token = line_token.strip()
        line_token_valid, reason = validate_line_token(line_token)

        if line_token_valid:
            questionary.print(">>> 權杖驗證成功！", style="bold fg:lightyellow")
            break

        if required:
            cancel = questionary.confirm("權杖無效，是否不使用Line通知？").ask()

        if not required or cancel:
            if line_token:
                questionary.print(
                    "權杖無效，請從 https://notify-bot.line.me/my/ 申請或是稍後修改config.json檔",
                    style="bold italic fg:red")
                line_token = ""
            notification_type["line"] = False
            break

        questionary.print(
            "權杖無效。請重新輸入",
            style="bold italic fg:red")

    return notification_type, line_token


def ask_for_target(url="") -> dict:
    while True:
        if not url:
            url = questionary.text(
                "輸入網址："
            ).ask()
        url = url.strip()
        url_valid, reason = validate_url(url)
        if not url_valid:
            questionary.print(
                f"網址無效 ({url}, {reason})，請重新輸入",
                style="bold italic fg:red")
            url = ""
        else:
            soup = request(url)
            title = parser.parse_title(soup)
            if questionary.confirm(f"確認監控{title}嗎？").ask():
                break
            url = ""

    zone_info_dict = parser.parse_zone_info(soup)
    group_ids, zone_verboses = ask_for_region(zone_info_dict)
    return {
        "url": url,
        "group_ids": group_ids,
        "title": title,
        "zone_verboses": zone_verboses
    }

def ask_for_region(regions: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """
    regions format
        verbose_region: group_#
        e.g. "一樓站區 已售完": group_22542
    """
    keys = questionary.checkbox(
        "選擇要監控的範圍 (上下鍵移動｜按空白鍵勾選(可複選)｜Enter確認)",
        regions.keys()).ask()
    return [regions[k] for k in keys], keys

def create_config_content() -> dict:
    questionary.print(
        "現在開始創建設定檔",
        style="bold fg:lightgreen")

    notification_type = ask_for_notification_type()

    notification_type, line_token = ask_for_line_token(notification_type)

    target = {"url": "", "group_ids": []}
    if questionary.confirm("是否預先設定監控網址及區間？").ask():
        target = ask_for_target()

    config = {
        "notification_type": notification_type,
        "token":
        {
            "line": line_token or ""
        },
        "target": target
    }

    # questionary.print(f"\n設定檔：\n{json.dumps(config, indent=3)}\n", style="bold fg:lightblue")
    return config

    # 判斷是否沿用舊的設定
def ask_for_reset(config):
    with open(config, "r") as f:
        config_data = json.load(f)
        title = config_data["target"].get("title")
    if title:
        questionary.print(f"監控：{title}中", style="bold fg:lightgreen")
    zone_verboses = config_data["target"].get("zone_verboses")
    if zone_verboses:
        questionary.print(f"監控票區：{zone_verboses}", style="bold fg:lightgreen")
    
    reset_config = 0  # 預設值為 0
    if not questionary.confirm("請問是否繼續使用此設定檔？").ask():
        questionary.print("建立新的設定檔...", style="bold fg:lightgreen")
        reset_config = 1

    return reset_config



if __name__ == "__main__":
    create_config_content()