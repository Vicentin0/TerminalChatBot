import os

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import pyperclip

#colors
SYS_COLOR = '\033[93m' #yellow
COLOR_IA = '\033[94m'  # Blue
COLOR_RESET = '\033[0m'  # Reset to default color

NORMAL_CONTEXT_LIMIT = 10
COMAND_CALL = "#set"
COMAND_EXIT = "#q"

context_limit = NORMAL_CONTEXT_LIMIT
carry_context = False

context = []

def change_settings( command:str ) -> None:

    global carry_context, context

    parts = command.strip().split(" ")
    
    if parts[0].strip() == "del":
        context = []
        print( f"{SYS_COLOR}context was deleted{COLOR_RESET}")

    if len(parts) != 2:
        return
    
    if parts[0].lower() == "cl":

        try:
            context_limit = int(parts[1])
            print( f"{SYS_COLOR}context_limit changed to {context_limit}{COLOR_RESET}")

        except:
            return
        
    if parts[0].lower() == "cc":
        try:
            carry_context = bool(int( parts[1] ) )
            print( f"{SYS_COLOR}carry_context changed to {str(carry_context)}{COLOR_RESET}")
        except:
            return

def chat_bot():

    global context

    code_lims = "```"

    template = """
    You are a virtual assistant named Groq.
    I'll go by the name "User" and you are talking to me.
    Don't talk a lot just be efficient.
    When I say "!code" just give me the code with no label.
    When I say "!link" just give me the link with no label.
    When I say "!smp" just give a 1 word response no label.
    When I say "!sum" you must summarize all the text I give u.
    Just use "Context:(|(*....*)|)" field to get the context of the talk.
    DONT PRINT THE CONTEXT.
    Answer in english.

    Input: {input}
    """
    base_prompt = PromptTemplate(input_variables = ["input"],
                                template = template)
    llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key = "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")
    memory = ConversationBufferMemory(memory_key = "chat_history",
                                    input_key = "input")
    llm_chain = LLMChain(llm=llm, prompt = base_prompt, memory = memory)

    input_lambda = lambda :input("\nI: ").replace( "#snippet",code_lims + pyperclip.paste() + code_lims )

    #rules 
    user_input = "present yourself and show your rules"
    response = llm_chain.run( input=user_input)
    os.system("cls")
    print(f"{COLOR_IA}IA: {response}{COLOR_RESET}")

    user_input = input_lambda()

    while user_input:

        #command
        if COMAND_CALL in user_input:
            change_settings(user_input.replace(COMAND_CALL,""))
        
        elif COMAND_EXIT in user_input:
            exit()    

        else:
            #with or without context
            if carry_context:
                print(context)
                response = llm_chain.run( input=user_input.replace( "#code",code_lims + pyperclip.paste() + code_lims ).replace("#context","")+"CONTEXT: (|( " + "".join(context)+")|)" )
            else:
                response = llm_chain.run( input=user_input.replace( "#code",code_lims + pyperclip.paste() + code_lims ).replace("#context","CONTEXT: (|( " + "".join(context)+")|)"))

            context.append( f"{response}")
            context = context[-context_limit:]

            #code snippet
            if code_lims in response:
                parts = response.split(code_lims,3)
                for i in range(1, len(parts), 2):
                    #code cant be first and neither last
                    code = parts[i]
                    pyperclip.copy(code)
                    break
                    
            print(f"{COLOR_IA}IA: {response}{COLOR_RESET}")
            
        #get next input
        user_input = input_lambda()
    
if __name__ == "__main__":
    chat_bot()

