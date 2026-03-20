#importing prompttemplate class from llamaindex for newer version it's llma_index.core.prompts

from llama_index.core.prompts import PromptTemplate
my_context="" 
my_query=""

qa_prompt_tmpl_str = """\
    context information is below.
    ---------------------
    {my_context}
    ---------------------
    Given the context information and not prior knowledge, answer the question.
    Question: {my_query}
    Answer: \
    """
#variable mapping for the prompt template
template_var_mappings={"context_str":"my_context", "query_str":"my_query"}

#prompt template creation with variable mapping                  
prompt_tmpl=PromptTemplate(qa_prompt_tmpl_str, template_var_mappings=template_var_mappings)
#formatting the prompt template by providing values for my_context and my_query, which will be mapped to context_str and query_str respectively in the prompt template
fmt_prompt=prompt_tmpl.format(my_context="The sky is blue.", my_query="What color is the sky?")
print(fmt_prompt)