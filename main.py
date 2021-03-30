import os
import io
import requests
import sys
from searchtweets import collect_results, gen_request_parameters, load_credentials
from wordcloud import WordCloud
from termcolor import colored

OUT_DIR = "output"
TWITTER_QUANTITY = 10
OUT_FILE = "user_tweets"


def wordCloud():
    txtfile = io.open(os.path.join("output", f"{OUT_FILE}.txt"), encoding="utf-8")
    text = txtfile.read()
    txtfile.close()
    if len(text) == 0:
        print("Empty txt can't generate a word cloud")
    else:
        wordcloud = WordCloud().generate(text)

        image = wordcloud.to_image()
        image.save(os.path.join("output", f"{OUT_FILE}.png"))
        print("Image Loaded")


stream_args = load_credentials(filename="config.yalm", yaml_key="search_tweets_v2", env_overwrite=False)

tweeterUser = input("Inform the Tweet user: ")

query = gen_request_parameters(f"from:{tweeterUser} -has:links", results_per_call=TWITTER_QUANTITY)

try:
    tweets = collect_results(query, max_tweets=TWITTER_QUANTITY, result_stream_args=stream_args)
except requests.exceptions.HTTPError as exception:
    print(colored("There's an error in your api request, Error: ", 'red'))
    sys.exit()

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

with io.open(os.path.join(OUT_DIR, f"{OUT_FILE}.txt"), "w", encoding="utf-8") as tweetsfile:
        for tweet in tweets:
            if 'text' in tweet:
                tweetsfile.writelines(tweet['text'])

wordCloud()
