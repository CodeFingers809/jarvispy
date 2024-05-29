import pyttsx3, datetime, pywhatkit, pyjokes, pyautogui, pygame, os, random, requests, openai
from newsapi import NewsApiClient
from nltk.sentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
import webbrowser as wb
from config import apikey


def ai(prompt):
    text = ""
    openai.api_key = apikey

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # return response.choices[0].text
    text += response.choices[0].text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{prompt}.txt", "w") as f:
        f.write(text)
        return text


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def greet():
    hr = datetime.datetime.now().hour
    if hr >= 6 and hr < 12:
        say("Good Morning Sir!")
    elif hr >= 12 and hr < 17:
        say("Good Afternoon Sir!")
    elif hr >= 17 and hr < 24:
        say("Good Evening Sir!")
    else:
        say("Good Night Sir!")


def take_ss():
    timestamp = datetime.datetime.now().strftime("%Y-%m-$d_%H-%M-%S")
    ss = pyautogui.screenshot()
    ss.save("Screenshot_" + timestamp + ".png")
    say("Taken a screenshot")


pygame.mixer.init()


def get_music_files(directory):
    music_files = [
        f for f in os.listdir(directory) if f.endswith((".mp3", ".wav", ".ogg"))
    ]
    return music_files


def play_random_music():
    music_folder = os.path.join(os.environ["HOMEPATH"], "Music")
    if os.path.exists(music_folder):
        music_files = get_music_files(music_folder)
        if music_files:
            chosen_music = os.path.join(music_folder, random.choice(music_files))

            pygame.mixer.music.load(chosen_music)
            say("Playing: " + chosen_music)
            pygame.mixer.music.play()
        else:
            say("No files found!")
    else:
        say("No correct folder found!")


music_playing = False


def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        say("Music stopped!")
    else:
        play_random_music()
    music_playing = not music_playing


def get_news(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    headlines = newsapi.get_top_headlines(language="en", country="us")

    if headlines["status"] == "ok":
        articles = headlines["articles"]
        return articles
    else:
        return None


def read_news():
    api_key = (
        "31d075d55aa94617b63a765673f68268"  # Replace with your actual News API key
    )
    articles = get_news(api_key)

    if articles:
        say("Here are the latest news headlines:")
        for i, article in enumerate(articles, start=1):
            title = article["title"]
            say(f"News {i}: {title}")

            # Check for the stop command after each news item
            query = take_cmd().lower()
            if "stop" in query or "offline" in query:
                say("Stopping the news reading.")
                return

    else:
        say("Sorry, I couldn't fetch the latest news at the moment.")


def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    # Get a compound sentiment score between -1 (negative) and 1 (positive)
    sentiment_score = sid.polarity_scores(text)["compound"]

    if sentiment_score >= 0.05:
        return "positive"
    elif sentiment_score <= -0.05:
        return "negative"
    else:
        return "neutral"


def take_cmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"Ayush said: {query}")
            return query
        except Exception as e:
            return "Some Error"


if __name__ == "__main__":
    say("Hello sir! I am Jarvis.")
    greet()
    while True:
        query = take_cmd().lower()

        if "time" in query:
            hr = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir the current time is {hr} and {min} minutes.")

        elif "remember" in query:
            say("What should i remember?")
            data = take_cmd()
            say("You told me to remember that " + data)
            remember = open("data.txt", "a")
            remember.write(data + "\n")
            remember.close()

        elif "forgot" in query:
            remember = open("data.txt", "r")
            say(
                "In case you forgot sir here's what you told me to remember: "
                + remember.read()
            )

        elif "youtube" in query:
            say("Search for what?")
            search = take_cmd()
            pywhatkit.playonyt(search)

        elif "search" in query:
            say("What should I search for?")
            search = take_cmd()
            wb.open("https://www.google.com/search?q=" + search)

        elif "instagram" in query:
            wb.open("www.instagram.com")

        elif "camera" in query:
            camera_url = "microsoft.windows.camera:"
            wb.open(camera_url)

        elif "joke" in query:
            joke = pyjokes.get_joke()
            print(joke)
            say(joke)

        elif "screenshot" in query:
            take_ss()

        elif "music" in query:
            toggle_music()

        elif "read news" in query:
            read_news()

        elif "how" in query:
            mood = get_sentiment(query)
            if mood == "positive":
                say("I'm doing well, thank you!")
            elif mood == "negative":
                say("I'm sorry to hear that. Is there anything I can do to help?")
            else:
                say("I'm doing fine, thanks for asking!")

        elif "bye" in query:
            say("Thank you! Turning off...")
            quit()

        elif "using artificial intelligence" in query:
            say(ai(prompt=query))
