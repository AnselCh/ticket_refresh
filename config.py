import json

import questionary

from requests_operations import validate_line_token, validate_url

def input_number(num: str) -> int:
    try:
        num = int(num)
        if num < 0:
            return -1
        return num
    except:
        return -1
        

def create_config_content() -> dict:
    questionary.print(
        "\n未找到設定檔，現在開始創建設定檔\n",
        style="bold fg:lightgreen")

    notification_type = questionary.checkbox(
        '選擇通知方式 (上下鍵移動｜空白鍵選擇｜Enter送出)',
        choices = [
            "跳出視窗通知",
            "傳送Line通知"
        ]
    ).ask()

    line_token = questionary.text(
        "輸入Line權杖（可從 https://notify-bot.line.me/my/ 申請或是按Enter跳過）："
    ).skip_if("傳送Line通知" not in notification_type).ask()

    if line_token:
        line_token = line_token.strip()
        line_token_valid, reason = validate_line_token(line_token)
        if not line_token_valid:
            questionary.print(
                "權杖無效，請從 https://notify-bot.line.me/my/ 申請或是稍後修改config.json檔",
                style="bold italic fg:red")
            line_token = ""
            notification_type.remove("傳送Line通知")
        else:
            questionary.print(
                ">>> 權杖驗證成功！",
                style="bold fg:lightyellow"
            )

    set_target = questionary.confirm(
        "是否預先設定監控網址及區間？"
    ).ask()

    url = questionary.text(
        "輸入網址（或稍後從config.json設定/或在執行程式時輸入）："
    ).skip_if(not set_target).ask()

    if url:
        url = url.strip()
        url_valid, reason = validate_url(url)
        if not url_valid:
            questionary.print(
                "網址無效，請稍候從config.json設定",
                style="bold italic fg:red")
            url = ""
        else:
            questionary.print(
                ">>> 網址存在！",
                style="bold fg:lightyellow"
            )

    start_group_number = questionary.text(
        "起始編號（或稍後從config.json設定/或在執行程式時輸入）："
    ).skip_if(not set_target).ask()

    end_group_number = questionary.text(
        "終止編號（或稍後從config.json設定/或在執行程式時輸入）："
    ).skip_if(not set_target).ask()

    config = {
        "notification_type":
        {
            "Window": "跳出視窗通知" in notification_type,
            "line": "傳送Line通知" in notification_type
        },
        "token":
        {
            "line": line_token or ""
        },
        "target":
        {
            "url": url or "",
            "start": input_number(start_group_number),
            "end": input_number(end_group_number)
        }
    }
    
    questionary.print(f"\n設定檔：\n{json.dumps(config, indent=3)}\n", style="bold fg:lightblue")
    return config

if __name__ == "__main__":
    create_config_content()