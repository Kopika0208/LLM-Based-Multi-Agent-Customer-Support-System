from agents.retrieval_agent import RetrievalAgent
from agents.intent_agent import IntentAgent
from agents.action_agent import ActionAgent
from agents.memory_agent import MemoryAgent

class OrchestratorAgent:
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.intent_agent = IntentAgent()
        self.action_agent = ActionAgent()
        self.memory_agent = MemoryAgent()

    def handle_query(self, user_query, user_id="default_user"):
        # Step 1: Detect intent
        intent = self.intent_agent.detect_intent(user_query)

        # Step 2: Retrieve answer from knowledge base
        kb_response = self.retrieval_agent.retrieve(user_query)

        # Step 3: Incorporate conversation memory
        memory_context = self.memory_agent.get_context(user_id)
        self.memory_agent.update_context(user_id, user_query)

        # Step 4: Decide if an action is needed
        action_response = self.action_agent.perform_action(intent, user_query)

        # Step 5: Construct final response
        final_response = f"{kb_response}\n{action_response}"
        return final_response
