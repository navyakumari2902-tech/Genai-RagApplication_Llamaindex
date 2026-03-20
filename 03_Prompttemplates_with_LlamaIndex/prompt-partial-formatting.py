#importing prompttemplate class from llamaindex for newer version it's llma_index.core.prompts
from llama_index.core.prompts import PromptTemplate
#define a prompt template string with three place holders: context_str, query_str, and tone_name
qa_prompt_tmpl_str = """\
    context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and not prior knowledge, answer the question.
    please answer in a {tone_name} tone.
    Question: {query_str}   
    Answer: \
    """
#creating an object prompt_tmpl of prompttemplate class
prompt_tmpl=PromptTemplate(qa_prompt_tmpl_str)

#partially formatting the prompt template by providing a value for tone_name, leaving context_str and query_str as placeholders
partial_prompt_tmpl=prompt_tmpl.partial_format(tone_name="friendly")

#printing the partially formatted prompt template to see the result
fmt_prompt=partial_prompt_tmpl.format(context_str="The sky is blue.", query_str="What color is the sky?")
print(fmt_prompt)