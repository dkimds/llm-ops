import langsmith
from langchain_core.runnables import chain
from langsmith.run_helpers import get_current_run_tree

@chain
def child_chain(inputs):
    return inputs["test"] + 1

def child_wrappers(x, headers):
    with langsmith.tracing_context(parent=headers):
        child_chain.invokr({"test": x})

@chain
def parent_chain(inputs):

    rt = get_current_run_tree()
    headers = rt.to_headers()
    # ... make a request to another service with the headers
    # The headers should be passed to the other service, eventually to the child_wrapper function

parent_chain.invoke({"test": 1})
