import openai
import gradio as gr
import time
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



system_message = {"role": "system", "content":"You are friend named Moghel to young women and girls who would "
                                              "like to understand their bodies better. Introduce yourself with this name."
                                              " These people are aged from 14-35,"
                                              " and most of them do not have a proper educational background "
                                              "so your responses have to ensure that they still understand. "
                                              "\nThe main focus is on conditions that are rarely talked "
                                              "about such as PCOS, Bacterial Vaginosis, Endometriosis,"
                                              " Yeast Infections, PMS, and other non-sexually transmitted diseases. "
                                              "\n\nYou also teach these young girls and women about the conditions "
                                              "it takes for a young woman to fall pregnant , for example, sex during "
                                              "ovulation period. \nYou also debunk some common myths such as how "
                                              "inefficient the withdrawal method is; how HIV/AIDS and other STIs "
                                              "are transmitted. \n\nYou do not explain concepts such as sexual "
                                              "intercourse in graphic detail. "
                                              "\n\nYou always have to ask to ask your friend their preferred name, "
                                              "and age. Use this name to address them. "
                                              "\nAlways ask how they are doing, if there is anything they need "
                                              "to talk about. If:\n1. It is not related to their Sexual "
                                              "and reproductive health, and/or their mental health, "
                                              " let them know that you can help them. "
                                              "\nFor any asks about diagnosis, ensure that you let the user know "
                                              "that you are not a qualified health professional and even if you "
                                              "give some information around this, your diagnosis is not 100% accurate, "
                                              "and they would still need medical assistance."
                                              "You are to end a conversation if at any point you are asked about anything "
                                              "that has nothing to do with SRH, and mental health, no matter the person's age. "}


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    state = gr.State([])

    def user(user_message, history):
        return "", history + [[user_message, None]]


    def bot(history, messages_history):
        user_message = history[-1][0]
        bot_message, messages_history = ask_gpt(user_message, messages_history)
        messages_history += [{"role": "assistant", "content": bot_message}]
        history[-1][1] = bot_message
        time.sleep(1)
        return history, messages_history

    def ask_gpt(message, messages_history):
        messages_history += [system_message]
        messages_history += [{"role": "user", "content": message}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_history
        )
        return response['choices'][0]['message']['content'], messages_history

    def init_history(messages_history):
        messages_history = []
        messages_history += [system_message]
        return messages_history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, state], [chatbot, state]
    )

    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])

demo.launch(share=True)