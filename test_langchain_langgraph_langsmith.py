"""
LangChain, LangGraph, and LangSmith tests for ollama-mac.

Run with the LangSmith conda environment:
  conda activate LangSmith
  cd src/python && pytest tests/test_langchain_langgraph_langsmith.py -v

Or from repo root:
  conda run -n LangSmith pytest src/python/tests/ -v
"""

import os
import pytest


# ---------------------------------------------------------------------------
# LangChain tests
# ---------------------------------------------------------------------------

def test_langchain_imports():
    """LangChain core and community are importable."""
    import langchain_core
    import langchain_community
    assert langchain_core.__version__
    assert langchain_community.__version__


def test_langchain_simple_chain():
    """Build and run a simple LCEL chain with a fake LLM."""
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_community.chat_models.fake import FakeListChatModel

    model = FakeListChatModel(responses=["Hello from LangChain."])
    prompt = ChatPromptTemplate.from_messages([("human", "{input}")])
    chain = prompt | model

    result = chain.invoke({"input": "Hi"})
    assert result is not None
    assert isinstance(result, AIMessage)
    assert "Hello from LangChain" in result.content


def test_langchain_prompt_template():
    """Prompt template and output parser work together."""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_community.chat_models.fake import FakeListChatModel

    model = FakeListChatModel(responses=["42"])
    chain = (
        ChatPromptTemplate.from_template("What is 40+2? Reply with one number.")
        | model
        | StrOutputParser()
    )
    out = chain.invoke({})
    assert out.strip() == "42"


# ---------------------------------------------------------------------------
# LangGraph tests
# ---------------------------------------------------------------------------

def test_langgraph_imports():
    """LangGraph is importable."""
    import langgraph
    from langgraph.graph import StateGraph
    assert StateGraph is not None


def test_langgraph_simple_graph():
    """Build and invoke a minimal LangGraph StateGraph."""
    from typing import Annotated, TypedDict
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain_community.chat_models.fake import FakeListChatModel

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def node_call_model(state: State) -> State:
        model = FakeListChatModel(responses=["Echo from LangGraph."])
        last = state["messages"][-1]
        response = model.invoke([last])
        return {"messages": [response]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("model", node_call_model)
    graph_builder.add_edge("__start__", "model")
    graph_builder.add_edge("model", END)

    graph = graph_builder.compile()
    result = graph.invoke({"messages": [HumanMessage(content="Hello")]})

    assert "messages" in result
    msgs = result["messages"]
    assert len(msgs) >= 1
    assert any("Echo from LangGraph" in (m.content if hasattr(m, "content") else str(m)) for m in msgs)


def test_langgraph_two_node_graph():
    """Graph with two nodes and state passing."""
    from typing import TypedDict
    from langgraph.graph import StateGraph, END
    from langchain_community.chat_models.fake import FakeListChatModel

    class State(TypedDict):
        value: str

    def node_a(state: State) -> State:
        return {"value": state.get("value", "") + "A"}

    def node_b(state: State) -> State:
        return {"value": state.get("value", "") + "B"}

    builder = StateGraph(State)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_edge("__start__", "a")
    builder.add_edge("a", "b")
    builder.add_edge("b", END)

    graph = builder.compile()
    out = graph.invoke({"value": ""})
    assert out["value"] == "AB"


# ---------------------------------------------------------------------------
# LangSmith tests
# ---------------------------------------------------------------------------

def test_langsmith_imports():
    """LangSmith client and tracing utilities are importable."""
    import langsmith
    from langsmith import Client
    assert langsmith.__version__
    assert Client is not None


def test_langsmith_tracing_context():
    """tracing_v2_enabled context manager is available and can be used."""
    from langchain_core.tracers.context import tracing_v2_enabled

    # Without API key we only check the context manager exists and can be entered
    with tracing_v2_enabled(project_name="ollama-mac-tests"):
        pass  # No-op; real trace would require LANGCHAIN_API_KEY


def test_langsmith_env_vars_documented():
    """Standard LangSmith env var names are known (for docs/setup)."""
    expected = {
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_PROJECT",
        "LANGCHAIN_ENDPOINT",
    }
    for name in expected:
        assert name.isupper()
        assert name.startswith("LANGCHAIN_")


@pytest.mark.skipif(
    not os.environ.get("LANGCHAIN_API_KEY"),
    reason="LANGCHAIN_API_KEY not set; optional integration test",
)
def test_langsmith_traced_invocation():
    """With LANGCHAIN_API_KEY set, a traced chain run is sent to LangSmith."""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_community.chat_models.fake import FakeListChatModel
    from langchain_core.tracers.context import tracing_v2_enabled

    model = FakeListChatModel(responses=["Traced reply"])
    chain = (
        ChatPromptTemplate.from_template("Say: {text}")
        | model
        | StrOutputParser()
    )
    with tracing_v2_enabled(project_name="ollama-mac-tests"):
        result = chain.invoke({"text": "hello"})
    assert "Traced reply" in result
