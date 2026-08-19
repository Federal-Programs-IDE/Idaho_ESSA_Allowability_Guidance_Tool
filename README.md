A search tool users can access on a web browser to receive guidance on what expenses are allowable, as well as relevant information

Initially developed in python.  'embeddings' is from an LLM that translates user entries and connects to the 'allowable_use_mapping.csv" to provide guidance.

allowable_use_mapping.csv is the document created from the Use of Funds Mannual

app.py was the original python code to make this, which was converted to grant_guidance_tool.html

index.html is the code that puts it all together

**CAREFUL LOOKING AT THE blocked_words.txt FILE**

Unfortunately there isn't an easy way to tell a computer what is suggestive, inappropriate, derogatory, or otherwise offensive without making an explicit list. The list contains those words. If anyone enters something that is either in that list, or similar to what's in the list, an error message will appear. I did this so that people don't enter inappropriate things, the LLM forces a response, and it gives the wrong impression we're saying the innaporpriate thing is reimbursable. Don't blame me, blame the weirdos who go online.

Final app found at:
https://federal-programs-ide.github.io/Idaho_ESSA_Allowability_Guidance_Tool/
