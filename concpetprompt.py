# raisecard.py

# encoding:utf-8
import os
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

@plugins.register(
    name="ConceptPlugin",
    desire_priority=100,
    hidden=False,
    desc="A plugin that generates responses based on concept prompts",
    version="0.1",
    author="Your Name",
)
class ConceptPlugin(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            self.prompt_file = self.load_prompt()
            logger.info("[ConceptPlugin] initialized.")
        except Exception as e:
            logger.warn("[ConceptPlugin] init failed, ignore.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        content = e_context["context"].content.strip()
        
        if content.startswith("概念"):
            concept = content.replace("概念", "").strip()
            response = self.generate_response(concept)
            reply = Reply(ReplyType.TEXT, response)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, **kwargs):
        help_text = "输入【概念 [内容]】来获取基于概念的回答。"
        return help_text

    def load_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "concept_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_path}")
            return ""

    def generate_response(self, concept):
        # 这里您可以使用 self.prompt_file 和 concept 来生成回答
        # 示例实现（您需要根据实际情况修改）：
        prompt = self.prompt_file.replace("{concept}", concept)
        # 这里应该调用您的 AI 模型或其他逻辑来生成回答
        # 示例：response = ai_model.generate(prompt)
        response = f"关于 '{concept}' 的回答：[这里是生成的回答]"
        return response

# 示例调用
if __name__ == "__main__":
    plugin = ConceptPlugin()
    print(plugin.generate_response("人工智能"))
