from llama_index.core.prompts import PromptTemplate
#Defines the template string with two placeholders ({context_str} and {query_str})
qa_prompt_tmpl_str = """\
    context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and not prior knowledge, answer the question.
    question: {query_str}
    answer: \
    """
#function to format the context string with bullet points
def format_context_fn(**kwargs):
    #format context with bullet points
    context_list=kwargs.get("context_str").split("\n")
    fntted_context="\n".join([f"- {c}" for c in context_list])
    return fntted_context
#creating a prompt template object with the custom formatting function for context_str
prompt_tmpl=PromptTemplate(qa_prompt_tmpl_str, function_mappings={"context_str": format_context_fn})

context_str="""\
in thsi example, we will see how to use function mapping in prompt template to format the context string with bullet points.
we will define a custom formatting function that takes the context string, splits it into lines, and formats each line with a bullet point. we will then pass this function as a mapping for the context_str placeholder in the prompt template. when we format the prompt template with a context string, the custom formatting function will be applied to the context string, and the formatted context will be included in the final prompt.
our context string will have multiple lines, and we want to format it with bullet points for better readability.
\
"""

#
fmt_prompt=prompt_tmpl.format(context_str=context_str, query_str="What context string was formatted?")
print(fmt_prompt)