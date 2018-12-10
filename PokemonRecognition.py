import discord
import asyncio
import requests
import urllib
from urllib.request import urlopen
from http.cookiejar import CookieJar
import time
import re
from bs4 import BeautifulSoup
import datetime

token = ""

with open("..\\token.txt") as f:
	token = f.read()
	f.close()

pokemon = ""

with open ("pokemon_unique.txt") as p:
	pokemon = p.readlines()
	p.close()

pokemon = [x.strip() for x in pokemon]

client = discord.Client()

def googleSearch(url):
	possibles = []
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
	googlepath = "http://images.google.com/searchbyimage?image_url=" + url
	print(googlepath)
	rawHTML = opener.open(googlepath).read()
	soup = BeautifulSoup(rawHTML, 'html.parser')
	found = False
	for tag in soup.find_all("h3"):
		for p in pokemon:
			if p in tag.getText():
				if p not in possibles:
					possibles.append(p)

	print("I think this Pokemon could be: " + possibles)

@client.event
async def on_ready():
	print("Logged in!")
	print(client.servers)

@client.event
async def on_message(message):
	img = ""
	await log_message(message)
	if (len(message.embeds) > 0):
		googleSearch(message.embeds[0]["image"]["url"])

	if (message.content == "!shutdown"):
		exit()

async def log_message(message):
	print("[" + str(datetime.datetime.now()) + "] - (" + message.author.name + "): " + message.content)

client.run(token)