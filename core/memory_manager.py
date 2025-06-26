import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import uuid
from dataclasses import dataclass, asdict, field
from schemas import ChatRequest, ChatMessage, ToolMessage

@dataclass
class Conversation:
    id: str
    title: str
    messages: List[ChatMessage]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

class MemoryManager:
    """记忆管理系统（支持持久化）"""
    def __init__(self, storage_dir: str = "conversation_data"):
        self.storage_dir = storage_dir
        self.current_conversation: Optional[Conversation] = None
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_conversation_path(self, conv_id: str) -> str:
        return os.path.join(self.storage_dir, f"{conv_id}.json")
    
    def start_new_conversation(self, first_message: Optional[str] = None) -> Conversation:
        """创建新对话"""
        conv_id = str(uuid.uuid4())
        title = first_message[:30] + "..." if first_message else "新对话"
        
        self.current_conversation = Conversation(
            id=conv_id,
            title=title,
            messages=[]
        )
        self.save_conversation()
        return self.current_conversation

    def add_message(self, role: str, content: str):
        """添加消息到当前对话"""
        if self.current_conversation is None:
            self.start_new_conversation(content)
        
        self.current_conversation.messages.append(ChatMessage(role=role, content=content))
        self.current_conversation.updated_at = datetime.now().isoformat()
        self.save_conversation()
    
    def save_conversation(self):
        """持久化当前对话"""
        if self.current_conversation:
            path = self._get_conversation_path(self.current_conversation.id)
            conv_dict = {
                "id": self.current_conversation.id,
                "title": self.current_conversation.title,
                "messages": [msg.model_dump() for msg in self.current_conversation.messages],
                "created_at": self.current_conversation.created_at,
                "updated_at": self.current_conversation.updated_at
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(conv_dict, f, ensure_ascii=False, indent=2)

    def load_conversation(self, conv_id: str) -> Conversation:
        """加载特定对话"""
        path = self._get_conversation_path(conv_id)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            messages = [ChatMessage(**msg) for msg in data['messages']]
            conv = Conversation(
                id=data['id'],
                title=data['title'],
                messages=messages,
                created_at=data['created_at']
            )
            self.current_conversation = conv
            return conv
    
    def list_conversations(self) -> List[Dict]:
        """列出所有历史对话（元数据）"""
        convs = []
        for fname in os.listdir(self.storage_dir):
            if fname.endswith('.json'):
                path = os.path.join(self.storage_dir, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    convs.append({
                        'id': data['id'],
                        'title': data['title'],
                        'updated_at': data.get('updated_at', data['created_at']),
                        'message_count': len(data['messages'])
                    })
        
        # 按最后更新时间排序
        return sorted(convs, key=lambda x: x['updated_at'], reverse=True)
    
    def delete_conversation(self, conv_id: str) -> bool:
        """
        删除指定对话
        :param conv_id: 对话ID
        :return: 是否删除成功
        """
        path = self._get_conversation_path(conv_id)
        try:
            if os.path.exists(path):
                os.remove(path)
                # 如果删除的是当前对话，清除引用
                if self.current_conversation and self.current_conversation.id == conv_id:
                    self.current_conversation = None
                return True
            return False
        except Exception as e:
            return False
    
    def clear_all_conversations(self):
        """清空所有对话（危险操作）"""
        print("警告：这将删除所有对话记录！")
        choice = input("确认全部删除？(输入'DELETEALL'确认): ").strip()
        if choice == "DELETEALL":
            for fname in os.listdir(self.storage_dir):
                if fname.endswith('.json'):
                    os.remove(os.path.join(self.storage_dir, fname))
            self.current_conversation = None
            print("已删除所有对话")
            return True
        print("取消操作")
        return False
    