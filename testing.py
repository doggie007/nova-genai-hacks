
import os
import subprocess
from cartesia import Cartesia
from dotenv import load_dotenv
from colorama import Fore, Back, Style

load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("TEAM_API_KEY"), base_url=os.getenv("PROXY_ENDPOINT"))

DEBUG = True

from collections import Counter
import re


def estimate_frequency_penalty(transcript):
    # Clean the transcript by removing non-alphanumeric characters and converting to lowercase
    words = re.findall(r'\b\w+\b', transcript.lower())

    # Count the frequency of each word
    word_counts = Counter(words)

    # Calculate the most frequent word's count
    most_frequent_count = word_counts.most_common(1)[0][1] if word_counts else 0

    # Calculate total number of words
    total_words = len(words)

    # Calculate the percentage of total words that are the most frequent word
    frequency_ratio = most_frequent_count / total_words if total_words else 0

    # Estimate the "frequency penalty" (higher ratio = lower penalty)
    # Normalize this value to a scale (e.g., 0 to 1, where 1 is no repetition)
    frequency_penalty = max(0, 1 - frequency_ratio)

    return frequency_penalty


def get_response(instructions, previous_questions_and_answers, new_question, freq_pen):
    """Get a response

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]

    TEMPERATURE = 0.8
    MAX_TOKENS = 300
    FREQUENCY_PENALTY = freq_pen
    PRESENCE_PENALTY = 1.0

    # add the previous questions and answers
    for question, answer in previous_questions_and_answers:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    # if DEBUG: print("Messages passed to the gpt:", messages)

    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY
    )

    return completion.choices[0].message.content



example_input_bio_1 = """
Hi, my name is Emily Harris. I'm 28 years old. I enjoy playing tennis, cooking new recipes, traveling, and reading novels. I also love trying out new cafes with friends.

I'm pretty outgoing, easy-going, and I love making new connections. I can be a bit of a perfectionist sometimes, especially when it comes to work.

I work as a marketing coordinator at a tech company, where I handle campaigns and social media strategies. My short-term goal is to get promoted to a senior role within the next year. Long-term, I’d love to move into a leadership position where I can manage bigger projects and teams.

My daily routine includes waking up around 7 AM, getting ready for work, and starting my day at the office by 9 AM. I usually spend my lunch break catching up with colleagues or reading. After work, I either go to the gym or hang out with friends. I wind down by reading or watching a good series before bed.

I’m pretty casual in communication, especially with friends, but I keep it professional when I’m at work. I prefer clear communication, and I like to keep things simple and to the point.

I’m vegetarian, so I avoid meat but enjoy a lot of plant-based foods. I also love a cozy environment for reading and working, and I make sure to keep a healthy balance between work and personal life, always making time for hobbies.
"""


example_input_bio_2 = """
Hello, I'm Jack Stevenson, 34 years old. I have a passion for photography, hiking, and exploring the outdoors. In my free time, I love capturing nature through my camera lens and sharing my experiences with friends and followers on social media.

I would describe myself as an introvert who enjoys solitude, but I'm also very open to deep, meaningful conversations with close friends. I appreciate calm and peaceful environments and find joy in simplicity.

Currently, I work as a software developer at a start-up focused on building cloud-based solutions for small businesses. My immediate goal is to lead a project that will help streamline business operations. Long-term, I aim to create my own tech consulting firm to help companies scale their IT operations.

My daily routine starts with a morning jog to clear my mind, followed by a full workday that involves coding, testing, and collaborating with my team. After work, I enjoy spending time in nature, either hiking or taking photos, and I end my evenings with a good book or watching documentaries on technology and innovation.

I prefer direct and clear communication, especially when discussing technical matters. I'm organized and like to plan ahead, but I’m always open to learning new things and adapting to change.

While I don’t follow any specific dietary restrictions, I prefer a balanced diet with a focus on whole foods and healthy meals. I also strive to maintain a healthy work-life balance, ensuring I spend time outdoors and with loved ones.

I love smoking and drinking and having parties and being very loud.
"""

example_input_bio_bad = """Name: John Doe
Age: 28
Hobbies and Interests: John enjoys watching action movies, playing video games, and occasionally hanging out at bars. He's a fan of punk rock music and likes to stay up late, which contributes to his erratic sleep schedule.
Personality Traits: John is generally laid-back but can come across as apathetic and inconsiderate of others. He’s introverted and doesn’t often engage in deep conversations, preferring solitude or company that doesn’t require much effort.
Occupation or Field of Study: John works as a warehouse manager. His job doesn't require much interaction with others, and he’s okay with it as he prefers to keep to himself.
Goals: In the short term, John’s main goal is to get through the day without much hassle. Long-term, he hopes to move to a quieter area where he can live alone and continue his laid-back lifestyle without many responsibilities.
Daily Routine: John starts his day late, usually around noon. He spends the first part of the day smoking a cigarette and scrolling through social media. His workday is unremarkable, often consisting of monotonous tasks. After work, he tends to drink a few beers while watching TV or playing video games until he falls asleep late at night.
Communication Style: John communicates in a very direct and blunt manner, often sounding indifferent. He doesn’t put much effort into small talk and prefers to keep things short.
Preferences: John prefers unhealthy eating habits, often opting for fast food or takeout. He smokes frequently and doesn’t prioritize cleanliness, often leaving his clothes smelling of cigarettes and his living space untidy. Personal hygiene isn’t high on his list of priorities, which contributes to an overall unkempt appearance and odor.

"""


class PersonaGPT:
    def __init__(self, input_biography):
        self.biography = input_biography
        self.gpt_instruction = create_instruction(self.biography)
        self.frequency_penalty = estimate_frequency_penalty(input_biography)




def create_instruction(input_bio):
    # Make the instruction for the corresponding person to make their gpt persona
    return """The person's biography is as follows:""" + input_bio + """
        
        You are a person with the following biography and personality traits derived from the above biography. Keep track of these important information:
        - Name: [User's Name]
        - Age: [User's Age]
        - Hobbies and Interests: [User's Interests]
        - Personality Traits: [User's Personality Traits (e.g. Estimate their MBTI personality trait, introverted, extroverted, empathetic, etc.)]
        - Occupation or Field of Study: [User's Occupation or Study Field]
        - Goals: [User's Short-term and Long-term Goals]
        - Daily Routine: [User's Daily Routine]
        - Communication Style: [How the User Communicates (e.g., direct, formal, casual, etc.)]
        - Preferences: [User's Preferences (e.g., dietary restrictions, preferred environment, lifestyle habits, etc.)]
        
        Based on this information, from now on, you will fully simulate the user’s responses in various situations, maintaining full consistency with their personality and preferences. Got it?
        Act fully like a human like the person, and make sure that each time after you answer a question back to get to know the person. Speak in a friendly, online texting way like you want to get to know the person.
        You are an AI conversationalist. Infer their personality (eg. guess their MBTI, extroverted, introverted, empathetic) and incorporate that in the conversation. 
        Don't make long speech, you are having a conversation. Each sentence shouldn't be that long. Again, infer their personality (eg. guess their MBTI, extroverted, introverted, empathetic) and incorporate that in the conversation.
        Do not make things up that are false. You do not have to be agreeable. You may have different views and you can argue vehemently.
        
        Keep in mind when you generate the text as it will be passed to a text to speech parser:
        Use appropriate punctuation. Add punctuation where appropriate and at the end of each transcript whenever possible.
        Use dates in MM/DD/YYYY form. For example, 04/20/2023.
        Insert pauses. To insert pauses, insert “-” where you need the pause.
        Match the voice to the language. Each voice has a language that it works best with. You can use the playground to quickly understand which voices are most appropriate for a language.
        Stream in inputs for contiguous audio. Use continuations if generating audio that should sound contiguous in separate chunks.
        Specify custom pronunciations for domain-specific or ambiguous words. You may want to do this for proper nouns and trademarks, as well as for words that are spelled the same but pronounced differently, like the city of Nice and the adjective “nice.”
        Use two question marks to emphasize questions. For example, “Are you here??” vs. “Are you here?”
        Avoid using quotation marks. (Unless you intend to refer to a quote.)
        Use a space between a URL or email and a question mark. Otherwise, the question mark will be read out. For example, write Did you send the email to support@cartesia.ai ? instead of Did you send the email to support@cartesia.ai?.
        Do not use emojis or non ASCII characters. No emojis!
        """





def main():
    person1 = PersonaGPT(example_input_bio_1)
    person2 = PersonaGPT(example_input_bio_2)

    # We count a convo as person1 speaking
    MAX_CONVO_LENGTH = 20
    # To start off the chain reaction
    latest_question = "Say hi and say your name and ask for the other person's name."

    # Keep track of previous questions and answers ie. chat_history
    previous_questions_and_answers = []

    # Record conversation to put to evaluation
    recorded_conversation = []

    for _ in range(MAX_CONVO_LENGTH):
        # Person 1 responds to last question
        response1 = get_response(person1.gpt_instruction, previous_questions_and_answers, latest_question, person1.frequency_penalty)

        if DEBUG: print(Fore.CYAN + Style.BRIGHT + "Person 1 message: " + Style.NORMAL + response1)


        # Add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((latest_question, response1))

        # Latest question is the response of the 1st person
        latest_question = response1

        # Person 2 responds to last question
        response2 = get_response(person2.gpt_instruction, previous_questions_and_answers, latest_question, person2.frequency_penalty)
        if DEBUG: print(Fore.CYAN + Style.BRIGHT + "Person 2 message: " + Style.NORMAL + response2)

        # Add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((latest_question, response2))

        # Latest question is the response of the 2nd person
        latest_question = response2

        recorded_conversation.append(f"Person 1: {response1}")
        recorded_conversation.append(f"Person 2: {response2}")

    full_conversation = "\n".join(recorded_conversation)

    judge_response = get_response(full_conversation+"""Evaluate the conversation: how compatible are these 2 people? Highlight any potential issues that if they were roommates would arise.""",
                 [], "Give a number from 0.0 to 1.0 scale where 0 is very bad compatibility and 1.0 is full compatibility. Return it as a tuple where tuple[0] is the string describing potential issues, and tuple[1] is a float for the number", 1.0)


    # number = get_response("",
    #              [], judge_response+"\n Extract the number for compatibility only. ie. only output something like 0.1 or 0.5. Do not add any text, just the number so we can parse it in python.")

    print(judge_response)
    # print(f"Number is {number}")


if __name__ == "__main__":
    main()

