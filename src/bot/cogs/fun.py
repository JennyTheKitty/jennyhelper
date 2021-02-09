import re
import random
import itertools

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
    exclamations = ["!!!!11", "1!!", "!¡¡!1!", "!!1¡1", "!!", "¡"]
    questions = ["!?", "?!!?", "?!?1", "?!?!"]
    uwuMap = [
        # r|l => w, but not if at the end of word
        [r"(?:l|r)(?!l$|r$)(?!$)", r"w"],
        [r"(?:L|R)(?!L$|R$)(?!$)", r"W"],
        # Nyaa
        [r"(n|N)([aeiou])", r"\1y\2"],
        [r"(N)([AEIOU])", r"\1Y\2"],
        # Love => Luv
        [r"ove", r"uv"],
        [r"OVE", r"UV"],
        # with => wiff
        [r"(?<!^)th", r"ff"],
        [r"(?<!^)TH", r"FF"],
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uwu(self, ctx: commands.Context, *, text: str):
        words = [
            ([x] if re.match(URL_PATTERN, x) else re.findall(r"[\w\']+|[^\w\s]+", x))
            for x in re.split(" ", text)
        ]
        out = ""

        for word in itertools.chain(*words):
            if re.match(URL_PATTERN, word):
                out += " " + word
            elif re.match(r"!+", word):
                out += random.choice(self.exclamations)
            elif "?" in word and re.match(r"[?!]+", word):
                out += random.choice(self.questions)
            elif re.match(r"[,.]+", word):
                out += " " + " ".join(random.choice(self.faces) for _ in word)
            else:
                outWord = word
                for pattern, repl in self.uwuMap:
                    outWord = re.sub(pattern, repl, outWord)

                out += " " + outWord

        await ctx.send(out)
