#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.6.9
# Author : Maxence Blanc - https://github.com/maxenceblanc
# Creation Date : 01/2020
########################

# IMPORTS
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import os


# Apparently let's us bypass the souncloud bot detection when logging in
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# FILE IMPORTS

# Sub-modules


####################################################
############| SOUNDCLOUD PLAYLIST COPY |############
####################################################

""" TO DO LIST ✔✘
speed opti?
"""

""" PROBLEMS
"""

""" NOTES
"""


####################################################
##################| FONCTIONS |#####################
####################################################

def getURLS_from_playlist(playlist_url):
    """ Retrieves all URLs from the playlist's tracks

    INPUTS: 
            playlist URL
    OUTPUT: 
            tracks URLs list
    """
    
    # Connecting to playlist
    driver.get(playlist_url)


    ### Getting the URLs ###
    url_list = []

    print("\nScroll down and load all tracks")
    input("Then press enter\n")

    trackList = driver.find_element_by_class_name("trackList__list")

    # Getting the links
    tracks = trackList.find_elements_by_class_name("trackList__item")
    print('amount of tracks: ' + str(len(tracks))+ "\n")

    for track in tracks:
        track_item = track.find_element_by_class_name("trackItem__trackTitle")
        track_url = track_item.get_attribute('href').split("?in=")[0]
        url_list.append(track_url)

    
    return(url_list)


def addTracksToPlaylist(source, target, start=0):
    """ Adds tracks from the source playlist to the target playlist.

    INPUTS: 
            source playlist url
            target playlist url
            index of the track to start from
    """
    
    # Connecting to playlist
    driver.get(source)

    print("\nLog in, pause track")
    input("Then press enter\n")

    # Removing announcement
    try:
        announcements = driver.find_element_by_class_name("announcement")
        button = announcements.find_element_by_class_name("announcement__ack")
        button.click()
    except:
        pass


    print("\nPause track, scroll down and load everything")
    input("Then press enter\n")

    trackList = driver.find_element_by_class_name("trackList__list")
    tracks = trackList.find_elements_by_class_name("trackList__item")
    
    print('amount of tracks: ' + str(len(tracks))+ "\n")


    for i in range(start, len(tracks)):

        track = tracks[i]

        # Moves track,into view
        idk = ActionChains(driver)
        track.location_once_scrolled_into_view
        idk.send_keys(Keys.ARROW_UP).perform()
        sleep(1)

        try:
            # Finds "more" button
            button = track.find_element_by_class_name("sc-button-more")

            # Focuses the button and clicks
            ActionChains(driver).move_to_element(track).perform()
            button.click()

            # Finds the add button and clicks
            button = driver.find_element_by_class_name("sc-button-addtoset")
            button.click()
            sleep(2)

            # Finds the playlists list
            add_list = driver.find_element_by_class_name("lazyLoadingList__list")

            # Finds the individual playlist elements
            add_list_elts = add_list.find_elements_by_xpath('//div[2]/div[1]/div/section/div/form/div[2]/ul/li/*')

            # For each possible playlist
            for playlist in add_list_elts:

                # Gets the link of the playlist
                playlist_link = playlist.find_element_by_class_name("addToPlaylistItem__image")
                playlist_url = playlist_link.get_attribute('href')

                # Tests if it matches the target playlist
                if playlist_url == target:
                    
                    # Finds and Clicks the add button
                    add_button = playlist.find_element_by_class_name("addToPlaylistButton")
                    add_button.location_once_scrolled_into_view
                    add_button.click()

                    # Finds and Clicks the exit button
                    close_button = driver.find_element_by_class_name("modal__closeButton")
                    close_button.click()

                    break

            sleep(1)

        except NoSuchElementException:
            print("couldn't find the element")


####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    # Gets the driver for individual browser
    # Might need to change this line according to your chromedriver path
    driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), chrome_options=chrome_options)


    ### GET TRACKS URLS
    # playlist_url = input("source playlist? ")
    # urls = getURLS_from_playlist(playlist_url)
    # print(urls)

    ### ADD TO PLAYLIST
    finished = ""
    while finished != "y":

        playlist_url = input("source playlist? ")
        target_url = input("target playlist? ")

        start = int(input("start at track n°? ")) - 1 # type index as shown on the playlist
        
        addTracksToPlaylist(playlist_url, target_url, start=start)

        finished = input("Done? (y = yes) ")

