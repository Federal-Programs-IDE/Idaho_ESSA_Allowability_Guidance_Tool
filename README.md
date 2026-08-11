A search tool users can access on a web browser to receive guidance on what expenses are allowable, as well as relevant information

Initially developed in python.  'embeddings' is from an LLM that translates user entries and connects to the 'allowable_use_mapping.csv" to provide guidance.

allowable_use_mapping.csv is the document created from the Use of Funds Mannual

app.py is the main file the program is run through

the config.toml file sets up the color schemes (works in conjunction with the color scheme at the beginning of the app.py file

****CAREFUL LOOKING AT THE blocked_words.txt FILE******
To ensure individuals don't get misleading guidance when entering inappropriate prompts, that file is referenced. Unfortunately there isn't an easy way to tell a computer what is suggestive, inappropriate, derogatory, or otherwise offensive without making an explicit list. The list contains those words. People are weird, end statement.

Final app found at:
https://idaho-essa-allowability.streamlit.app/
