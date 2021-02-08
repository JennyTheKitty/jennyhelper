import re

import discord
from discord.ext import commands

URL_PATTERN = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


class Fun(commands.Cog):
    faces = ["(・`ω´・)", ";;w;;", "OwO", "UwU", ">w<", "^w^", "ÚwÚ", "^-^", ":3", "x3"]
    exclamations = ["!?", "?!!", "?!?1", "!!11", "?!?!"]
    uwuMap = [
        [r"(.*)(?:r|l)(.*)", r"\1w\2"],
        [r"(.*)(?:R|L)(.*)", r"\1W\2"],
        [r"(.*)n([aeiou])(.*)", r"\1ny\2\3"],
        [r"(.*)N([aeiou])(.*)", r"\1Ny\2\3"],
        [r"(.*)N([AEIOU])(.*)", r"\1Ny\2\3"],
        [r"(.*)ove(.*)", r"\1uv\2"],
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uwu(self, ctx: commands.Context, *, text: str):
        words = re.split(r"\s", text)
        outWords = []

        for word in words:
            if re.match(URL_PATTERN, word):
                outWords.append(word)
                continue

            outWord = word
            for pattern, repl in self.uwuMap:
                print(outWord)
                outWord = re.sub(pattern, repl, outWord)
                
            outWords.append(outWord)

        await ctx.send(" ".join(outWords))
