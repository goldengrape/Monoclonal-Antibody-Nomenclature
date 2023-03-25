import streamlit as st
from generate_name import generate_name,check_in_languages
from query import main as query_poca
import asyncio
import openai 
import os 
import platform


st.title("Ideas for Monoclonal Antibody Nomenclature")
st.info("This app is powered by [OpenAI](https://openai.com/) and [POCA](https://poca.ai/).")
st.markdown("## Input your API key")
openai_api_key=st.text_input(" ",value="",type="password")
openai.api_key=openai_api_key or os.environ.get("OPENAI_API_KEY")

stem_info=[
'''
**Group 1 -tug for unmodified immunoglobulins**

Monospecific full length and Fc unmodified immunoglobulins of any class. Molecules which might 
occur as such in the immune system. Including:
- IgG, IgA, IgM, IgD, IgE
- only allelic variants
- Glycoengineering without mutation
- C-terminal lysine deletion without any other mutation in the Fc region''',

'''
**Group 2 -bart for antibody artificial**

Monospecific full length immunoglobulins with engineered constant domains (CH1/2/3).
Monospecific full length immunoglobulins that contain any point mutation introduced by engineering 
for any reason anywhere (hinge, new glycan attachment site, mixed allelic variants which would not 
occur in nature, altered complement binding, altered FcRn binding, altered Fc-gamma receptor binding, 
etc.)
e.g. IGHG4 with S>P mutation, stabilized IgA''',
'''
**Group 3 -mig for multi-immunoglobulin**

Bi- and multi-specific immunoglobulins regardless of the format, type or shape (full length, full length 
plus, fragments)''',
'''
**Group 4 -ment for fragment**

All monospecific domains, fragments of any kind, derived from an immunoglobulin variable domain
(all monospecific constructs that do not contain an Fc domain)
''']
st.markdown("## Select a Stem")
col1, col2=st.columns(2)
stem_selection=[
    'Group 1 -tug for unmodified immunoglobulins',
    'Group 2 -bart for antibody artificial',
    'Group 3 -mig for multi-immunoglobulin',
    'Group 4 -ment for fragment'
    ]
stem_choice=col1.radio(" ",stem_selection,
    index=0)
stem_index=stem_selection.index(stem_choice)
col2.markdown(stem_info[stem_index])

infix_selection=[
"-ami- serum amyloid protein (SAP)/amyloidosis (presubstem)",
"-ba- bacterial",
"-ci- cardiovascular",
"-de- metabolic or endocrine pathways",
"-eni- enzyme inhibition",
"-fung- fungal",
"-gro- skeletal muscle mass related growth factors and receptors (pre-substem)",
"-ki- cytokine and cytokine receptor",
"-ler- allergen",
"-sto- immunostimulatory",
"-pru- immunosuppressive",
"-ne- neural",
"-os- bone",
"-ta- tumour",
"-toxa- toxin",
"-vet- veterinary use (sub-stem)",
"-vi- viral",]
st.markdown("## Select a Infix")
infix_choice=st.radio(" ",infix_selection,index=0,horizontal = True)
infix_index=infix_selection.index(infix_choice)

stem_dict={0:'tug',1:'bart',2:'mig',3:'ment'}
infix_dict={0:"ami",1:"ba",
            2:"ci",3:"de",4:"eni",
            5:"fung",6:"gro",7:"ki",8:"ler",9:"sto",10:"pru",11:"ne",12:"os",13:"ta",14:"toxa",15:"vet",16:"vi"}

stem=stem_dict[stem_index]
infix=infix_dict[infix_index]
name_part=infix+stem
print(name_part)
st.markdown("## How many names do you want to generate?")
col1,col2=st.columns([1,5])
number_of_name=col1.number_input(" ",min_value=1,max_value=100,value=3)
st.markdown("## Check in these languages")
lang_check=st.multiselect(" ",
    ["English","Chinese","Japanese",
    "Korean","Spanish","French",
    "German","Italian","Portuguese",
    "Russian","Arabic",],
    default=["Russian","Italian","Spanish"])

st.markdown("## Requirements")
requirement=st.text_area(" ",value="The name has 3-5 syllables and is related to the treatment of digestive system tumors.")


generate_button=st.button("Generate")




if generate_button:

    st.markdown("## Generate Names")
    with st.spinner("Generating..."):
        name_list=generate_name(number_of_name,name_part,requirement)
        st.markdown("\n* "+"\n* ".join(name_list))

    name_prefix=[name.split(infix)[0] for name in name_list]
    print(name_prefix)

    if len(name_prefix)>1:
        st.markdown("## Check prefix in Languages")
        with st.spinner("Checking..."):
            for name in name_prefix:
                check_list=check_in_languages(lang_check,name)
                st.markdown(f"#### {name}-")
                for key,value in check_list.items():
                    st.markdown(f"* {key}:")
                    for v in value:
                        st.markdown(f"> {v}")
                # st.dataframe(check_list)
                print(check_list)
        
        st.write("## POCA Query")
        with st.spinner("Querying POCA..."):
            # if platform.system() == 'Windows':
            #     loop = asyncio.ProactorEventLoop()
            #     asyncio.set_event_loop(loop)
            # else:
            #     loop = asyncio.get_event_loop()
            # df=loop.run_until_complete(query_poca(name_list,item_sep="\t\t"))
            df=asyncio.run(query_poca(name_list,item_sep="\t\t"))
            for key, value in df.items():
                st.markdown(f"* {key}")
                st.markdown(f"> {value}")
    

