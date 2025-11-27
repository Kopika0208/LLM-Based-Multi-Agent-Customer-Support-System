# memory_agent.py
class MemoryAgent:
    def __init__(self):
        self.memory_store = {}

    def get_context(self, user_id):
        return " ".join(self.memory_store.get(user_id, []))

    def update_context(self, user_id, message):
        if user_id not in self.memory_store:
            self.memory_store[user_id] = []
        self.memory_store[user_id].append(message)
        # Keep last 5 messages only
        self.memory_store[user_id] = self.memory_store[user_id][-5:]
