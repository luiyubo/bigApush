"""飞书机器人通知 + Server酱微信推送"""
import json
import logging
import os  # 👈 新增：用来读取环境变量
import requests

logger = logging.getLogger(__name__)


class FeishuNotifier:
    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url
        # 👈 新增：读取你在 GitHub Secrets 里配置的 Server酱 AppKey
        self.server3_key = os.environ.get("SERVER3_SEND_KEY")

    def send_text(self, text: str) -> bool:
        # 1. 尝试发送飞书
        if self.webhook_url:
            payload = {"msg_type": "text", "content": {"text": text}}
            try:
                resp = requests.post(self.webhook_url, json=payload, timeout=10)
                result = resp.json()
                if result.get("code") == 0:
                    logger.info("飞书推送成功")
                else:
                    logger.error("飞书推送失败: %s", result)
            except Exception as e:
                logger.error("飞书推送异常: %s", e)
        else:
            logger.warning("飞书 webhook_url 未配置，跳过飞书推送")

        # 2. 👈 新增：尝试发送微信推送
        if self.server3_key:
            wx_url = f"https://sctapi.ftqq.com/{self.server3_key}.send"
            wx_data = {
                "title": "今日A股量化选股推送",
                "desp": text  # 内容
            }
            try:
                resp = requests.post(wx_url, data=wx_data, timeout=10)
                result = resp.json()
                if result.get("code") == 0:
                    logger.info("微信推送成功")
                    return True
                logger.error("微信推送失败: %s", result)
            except Exception as e:
                logger.error("微信推送异常: %s", e)
        else:
            logger.warning("SERVER3_SEND_KEY 未配置，跳过微信推送")

        return False

    def send_post(self, title: str, content_lines: list) -> bool:
        # 1. 尝试发送飞书
        if self.webhook_url:
            post_content = []
            for line in content_lines:
                post_content.append([{"tag": "text", "text": line}])
            payload = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": post_content
                        }
                    }
                }
            }
            try:
                resp = requests.post(self.webhook_url, json=payload, timeout=10)
                result = resp.json()
                if result.get("code") == 0:
                    logger.info("飞书推送成功")
                else:
                    logger.error("飞书推送失败: %s", result)
            except Exception as e:
                logger.error("飞书推送异常: %s", e)
        else:
            logger.warning("飞书 webhook_url 未配置，跳过飞书推送")

        # 2. 👈 新增：尝试发送微信推送
        if self.server3_key:
            wx_url = f"https://sctapi.ftqq.com/{self.server3_key}.send"
            # 微信不支持复杂的富文本排版，我们将列表用换行符合并成纯文本发送
            wx_text = "\n".join(content_lines)
            wx_data = {
                "title": title,
                "desp": wx_text
            }
            try:
                resp = requests.post(wx_url, data=wx_data, timeout=10)
                result = resp.json()
                if result.get("code") == 0:
                    logger.info("微信推送成功")
                    return True
                logger.error("微信推送失败: %s", result)
            except Exception as e:
                logger.error("微信推送异常: %s", e)
        else:
            logger.warning("SERVER3_SEND_KEY 未配置，跳过微信推送")

        return False