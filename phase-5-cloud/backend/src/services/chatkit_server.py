"""
ChatKit server implementation with task management widgets.

This module provides a ChatKit server that integrates with the existing
Agent SDK and MCP tools to provide a widget-based chat interface.
"""

import logging
from typing import Any, AsyncIterator

from agents import Agent, Runner
from chatkit.server import ChatKitServer, ThreadStreamEvent, ThreadMetadata, UserMessageItem, Store
from chatkit.agents import AgentContext, stream_agent_response, simple_to_agent_input

from ..agents.todo_agent import create_todo_agent
from ..mcp.tools import set_tool_context

logger = logging.getLogger(__name__)


class TaskChatKitServer(ChatKitServer):
    """ChatKit server for task management with widget support."""

    def __init__(self, store: Store):
        """
        Initialize the ChatKit server.

        Args:
            store: ChatKit store for persisting threads and messages
        """
        super().__init__(store)
        self.agent: Agent = create_todo_agent()
        logger.info("TaskChatKitServer initialized")

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """
        Process user messages and stream responses.

        Args:
            thread: Thread metadata
            input: User message
            context: Request context containing user_id

        Yields:
            ThreadStreamEvent: Chat events (text, widgets, etc.)
        """
        # Extract user_id from context
        user_id = context.get("user_id")
        if not user_id:
            logger.error("No user_id in context")
            # TODO: Yield error event
            return

        logger.info(
            f"Processing message for user {user_id}, thread {thread.id}"
        )

        # Set tool context for MCP tools
        # Note: We pass None for session since MCP tools create their own sessions
        set_tool_context(None, user_id)

        # Create agent context with user info
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Add user name to context for personalization
        user_name = context.get("user_name", "there")
        logger.info(f"User name for personalization: {user_name}")

        # Convert ChatKit input to Agent SDK format
        agent_input = await simple_to_agent_input(input) if input else []

        # Prepend user context to agent input for personalization
        personalized_input = [
            {"role": "system", "content": f"The user's name is {user_name}. Address them by name when appropriate."}
        ] + agent_input

        # Run agent with streaming
        result = Runner.run_streamed(
            self.agent,
            personalized_input,
            context=agent_context,
        )

        # Stream agent response (widgets are streamed directly by tools)
        async for event in stream_agent_response(agent_context, result):
            yield event

        logger.info(f"Completed response for thread {thread.id}")
