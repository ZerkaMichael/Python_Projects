import discord
import os
from discord.ext import commands, tasks
import asyncio
import aiohttp
import json
import re
import requests
from discord.utils import get
from datetime import date,datetime
from embeds import *
import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

def get_Date_Time():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

async def get_crypto(crypto,type):
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids='+crypto+'&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h'
        raw_response = await session.get(url)
        raw_response = await raw_response.text()
        response = json.loads(raw_response)
        match type:
            case "price":
                return response[0]['current_price']
            case "1hr":
                return response[0]['price_change_percentage_1h_in_currency']
            case "24hr":
                return response[0]['price_change_percentage_24h_in_currency']

async def get_stock_price(stock):
        url = 'https://finnhub.io/api/v1/quote?symbol='+stock.upper()+'&token=c65ih0iad3i9pn79r9j0'
        response = requests.request("GET", url)
        response = response.text
        response = json.loads(response)
        return response['c']


async def ArticleAnalysis(arg):
    url = arg
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    analysis = TextBlob(article.text)
    title = f'{article.title}'
    authors = f'{article.authors}'
    publish_date = f'{article.publish_date}'
    summary = f'{article.summary}'
    sentiment = f'{analysis.polarity} {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'
    embed=discord.Embed(title="Article Analysis", description="Analysis and Summary of the requested article", color=0x0000ff)
    embed.set_thumbnail(url="https://i.imgur.com/fwqU9HR.png")
    embed.add_field(name="Title:", value=title, inline=True)
    embed.add_field(name="Authors:", value=authors, inline=True)
    embed.add_field(name="Publish Date:", value=publish_date, inline=True)
    embed.add_field(name="Sentiment:", value=sentiment, inline=True)
    embed.add_field(name="Summary:", value=summary, inline=False)
    return embed
