"""
Module providing functions for scraping information from instagram accounts.
"""
import csv
import json
import re
import time
from datetime import datetime
from io import BytesIO
from itertools import dropwhile, takewhile
from typing import Iterator, Optional

import instaloader
import requests
from PIL import Image
from tqdm import tqdm

from app.dependency import get_settings
from app.utils.logger import configure_logger

settings = get_settings()

logger = configure_logger()


class GetInstagramProfile:
    """
    Class to load a profile and download its data.
    """

    def __init__(self) -> None:
        self.L = instaloader.Instaloader(user_agent="Edg/113.0.1774.50")
        try:
            self.L.login(settings.USERNAME_IG,settings.PSW_IG)
            logger.info(f"Correct instagram logging with {settings.USERNAME_IG}")
        except Exception as error:
            logger.info(f"Error during instagram logging with {settings.USERNAME_IG} - {settings.PSW_IG}\n{error}")

    @staticmethod
    def remove_tagged_users(caption:str) -> str:
        """ IF activate remove all tagged users and
        substitute the tag with @taggeduser, only from the post caption
        """
        return re.sub(r"@[\w.-]+(?<!\.)", "@taggeduser", caption)


    def download_users_profile_picture(self, username: str) -> None:
        """
        Download a user's profile picture.
        """
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self, username: str) -> None:
        """
        Download posts from a user within a specified period of time.
        """
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        since = datetime(2021, 8, 28)
        until = datetime(2021, 9, 30)

        for post in takewhile(
            lambda p: p.date > since, dropwhile(lambda p: p.date > until, posts)
        ):
            self.L.download_post(post, username)

    def download_hastag_posts(self, hashtag: str) -> None:
        """
        Download posts that contains a certain hashtag.
        """
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target="#" + hashtag)

    def get_users_followers(self, user_name: str) -> None:
        """
        Function to get a profile's followers.
        Note: login required to get a profile's followers.
        """
        self.L.login(input("input your username: "), input("input your password: "))
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        with open("follower_names.txt", "a+", encoding="utf-8") as file:
            for follower in profile.get_followers():
                username = follower.username
                file.write(username + "\n")
                print(username)

    def get_users_followings(self, username: str) -> None:
        """
        Function to get a profile's followings.
        Note: login required to get a profile's followings.
        """
        self.L.login(input("input your username: "), input("input your password: "))
        profile = instaloader.Profile.from_username(self.L.context, username)
        with open("following_names.txt", "a+", encoding="utf-8") as file:
            for followee in profile.get_followees():
                username = followee.username
                file.write(username + "\n")
                print(username)

    def get_post_comments(self, username: str) -> None:
        """
        Function to get a post's comments and print them at screen.
        """

        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        for post in posts:
            for comment in post.get_comments():
                print("comment.id  : " + str(comment.id))
                print("comment.owner.username  : " + comment.owner.username)
                print("comment.text  : " + comment.text)
                print("comment.created_at_utc  : " + str(comment.created_at_utc))
                print("************************************************")

    def get_post_info_csv(self, username: str) -> None:
        """
        Function to get info from every post of a user and store them in a csv file.
        """

        with open(username + ".csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            posts = instaloader.Profile.from_username(
                self.L.context, username
            ).get_posts()
            for post in posts:
                print("post date: " + str(post.date))
                print("post profile: " + post.profile)
                print("post caption: " + post.caption)
                print("post location: " + str(post.location))

                posturl = "https://www.instagram.com/p/" + post.shortcode
                print("post url: " + posturl)
                writer.writerow(
                    [
                        "post",
                        post.mediaid,
                        post.profile,
                        post.caption,
                        post.date,
                        post.location,
                        posturl,
                        post.typename,
                        post.mediacount,
                        post.caption_hashtags,
                        post.caption_mentions,
                        post.tagged_users,
                        post.likes,
                        post.comments,
                        post.title,
                        post.url,
                    ]
                )

                for comment in post.get_comments():
                    writer.writerow(
                        [
                            "comment",
                            comment.id,
                            comment.owner.username,
                            comment.text,
                            comment.created_at_utc,
                        ]
                    )
                    print("comment username: " + comment.owner.username)
                    print("comment text: " + comment.text)
                    print("comment date : " + str(comment.created_at_utc))
                print("\n\n")

    def get_post_info_json(self, username: str, last_n_posts: int = 100) -> Iterator[dict]:
        """
        Function to get info from every post of a user and store them in a json file (dictionary style).
        """
        data: dict[str, dict] = {}
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        print(
            "Downloading last " + str(last_n_posts) + " posts from " + username + "..."
        )
        for ies,_i in enumerate(tqdm(range(last_n_posts))):
            post = next(posts) # pylint: disable=R1708
            shortcode = post.mediaid_to_shortcode(post.mediaid)
            data[shortcode] = {}
            # Store the post info
            try:
                data[shortcode]["post"] = self.remove_tagged_users(str(post.caption))
                data[shortcode]["hashtags"] = str(post.caption_hashtags)
                data[shortcode]["mentions"] = str(post.caption_mentions)
                data[shortcode]["tagged_users"] = str(post.tagged_users)
                data[shortcode]["likes"] = str(post.likes)
                data[shortcode]["comments"] = str(post.comments)
                data[shortcode]["date"] = str(post.date)
                data[shortcode]["location"] = str(post.location)
                data[shortcode]["typename"] = str(post.typename)
                data[shortcode]["mediacount"] = str(post.mediacount)
                data[shortcode]["title"] = str(post.title)
                data[shortcode]["posturl"] = "https://www.instagram.com/p/" + shortcode
                yield data[shortcode]
            except Exception as error:
                logger.error(f"Error during extraction of data of the post:\
                            https://www.instagram.com/p/{shortcode}\n{error}")
            if ies%5 == 0:
                # wait 1 second every 5 posts
                time.sleep(1)

    def get_profile_pic(self, username:str)-> BytesIO:
        """ Return the profile pic of the user """
        profilo = instaloader.Profile.from_username(self.L.context, username)
        path_pic = str(profilo.profile_pic_url)
        response = requests.get(path_pic, timeout=10)
        image = Image.open(BytesIO(response.content))
        return image # type: ignore


def load_post_captions_from_json(
    json_file: str, shortcodes: Optional[list] = None
) -> list:
    """
    Function to load post captions from a json file. The post loaded are the one specified by the shortcodes list.
    This to allow compatibility with eventual search functions on the specific post.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data: dict[str, dict] = json.load(f)

    captions = []
    if shortcodes is None:
        # Load the complete file
        shortcodes = list(data.keys())
        for shortcode in shortcodes:
            captions.append(data[shortcode]["post"])
    else:
        for shortcode in shortcodes:
            captions.append(data[shortcode]["post"])

    return list(captions)
