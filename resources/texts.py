# resources/texts.py

BANNER = """ 
   _____      __          ___              
  / ___/___  / /___  ____/ (_)___  _____   
  \__ \/ _ \/ / __ \/ __  / / __ \/ ___/   
 ___/ /  __/ / /_/ / /_/ / / /_/ / /      
/____/\___/_/\____/\__,_/_/\____/_/       
                                          
多轮对话智能体（输入 help 查看命令帮助）"""

HELP_TEXT = """可用命令：
new         - 新建对话
history     - 查看历史对话列表
load [id]   - 加载指定对话
delete [id] - 删除指定对话 
exit        - 退出程序"""

ERROR_MESSAGES = {
    "invalid_command": "⚠️ 无效命令",
    "load_failed": "加载失败：{error}",
    "not_found": "找不到对话：{id}",
    "delete_failed": "删除失败：{error}"
}
