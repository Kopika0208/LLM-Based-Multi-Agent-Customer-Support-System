class ActionAgent:
    def perform_action(self, intent, query):
        # Refund or return-related actions
        if "refund" in intent or "return" in intent:
            return (
                "Refund/Return process initiated. "
            )
        # Support ticket creation
        elif "ticket" in intent or "support" in intent:
            return "Support ticket created (simulated). Our team will contact you shortly."
        # Escalation
        elif "escalate" in intent or "urgent" in intent:
            return "Issue escalated to supervisor (simulated). You will receive a response soon."
        # No action needed
        else:
            return ""  # No action needed
