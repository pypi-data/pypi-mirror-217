import disnake
from typing import List

from disnake.ext import commands
from _discord import emojis
from views.learnviews import MainView2


class MainMenu(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=80
)




    @disnake.ui.button(label="🟢Core Calls", style=disnake.ButtonStyle.url, url="https://www.alphaquery.com/stock-screener/600010230?run=1")
    async def coreputs(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        pass


    @disnake.ui.button(label="🔴Core Puts", style=disnake.ButtonStyle.url, url="https://www.alphaquery.com/stock-screener/600010229?run=1")
    async def coreputs(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        pass



    @disnake.ui.button(style=disnake.ButtonStyle.url, label="🟢Core Calls".center(1, " "), url="https://www.alphaquery.com/stock-screener/600010230?run=1")
    async def corecalls(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        pass


    @disnake.ui.button(label="Market Data", style=disnake.ButtonStyle.blurple)
    async def opportunity(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        em = disnake.Embed(title="🪙 Opportunity",description="```py\nLooking for play opportunities? Besides the core logic - here are some other avenues to explore:```",color=disnake.Colour.dark_orange())
        em.add_field(name="TradyTics AI Alerts", value=f"```py\nIf you want some play-call alerts - you should definitely try TradyTics via Paper Trading with Options. They're pretty accurate - but as with everything else it comes with a certain degree of risk.```")
        await interaction.response.edit_message(embed=em,view=self)
        self.clear_items()
    
        

    @disnake.ui.button(label="Commands", style=disnake.ButtonStyle.blurple,emoji="<a:_:1042689688022024212>")
    async def botcommands(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="Bot 🤖 Commands", description="```py\nChoose from the drop-down list below to view the commands for each category.```", color=disnake.Colour.dark_gold(), url = "https://www.fudstop.io")
        self.clear_items()
        self.add_item(BotCmdMenu())
        await interaction.response.edit_message(embed=embed, view=self)


    @disnake.ui.button(label="🇱 🇪 🇦 🇷 🇳", style=disnake.ButtonStyle.grey, row=2, emoji="<a:_:1042676749357555794>")
    async def learn(self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction):
        view = disnake.ui.View()
        embed = disnake.Embed(title="🧠 Select a category from the dropdown!", color=disnake.Colour.fuchsia())
        embed.set_image(url="https://media.giphy.com/media/waq1okC7KZgqC6N229/giphy.gif")
        embed.set_footer( text="Implemented by Fudstop Trading")
        await interaction.response.edit_message(embed=embed)


    @disnake.ui.button(style=disnake.ButtonStyle.red, row=2)
    async def close( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="⭕ FUDSTOP Application Closed", color=disnake.Colour.dark_red())
        embed.set_image(url="https://media.giphy.com/media/waq1okC7KZgqC6N229/giphy.gif")

        embed.set_footer( text="Implemented by Fudstop Trading")
        await interaction.response.edit_message(embed=embed, view=None)




class AlertsView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=80
)



    @disnake.ui.button(label="Analyst Upgrades", style=disnake.ButtonStyle.grey, )
    async def analysts( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Analyst Upgrades", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Analyst Upgrades",value='<#1016372139802234991>', inline=False)
        embed.set_image(url="https://ucarecdn.com/6ef20032-5263-4e04-8265-cf3b02b59d21/ANALYST.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Social Spike 🫂", style=disnake.ButtonStyle.grey, )
    async def sspike( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Social Spike 🫂", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Social Spike 🫂", value="<#1016369975864348673>", inline=True)
        embed.set_image(url="https://ucarecdn.com/191849f9-3bc0-4dd4-b68d-6440b08c0639/sspike.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Crypto Alerts🪙", style=disnake.ButtonStyle.grey, )
    async def crypt( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Crypto Alerts🪙", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Crypto Alerts🪙", value="<#1016372517251850360> \n\n <#1016372323051388999>", inline=True)
        embed.set_image(url="https://ucarecdn.com/db5a9e00-1b30-4246-9207-a5f1e25d31da/CRYPTOS.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Important News📰", style=disnake.ButtonStyle.blurple, )
    async def impnews( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Important News📰", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Important News📰", value="<#1016372151596630016>", inline=True)
        embed.set_image(url="https://ucarecdn.com/5fdb8028-210b-421f-b449-f43be8518b36/nrwea.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Options Sweeps🧹", style=disnake.ButtonStyle.blurple, )
    async def osweeps( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Options Sweeps🧹", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Options Sweeps🧹", value="<#1016369913759285338>", inline=True)
        embed.set_image(url="https://ucarecdn.com/8ef30c41-ff02-47a7-bf3f-048e3d783321/sweeps.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Stock Breakouts📈", style=disnake.ButtonStyle.blurple, )
    async def stkbrk( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Stock Breakouts📈", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Stock Breakouts📈", value="<#1016369985867743394>", inline=True)
        embed.set_image(url="https://ucarecdn.com/d3c602d7-4cd7-4393-b603-42339733ecf3/breakout.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Scalps🤳", style=disnake.ButtonStyle.blurple, )
    async def realtimealerts( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Scalps🤳", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Scalps🤳", value="<#1016369974945775666>", inline=True)
        embed.set_image(url="https://ucarecdn.com/475cb5d9-77b4-451a-a4f7-484d2a8b705c/bryancohen.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Insider Trades🔀", style=disnake.ButtonStyle.green, )
    async def inst( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Insider Trades🔀", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Insider Trades🔀", value="<#1016369984768852090>", inline=True)
        embed.set_image(url="https://ucarecdn.com/4d245ffb-a2cf-4c56-88d1-a3d40074701b/INSIDERSELLING.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Bullseye Alerts", style=disnake.ButtonStyle.grey, )
    async def bullseye( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Bullseye Alerts", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Analyst Upgrades",value='<#1016369960810979388>', inline=False)
        embed.set_image(url="https://ucarecdn.com/e493d847-f98f-484f-af36-02cefb581360/BULLSEYEBOT.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="Trady Flow🌻", style=disnake.ButtonStyle.grey, )
    async def tflow( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        embed = disnake.Embed(title="Trady Flow🌻", description=" \n\n WHEN TRADING THE ALERTS: **GO IN THE MONEY**. They often recommend OTM strikes - but I have found with experience that if you play these alerts ITM, you'll see a much higher success rate.", color=disnake.Colour.random())
        embed.add_field(name="Trady Flow🌻", value="<#1016369947829600297>", inline=True)
        embed.set_image(url="https://ucarecdn.com/d5df00da-bca4-4dd4-b34b-a21acdade66c/tradyflow.png")
        await interaction.response.edit_message(embed=embed, view=AlertsView())

    @disnake.ui.button(label="🏡", style=disnake.ButtonStyle.green, )
    async def goback( self,button: disnake.ui.Button,interaction: disnake.ApplicationCommandInteraction ):
        await interaction.response.edit_message(view=MainView2())


class Menus(disnake.ui.View):
    def __init__(
        self, embeds: List[disnake.Embed], options: List[disnake.SelectOption]
    ):
        super().__init__(timeout=None)

        # Sets the embed list variable.
        self.embeds = embeds
        self.options = options
        #self.options2 = options2

        # Current embed number.
        self.embed_count = 0

        # Disables previous page button by default.

        # Sets the footer of the embeds with their respective page numbers.
        self.count = 0
        self.set_link_button()

        for opt in options:
            self.selector.append_option(opt)  # pylint: disable=E1101
        for i, embed in enumerate(self.embeds):
            embed.set_footer(
                text=f"Page {i + 1} of {len(self.embeds)}",
                icon_url="https://static.wixstatic.com/media/3235bb_a6ebb092eaa0466792f4925f3af3d46c~mv2.gif",
            )


        #for opt2 in options2:
          #  self.selector2.append_option(opt2)  # pylint: disable=E1101


    def set_link_button(self) -> None:
        if not hasattr(self, "link_button"):
            self.link_button: disnake.ui.Button = disnake.ui.Button(
                style=disnake.ButtonStyle.url,
                url="https://chuckdustin12.wixsite.com/my-site",
                label="Site",
                row=0,
            )
            self.add_item(self.link_button)
        self.link_button.label = "Site"
        self.count += 1

    @disnake.ui.select(
        placeholder="Page Select",
        custom_id=f"select_{str(disnake.Member)}_",
        row=1,
    )
    async def selector(
        self,
        select: disnake.ui.Select,
        inter: disnake.MessageInteraction,
    ) -> None:
        self.set_link_button()
        s = ""
        str1 = s.join(select.values)
        ind = int(str1)
        self.embed_count = str1
        self.next_page.disabled = False
        self.prev_page.disabled = False
        print(select.values)
        await inter.response.edit_message(embed=self.embeds[ind], view=self)



    @disnake.ui.button(
        label="Previous page",
        emoji="<a:leftarrow:929686892339937371>",
        style=disnake.ButtonStyle.red,
        custom_id=f"persistent_view:prevpage_{str(disnake.Member)}_",
    )
    async def prev_page(  # pylint: disable=W0613
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction,
    ):
        # Decrements the embed count.
        self.embed_count -= int(1)

        # Gets the embed object.
        embed = self.embeds[self.embed_count]

        # Enables the next page button and disables the previous page button if we're on the first embed.
        self.next_page.disabled = False

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(
        label="🔙🅱️ 🇦 🇨 🇰", 
        style=disnake.ButtonStyle.blurple,
        custom_id="yeetback",
    )

    async def back(
        self,
        button:disnake.ui.Button,
        interaction: disnake.MessageCommandInteraction,
    ):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(
        label="Next page",
        emoji="<a:rightarrow:929686891891155006>",
        style=disnake.ButtonStyle.red,
        custom_id=f"persistent_view:nextpage_{str(disnake.Member)}_",
    )
    async def next_page(  # pylint: disable=W0613
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction,
    ):
        # Increments the embed count.
        self.embed_count += 1
        self.add_item(BotCmdMenu())
        # Gets the embed object.
        embed = self.embeds[self.embed_count]

        # Enables the previous page button and disables the next page button if we're on the last embed.
        self.prev_page.disabled = False

        await interaction.response.edit_message(embed=embed, view=self)


class FUDSTOPMenu(disnake.ui.Select):
    def __init__(self):
        
        options = [
    
            disnake.SelectOption(label="map🗾Heatmaps"),
            disnake.SelectOption(label="ch💬Chats⬅"),
            disnake.SelectOption(label="flow💦Options Flow"),
            disnake.SelectOption(label="fd📶Market & Social Feeds"),
            disnake.SelectOption(label="rss🔊RSS Feeds"),
            disnake.SelectOption(label="nw🌐News Feeds"),
            disnake.SelectOption(label="tt🚀TradyTics Realtime Alerts"),
            disnake.SelectOption(label="fm📜Forums"),
            disnake.SelectOption(label="ut💡Utilities Sector"),
            disnake.SelectOption(label="etf⚓ETF Sector"),
            disnake.SelectOption(label="cc🌒Consumer Cyclical Sector"),
            disnake.SelectOption(label="cs📣Communication Services Sector"),
            disnake.SelectOption(label="re🏠Real Estate Sector"),
            disnake.SelectOption(label="he💉Healthcare Sector"),
            disnake.SelectOption(label="te💿Technology Sector"),
            disnake.SelectOption(label="in🌆Industrials Sector"),
            disnake.SelectOption(label="cd⛴️Consumer Defensive Sector"),
            disnake.SelectOption(label="fs💰Financial Services Sector"),
            disnake.SelectOption(label="en⚡Energy Sector"),
            disnake.SelectOption(label="bm🧱Basic Materials Sector")]

        super().__init__(
            placeholder="🗺️  🇲 🇪 🇳 🇺  🗾",
            min_values=1,
            max_values=1,
            custom_id="fudmenu",
            options=options
        )



class PersistentView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)




class MasterView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)



class BotCmdMenu(disnake.ui.Select):
    def __init__(self):
    
        options = [ 
            disnake.SelectOption(label="📊 Stock Commands", description="These commands are used to gather stock data."),
            disnake.SelectOption(label="💦 Flow Commands", description="Commands displaying options flow from Open BB."),
            disnake.SelectOption(label="📉 Charting Commands", description="Commands used to call stock charts to Discord."),
            disnake.SelectOption(label="💸 Earnings Commands", description="Commands used for earnings related data."),
            disnake.SelectOption(label="🫧 Streaming Commands", description="Commands that return real-time data."),
            disnake.SelectOption(label="🎱 Dark Pool Commands", description="Dark Pool Commands - Open BB Bot."),
            disnake.SelectOption(label="🔎 Analysis Commands", description="Analyze markets, situations, and trends."),
            disnake.SelectOption(label="🩸 Jasmy Commands", description="Jasmycoin related commands!"),
            disnake.SelectOption(label="🐂 Webull Commands", description="Commands using Webull's API!"),
            disnake.SelectOption(label="🪙 Economy Commands", description="Commands related to economic information / data."),
            disnake.SelectOption(label="🧠 Learning Commands", description="Commands used to learn several topics from discord to markets."),
            disnake.SelectOption(label="🕵️ Due Dilligence Commands", description="Due diligence commands from Open BB Bot."),]

        super().__init__(    
            placeholder="🅱️ 🇴 🇹  🤖  🇨 🇴 🇲 🇲 🇦 🇳 🇩 🇸",
            min_values=1,
            max_values=1,
            custom_id="botcmdssecl",
            options=options)


    async def callback(self, interaction: disnake.MessageCommandInteraction):
        if self.values[0] == "📊 Stock Commands":
            embeds = [
            disnake.Embed(title="🤖/stock shortinterest", description="```py\nDisplays current and historic short interest for a ticker.```\n</stock shortinterest:1036711345468477514>"),
            disnake.Embed(title="🤖/stock ipos",description="```py\nDisplays the upcoming IPOs.```\n</stock ipos:1036711345468477514>"),
            disnake.Embed(title="🤖/stock capitalflow", description="```py\nShows capitalflow for a ticker broken down by player size.```\n</stock capitalflow:1036711345468477514>"),
            disnake.Embed(title="🤖/stock orderflow",description="```py\nShows the current day's orderflow in terms of buy, sell, and neutral.```\n</stock orderflow:1036711345468477514>"),
            disnake.Embed(title="🤖/stock liquidity", description="```py\nDisplays the liquidity level for a stock. 0 = lowest. 5 = highest.```\n</stock liquidity:1036711345468477514>"),
            disnake.Embed(title="🤖/stock criminals", description="```py\nReturns the latest insider buys/sells from government officials.```\n</stock criminals:1036711345468477514>"),
            disnake.Embed(title="🤖/stock leverage", description="```py\nReturns leverage stats fora  stock.```\n</stock leverage:1036711345468477514>"),
            disnake.Embed(title="🤖/stock company_brief", description="```py\nReturns core information for a company - such as location & contact.```\n</stock company_brief:1036711345468477514>"),
            disnake.Embed(title="🤖/stock insider_summary", description="```py\nReturns the latest insider summary information for a tciker.```\n</stock insider_summary:1036711345468477514>"),
            disnake.Embed(title="🤖/stock institutions", description="```py\nReturns the top 10 institutional holders for a ticker.```\n</stock institutions:1036711345468477514>"),]

            options = [
            disnake.SelectOption(label="🤖/stock shortinterest",value="</stock shortinterest:1036711345468477514>"),
            disnake.SelectOption(label="🤖/stock ipos",value=2,description="```py\nDisplays the upcoming IPOs.```\n</stock ipos:1036711345468477514>"),
            disnake.SelectOption(label="🤖/stock capitalflow",value=3),
            disnake.SelectOption(label="🤖/stock orderflow",value=4),
            disnake.SelectOption(label="🤖/stock liquidity",value=5),
            disnake.SelectOption(label="🤖/stock criminals",value=6),
            disnake.SelectOption(label="🤖/stock leverage",value=7),
            disnake.SelectOption(label="🤖/stock company_brief",value=8),
            disnake.SelectOption(label="🤖/stock insider_summary",value=9),
            disnake.SelectOption(label="🤖/stock institutions",value=10),]
            
            await interaction.response.edit_message(view=Menus(embeds,options))
        elif self.values[0] == "📉 Charting Commands":
            embeds = [
            disnake.Embed(title="📉Charting Commands",description="```py\nThese commands are used to utilize charting right from discord.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
            disnake.Embed(title="Charting Timeframe Arguments:", description="```py\nAccepted timeframes:``` ```py\n 1-minute 2-minute, 3-minute, 4-minute, 5-minute, 6-minute, 10-minute, 15-minute, 20-minute, 30-minute, 45-minute, 1-hour, 2-hour, 3-hour, 4-hour, 6-hour, 8-hour, 12-hour, 1-day, 2-day, 3-day, 4-day, 5-day, 6-day, 1-week, 2-week, 3-week, 1-month, 2-month, 3-month, 4-month, 6-month, 1-year```"),
            disnake.Embed(title="Charting Indicators:", description="```py\nAccepted Indicators:``` ```py\n'AbandonedBaby' 'AccumulationSwingIndex', 'Accumulation/Distribution', 'Advance/DeclineRatio','Alligator', ArnaudLegouxMovingAverage, 'Aroon', Aroon Oscillator, ATR, ATRBands, ATRTrailingStop, 'AverageDirectionalMovementIndex', AveragePrice, AwesomeOscillator, BalanceofPower, BearishEngulfing, BearishHammer, BearishHaramiCross, BearishHarami, BearishInvertedHammer, 'BearishMarubozu', BearishSpinningTop, 'BollingerBands', BollingerBands%B, BollingerBandsWidth, BullishEngulfing, BullishHammer, BullishHaramiCross Pattern, Bullish Harami Pattern, Bullish Inverted Hammer Pattern, Bullish Marubozu Pattern, Bullish Spinning Top Pattern```"),
            disnake.Embed(title="Charting Indicators:", description="```py\nMore Accepted Indicators:``` ```py\n'CenterofGravity', ChaikinMoneyFlowIndex, ChaikinOscillator, ChaikinVolatility, ChandeForecast, ChandeKrollStop, Chande Momentum Oscillator, Chop Zone, Choppiness Index, CommodityChannelIndex, Connors RSI, Coppock, Coppock Curve, Correlation-Log, CorrelationCoefficient, CumulativeTick'"),
            disnake.Embed(title="Charting Indicators:",description="```py\nMore Accepted Indicators:``` ```py\nDarkCloudCoverPattern, DetrendedPriceOscillator, DirectionalMovement, DisparityOscillator, DojiPattern, DONCH, DonchainWidth, 'DoubleEMA', DownsideTasukiGap, DragonflyDoji, Ease of Movement, ElderRay, Elder'sForceIndex, ElliottWave, EMA, EMACross, Envelopes, EveningDojiStar, EveningStar, FisherTransform, ForceIndex, FullStochasticOscillator, GatorOscillator, GopalakrishnanRangeIndex, GravestoneDoji, GuppyMovingAverage, GuppyOscillator, 'Hangman', HighMinus Low, Highest High Volume, HistoricalVolatility, Hull MA, IchimokuCloud, Intraday MomentumIndex, KeltnerChannel, Klinger, KnowSureThing, LeastSquaresMovingAverage, LinearRegressionChannel, LinearRegressionCurve, LinearRegressionSlope, 'LowestLowVolume', 'MACross', MAwithEMACross, 'MACD', MajorityRule, MarketProfile, MassIndex, McGinleyDynamic, MedianPrice, MedianPrice, Momentum, MoneyFlowIndex, MoonPhases, 'MorningDojiStar', MorningStar, 'MovingAverage'```"),
            disnake.Embed(title="Charting Indicators:",description="```py\nMore Accepted Indicators:``` ```py\nMovingAverageAdaptive, MovingAverageChannel, MovingAverageDouble, MovingAverageEnvelope, MovingAverage Hamming, MovingAverageMultiple, Negative Volume Index, 'OnBalanceVolume', 'ParabolicSAR', PerformanceIndex PiercingLinePattern, PivotPointsHighLow, PivotPointsStandard, PositiveVolumeIndex, PrettyGoodOscillator, PriceChannel, PriceMomentumOscillator, PriceOscillator, PriceROC, PriceVolumeTrend, PrimeNumberBands, PrimeNumberOscillator, PsychologicalLine, QstickIndicator, RandomWalk, Ratio, RaviOscillator, RelativeVolatility, 'RSI', Schaff, Shinohara, ShootingStar, SMIErgodicIndicator, SMIErgodicOscillator, SmoothedMovingAverage, Spread, StandardDeviation, StandardError, StandardErrorBands, Stochastic, 'StochasticRSI', Stoller AverageRangeChannelBands, 'Supertrend', 'SwingIndex'```"),
            disnake.Embed(title="Charting Indicators:", description="```py\nMore Accepted Indicators:``` ```py\nThreeBlackCrows, 'ThreeWhiteSoldiers', TimeSeriesMovingAverage, TradeVolumeIndex, 'TrendIntensity', TrendStrengthIndex, TriangularMovingAverage, TripleEMA, Triple ExponentialAverage, TripleMA, 'TrueStrengthIndicator', TweezerBottom, TweezerTop, TwiggsMoneyFlowIndex, TypicalPrice, UlcerIndex, UltimateOscillator, VariableMovingAverage, VIDYAMovingAverage, VigorIndex, VolatilityClose-to-Close, VolatilityIndex, VolatilityO-H-L-C, VolatilityZeroTrendClose-to-Close, VolumeOscillator, VolumeProfile, VolumeROC, VolumeUnderlay, Vortex, VSTOP, 'VWAP', 'VWMA', 'WeightedClose', 'Weighted Moving Average', Williams %R, WilliamsAlligator, WilliamsFractal, ZigZag```"),
            disnake.Embed(title="Chart Types and Styles:",description="```py\nAccepted Styles:``` ```py\nArea, Renko, Kagi, PF, Linebreak, Heikinashi, Hollow, Baseline, HiLo, Column, Logarithmic, Extended, Wide, Marketprofile``` ```py\nHeatmap arguments:\n Whale, Low, Normal, High```"),]
            options = [
            disnake.SelectOption(label="📉Charting Commands",value=1),
            disnake.SelectOption(label="Charting Timeframe Arguments",value=2),
            disnake.SelectOption(label="Charting Indicators",value=3),
            disnake.SelectOption(label="More Charting Indicators:",value=4),
            disnake.SelectOption(label="More Charting Indicators:",value=5),
            disnake.SelectOption(label="More Charting Indicators:",value=6),
            disnake.SelectOption(label="More Charting Indicators:",value=7),
            disnake.SelectOption(label="Chart Types and Styles:",value=8)]


            await interaction.response.edit_message(view=Menus(embeds,options))

        elif self.values[0] == "💸 Earnings Commands":

            embeds = [
            disnake.Embed(title="💸 Earnings Commands",description="```py\nYou can use these commands for earnings-specific data.```", color=disnake.Colour.dark_blue(), url="https://www.fudstop.io"),
            disnake.Embed(title="Earnings Projection", description="```py\nReturns a ticker's earnings projection as well as implied move.```\n</earnings projection:1036711345401372733>"),
            disnake.Embed(title="Earnings Crush", description="```py\nReturns a ticker's projecting earnings crush. It will display a % of IV expected to be lost AFTER EARNINGS. A high number indicates earnings will likely be IV crushed.```\n</earnings crush:1036711345401372733>"),
            disnake.Embed(title="Earnings Calendar", description="```py\nReturns a booklet that has upcoming earnings organized by premarket and after hours. Command Provided by Quant Data```\n</earnings calendar:911140318118838277>"),
            disnake.Embed(title="Earnings Today", description="```py\nReturns the earnings scheduled for the current day.```\n</earnings today:911140318118838277>"),
            disnake.Embed(title="Earnings Date", description="```py\nReturns a ticker's earnings projection as well as implied move.```\n</earnings date:911140318118838277>"),
            disnake.Embed(title="Earnings Day of Week", description="```py\nReturns the tickers scheduled for a specific day of the week.```\n</earnings day-of-week:911140318118838277>"),]

            options = [
            disnake.SelectOption(label="💸 Earnings Commands",value=1, description="```py\nYou can use these commands for earnings-specific data.```"),
            disnake.SelectOption(label="Earnings Projection",value=2,description="```py\nReturns a ticker's earnings projection as well as implied move.```"),
            disnake.SelectOption(label="Earnings Crush",value=3, description="```py\nReturns project earnings crush. It will display a % of IV expected to be lost AFTER EARNINGS.```"),
            disnake.SelectOption(label="Earnings Calendar",value=4, description="```py\nReturns a booklet that has upcoming earnings organized by premarket and after hours.```"),
            disnake.SelectOption(label="Earnings Today",value=5,description="```py\nReturns the earnings scheduled for the current day.```"),
            disnake.SelectOption(label="Earnings Date",value=6, description="```py\nReturns a ticker's earnings projection as well as implied move.```"),
            disnake.SelectOption(label="Earnings Day of Week",value=7, description="```py\nReturns the tickers scheduled for a specific day of the week.```")]
            await interaction.response.edit_message(view=Menus(embeds,options))
        elif self.values[0] == "🫧 Streaming Commands":
            embeds = [
            disnake.Embed(title="🫧 Streaming Commands",description="```py\nThese commands return live data for a period of time when called.```", color=disnake.Colour.fuchsia(), url="https://www.fudstop.io"),
            disnake.Embed(title="Quote", description="```py\nStream TWO stock tickers live.```\n</stream quote:1036711345401372738>"),
            disnake.Embed(title="Crypto", description="```py\nStream a crypto currency live.```\n</stream crypto:1036711345401372738>"),
            disnake.Embed(title="Time and Sales", description="```py\nStream time and sales for a ticker in real time.```\n</stream time_and_sales:1036711345401372738>"),
            disnake.Embed(title="Double Crypto", description="```py\nStream TWO crypto currencies live.```\n</stream double_crypto:1036711345401372738>"),
            disnake.Embed(title="Double Crypto", description="```py\nStream TWO stock tickers live.```\n</stream double_quote:1036711345401372738>"),
            disnake.Embed(title="Tits", description="```py\nYup - stream tits.```\n</stream tits:1036711345401372738>"),]

            options = [
            disnake.SelectOption(label="🫧 Streaming Commands",value=1, description="```py\nThese commands return live data for a period of time when called.```"),
            disnake.SelectOption(label="Quote",value=2, description="```py\nStream TWO stock tickers live.```"),
            disnake.SelectOption(label="Crypto", value=3, description="```py\nStream a crypto currency live.```"),
            disnake.SelectOption(label="Time and Sales",value=4, description="```py\nStream time and sales for a ticker in real time.```"),
            disnake.SelectOption(label="Double Crypto",value=5, description="```py\nStream TWO crypto currencies live.```"),
            disnake.SelectOption(label="Double Quote",value=6,description="```py\nStream TWO stock tickers live```"),
            disnake.SelectOption(label="Tits",value=7,description="```py\nStream some tits.```"),]

            await interaction.response.edit_message(Menus(embeds,options))
        elif self.values[0] == "🎱 Dark Pool Commands":

            embeds = [
            disnake.Embed(title="🎱 Dark Pool Commands",description="```py\nCommands for dark-pool data.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
            disnake.Embed(title="All DP", description="```py\nThis command calls the latest 15 dark pools.```\n</dp alldp:1004263746170011748>"),
            disnake.Embed(title="Allprints", description="```py\nTop total block and dark pool data.```\n</dp topsum:1004263746170011748>"),
            disnake.Embed(title="Topsum", description="```py\nLast 15 block trades.```\n</dp allblocks:1004263746170011748>"),
            disnake.Embed(title="All Blocks", description="```py\nInput a date to look for the largest block trades for that date.```\n</dp bigprints:1004263746170011748>"),
            disnake.Embed(title="Big Prints", description="```py\nLast 15 combo of dark pools and blocks.```\n</dp allprints:1004263746170011748>"),
            disnake.Embed(title="Levels", description="```py\nBiggest levels for all prints over the last X days.```\n</dp levels:1004263746170011748>"),
            disnake.Embed(title="Sectors", description="```py\nSummary of all prints by % market cap by sector.```\n</dp sectors:1004263746170011748>"),]

            options = [
            disnake.SelectOption(label="🎱 Dark Pool Commands",value=1),
            disnake.SelectOption(label="All DP",value=2),
            disnake.SelectOption(label="Allprints",value=3),
            disnake.SelectOption(label="Topsum",value=4),
            disnake.SelectOption(label="All Blocks",value=5),
            disnake.SelectOption(label="Big Prints",value=6),
            disnake.SelectOption(label="Levels",value=7),
            disnake.SelectOption(label="Sectors",value=8),]

            await interaction.response.edit_message(Menus(embeds,options))
        elif self.values[0] == "🔎 Analysis Commands":
            embeds = [
            disnake.Embed(title="🔎 Analysis Commands",description="```py\nCommands used for stock and options analysis as well as general market analysis.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
            disnake.Embed(title="Top_Shorts", description="```py\nReturns tickers with over 30% short interest.``` </analysis topshorts:1036711345401372740>"),
            disnake.Embed(title="Gaps_Down", description="```py\nEnter a % and it returns tickers that have gapped down.``` </analysis gaps_down:1036711345401372740>"),
            disnake.Embed(title="Gaps_up", description="```py\nEnter a % and it returns tickers that have gapped up.``` </analysis gaps_up:1036711345401372740>"),
            disnake.Embed(title="Finscreen", description="```py\nUse the finscreener with several customizable options.``` </analysis finscreen:1036711345401372740>"),
            disnake.Embed(title="Overbought_Gap", description="```py\nReturns tickers that have gapped up and are overbought in a downward channel.``` </analysis overbought_gap:1036711345401372740>"),
            disnake.Embed(title="Rating", description="```py\nReturns the buy vs hold vs sell ratings for a ticker.``` </analysis rating:1036711345401372740>"),]

            options = [
            disnake.SelectOption(label="🔎 Analysis Commands",value=1,description="```py\nCommands used for stock and options analysis as well as general market analysis.```"),
            disnake.SelectOption(label="Top_Shorts",value=2),
            disnake.SelectOption(label="Gaps_Down",value=3),
            disnake.SelectOption(label="Gaps_up",value=4),
            disnake.SelectOption(label="Finscreen",value=5),
            disnake.SelectOption(label="Overbought_Gap",value=6),
            disnake.SelectOption(label="Rating",value=7)]

            await interaction.response.edit_message(view=Menus(embeds,options))

        elif self.values[0] == "🩸 Jasmy Commands":
            embeds = [
            disnake.Embed(title="🩸 Jasmy Commands",description="```py\nCommands for the beloved Jasmycoin.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
            disnake.Embed(title="Holders", description="```py\nReturns the current number of Jasmy Wallets.```\n</jasmy holders:1036711345401372735>"),
            disnake.Embed(title="Price", description="```py\nStreams the current Jasmy price across 20 exchanges.```\n</jasmy price:1036711345401372735>"),]

            options = [
            disnake.SelectOption(label="🩸 Jasmy Commands",value=1),
            disnake.SelectOption(label="Holders",value=2),
            disnake.SelectOption(label="Price",value=3),]



            await interaction.response.edit_message(view=Menus(embeds,options))
        elif self.values[0] == "🐂 Webull Commands":
            embeds = [
            disnake.Embed(title="🐂 Webull Commands",description="```py\nCommands specifically from Webull's API.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
            disnake.Embed(title="Cost", description="```py\nReturns the cost distribution profited shares proportion straight from Webull.```\n</webull cost:1036711345401372739>"),
            disnake.Embed(title="Webull_Quote", description="```py\nPulls webull data to discord and gives pricing data and information.```\n</webull webull_quote:1036711345401372739>"),
            disnake.Embed(title="Analysis Tools", description="```py\nLearn about Webull Analysis tools.```\n</webull analysis_tools:1036711345401372739>"),
            disnake.Embed(title="Bid_ask_Spread", description="```py\nReturns educational material regarding the bid ask spread.```\n</webull bid_ask_spread:1036711345401372739>"),
            disnake.Embed(title="News", description="```py\nSearch for news articles from within Webull's news database.```\n</webull news:1036711345401372739>"),
            disnake.Embed(title="Graphics", description="```py\nSearch by keyword for a list of helpful graphics.```\n</webull graphics:1036711345401372739>"),
            disnake.Embed(title="News", description="```py\nLearn how to read and customize your options chain in Webull.```\n</webull options_chain:1036711345401372739>")]

            options = [
            disnake.Embed(title="Cost",value=1),
            disnake.Embed(title="Webull_Quote",value=2),
            disnake.Embed(title="Analysis Tools",value=3),
            disnake.Embed(title="Bid_ask_Spread",value=4),
            disnake.Embed(title="News",value=5),
            disnake.Embed(title="Graphics",value=6),
            disnake.Embed(title="News",value=7)]

            await interaction.response.edit_message(view=Menus(embeds,options))
        elif self.values[0] == "🪙 Economy Commands":

            embeds = [
            disnake.Embed(title="🪙 Economy Commands",description="```py\nImportant economic data such as inflation, jobless claims, repo, and more.```", color=disnake.Colour.yellow(), url="https://www.fudstop.io"),
            disnake.Embed(title="Jobless_Claims", description="```py\nReturns latest and historic Jobless Numbers.```\n</economy jobless_claims:1036711345401372742>"),
            disnake.Embed(title="Inflation", description="```py\nReturns inflation numbers with averaged and historic data.```\n</economy inflation:1036711345401372742>"),
            disnake.Embed(title="AMBS", description="```py\nReturns amount of retail capital in money market funds.```\n</economy retail_repo:1036711345401372742>"),
            disnake.Embed(title="Retail_Repo", description="```py\nReturns the latest roll, swap, new, or all agency mortgage backed securities.```\n</economy ambs:1036711345401372742>"),
            disnake.Embed(title="Data", description="```py\nReturns a large list of economic data.```\n</economy data:1036711345401372742>"),
            disnake.Embed(title="House_trades", description="```py\nReturns a list of the latest trades from the House.```\n</economy house_trades:1036711345401372742>"),
            disnake.Embed(title="econ RevRepo", description="```py\nReturns the latest and historic Reverse Repo Data with differences.```\n</econ revrepo:1004263746111275130>"),
            disnake.Embed(title="econ Calendar", description="```py\nDisplays a calendar of important economic events.```\n</econ calendar:1004263746111275130>"),
            disnake.Embed(title="econ GlBonds", description="```py\nDisplays global bond data.```\n</econ glbonds:1004263746111275130>"),
            disnake.Embed(title="econ USBonds", description="```py\nDisplays US bond data.```\n</econ usbonds:1004263746111275130>"),
            disnake.Embed(title="econ YieldCurve", description="```py\nDisplays US Bond yield curve data.```\n</econ yieldcurve:1004263746111275130>"),
            disnake.Embed(title="econ indices", description="```py\nDisplays US indices overview.```\n</econ indices:1004263746111275130>"),
            disnake.Embed(title="econ currencies", description="```py\nDisplays global currency data.```\n</econ currencies:1004263746111275130>"),
            disnake.Embed(title="econ fedrates", description="```py\nDisplays upcoming FOMC events and projected BPS hike percentage.```\n</econ fedrates:1004263746111275130>"),]

            options = [
            disnake.SelectOption(label="🪙 Economy Commands",value=1),
            disnake.SelectOption(label="Jobless_Claims",value=2),
            disnake.SelectOption(label="Inflation",value=3),
            disnake.SelectOption(label="AMBS",value=4),
            disnake.SelectOption(label="Retail_Repo",value=5),
            disnake.SelectOption(label="Data",value=6),
            disnake.SelectOption(label="House_trades",value=7),
            disnake.SelectOption(label="econ RevRepo",value=8),
            disnake.SelectOption(label="econ Calendar",value=9),
            disnake.SelectOption(label="econ GlBonds",value=10),
            disnake.SelectOption(label="econ USBonds",value=11),
            disnake.SelectOption(label="econ YieldCurve",value=12),
            disnake.SelectOption(label="econ indices",value=13),
            disnake.SelectOption(label="econ currencies",value=14),
            disnake.SelectOption(label="econ fedrates",value=15)]

            await interaction.response.edit_message(view=Menus(embeds,options))
        elif self.values[0] == "🧠 Learning Commands":
            embeds = [
            disnake.Embed(title="🧠 Learning Commands",description="```py\nImportant economic data such as inflation, jobless claims, repo, and more.```", color=disnake.Colour.yellow(), url="https://www.fudstop.io"),
            disnake.Embed(title="Option_Strategies", description="```py\nLearn about different options strategies.```\n</learn option_strategies:1036711345468477510>"),
            disnake.Embed(title="Calls", description="```py\nLearn about call options.```\n</learn calls:1036711345468477510>"),
            disnake.Embed(title="Puts", description="```py\nLearn about put options.```\n</learn puts:1036711345468477510>"),
            disnake.Embed(title="Candle_Patterns", description="```py\nLearn about different candlestick patterns.```\n</learn candle_patterns:1036711345401372742>"),
            disnake.Embed(title="Core_Logic", description="```py\nLearn about the core logic and how it works.```\n</learn core_logic:1036711345401372742>"),
            disnake.Embed(title="China", description="```py\nLearn about China's economic transformation.```\n</learn china:1036711345401372742>"),
            disnake.Embed(title="Covered_Calls", description="```py\nLearn about selling calls to generate revenue.```\n</learn covered_calls:1036711345401372742>"),
            disnake.Embed(title="ETFs", description="```py\nLearn about exchange traded funds.```\n</learn etfs:1036711345401372742>"),
            disnake.Embed(title="Filings", description="```py\nLearn about different SEC filings.```\n</learn filings:1036711345401372742>"),
            disnake.Embed(title="Options 101", description="```py\nTake the Options 101 course from the Options Industry Council.```\n</learn options_101:1036711345401372742>"),
            disnake.Embed(title="Greeks", description="```py\nLearn about the greeks: delta, gamma, rho, vega, and theta.```\n</learn greeks:1036711345401372742>"),
            disnake.Embed(title="Order_types", description="```py\nLearn about the different order types.```\n</learn order_types:1036711345401372742>"),
            disnake.Embed(title="OCC", description="```py\nLearn about important filings out of the Options Clearing Corporation.```\n</learn occ:1036711345401372742>"),
            disnake.Embed(title="FINRA", description="```py\nLearn about important FINRA filings.```\n</learn finra:1036711345401372742>"),
            disnake.Embed(title="NSFR_ratio", description="```py\nLearn about the critical Net Stable Funding Ratio regarding big banks.```\n</learn nsfr_ratio:1036711345401372742>"),
            disnake.Embed(title="Webull_School", description="```py\nLearn about the Webull App.```\n</learn webull_school:1036711345401372742>"),]


            options = [
            disnake.SelectOption(label="🧠 Learning Commands",value=1),
            disnake.SelectOption(label="Option_Strategies",value=2),
            disnake.SelectOption(label="Calls",value=3,description="Learn about call options."),
            disnake.SelectOption(label="Puts",value=4,description="Learn about put options."),
            disnake.SelectOption(label="Candle_Patterns",value=5,description="Learn about different candlestick patterns."),
            disnake.SelectOption(label="Core_Logic",value=6,description="Learn about the core logic and how it works."),
            disnake.SelectOption(label="China",value=7,description="Learn about China's economic transformation.``'"),
            disnake.SelectOption(label="Covered_Calls",value=8,description="Learn about selling calls to generate revenue."),
            disnake.SelectOption(label="ETFs",value=9,description="Learn about exchange traded funds."),
            disnake.SelectOption(label="Filings",value=10,description="Learn about different SEC filings."),
            disnake.SelectOption(label="Options 101",value=11,description="Take the Options 101 course from the Options Industry Council."),
            disnake.SelectOption(label="Greeks",value=12,description="Learn about the greeks: delta, gamma, rho, vega, and theta."),
            disnake.SelectOption(label="Order_types",value=13,description="Learn about the different order types."),
            disnake.SelectOption(label="OCC",value=14,description="Learn about important filings out of the Options Clearing Corporation."),
            disnake.SelectOption(label="FINRA",value=15,description="Learn about important FINRA filings."),
            disnake.SelectOption(label="NSFR_ratio",value=16,description="Learn about the critical Net Stable Funding Ratio regarding big banks."),
            disnake.SelectOption(label="Webull_School",value=17,description="Learn about the Webull App."),]
            await interaction.response.edit_message(Menus(embeds,options))
        elif self.values[0] == "🕵️ Due Dilligence Commands":
            embeds= [
            disnake.Embed(title="🕵️ Due Diligence Commands",description="```py\nThese commands are somewhat useful. I don't really ever use these much, but depending on your trading strategy or type of trading personality - these could be a good fit for you. I'd at least give them a shot.```", color=disnake.Colour.dark_magenta(), url="https://www.fudstop.io"),
            disnake.Embed(title="AH", description="```py\nDisplays After Hours Data for a ticker.```\n</dd ah:1004263746090324066>"),
            disnake.Embed(title="Analyst", description="```py\nReturns analyst ratings for a ticker.```\n</dd analyst:1004263746090324066>"),
            disnake.Embed(title="Bio", description="```py\nReturns the stock company's profile.```\n</dd bio:1004263746090324066>"),
            disnake.Embed(title="Customer", description="```py\nDisplays customers of a company.```\n</dd customer:1004263746090324066>"),
            disnake.Embed(title="ermove", description="```py\nDisplays implied move for a ticker based on option prices.```\n</dd ermove:1004263746090324066>"),
            disnake.Embed(title="divinfo", description="```py\nDisplays dividend information for a ticker.```\n</dd divinfo:1004263746090324066>"),
            disnake.Embed(title="earnings", description="```py\nPick a date and return the earnings scheduled for that day.```\n</dd earnings:1004263746090324066>"),
            disnake.Embed(title="pm", description="```py\nDisplay premarket data for a stock.```\n</dd pm:1004263746090324066>"),
            disnake.Embed(title="pt", description="```py\nDisplays a chart with price targets```\n</dd pt:1004263746090324066>"),
            disnake.Embed(title="ytd", description="```py\nDisplays period performance for a stock.```\n</dd ytd:1004263746090324066>"),
            disnake.Embed(title="sec", description="```py\nDisplays recent SEC filings.```\n</dd sec:1004263746090324066>"),
            disnake.Embed(title="est", description="```py\nDisplays earnings estimates.```\n</dd est:1004263746090324066>"),]


            options= [
            disnake.SelectOption(label="🕵️ Due Diligence Commands",value=1),
            disnake.SelectOption(label="AH",value=2, description="Displays After Hours Data for a ticker."),
            disnake.SelectOption(label="Analyst", value=3,description="Returns analyst ratings for a ticker."),
            disnake.SelectOption(label="Bio",value=4, description="Returns the stock company's profile."),
            disnake.SelectOption(label="Customer",value=5, description="Displays customers of a company."),
            disnake.SelectOption(label="ermove",value=6, description="Displays implied move for a ticker based on option prices."),
            disnake.SelectOption(label="divinfo",value=7, description="Displays dividend information for a ticker."),
            disnake.SelectOption(label="earnings",value=8, description="Pick a date and return the earnings scheduled for that day."),
            disnake.SelectOption(label="pm",value=9, description="Display premarket data for a stock."),
            disnake.SelectOption(label="pt",value=10, description="Displays a chart with price targets"),
            disnake.SelectOption(label="ytd",value=11, description="Displays period performance for a stock."),
            disnake.SelectOption(label="sec",value=12, description="Displays recent SEC filings."),
            disnake.SelectOption(label="est",value=13, description="Displays earnings estimates."),]
            await interaction.response.edit_message(Menus(embeds,options))
        elif self.values[0] == "💦 Flow Commands":
            

            embeds = [
            disnake.Embed(title="💦 Flow Commands",description="```py\nThese commands are for visualizing flow data for options.```", color=disnake.Colour.purple(), url="https://www.fudstop.io"),
            disnake.Embed(title="Flow - Quant Data", description="```py\nThis command searches for options flow using Quant Data's database and returns the results.``` ```py\nAccepted Arguments:\n'ticker' 'size' 'premium' 'moneyness' 'contract-type' 'trade-consolidation-type' 'expiration' 'unusual' 'golden-sweep' 'opening-position'```\n</flow:910724015490998293>"),
            disnake.Embed(title="Day", description="```py\nReturns the most recent flow for a stock.```\n</flow day:1004263746170011749>"),
            disnake.Embed(title="Bigflow", description="```py\nReturns the top 20 flow tickers by premium.```\n</flow bigflow:1004263746170011749>"),
            disnake.Embed(title="Sumexp", description="```py\nReturns flow summary by expiration date for a ticker.```\n</flow sumexp:1004263746170011749>"),
            disnake.Embed(title="Opening", description="```py\nTop 20 flow tickers with opening condition met.```\n</flow opening:1004263746170011749>"),
            disnake.Embed(title="Sumday", description="```py\nGraph the current day's premium for a stock.```\n</flow sumday:1004263746170011749>"),
            disnake.Embed(title="Sumweek", description="```py\nGraph total premium weekly summary for a stock.```\n</flow sumweek:1004263746170011749>"),
            disnake.Embed(title="Prem", description="```py\nReturns a chart with sum of premium per day by calls/puts.```\n</flow prem:1004263746170011749>"),
            disnake.Embed(title="Unu", description="```py\nReturns unusual options trade with over 100k Premium.```\n</flow unu:1004263746170011749>"),
            disnake.Embed(title="Weekly", description="```py\nTop 20 flow by premium for weekly expiring stocks.```\n</flow weekly:1004263746170011749>"),
            disnake.Embed(title="Sectors", description="```py\nSummary by % market cap by Sector.```\n</flow sectors:1004263746170011749>"),
            disnake.Embed(title="Sumtop", description="```py\nTop flow for the day for a stock calls vs puts.```\n</flow sumtop:1004263746170011749>"),
            disnake.Embed(title="Summary", description="```py\nSummary of all flow by % market cap.```\n</flow summary:1004263746170011749>"),]

            options = [
            disnake.SelectOption(label="💦 Flow Commands",value=1,description="These commands are for visualizing flow data for options."),
            disnake.SelectOption(label="Flow - Quant Data",value=2),
            disnake.SelectOption(label="Day",value=3, description="Returns the most recent flow for a stock."),
            disnake.SelectOption(label="Bigflow",value=4, description="Returns the top 20 flow tickers by premium."),
            disnake.SelectOption(label="Sumexp",value=5, description="Returns flow summary by expiration date for a ticker."),
            disnake.SelectOption(label="Opening",value=6, description="Top 20 flow tickers with opening condition met."),
            disnake.SelectOption(label="Sumday",value=7, description="Graph the current day's premium for a stock."),
            disnake.SelectOption(label="Sumweek",value=8, description="Graph total premium weekly summary for a stock."),
            disnake.SelectOption(label="Prem",value=9, description="Returns a chart with sum of premium per day by calls/puts."),
            disnake.SelectOption(label="Unu",value=10, description="Returns unusual options trade with over 100k Premium."),
            disnake.SelectOption(label="Weekly",value=11, description="Top 20 flow by premium for weekly expiring stocks."),
            disnake.SelectOption(label="Sectors",value=12, description="Summary by % market cap by Sector."),
            disnake.SelectOption(label="Sumtop",value=13, description="Top flow for the day for a stock calls vs puts."),
            disnake.SelectOption(label="Summary",value=14, description="Summary of all flow by % market cap."),]
            await interaction.response.edit_message(Menus(embeds,options))
class MasterCommand(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @disnake.ui.button(label="📊 Stock Commands", style=disnake.ButtonStyle.gray,custom_id="stockbutton")
    async def commands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        switcher = disnake.ui.Button(label="🔙🅱️ 🇦 🇨 🇰", style=disnake.ButtonStyle.red,custom_id="siwtcherstock")
        switcher.callback = lambda interaction: interaction.response.edit_message(view=MasterView())
        self.add_item(switcher)
        select = disnake.ui.Select(
            placeholder="🇸 🇹 🇴 🇨 🇰 📊 🇨 🇴 🇲 🇲 🇦 🇳 🇩 🇸",
            min_values=1,
            max_values=1,
            custom_id="stockcmd",
            options=[ 
                disnake.SelectOption(label="🤖/stock shortinterest", description="Displays current and historic short interest for a ticker."),
                disnake.SelectOption(label="🤖/stock ipos",description="Displays the upcoming IPOs."),
                disnake.SelectOption(label="🤖/stock capitalflow", description="Shows capitalflow for a ticker broken down by player size."),
                disnake.SelectOption(label="🤖/stock orderflow",description="Shows the current day's orderflow in terms of buy, sell, and neutral."),
                disnake.SelectOption(label="🤖/stock liquidity", description="Displays the liquidity level for a stock. 0 = lowest. 5 = highest."),
                disnake.SelectOption(label="🤖/stock criminals", description="Returns the latest insider buys/sells from government officials."),
                disnake.SelectOption(label="🤖/stock leverage", description="Returns leverage stats fora  stock."),
                disnake.SelectOption(label="🤖/stock company_brief", description="Returns core information for a company - such as location & contact."),
                disnake.SelectOption(label="🤖/stock insider_summary", description="Returns the latest insider summary information for a tciker."),
                disnake.SelectOption(label="🤖/stock institutions", description="Returns the top 10 institutional holders for a ticker."),



            ]
        )
        em = disnake.Embed(title="📊 Commands",description="```py\nThese commands are used to retrieve data revolving around specific tickers. Use the dropdown below to select a command!```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io")

        embeds=[
            disnake.Embed(title="Capitalflow", description="```py\nReturns an overall picture of orderflow broken down by player size.```\n</stock capitalflow:1036711345468477514>"),
            disnake.Embed(title="Shortinterest", description="```py\nDisplays current and historic short interest for a ticker.```\n</stock shortinerest:1036711345468477514>"),
            disnake.Embed(title="Company_Brief", description="```py\nReturns core company information such as location and contact info.```\n</stock company_brief:1036711345468477514>"),
            disnake.Embed(title="Liquidity", description="```py\nReturns the liqudity rating for a stock. Lowest = 0. Highest = 5.```\n</stock liquidity:1036711345468477514>"),
            disnake.Embed(title="Leverage", description="```py\nDisplays the current leverage statistics for a ticker.```\n</stock leverage:1036711345468477514>"),
            disnake.Embed(title="Insider_Summary", description="```py\nDisplays the latest insider buys from the House and Senate.```\n</stock criminals:1036711345468477514>"),
            disnake.Embed(title="Orderflow", description="```py\nShows the current day's orderflow in terms of buy, sell, and neutral.```\n</stock criminals:1036711345468477514>"),
            disnake.Embed(title="Institutions", description="```py\nDisplays the latest insider buys from the House and Senate.```\n</stock criminals:1036711345468477514>"),]


        await inter.response.edit_message(AlertsView(embeds), view=embeds[0])

    @disnake.ui.button(label="💦 Flow Commands", style=disnake.ButtonStyle.gray,custom_id="flowbutton")
    async def flowcommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        view = disnake.ui.View()
        switcher = disnake.ui.Button(label="🔙🅱️ 🇦 🇨 🇰", style=disnake.ButtonStyle.red,custom_id="flowback")
        switcher.callback = lambda interaction: interaction.response.edit_message(view=MasterView())
        view.add_item(switcher)
        options = [
                disnake.SelectOption(label="💦 Flow", description="Searches Quant Data's flow database and returns the results."),
                disnake.SelectOption(label="💦 Day", description="Returns the most recent flow for a stock."),
                disnake.SelectOption(label="💦 Bigflow", description="Returns the top 20 flow tickers by premium."),
                disnake.SelectOption(label="💦 Opening", description="Top 20 flow tickers with opening condition met."),
                disnake.SelectOption(label="💦 Sumday", description="Returns flow summary by expiration date for a ticker."),
                disnake.SelectOption(label="💦 Sumweek", description="Graph total premium weekly summary for a stock."),
                disnake.SelectOption(label="💦 Sumexp", description="Searches Quant Data's flow database and returns the results."),
                disnake.SelectOption(label="💦 Prem", description="Returns a chart with sum of premium per day by calls/puts."),
                disnake.SelectOption(label="💦 Unu", description="Returns unusual options trade with over 100k Premium."),
                disnake.SelectOption(label="💦 Weekly", description="Top 20 flow by premium for weekly expiring stocks."),
                disnake.SelectOption(label="💦 Sectors", description="Summary by % market cap by Sector."),
                disnake.SelectOption(label="💦 Sumtop", description="Top flow for the day for a stock calls vs puts."),
                disnake.SelectOption(label="💦 Summary", description="Summary of all flow by % market cap."),]
        
        embeds = [
        disnake.Embed(title="💦 Flows",description="```py\nThese commands are for visualizing flow data for options.```", color=disnake.Colour.dark_teal(), url="https://www.fudstop.io"),
        disnake.Embed(title="Flow - Quant Data", description="```py\nThis command searches for options flow using Quant Data's database and returns the results.``` ```py\nAccepted Arguments:\n'ticker' 'size' 'premium' 'moneyness' 'contract-type' 'trade-consolidation-type' 'expiration' 'unusual' 'golden-sweep' 'opening-position'```\n</flow:910724015490998293>"),
        disnake.Embed(title="Day", description="```py\nReturns the most recent flow for a stock.```\n</flow day:1004263746170011749>"),
        disnake.Embed(title="Bigflow", description="```py\nReturns the top 20 flow tickers by premium.```\n</flow bigflow:1004263746170011749>"),
        disnake.Embed(title="Sumexp", description="```py\nReturns flow summary by expiration date for a ticker.```\n</flow sumexp:1004263746170011749>"),
        disnake.Embed(title="Opening", description="```py\nTop 20 flow tickers with opening condition met.```\n</flow opening:1004263746170011749>"),
        disnake.Embed(title="Sumday", description="```py\nGraph the current day's premium for a stock.```\n</flow sumday:1004263746170011749>"),
        disnake.Embed(title="Sumweek", description="```py\nGraph total premium weekly summary for a stock.```\n</flow sumweek:1004263746170011749>"),
        disnake.Embed(title="Prem", description="```py\nReturns a chart with sum of premium per day by calls/puts.```\n</flow prem:1004263746170011749>"),
        disnake.Embed(title="Unu", description="```py\nReturns unusual options trade with over 100k Premium.```\n</flow unu:1004263746170011749>"),
        disnake.Embed(title="Weekly", description="```py\nTop 20 flow by premium for weekly expiring stocks.```\n</flow weekly:1004263746170011749>"),
        disnake.Embed(title="Sectors", description="```py\nSummary by % market cap by Sector.```\n</flow sectors:1004263746170011749>"),
        disnake.Embed(title="Sumtop", description="```py\nTop flow for the day for a stock calls vs puts.```\n</flow sumtop:1004263746170011749>"),
        disnake.Embed(title="Summary", description="```py\nSummary of all flow by % market cap.```\n</flow summary:1004263746170011749>"),]
        
        await inter.response.edit_message(view=Menus(embeds, options))
    @disnake.ui.button(label="📉 Charting Commands", style=disnake.ButtonStyle.gray,custom_id="chartbutton")
    async def chartcommands(self, inter: disnake.AppCmdInter):
        switcher = disnake.ui.Button(label="🔙🅱️ 🇦 🇨 🇰", style=disnake.ButtonStyle.red,custom_id="switcherchart")
        switcher.callback = lambda interaction: interaction.response.edit_message(view=MasterView())
        self.add_item(switcher)
        options=[ 
                disnake.SelectOption(label="/c", description="Use the gigantic list below for a list of arguments."),

    
            ]
        
        embeds = [
        disnake.Embed(title="📉Charting Commands",description="```py\nThese commands are used to utilize charting right from discord.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
        disnake.Embed(title="Charting Timeframe Arguments:", description="```py\nAccepted timeframes:``` ```py\n 1-minute 2-minute, 3-minute, 4-minute, 5-minute, 6-minute, 10-minute, 15-minute, 20-minute, 30-minute, 45-minute, 1-hour, 2-hour, 3-hour, 4-hour, 6-hour, 8-hour, 12-hour, 1-day, 2-day, 3-day, 4-day, 5-day, 6-day, 1-week, 2-week, 3-week, 1-month, 2-month, 3-month, 4-month, 6-month, 1-year```"),
        disnake.Embed(title="Charting Indicators:", description="```py\nAccepted Indicators:``` ```py\n'AbandonedBaby' 'AccumulationSwingIndex', 'Accumulation/Distribution', 'Advance/DeclineRatio','Alligator', ArnaudLegouxMovingAverage, 'Aroon', Aroon Oscillator, ATR, ATRBands, ATRTrailingStop, 'Average DirectionalMovementIndex', AveragePrice, AwesomeOscillator, BalanceofPower, BearishEngulfing, BearishHammer, BearishHaramiCross, BearishHarami, BearishInvertedHammer, 'BearishMarubozu', BearishSpinningTop, 'BollingerBands', BollingerBands%B, BollingerBandsWidth, BullishEngulfing, BullishHammer, BullishHaramiCross Pattern, Bullish Harami Pattern, Bullish Inverted Hammer Pattern, Bullish Marubozu Pattern, Bullish Spinning Top Pattern```"),
        disnake.Embed(title="Charting Indicators:", description="```py\nMore Accepted Indicators:``` ```py\n'Center of Gravity', Chaikin Money Flow Index, Chaikin Oscillator, ChaikinVolatility, ChandeForecast, ChandeKrollStop, Chande Momentum Oscillator, Chop Zone, Choppiness Index, CommodityChannelIndex, Connors RSI, Coppock, Coppock Curve, Correlation-Log, CorrelationCoefficient, CumulativeTick'"),
        disnake.Embed(title="Charting Indicators:",description="```py\nMore Accepted Indicators:``` ```py\nDarkCloudCoverPattern DetrendedPriceOscillator, DirectionalMovement, DisparityOscillator, DojiPattern, DONCH, DonchainWidth, 'DoubleEMA', DownsideTasukiGap, DragonflyDoji, Ease of Movement, ElderRay, Elder'sForceIndex, Elliott Wave, EMA, EMACross, Envelopes, EveningDojiStar, Evening Star Pattern, Fisher Transform, Force Index, FullStochasticOscillator, GatorOscillator, GopalakrishnanRangeIndex, GravestoneDoji, GuppyMovingAverage, GuppyOscillator, 'Hangman', HighMinus Low, Highest High Volume, HistoricalVolatility, Hull MA, IchimokuCloud, Intraday MomentumIndex, KeltnerChannel, Klinger, KnowSureThing, LeastSquaresMovingAverage, LinearRegressionChannel, LinearRegressionCurve, LinearRegressionSlope, 'LowestLowVolume', 'MACross', MAwithEMACross, 'MACD', MajorityRule, MarketProfile, MassIndex, McGinleyDynamic, MedianPrice, MedianPrice, Momentum, MoneyFlowIndex, MoonPhases, 'MorningDojiStar', MorningStar, 'MovingAverage'```"),
        disnake.Embed(title="Charting Indicators:",description="```py\nMore Accepted Indicators:``` ```py\nMovingAverageAdaptive MovingAverageChannel, MovingAverageDouble, MovingAverageEnvelope, MovingAverage Hamming, MovingAverageMultiple, Negative Volume Index, 'OnBalanceVolume', 'ParabolicSAR', PerformanceIndex PiercingLinePattern, PivotPointsHighLow, PivotPointsStandard, PositiveVolumeIndex, PrettyGoodOscillator, PriceChannel, PriceMomentumOscillator, PriceOscillator, PriceROC, PriceVolumeTrend, PrimeNumberBands, PrimeNumberOscillator, PsychologicalLine, QstickIndicator, RandomWalk, Ratio, RaviOscillator, RelativeVolatility, 'RSI', Schaff, Shinohara, ShootingStar, SMIErgodicIndicator, SMI Ergodic Oscillator, SmoothedMovingAverage, Spread, StandardDeviation, StandardError, StandardErrorBands, Stochastic, 'StochasticRSI', Stoller AverageRangeChannelBands, 'Supertrend', 'SwingIndex'```"),
        disnake.Embed(title="Charting Indicators:", description="```py\nMore Accepted Indicators:``` ```py\nThreeBlackCrows 'Three White Soldiers Pattern', TimeSeriesMovingAverage, TradeVolumeIndex, 'TrendIntensity', TrendStrengthIndex, TriangularMovingAverage, TripleEMA, Triple ExponentialAverage, TripleMA, 'TrueStrengthIndicator', TweezerBottom, TweezerTop, TwiggsMoneyFlowIndex, TypicalPrice, UlcerIndex, UltimateOscillator, VariableMovingAverage, VIDYAMovingAverage, VigorIndex, VolatilityClose-to-Close, VolatilityIndex, VolatilityO-H-L-C, VolatilityZeroTrendClose-to-Close, VolumeOscillator, VolumeProfile, VolumeROC, VolumeUnderlay, Vortex, VSTOP, 'VWAP', 'VWMA', 'WeightedClose', 'Weighted Moving Average', Williams %R, WilliamsAlligator, WilliamsFractal, ZigZag```"),
        disnake.Embed(title="Chart Types and Styles:",description="```py\nAccepted Styles:``` ```py\nArea, Renko, Kagi, PF, Linebreak, Heikinashi, Hollow, Baseline, HiLo, Column, Logarithmic, Extended, Wide, Marketprofile``` ```py\nHeatmap arguments:\n Whale, Low, Normal, High```"),]


        await inter.response.edit_message(view=Menus(options,embeds))

    @disnake.ui.button(label="💸 Earnings Commands", style=disnake.ButtonStyle.gray,custom_id="earningsbutton")
    async def earningscommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        switcher = disnake.ui.Button(label="🔙🅱️ 🇦 🇨 🇰", style=disnake.ButtonStyle.red, custom_id="switcherearnings")
        switcher.callback = lambda interaction: interaction.response.edit_message(view=MasterView())
        self.add_item(switcher)
        options=[ 
                disnake.SelectOption(label="Earnings Projection", description="Returns a ticker's earnings projection as well as implied move."),
                disnake.SelectOption(label="Earnings Crush", description="Returns a ticker's projecting earnings crush."),
                disnake.SelectOption(label="Earnings Calendar", description="Returns a ticker's projecting earnings crush."),
                disnake.SelectOption(label="Earnings Today", description="Returns all tickers with earnings for the current day."),
                disnake.SelectOption(label="Earnings Date", description="Select a date and return the earnings scheduled for that date."),

            ]
        
        embeds = [
        disnake.Embed(title="💸 Earnings Commands",description="```py\nYou can use these commands for earnings-specific data.```", color=disnake.Colour.dark_blue(), url="https://www.fudstop.io"),
        disnake.Embed(title="Earnings Projection", description="```py\nReturns a ticker's earnings projection as well as implied move.```\n</earnings projection:1036711345401372733>"),
        disnake.Embed(title="Earnings Crush", description="```py\nReturns a ticker's projecting earnings crush. It will display a % of IV expected to be lost AFTER EARNINGS. A high number indicates earnings will likely be IV crushed.```\n</earnings crush:1036711345401372733>"),
        disnake.Embed(title="Earnings Calendar", description="```py\nReturns a booklet that has upcoming earnings organized by premarket and after hours. Command Provided by Quant Data```\n</earnings calendar:911140318118838277>"),
        disnake.Embed(title="Earnings Today", description="```py\nReturns the earnings scheduled for the current day.```\n</earnings today:911140318118838277>"),
        disnake.Embed(title="Earnings Date", description="```py\nReturns a ticker's earnings projection as well as implied move.```\n</earnings date:911140318118838277>"),
        disnake.Embed(title="Earnings Day of Week", description="```py\nReturns the tickers scheduled for a specific day of the week.```\n</earnings day-of-week:911140318118838277>"),]


        await inter.response.edit_message(view = Menus(options,embeds))


    @disnake.ui.button(label="🫧 Streaming Commands", style=disnake.ButtonStyle.gray,row=1,custom_id="streambutton")
    async def streamingcommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 
                disnake.SelectOption(label="🫧Time and Sales", description="Stream time and sales in real time."),
                disnake.SelectOption(label="🫧Quote", description="Stream a stock quote live."),
                disnake.SelectOption(label="🫧Crypto", description="Stream crypto live."),
                disnake.SelectOption(label="🫧Double Crypto", description="Stream two cryptos live - simultaneously."),
                disnake.SelectOption(label="🫧Double Quote", description="Stream two stocks live - simultaneously."),
                disnake.SelectOption(label="🫧Tits", description="Stream some tits."),

            ]
        
        embeds=[
        disnake.Embed(title="🫧 Streaming Commands",description="```py\nThese commands return live data for a period of time when called.```", color=disnake.Colour.fuchsia(), url="https://www.fudstop.io"),
        disnake.Embed(title="Quote", description="```py\nStream TWO stock tickers live.```\n</stream quote:1036711345401372738>"),
        disnake.Embed(title="Crypto", description="```py\nStream a crypto currency live.```\n</stream crypto:1036711345401372738>"),
        disnake.Embed(title="Time and Sales", description="```py\nStream time and sales for a ticker in real time.```\n</stream time_and_sales:1036711345401372738>"),
        disnake.Embed(title="Double Crypto", description="```py\nStream TWO crypto currencies live.```\n</stream double_crypto:1036711345401372738>"),
        disnake.Embed(title="Double Crypto", description="```py\nStream TWO stock tickers live.```\n</stream double_quote:1036711345401372738>"),
        disnake.Embed(title="Tits", description="```py\nYup - stream tits.```\n</stream tits:1036711345401372738>"),]

        
        

        await inter.response.edit_message(view=Menus(options, embeds))

    @disnake.ui.button(label="🎱 Dark Pool Commands", style=disnake.ButtonStyle.gray,row=1,custom_id="dpoolbutton")
    async def darkpoolcommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 
                disnake.SelectOption(label="🎱All DP",value=1, description="Returns the last 15 dark pools."),
                disnake.SelectOption(label="🎱Allprints",value=2, description="Last 15 combo of dark pools and blocks."),
                disnake.SelectOption(label="🎱Topsum",value=3, description="Top total block and dark pool data."),
                disnake.SelectOption(label="🎱All Blocks",value=4, description="Last 15 block trades."),
                disnake.SelectOption(label="🎱Big Prints",value=5, description="Input a date to look for the largest block trades for that date."),
                disnake.SelectOption(label="🎱Levels",value=6, description="Biggest levels for all prints over the last X days."),
                disnake.SelectOption(label="🎱Sectors",value=7, description="Summary of all prints by % market cap by sector."),

            ]
        
        embeds = [
        disnake.Embed(title="🎱 Dark Pool Commands",description="```py\nCommands for dark-pool data.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
        disnake.Embed(title="All DP", description="```py\nThis command calls the latest 15 dark pools.```\n</dp alldp:1004263746170011748>"),
        disnake.Embed(title="Allprints", description="```py\nTop total block and dark pool data.```\n</dp topsum:1004263746170011748>"),
        disnake.Embed(title="Topsum", description="```py\nLast 15 block trades.```\n</dp allblocks:1004263746170011748>"),
        disnake.Embed(title="All Blocks", description="```py\nInput a date to look for the largest block trades for that date.```\n</dp bigprints:1004263746170011748>"),
        disnake.Embed(title="Big Prints", description="```py\nLast 15 combo of dark pools and blocks.```\n</dp allprints:1004263746170011748>"),
        disnake.Embed(title="Levels", description="```py\nBiggest levels for all prints over the last X days.```\n</dp levels:1004263746170011748>"),
        disnake.Embed(title="Sectors", description="```py\nSummary of all prints by % market cap by sector.```\n</dp sectors:1004263746170011748>"),]

        await inter.response.edit_message(view=Menus(options, embeds))



    @disnake.ui.button(label="🔎 Analysis Commands", style=disnake.ButtonStyle.gray, row=2,custom_id="analysisbutton")
    async def analysiscommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 
                disnake.SelectOption(label="🔎TopShorts", description="Returns tickers with over 30% short interest."),
                disnake.SelectOption(label="🔎Gaps_Down", description="Enter a % and it returns tickers that have gapped down."),
                disnake.SelectOption(label="🔎Gaps_Up", description="Enter a % and it returns tickers that have gapped up."),
                disnake.SelectOption(label="🔎Finscreen", description="Use the finscreener with several customizable options."),
                disnake.SelectOption(label="🔎Overbought_Gap", description="Returns tickers that have gapped up and are overbought in a downward channel."),
                disnake.SelectOption(label="🔎Rating", description="Returns the buy vs hold vs sell ratings for a ticker."),
  
            ]
        
        embeds = [
        disnake.Embed(title="🔎 Analysis Commands",description="```py\nCommands used for stock and options analysis as well as general market analysis.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
        disnake.Embed(title="Top Shorts", description="```py\nReturns tickers with over 30% short interest.``` </analysis topshorts:1036711345401372740>"),
        disnake.Embed(title="Top Shorts", description="```py\nEnter a % and it returns tickers that have gapped down.``` </analysis gaps_down:1036711345401372740>"),
        disnake.Embed(title="Top Shorts", description="```py\nEnter a % and it returns tickers that have gapped up.``` </analysis gaps_up:1036711345401372740>"),
        disnake.Embed(title="Top Shorts", description="```py\nUse the finscreener with several customizable options.``` </analysis finscreen:1036711345401372740>"),
        disnake.Embed(title="Top Shorts", description="```py\nReturns tickers that have gapped up and are overbought in a downward channel.``` </analysis overbought_gap:1036711345401372740>"),
        disnake.Embed(title="Top Shorts", description="```py\nReturns the buy vs hold vs sell ratings for a ticker.``` </analysis rating:1036711345401372740>"),]


        await inter.response.edit_message(view=Menus(options,embeds))





    @disnake.ui.button(label="🩸 Jasmy Commands", style=disnake.ButtonStyle.gray,row=2,custom_id="jasmybutton")
    async def jasmycommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 
                disnake.SelectOption(label="🩸Holders", description="Returns the current number of Jasmy Wallets."),
                disnake.SelectOption(label="🩸Price", description="Streams the current Jasmy price across 20 exchanges."),
                disnake.SelectOption(label="🩸", description=""),

            ]
        
        embeds = [
        disnake.Embed(title="🩸 Jasmy Commands",description="```py\nCommands for the beloved Jasmycoin.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
        disnake.Embed(title="Holders", description="```py\nReturns the current number of Jasmy Wallets.```\n</jasmy holders:1036711345401372735>"),
        disnake.Embed(title="Price", description="```py\nStreams the current Jasmy price across 20 exchanges.```\n</jasmy price:1036711345401372735>"),]


        await inter.response.edit_message(view=Menus(embeds,options))


    @disnake.ui.button(label="🐂 Webull Commands", style=disnake.ButtonStyle.gray,row=2,custom_id="webullbutton")
    async def webullcommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 
                disnake.SelectOption(label="🐂Cost", description="Returns the cost distribution profited shares proportion straight from Webull."),
                disnake.SelectOption(label="🐂Webull_Quote", description="Pulls webull data to discord and gives pricing data and information."),
                disnake.SelectOption(label="🐂Analysis_Tools", description="Learn about Webull's analysis tools."),
                disnake.SelectOption(label="🐂Bid_Ask_Spread", description="Returns educational material regarding the bid ask spread."),
                disnake.SelectOption(label="🐂News", description="Search for news articles from within Webull's news database."),
                disnake.SelectOption(label="🐂Graphics", description="Search by keyword for a list of helpful graphics."),
                disnake.SelectOption(label="🐂Options_Chain", description="Learn how to read and customize your options chain in Webull."),

            ]
        
        embeds= [
        disnake.Embed(title="🐂 Webull Commands",description="```py\nCommands specifically from Webull's API.```", color=disnake.Colour.dark_gold(), url="https://www.fudstop.io"),
        disnake.Embed(title="Cost", description="```py\nReturns the cost distribution profited shares proportion straight from Webull.```\n</webull cost:1036711345401372739>"),
        disnake.Embed(title="Webull_Quote", description="```py\nPulls webull data to discord and gives pricing data and information.```\n</webull webull_quote:1036711345401372739>"),
        disnake.Embed(title="Analysis Tools", description="```py\nLearn about Webull Analysis tools.```\n</webull analysis_tools:1036711345401372739>"),
        disnake.Embed(title="Bid_ask_Spread", description="```py\nReturns educational material regarding the bid ask spread.```\n</webull bid_ask_spread:1036711345401372739>"),
        disnake.Embed(title="News", description="```py\nSearch for news articles from within Webull's news database.```\n</webull news:1036711345401372739>"),
        disnake.Embed(title="Graphics", description="```py\nSearch by keyword for a list of helpful graphics.```\n</webull graphics:1036711345401372739>"),
        disnake.Embed(title="News", description="```py\nLearn how to read and customize your options chain in Webull.```\n</webull options_chain:1036711345401372739>"),]


        await inter.response.edit_message(view = Menus(embeds,options))


    @disnake.ui.button(label="🪙 Economy Commands", style=disnake.ButtonStyle.gray,row=2, custom_id="econbutton")
    async def economycommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        select10 = disnake.ui.Select(
            placeholder="🇴 🇵 🇹 🇮 🇴 🇳 🇸 🪙 🇨 🇴 🇲 🇲 🇦 🇳 🇩 🇸",
            min_values=1,
            max_values=1,
            custom_id="econcmds",
            options=[ 
                disnake.SelectOption(label="🪙Jobless Claims", description="Returns latest and historic Jobless Numbers."),
                disnake.SelectOption(label="🪙Inflation", description="Returns latest and historic inflation numbers with averages"),
                disnake.SelectOption(label="🪙AMBS", description="Returns the latest roll, swap, new, or all agency mortgage backed securities."),
                disnake.SelectOption(label="🪙Retail_Repo", description="Returns the amount of retail capital in money market funds."),
                disnake.SelectOption(label="🪙Data", description="Returns a large list of economic data."),
                disnake.SelectOption(label="🪙House_Trades", description="Returns a list of the latest trades from the House."),
                disnake.SelectOption(label="🪙econ revrepo", description="Returns the latest and historic Reverse Repo Data with differences."),
                disnake.SelectOption(label="🪙econ calendar", description="Displays a calendar of important economic events."),
                disnake.SelectOption(label="🪙econ glbonds", description="Displays global bond data."),
                disnake.SelectOption(label="🪙econ usbonds", description="Displays US bond data."),
                disnake.SelectOption(label="🪙econ yieldcurve", description="Displays US Bond yield curve data."),
                disnake.SelectOption(label="🪙econ indices", description="Displays US indices overview."),
                disnake.SelectOption(label="🪙econ currencies", description="Displays global currency data."),
                disnake.SelectOption(label="🪙econ fedrates", description="Displays upcoming FOMC events and projected BPS hike percentage."),
    
            ]
        )
        em = disnake.Embed(title="🪙 Economy Commands",description="```py\nImportant economic data such as inflation, jobless claims, repo, and more.```", color=disnake.Colour.yellow(), url="https://www.fudstop.io")
        disnake.Embed(title="Jobless_Claims", description="```py\nReturns latest and historic Jobless Numbers.```\n</economy jobless_claims:1036711345401372742>")
        disnake.Embed(title="Inflation", description="```py\nReturns inflation numbers with averaged and historic data.```\n</economy inflation:1036711345401372742>")
        disnake.Embed(title="AMBS", description="```py\nReturns amount of retail capital in money market funds.```\n</economy retail_repo:1036711345401372742>")
        disnake.Embed(title="Retail_Repo", description="```py\nReturns the latest roll, swap, new, or all agency mortgage backed securities.```\n</economy ambs:1036711345401372742>")
        disnake.Embed(title="Data", description="```py\nReturns a large list of economic data.```\n</economy data:1036711345401372742>")
        disnake.Embed(title="House_trades", description="```py\nReturns a list of the latest trades from the House.```\n</economy house_trades:1036711345401372742>")
        disnake.Embed(title="econ RevRepo", description="```py\nReturns the latest and historic Reverse Repo Data with differences.```\n</econ revrepo:1004263746111275130>")
        disnake.Embed(title="econ Calendar", description="```py\nDisplays a calendar of important economic events.```\n</econ calendar:1004263746111275130>")
        disnake.Embed(title="econ GlBonds", description="```py\nDisplays global bond data.```\n</econ glbonds:1004263746111275130>")
        disnake.Embed(title="econ USBonds", description="```py\nDisplays US bond data.```\n</econ usbonds:1004263746111275130>")
        disnake.Embed(title="econ YieldCurve", description="```py\nDisplays US Bond yield curve data.```\n</econ yieldcurve:1004263746111275130>")
        disnake.Embed(title="econ indices", description="```py\nDisplays US indices overview.```\n</econ indices:1004263746111275130>")
        disnake.Embed(title="econ currencies", description="```py\nDisplays global currency data.```\n</econ currencies:1004263746111275130>")
        disnake.Embed(title="econ fedrates", description="```py\nDisplays upcoming FOMC events and projected BPS hike percentage.```\n</econ fedrates:1004263746111275130>")

        try:
            self.add_item(select10)
        except ValueError:
            self.clear_items()
            self.add_item(select10)



        
        select10.callback = lambda interaction: interaction.response.edit_message(view=MasterCommand())



    @disnake.ui.button(label="🧠 Learning Commands", style=disnake.ButtonStyle.gray,row=1,custom_id="learnbutton")
    async def learncommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 

                disnake.SelectOption(label="🧠Option_Strategies", description="Learn about different options strategies."),
                disnake.SelectOption(label="🧠Calls", description="Learn about call options."),
                disnake.SelectOption(label="🧠Puts", description="Learn about put options."),
                disnake.SelectOption(label="🧠Candle_patterns", description="Learn about different candlestick patterns."),
                disnake.SelectOption(label="🧠China", description=""),
                disnake.SelectOption(label="🧠Core Logic", description="Learn about the core logic and how it works."),
                disnake.SelectOption(label="🧠Covered_Calls", description="Learn about selling calls to generate revenue."),
                disnake.SelectOption(label="🧠SEC", description="Learn about different SEC filings."),
                disnake.SelectOption(label="🧠ETFs", description="Learn about Exchange Traded Funds."),
                disnake.SelectOption(label="🧠Greeks", description="Learn about the greeks: delta, gamma, rho, vega, and theta."),
                disnake.SelectOption(label="🧠Order_types", description="Learn about the different order types."),
                disnake.SelectOption(label="🧠Options_101", description="Take the Options 101 course from the Options Industry Council."),
                disnake.SelectOption(label="🧠OCC", description="Learn about important filings out of the Options Clearing Corporation."),
                disnake.SelectOption(label="🧠FINRA", description="Learn about important FINRA filings."),
                disnake.SelectOption(label="🧠NSFR_Ratio", description="Learn about the critical Net Stable Funding Ratio regarding big banks."),
                disnake.SelectOption(label="🧠webull_school", description="Learn about the Webull App."),

    
            ]
        
        embeds = [
        disnake.Embed(title="🧠 Learning Commands",description="```py\nImportant economic data such as inflation, jobless claims, repo, and more.```", color=disnake.Colour.yellow(), url="https://www.fudstop.io"),
        disnake.Embed(title="Option_Strategies", description="```py\nLearn about different options strategies.```\n</learn option_strategies:1036711345468477510>"),
        disnake.Embed(title="Calls", description="```py\nLearn about call options.```\n</learn calls:1036711345468477510>"),
        disnake.Embed(title="Puts", description="```py\nLearn about put options.```\n</learn puts:1036711345468477510>"),
        disnake.Embed(title="Candle_Patterns", description="```py\nLearn about different candlestick patterns.```\n</learn candle_patterns:1036711345401372742>"),
        disnake.Embed(title="Core_Logic", description="```py\nLearn about the core logic and how it works.```\n</learn core_logic:1036711345401372742>"),
        disnake.Embed(title="China", description="```py\nLearn about China's economic transformation.```\n</learn china:1036711345401372742>"),
        disnake.Embed(title="Covered_Calls", description="```py\nLearn about selling calls to generate revenue.```\n</learn covered_calls:1036711345401372742>"),
        disnake.Embed(title="ETFs", description="```py\nLearn about exchange traded funds.```\n</learn etfs:1036711345401372742>"),
        disnake.Embed(title="Filings", description="```py\nLearn about different SEC filings.```\n</learn filings:1036711345401372742>"),
        disnake.Embed(title="Options 101", description="```py\nTake the Options 101 course from the Options Industry Council.```\n</learn options_101:1036711345401372742>"),
        disnake.Embed(title="Greeks", description="```py\nLearn about the greeks: delta, gamma, rho, vega, and theta.```\n</learn greeks:1036711345401372742>"),
        disnake.Embed(title="Order_types", description="```py\nLearn about the different order types.```\n</learn order_types:1036711345401372742>"),
        disnake.Embed(title="OCC", description="```py\nLearn about important filings out of the Options Clearing Corporation.```\n</learn occ:1036711345401372742>"),
        disnake.Embed(title="FINRA", description="```py\nLearn about important FINRA filings.```\n</learn finra:1036711345401372742>"),
        disnake.Embed(title="NSFR_ratio", description="```py\nLearn about the critical Net Stable Funding Ratio regarding big banks.```\n</learn nsfr_ratio:1036711345401372742>"),
        disnake.Embed(title="Webull_School", description="```py\nLearn about the Webull App.```\n</learn webull_school:1036711345401372742>"),]






        await inter.response.edit_message(view = Menus(embeds,options))





    @disnake.ui.button(label="🕵️ Due Dilligence", style=disnake.ButtonStyle.gray,row=1,custom_id="ddbutton")
    async def ddcommands(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        options=[ 

                disnake.SelectOption(label="🕵️AH", description="Displays After Hours Data for a ticker."),
                disnake.SelectOption(label="🕵️Analyst", description="Displays Analyst recommendations."),
                disnake.SelectOption(label="🕵️Bio", description="Displays a stock company's profile."),
                disnake.SelectOption(label="🕵️Customer", description="Displays customers of a company."),
                disnake.SelectOption(label="🕵️ermove", description="Displays implied move for a ticker based on option prices."),
                disnake.SelectOption(label="🕵️divinfo", description="Displays dividend information for a ticker."),
                disnake.SelectOption(label="🕵️earnings", description="Pick a date and return the earnings scheduled for that day."),
                disnake.SelectOption(label="🕵️PM", description="Display premarket data for a stock."),
                disnake.SelectOption(label="🕵️pt", description="Displays a chart with price targets"),
                disnake.SelectOption(label="🕵️ytd", description="Displays period performance for a stock."),
                disnake.SelectOption(label="🕵️sec", description="Dispalys latest SEC filings for a company."),
                disnake.SelectOption(label="🕵️est", description="Dispalys earnings estimates."),


    
            ]
        
        embeds = [
        disnake.Embed(title="🕵️ Due Diligence Commands",description="```py\nThese commands are somewhat useful. I don't really ever use these much, but depending on your trading strategy or type of trading personality - these could be a good fit for you. I'd at least give them a shot.```", color=disnake.Colour.dark_magenta(), url="https://www.fudstop.io"),

        disnake.Embed(title="AH", description="```py\nDisplays After Hours Data for a ticker.```\n</dd ah:1004263746090324066>"),
        disnake.Embed(title="Analyst", description="```py\nReturns analyst ratings for a ticker.```\n</dd analyst:1004263746090324066>"),
        disnake.Embed(title="Bio", description="```py\nReturns the stock company's profile.```\n</dd bio:1004263746090324066>"),
        disnake.Embed(title="Customer", description="```py\nDisplays customers of a company.```\n</dd customer:1004263746090324066>"),
        disnake.Embed(title="ermove", description="```py\nDisplays implied move for a ticker based on option prices.```\n</dd ermove:1004263746090324066>"),
        disnake.Embed(title="divinfo", description="```py\nDisplays dividend information for a ticker.```\n</dd divinfo:1004263746090324066>"),
        disnake.Embed(title="earnings", description="```py\nPick a date and return the earnings scheduled for that day.```\n</dd earnings:1004263746090324066>"),
        disnake.Embed(title="pm", description="```py\nDisplay premarket data for a stock.```\n</dd pm:1004263746090324066>"),
        disnake.Embed(title="pt", description="```py\nDisplays a chart with price targets```\n</dd pt:1004263746090324066>"),
        disnake.Embed(title="ytd", description="```py\nDisplays period performance for a stock.```\n</dd ytd:1004263746090324066>"),
        disnake.Embed(title="sec", description="```py\nDisplays recent SEC filings.```\n</dd sec:1004263746090324066>"),
        disnake.Embed(title="est", description="```py\nDisplays earnings estimates.```\n</dd est:1004263746090324066>"),]

        





        await inter.response.edit_message(view=Menus(embeds,options))


class MasterPersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            # Register the persistent view for listening here.
            # Note that this does not send the view to any message.
            # In order to do this you need to first send a message with the View, which is shown below.
            # If you have the message_id you can also pass it as a keyword argument, but for this example
            # we don't have one.
            self.add_view(MasterCommand())
            self.add_view(MasterView())
            self.add_view(PersistentView())
            self.persistent_views_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")




me = MasterPersistentViewBot()

@me.command()
@commands.is_owner()
async def prepare(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("```py\nSelect a category and the channels will print out for you!```", view=PersistentView())

@me.slash_command()
async def cmds(inter:disnake.AppCmdInter):
    await inter.send(view=MasterPersistentViewBot())

@me.command()
@commands.is_owner()
async def preparecommands(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send(view=MasterCommand())
#me.run("MTAxNjAwNjI5MzU5ODc2OTIwMg.GztNZZ.5GnsEeZixqJZ2RuzooA_FdnyAVoB3xaNmVnEhs")



import disnake
import _discord.emojis as e


class CommandsStart(disnake.ui.View):
    def __init__(self):
        
        super().__init__(timeout=None)

        self.add_item(BotCmdMenu())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button1",row=0,disabled=True)#data
    async def command1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter, message=disnake.Message):
        await inter.response.edit_message(view=self)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.webullcmd}", custom_id="command1button2",row=0,disabled=False)#webull
    async def command1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):



        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)
        


    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.clockspin}", custom_id="command1button3",row=0,disabled=False)#stream
    async def command1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.optioncmd}", custom_id="command1button4",row=0,disabled=False)#options
    async def command1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.toprightarrow}", custom_id="command1button5",row=0,disabled=False)#data
    async def command1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.portal}", custom_id="command1button6",row=1,disabled=False)#dp commands
    async def command1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button7",row=1,disabled=True)
    async def command1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.pinkrocket}", custom_id="command1button8", disabled=False,row=1)#stockcmds
    async def command1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button9",row=1,disabled=True)
    async def command1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.learncmd}", custom_id="command1button10",row=1,disabled=False)
    async def command1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.glowstick}", custom_id="command1button16",row=3,disabled=False)#chart
    async def command1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button17",row=3,disabled=True)
    async def command1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.eye}", custom_id="command1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button19",row=3,disabled=True)#data
    async def command1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.flowcmd}", custom_id="command1button20",row=3,disabled=False)#magicwand
    async def command1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button21",row=4,disabled=True)#data
    async def command1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.earnings}", custom_id="command1button22",row=4,disabled=False)#pins
    async def command1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.economy}", custom_id="command1button23",row=4,disabled=False)#alert
    async def command1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.question}", custom_id="command1button24",row=4,disabled=True)#sectorrotation
    async def command1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="command1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


class WebullCmdDrop(disnake.ui.Select):
    def __init__(self):

        options = [ 
        disnake.SelectOption(label="/webull Cost",value=1, description="Displays average cost and proportioned shares profiting.",emoji="<a:_:1042676749357555794>"),
        disnake.SelectOption(label="/Webull Quote",value=2, description="Pulls a real-time quote from Webull.",emoji="<a:_:1042676749357555794>"),
        disnake.SelectOption(label="/webull Bid_ask_Spread",value=3, description="Learn about the bid/ask spread.",emoji="<a:_:1042676749357555794>"),
        disnake.SelectOption(label="/webull News",value=4,description="Search for Webull news!",emoji="<a:_:1042676749357555794>"),
        disnake.SelectOption(label="/webull Graphics",value=5, description="Choose from several helpful webull graphics.",emoji="<a:_:1042676749357555794>")]

        super().__init__(
            placeholder = "🇼 🇪 🇧 🇺 🇱 🇱  🇨 🇲 🇩 🇸",
            min_values=1,
            max_values=1,
            custom_id="webullcmd",
            options = options)

    
    async def callback(self, interaction: disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            await interaction.send("</webull cost:1042947625663610936>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</webull webull_quote:1042947625663610936>", ephemeral=False)
        elif self.values[0] == "3":
            await interaction.send("</webull bid_ask_spread:1042947625663610936>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</webull news:1042947625663610936>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</webull graphics:1042947625663610936>", ephemeral=False)



        


class WebullCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(WebullCmdDrop())
        self.embed = disnake.Embed(title=f"{e.webullcmd} /Webull Commands {e.webullcmd}", description="```py\nThese are high-quality commands coming straight from Webull's API. Enjoy CBOE Hanweck data - including real-time quotes, real-time crypto, cost anylsis, time and sales, order-flow ,leverage - and more.```", color=disnake.Colour.dark_magenta())
        self.embed.add_field(name="/webull<a:_:1042676749357555794>Cost", value="```py\nReturns the cost distribution profited shares proportion straight from Webull.```\n</webull cost:1042947625663610936>")
        self.embed.add_field(name="/webull<a:_:1042676749357555794>Webull_Quote", value="```py\nPulls webull data to discord and gives pricing data and information.```\n</webull webull_quote:1042947625663610936>")
        self.embed.add_field(name="/webull<a:_:1042676749357555794>Analysis_Tools", value="```py\nLearn about Webull Analysis tools.```\n</webull analysis_tools:1042947625663610936>")
        self.embed.add_field(name="/webull<a:_:1042676749357555794>Bid_ask_Spread", value="```py\nReturns educational material regarding the bid ask spread.```\n</webull bid_ask_spread:1042947625663610936>")
        self.embed.add_field(name="/webull<a:_:1042676749357555794>News", value="```py\nSearch for news articles from within Webull's news database.```\n</webull news:1042947625663610936>")
        self.embed.add_field(name="/webull<a:_:1042676749357555794>Graphics", value="```py\nSearch by keyword for a list of helpful graphics.```\n</webull graphics:1042947625663610936>")


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button1",row=0,disabled=False)
    async def webull1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.webullcmd}", custom_id="webull1button2",row=0,disabled=True)#webull
    async def webull1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="webull1button3",row=0,disabled=False)#stream
    async def webull1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="webull1button4",row=0,disabled=False)#options
    async def webull1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="webull1button5",row=0,disabled=False)#data
    async def webull1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="webull1button6",row=1,disabled=False)#dp commands
    async def webull1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button7",row=1,disabled=True)
    async def webull1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="webull1button8", disabled=False,row=1)#stockcmds
    async def webull1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button9",row=1,disabled=True)
    async def webull1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="webull1button10",row=1,disabled=False)
    async def webull1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="webull1button16",row=3,disabled=False)#chart
    async def webull1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button17",row=3,disabled=True)
    async def webull1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="webull1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button19",row=3,disabled=True)#data
    async def webull1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="webull1button20",row=3,disabled=False)#magicwand
    async def webull1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button21",row=4,disabled=True)#data>
    async def webull1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="webull1button22",row=4,disabled=False)#pins
    async def webull1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="webull1button23",row=4,disabled=False)#alert
    async def webull1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="webull1button24",row=4,disabled=True)#sectorrotation
    async def webull1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="webull1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

class DDCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"🇩 🇩 {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="dddropcmd",
            options =  [ 
            disnake.SelectOption(label="/dd AH",value=1, description="Displays After Hours Data for a ticker.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd Analyst", value=2,description="Returns analyst ratings for a ticker.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd Bio",value=3, description="Returns the stock company's profile.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd Customer",value=4, description="Displays customers of a company.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd ermove",value=5, description="Displays implied move for a ticker based on option prices.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd divinfo",value=6, description="Displays dividend information for a ticker.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd earnings",value=7, description="Pick a date and return the earnings scheduled for that day.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd pm",value=8, description="Display premarket data for a stock.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd pt",value=9, description="Displays a chart with price targets",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd ytd",value=10, description="Displays period performance for a stock.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd sec",value=11, description="Displays recent SEC filings.",emoji=f"{emojis.eye}"),
            disnake.SelectOption(label="/dd est",value=12, description="Displays earnings estimates.",emoji=f"{emojis.eye}"),])

    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</dd analyst:1004263746090324066>", ephemeral=False)
        if self.values[0] == "2":
            await interaction.send("</dd analyst:1004263746090324066>", ephemeral=False)

        if self.values[0] == "3":
            await interaction.send("</dd bio:1004263746090324066>", ephemeral=False)
        if self.values[0] == "4":
            await interaction.send("</dd customer:1004263746090324066>", ephemeral=False)
        if self.values[0] == "5":
            await interaction.send("</dd ermove:1004263746090324066>", ephemeral=False)

        if self.values[0] == "6":
            await interaction.send("</dd divinfo:1004263746090324066>", ephemeral=False)
        if self.values[0] == "7":
            await interaction.send("</dd earnings:1004263746090324066>", ephemeral=False)
        if self.values[0] == "8":
            await interaction.send("</dd pm:1004263746090324066>", ephemeral=False)

        if self.values[0] == "9":
            await interaction.send("</dd pt:1004263746090324066>", ephemeral=False)
        if self.values[0] == "10":
            await interaction.send("</dd ytd:1004263746090324066>", ephemeral=False)
        if self.values[0] == "11":
            await interaction.send("</dd sec:1004263746090324066>", ephemeral=False)

        if self.values[0] == "12":
            await interaction.send("</dd est:1004263746090324066>", ephemeral=False)





                


class DDCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)



        self.add_item(DDCmdDrop())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button1",row=0,disabled=True)
    async def dd1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="dd1button2",row=0,disabled=False)#webull
    async def dd1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="dd1button3",row=0,disabled=False)#stream
    async def dd1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="dd1button4",row=0,disabled=False)#options
    async def dd1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart())
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="dd1button5",row=0,disabled=False)#data
    async def dd1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="dd1button6",row=1,disabled=False)#dp commands
    async def dd1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button7",row=1,disabled=True)
    async def dd1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="dd1button8", disabled=False,row=1)#stockcmds
    async def dd1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button9",row=1,disabled=True)
    async def dd1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="dd1button10",row=1,disabled=False)
    async def dd1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="dd1button16",row=3,disabled=False)#chart
    async def dd1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button17",row=3,disabled=True)
    async def dd1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.confirmed}", custom_id="dd1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button19",row=3,disabled=True)#data
    async def dd1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="dd1button20",row=3,disabled=False)#magicwand
    async def dd1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button21",row=4,disabled=True)#data
    async def dd1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="dd1button22",row=4,disabled=False)#pins
    async def dd1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="dd1button23",row=4,disabled=False)#alert
    async def dd1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="dd1button24",row=4,disabled=True)#sectorrotation
    async def dd1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dd1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


class OptionCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__( 
            placeholder=f"/option & /op {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="optionscmddrop",
            options = [ 
            disnake.SelectOption(label=f"/op maxpain",value=1, description="Display the max pain price for a ticker and expiry.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op oi", value=2,description="Returns OI for a ticker. Also by expiration. In order by OI.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op oichart",value=3, description="Returns the stock company's profile.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op itm",value=4, description="View ITM vs OTM contracts for a ticker.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op smile",value=5, description="View volatility skew for a ticker.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op topoichange",value=6, description="View the overall largest change in Open Interest.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op gamma",value=7, description="Displays options' gamma levels for a ticker.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op unu",value=8, description="Display unusual options activity.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/op vsurf",value=9, description="Displays the volatility surface for an option contract.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options highest_stats",value=10, description="Displays contracts with the highest stats and money flow.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options top",value=11, description="Displays highest OI increase, highest OI decrease, top volume, OI, IV, and turnover.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options ivparkinson",value=12, description="View historic parkinson IV for a ticker.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options ivrank",value=13, description="Displays IV rank for a ticker.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options ivpercentile",value=14, description="Returns the % of measurements that have been lower than current IV.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options unusual",value=15, description="Displays tickers with the most Unusual Options Count",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options topequity",value=16, description="Ranks equities in order of call/put trades and flow.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options topetf",value=17, description="Ranks ETFs in order of call/put trades and flow.",emoji=f"{emojis.optioncmd}"),
            disnake.SelectOption(label=f"/options topindex",value=18, description="Ranks indexes in order of call/put trades and flow.",emoji=f"{emojis.optioncmd}"),]
            
        )

    async def callback(self, interaction: disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            await interaction.send("</op maxpain:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</op oi:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "3":
            await interaction.send("</op oichart:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</op itm:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</op smile:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "6":
            await interaction.send("</op topoichange:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "7":
            await interaction.send("</op gamma:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "8":
            await interaction.send("</op unu:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "9":
            await interaction.send("</op vsurf:1004263746111275138>", ephemeral=False)
        elif self.values[0] == "10":
            await interaction.send("</options highest_stats:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "11":
            await interaction.send("</options top:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "12":
            await interaction.send("</options ivparkinson:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "13":
            await interaction.send("</options ivrank:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "14":
            await interaction.send("</options ivpercentile:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "15":
            await interaction.send("</options unusual:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "16":
            await interaction.send("</options topequity:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "17":
            await interaction.send("</options topetf:1042947625944625164>", ephemeral=False)
        elif self.values[0] == "18":
            await interaction.send("</options topindex:1042947625944625164>", ephemeral=False)
class OptionCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)



        self.add_item(OptionCmdDrop())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button1",row=0,disabled=False)
    async def op1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="op1button2",row=0,disabled=False)#webull
    async def op1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="op1button3",row=0,disabled=False)#stream
    async def op1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.lightboltneon}", custom_id="op1button4",row=0,disabled=True)#options
    async def op1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="op1button5",row=0,disabled=False)#data
    async def op1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="op1button6",row=1,disabled=False)#dp commands
    async def op1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button7",row=1,disabled=True)
    async def op1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="op1button8", disabled=False,row=1)#stockcmds
    async def op1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button9",row=1,disabled=True)
    async def op1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="op1button10",row=1,disabled=False)
    async def op1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="op1button16",row=3,disabled=False)#chart
    async def op1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button17",row=3,disabled=True)
    async def op1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="op1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button19",row=3,disabled=True)#data
    async def op1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="op1button20",row=3,disabled=False)#magicwand
    async def op1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button21",row=4,disabled=True)#data
    async def op1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="op1button22",row=4,disabled=False)#pins
    async def op1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="op1button23",row=4,disabled=False)#alert
    async def op1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="op1button24",row=4,disabled=True)#sectorrotation
    async def op1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="op1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


class LearnCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"/Learn {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="dddropcmd",
            options =  [ 
            disnake.SelectOption(label="Option_Strategies",value=1),
            disnake.SelectOption(label="Calls",value=2,description="Learn about call options.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Puts",value=3,description="Learn about put options.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Candle_Patterns",value=4,description="Learn about different candlestick patterns.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Core_Logic",value=5,description="Learn about the core logic and how it works.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="China",value=6,description="Learn about China's economic transformation.``'", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Covered_Calls",value=7,description="Learn about selling calls to generate revenue.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="ETFs",value=8,description="Learn about exchange traded funds.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Filings",value=9,description="Learn about different SEC filings.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Options 101",value=10,description="Take the Options 101 course from the Options Industry Council.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Greeks",value=11,description="Learn about the greeks: delta, gamma, rho, vega, and theta.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="Order_types",value=12,description="Learn about the different order types.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="OCC",value=13,description="Learn about important filings out of the Options Clearing Corporation.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="FINRA",value=14,description="Learn about important FINRA filings.", emoji="<a:_:1043015881631993856>"),
            disnake.SelectOption(label="NSFR_ratio",value=15,description="Learn about the critical Net Stable Funding Ratio regarding big banks.", emoji="<a:_:1043015881631993856>"),])

    async def callback(self, interaction:disnake.MessageCommandInteraction):
        selv = "".join(self.values[0])
        if self.values[0] == "1":
            
            await interaction.send("</learn option_strategies:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</learn calls:1045554249469284362>", ephemeral=False)

        elif self.values[0] == "3":
            await interaction.send("</learn puts:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</learn candle_patterns:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</learn core_logic:1045554249469284362>", ephemeral=False)

        elif self.values[0] == "6":
            await interaction.send("</learn china:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "7":
            await interaction.send("</learn etfs:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "8":
            await interaction.send("</learn filings:1045554249469284362>", ephemeral=False)

        elif self.values[0] == "9":
            await interaction.send("</learn options_101:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "10":
            await interaction.send("</learn greeks:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "11":
            await interaction.send("</learn order_types:1045554249469284362>", ephemeral=False)

        elif self.values[0] == "12":
            await interaction.send("</learn occ:1045554249469284362>", ephemeral=False)


        elif self.values[0] == "10":
            await interaction.send("</learn finra:1045554249469284362>", ephemeral=False)
        elif self.values[0] == "11":
            await interaction.send("</learn nsfr_ratio:1045554249469284362>", ephemeral=False)

class LearnCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(LearnCmdDrop())



    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button1",row=0,disabled=False)
    async def learn1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="learn1button2",row=0,disabled=False)#webull
    async def learn1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="learn1button3",row=0,disabled=False)#stream
    async def learn1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="learn1button4",row=0,disabled=False)#options
    async def learn1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="learn1button5",row=0,disabled=False)#data
    async def learn1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="learn1button6",row=1,disabled=False)#dp commands
    async def learn1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button7",row=1,disabled=True)
    async def learn1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="learn1button8", disabled=False,row=1)#stockcmds
    async def learn1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button9",row=1,disabled=True)
    async def learn1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.learncmd}", custom_id="learn1button10",row=1,disabled=True)
    async def learn1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="learn1button16",row=3,disabled=False)#chart
    async def learn1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button17",row=3,disabled=True)
    async def learn1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="learn1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button19",row=3,disabled=True)#data
    async def learn1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="learn1button20",row=3,disabled=False)#magicwand
    async def learn1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button21",row=4,disabled=True)#data
    async def learn1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="learn1button22",row=4,disabled=False)#pins
    async def learn1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="learn1button23",row=4,disabled=False)#alert
    async def learn1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="learn1button24",row=4,disabled=True)#sectorrotation
    async def learn1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embeds=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="learn1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)



class FlowCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"/flow {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="flowcmddrop",
            options =  [ 

            disnake.SelectOption(label="/flow Bigflow",value=1,description="Returns the top 20 flow tickers by premium.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Day",value=2,description="Returns the most recent flow for a stock.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Flow",value=3, description="Searches Quant Data's flow database and returns the results.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Opening",value=4, description="Top 20 flow tickers with opening condition met.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Prem",value=5, description="Returns a chart with sum of premium per day by calls/puts.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Sectors",value=6, description="Summary by % market cap by Sector.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Sumday",value=7, description="Returns flow summary by expiration date for a ticker.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Sumexp",value=8, description="Searches Quant Data's flow database and returns the results.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Summary",value=9, description="Summary of all flow by % market cap.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Sumtop",value=10, description="Top flow for the day for a stock calls vs puts.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Sumweek",value=11, description="Graph total premium weekly summary for a stock.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Unu",value=12, description="Returns unusual options trade with over 100k Premium.",emoji="<a:_:1043016503710208030>"),
            disnake.SelectOption(label="/flow Weekly",value=13, description="Top 20 flow by premium for weekly expiring stocks.",emoji="<a:_:1043016503710208030>"),])

    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</flow bigflow:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</flow day:1004263746170011749>", ephemeral=False)

        elif self.values[0] == "3":
            await interaction.send("</flow:910724015490998293>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</flow opening:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</flow prem:1004263746170011749>", ephemeral=False)

        elif self.values[0] == "6":
            await interaction.send("</flow sectors:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "7":
            await interaction.send("</flow sumday:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "8":
            await interaction.send("</flow sumexp:1004263746170011749>", ephemeral=False)

        elif self.values[0] == "9":
            await interaction.send("</flow summary:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "10":
            await interaction.send("</flow sumtop:1004263746170011749>", ephemeral=False)
        elif self.values[0] == "11":
            await interaction.send("</flow sumweek:1004263746170011749>", ephemeral=False)

        elif self.values[0] == "12":
            await interaction.send("</flow unu:1004263746170011749>", ephemeral=False)


        elif self.values[0] == "13":
            await interaction.send("</flow weekly:1004263746170011749>", ephemeral=False)


class FlowCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(FlowCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button1",row=0,disabled=True)
    async def flow1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="flow1button2",row=0,disabled=False)#webull
    async def flow1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="flow1button3",row=0,disabled=False)#stream
    async def flow1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="flow1button4",row=0,disabled=False)#options
    async def flow1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="flow1button5",row=0,disabled=False)#data
    async def flow1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="flow1button6",row=1,disabled=False)#dp commands
    async def flow1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button7",row=1,disabled=True)
    async def flow1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="flow1button8", disabled=False,row=1)#stockcmds
    async def flow1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button9",row=1,disabled=True)
    async def flow1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="flow1button10",row=1,disabled=False)
    async def flow1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="flow1button16",row=3,disabled=False)#chart
    async def flow1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button17",row=3,disabled=True)
    async def flow1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="flow1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button19",row=3,disabled=True)#data
    async def flow1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.flowcmd}", custom_id="flow1button20",row=3,disabled=True)#magicwand
    async def flow1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button21",row=4,disabled=True)#data
    async def flow1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="flow1button22",row=4,disabled=False)#pins
    async def flow1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="flow1button23",row=4,disabled=False)#alert
    async def flow1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="flow1button24",row=4,disabled=True)#sectorrotation
    async def flow1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="flow1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)




class StockCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"Stock {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="stockcmddrop",
            options =  [
                disnake.SelectOption(label="/stock capitalflow",value=1,description="Shows capitalflow for a ticker broken down by player size.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock company_brief",value=2,description="Returns core information for a company - such as location & contact.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock criminals",value=3,description="Returns the latest insider buys/sells from government officials.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock insider_summary",value=4,description="Returns the latest insider summary information for a tciker.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock institutions",value=5,description="Returns the top 10 institutional holders for a ticker.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock ipos",value=6,description="Displays the upcoming IPOs.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock leverage", value=7,description="Returns leverage stats fora  stock.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock liquidity", value=8,description="Displays the liquidity level for a stock. 0 = lowest. 5 = highest.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock orderflow",value=9,description="Shows the current day's orderflow in terms of buy, sell, and neutral.",emoji="<a:_:1043013214180483112>"),
                disnake.SelectOption(label="/stock shortinterest",value=10,description="Displays current and historic short interest for a ticker.",emoji="<a:_:1043013214180483112>"),])

    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</stock capitalflow:1042947625944625166>", ephemeral=False)
        if self.values[0] == "2":
            await interaction.send("</stock company_brief:1042947625944625166>", ephemeral=False)
        if self.values[0] == "3":
            await interaction.send("</stock criminals:1042947625944625166>", ephemeral=False)

        if self.values[0] == "4":
            await interaction.send("</stock insider_summary:1042947625944625166>", ephemeral=False)
        if self.values[0] == "5":
            await interaction.send("</stock institutions:1042947625944625166>", ephemeral=False)
        if self.values[0] == "6":
            await interaction.send("</stock ipos:1042947625944625166>", ephemeral=False)

        if self.values[0] == "7":
            await interaction.send("</stock leverage:1042947625944625166>", ephemeral=False)
        if self.values[0] == "8":
            await interaction.send("</stock liquidity:1042947625944625166>", ephemeral=False)
        if self.values[0] == "9":
            await interaction.send("</stock orderflow:1042947625944625166>", ephemeral=False)

        if self.values[0] == "10":
            await interaction.send("</stock shortinterest:1042947625944625166>", ephemeral=False)




class StockCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(StockCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button1",row=0,disabled=True)
    async def stock1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="stock1button2",row=0,disabled=False)#webull
    async def stock1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="stock1button3",row=0,disabled=False)#stream
    async def stock1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="stock1button4",row=0,disabled=False)#options
    async def stock1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="stock1button5",row=0,disabled=False)#data
    async def stock1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="stock1button6",row=1,disabled=False)#dp commands
    async def stock1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button7",row=1,disabled=True)
    async def stock1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.pinkrocket}", custom_id="stock1button8", disabled=True,row=1)#stockcmds
    async def stock1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button9",row=1,disabled=True)
    async def stock1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="stock1button10",row=1,disabled=False)
    async def stock1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="stock1button16",row=3,disabled=False)#chart
    async def stock1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button17",row=3,disabled=True)
    async def stock1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="stock1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button19",row=3,disabled=True)#data
    async def stock1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="stock1button20",row=3,disabled=False)#magicwand
    async def stock1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button21",row=4,disabled=True)#data
    async def stock1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="stock1button22",row=4,disabled=False)#pins
    async def stock1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="stock1button23",row=4,disabled=False)#alert
    async def stock1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="stock1button24",row=4,disabled=True)#sectorrotation
    async def stock1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stock1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)




class DPSCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"DARK POOL {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="dpsropcmd",
            options =  [
            disnake.SelectOption(label="/dp AllDP",value=1,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp Allprints",value=2,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp Topsum",value=3,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp All Blocks",value=4,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp Big Prints",value=5,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp Levels",value=6,emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/dp Sectors",value=7,emoji="<a:_:1044503531878621195>"),])



    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</dp alldp:1004263746170011748>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</dp allprints:1004263746170011748>", ephemeral=False)

        elif self.values[0] == "3":
            await interaction.send("</dp topsum:1004263746170011748>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</dp allblocks:1004263746170011748>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</dp bigprints:1004263746170011748>", ephemeral=False)

        elif self.values[0] == "6":
            await interaction.send("</dp levels:1004263746170011748>", ephemeral=False)
        elif self.values[0] == "7":
            await interaction.send("</dp sectors:1004263746170011748>", ephemeral=False)



class DPSCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(DPSCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button1",row=0,disabled=True)
    async def dps1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="dps1button2",row=0,disabled=False)#webull
    async def dps1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="dps1button3",row=0,disabled=False)#stream
    async def dps1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="dps1button4",row=0,disabled=False)#options
    async def dps1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=CommandsEmbed())
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="dps1button5",row=0,disabled=False)#data
    async def dps1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.portal}", custom_id="dps1button6",row=1,disabled=True)#dp commands
    async def dps1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button7",row=1,disabled=True)
    async def dps1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="dps1button8", disabled=False,row=1)#stockcmds
    async def dps1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button9",row=1,disabled=True)
    async def dps1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="dps1button10",row=1,disabled=False)
    async def dps1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="dps1button16",row=3,disabled=False)#chart
    async def dps1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button17",row=3,disabled=True)
    async def dps1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="dps1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button19",row=3,disabled=True)#data
    async def dps1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="dps1button20",row=3,disabled=False)#magicwand
    async def dps1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button21",row=4,disabled=True)#data
    async def dps1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="dps1button22",row=4,disabled=False)#pins
    async def dps1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="dps1button23",row=4,disabled=False)#alert
    async def dps1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="dps1button24",row=4,disabled=True)#sectorrotation
    async def dps1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="dps1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

class OtherCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button1",row=0,disabled=True)
    async def other1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="other1button2",row=0,disabled=False)#webull
    async def other1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="other1button3",row=0,disabled=False)#stream
    async def other1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="other1button4",row=0,disabled=False)#options
    async def other1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="other1button5",row=0,disabled=False)#data
    async def other1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="other1button6",row=1,disabled=False)#dp commands
    async def other1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button7",row=1,disabled=True)
    async def other1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="other1button8", disabled=False,row=1)#stockcmds
    async def other1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button9",row=1,disabled=True)
    async def other1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="other1button10",row=1,disabled=False)
    async def other1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="other1button16",row=3,disabled=False)#chart
    async def other1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button17",row=3,disabled=True)
    async def other1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="other1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=None)


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button19",row=3,disabled=True)#data
    async def other1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="other1button20",row=3,disabled=False)#magicwand
    async def other1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button21",row=4,disabled=True)#data
    async def other1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="other1button22",row=4,disabled=False)#pins
    async def other1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="other1button23",row=4,disabled=False)#alert
    async def other1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.othercmd}", custom_id="other1button24",row=4,disabled=True)#sectorrotation
    async def other1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="other1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)



class StreamCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"Stream {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="streamcmddrop",
            options =  [
            disnake.SelectOption(label="/stream Crypto",value=1 , description="Stream crypto live.",emoji="<a:_:1043017902191808523>"),
            disnake.SelectOption(label="/stream Double Crypto",value=2 , description="Stream two cryptos live - simultaneously.",emoji="<a:_:1043017902191808523>"),
            disnake.SelectOption(label="/stream Double Quote",value=3 , description="Stream two stocks live - simultaneously.",emoji="<a:_:1043017902191808523>"),
            disnake.SelectOption(label="/stream Quote",value=4, description="Stream a stock quote live.",emoji="<a:_:1043017902191808523>"),
            disnake.SelectOption(label="/stream Time and Sales",value=5 , description="Stream time and sales in real time.",emoji="<a:_:1043017902191808523>"),
            disnake.SelectOption(label="/stream Tits",value=6 , description="Stream some tits.",emoji="<a:_:1043017902191808523>"),])



    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</stream crypto:1042947625663610935>", ephemeral=False)
        if self.values[0] == "2":
            await interaction.send("</stream double_crypto:1042947625663610935>", ephemeral=False)

        if self.values[0] == "3":
            await interaction.send("</stream double_quote:1042947625663610935>", ephemeral=False)
        if self.values[0] == "4":
            await interaction.send("</stream quote:1042947625663610935>", ephemeral=False)
        if self.values[0] == "5":
            await interaction.send("</stream time_and_sales:1042947625663610935>", ephemeral=False)

        if self.values[0] == "6":
            await interaction.send("</stream tits:1042947625663610935>", ephemeral=False)


class StreamCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(StreamCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button1",row=0,disabled=True)
    async def stream1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="stream1button2",row=0,disabled=False)#webull
    async def stream1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.clockspin}", custom_id="stream1button3",row=0,disabled=True)#stream
    async def stream1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(),embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="stream1button4",row=0,disabled=False)#options
    async def stream1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=CommandsEmbed())
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="stream1button5",row=0,disabled=False)#data
    async def stream1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="stream1button6",row=1,disabled=False)#dp commands
    async def stream1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button7",row=1,disabled=True)
    async def stream1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="stream1button8", disabled=False,row=1)#stockcmds
    async def stream1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button9",row=1,disabled=True)
    async def stream1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="stream1button10",row=1,disabled=False)
    async def stream1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="stream1button16",row=3,disabled=False)#chart
    async def stream1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button17",row=3,disabled=True)
    async def stream1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="stream1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button19",row=3,disabled=True)#data
    async def stream1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="stream1button20",row=3,disabled=False)#magicwand
    async def stream1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button21",row=4,disabled=True)#data
    async def stream1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="stream1button22",row=4,disabled=False)#pins
    async def stream1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="stream1button23",row=4,disabled=False)#alert
    async def stream1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="stream1button24",row=4,disabled=True)#sectorrotation
    async def stream1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)




class EarningsCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"/earnings {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="earningscmddrop",
            options =  [
            disnake.SelectOption(label="/earnings Calendar",value=1, description="Returns a ticker's projecting earnings crush.", emoji="<a:_:1043016743246901339>"),
            disnake.SelectOption(label="/earnings Crush",value=2, description="Returns a ticker's projecting earnings crush.", emoji="<a:_:1043016743246901339>"),
            disnake.SelectOption(label="/earnings Date",value=3, description="Select a date and return the earnings scheduled for that date.", emoji="<a:_:1043016743246901339>"),
            disnake.SelectOption(label="/earnings Projection",value=4, description="Returns a ticker's earnings projection as well as implied move.", emoji="<a:_:1043016743246901339>"),
            disnake.SelectOption(label="/earnings Today",value=5, description="Returns all tickers with earnings for the current day.", emoji="<a:_:1043016743246901339>"),
            disnake.SelectOption(label="/earnings Day-of-Week",value=6, description="Returns the tickers scheduled for a specific day of the week.", emoji="<a:_:1043016743246901339>")])



    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</earnings calendar:911140318118838277>", ephemeral=False)
        if self.values[0] == "2":
            await interaction.send("</earnings crush:1042947625663610930>", ephemeral=False)

        if self.values[0] == "3":
            await interaction.send("</earnings date:911140318118838277>", ephemeral=False)
        if self.values[0] == "4":
            await interaction.send("</earnings projection:1042947625663610930>", ephemeral=False)
        if self.values[0] == "5":
            await interaction.send("</earnings today:911140318118838277>", ephemeral=False)

        if self.values[0] == "6":
            await interaction.send("</earnings day-of-week:911140318118838277>", ephemeral=False)


class EarningsCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(EarningsCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button1",row=0,disabled=False)
    async def stream1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="stream1button2",row=0,disabled=False)#webull
    async def stream1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="stream1button3",row=0,disabled=False)#stream
    async def stream1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="stream1button4",row=0,disabled=False)#options
    async def stream1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="stream1button5",row=0,disabled=False)#data
    async def stream1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="stream1button6",row=1,disabled=False)#dp commands
    async def stream1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button7",row=1,disabled=True)
    async def stream1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="stream1button8", disabled=False,row=1)#stockcmds
    async def stream1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button9",row=1,disabled=True)
    async def stream1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="stream1button10",row=1,disabled=False)
    async def stream1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(), embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="stream1button16",row=3,disabled=False)#chart
    async def stream1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button17",row=3,disabled=True)
    async def stream1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="stream1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button19",row=3,disabled=True)#data
    async def stream1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="stream1button20",row=3,disabled=False)#magicwand
    async def stream1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button21",row=4,disabled=True)#data
    async def stream1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.earnings}", custom_id="stream1button22",row=4,disabled=True)#pins
    async def stream1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="stream1button23",row=4,disabled=False)#alert
    async def stream1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(),embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="stream1button24",row=4,disabled=True)#sectorrotation
    async def stream1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(),embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="stream1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)




class EconomyCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"/econ & /economy {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="economycmddrop",
            options =  [

            disnake.SelectOption(label="/economy joblessclaims",value=1,description="Returns latest and historic Jobless Numbers.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/economy inflation",value=2,description="Returns latest and historic inflation numbers with averages", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econonomy AMBS",value=3,description="Returns the latest roll, swap, new, or all agency mortgage backed securities.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/economy retailrepo",value=4,description="Returns the amount of retail capital in money market funds.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/economy Data",value=5, description="Returns a large list of economic data.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ housetrades",value=6, description="Returns a list of the latest trades from the House.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ revrepo",value=7, description="Returns the latest and historic Reverse Repo Data with differences.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ calendar",value=8, description="Displays a calendar of important economic events.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ glbonds", value=9,description="Displays global bond data.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ usbonds",value=10, description="Displays US bond data.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ yieldcurve",value=11,description="Displays US Bond yield curve data.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ indices",value=12,description="Displays US indices overview.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ currencies",value=13, description="Displays global currency data.", emoji="<a:_:1044503531878621195>"),
            disnake.SelectOption(label="/econ fedrates",value=14,description="Displays upcoming FOMC events and projected BPS hike percentage.", emoji="<a:_:1044503531878621195>"),])



    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            
            await interaction.send("</economy joblessclaims:1042947625663610939>", ephemeral=False)
        elif self.values[0] == "2":
            await interaction.send("</economy ambs:1042947625663610939>", ephemeral=False)

        elif self.values[0] == "3":
            await interaction.send("</economy retailrepo:1042947625663610939>", ephemeral=False)
        elif self.values[0] == "4":
            await interaction.send("</economy data:1042947625663610939>", ephemeral=False)
        elif self.values[0] == "5":
            await interaction.send("</economy house_trades:1042947625663610939>", ephemeral=False)

        elif self.values[0] == "6":
            await interaction.send("</econ revrepo:1004263746111275130>", ephemeral=False)
        elif self.values[0] == "7":
            await interaction.send("</econ calendar:1004263746111275130>", ephemeral=False)
        elif self.values[0] == "8":
            await interaction.send("</econ glbonds:1004263746111275130>", ephemeral=False)

        elif self.values[0] == "9":
            await interaction.send("</econ usbonds:1004263746111275130>", ephemeral=False)
        elif self.values[0] == "10":
            await interaction.send("</econ yieldcurve:1004263746111275130>", ephemeral=False)
        elif self.values[0] == "11":
            await interaction.send("</econ indices:1004263746111275130>", ephemeral=False)

        elif self.values[0] == "12":
            await interaction.send("</econ currencies:1004263746111275130>", ephemeral=False)
        elif self.values[0] == "13":
            await interaction.send("</econ fedrates:1004263746111275130>", ephemeral=False)


class EconomyCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(EconomyCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button1",row=0,disabled=False)
    async def economy1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="economy1button2",row=0,disabled=False)#webull
    async def economy1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="economy1button3",row=0,disabled=False)#stream
    async def economy1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(),embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="economy1button4",row=0,disabled=False)#options
    async def economy1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=CommandsEmbed())
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="economy1button5",row=0,disabled=False)#data
    async def economy1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="economy1button6",row=1,disabled=False)#dp commands
    async def economy1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button7",row=1,disabled=True)
    async def economy1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="economy1button8", disabled=False,row=1)#stockcmds
    async def economy1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button9",row=1,disabled=True)
    async def economy1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="economy1button10",row=1,disabled=False)
    async def economy1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(),embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.glowstick}", custom_id="economy1button16",row=3,disabled=False)#chart
    async def economy1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=ChartingCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button17",row=3,disabled=True)
    async def economy1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="economy1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button19",row=3,disabled=True)#data
    async def economy1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="economy1button20",row=3,disabled=False)#magicwand
    async def economy1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button21",row=4,disabled=True)#data
    async def economy1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="economy1button22",row=4,disabled=False)#pins
    async def economy1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.confirmed}", custom_id="economy1button23",row=4,disabled=False)#alert
    async def economy1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="economy1button24",row=4,disabled=True)#sectorrotation
    async def economy1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="economy1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)



class ChartingCmdDrop(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder=f"/c {e.cmdtext}",
            min_values=1,
            max_values=1,
            custom_id="chartcmddrop",
            options =  [

                disnake.SelectOption(label="Charting Timeframe Arguments",value=1, emoji="<a:_:1043016260415410206>"),])


    async def callback(self, interaction:disnake.MessageCommandInteraction):
        if self.values[0] == "1":
            await interaction.send("```py\nTo view possible indicators and arguments, please see:``` https://www.alphabotsystem.com/features/charting\n\n</c:928980578739568652>", ephemeral=False)


class ChartingCmdViewStart(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(ChartingCmdDrop())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button1",row=0,disabled=True)
    async def charting1button1(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.webullcmd}", custom_id="charting1button2",row=0,disabled=False)#webull
    async def charting1button2(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=WebullCmdViewStart(), embed=WebullCmdViewStart().embed)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.clockspin}", custom_id="charting1button3",row=0,disabled=False)#stream
    async def charting1button3(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StreamCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.optioncmd}", custom_id="charting1button4",row=0,disabled=False)#options
    async def charting1button4(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OptionCmdViewStart(), embed=None)
    @disnake.ui.button(style=disnake.ButtonStyle.blurple,emoji=f"{emojis.confirmed}", custom_id="charting1button5",row=0,disabled=False)#data
    async def charting1button5(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.portal}", custom_id="charting1button6",row=1,disabled=False)#dp commands
    async def charting1button6(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
    
        await inter.response.edit_message(view=DPSCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button7",row=1,disabled=True)
    async def charting1button7(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.pinkrocket}", custom_id="charting1button8", disabled=False,row=1)#stockcmds
    async def charting1button8(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=StockCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button9",row=1,disabled=True)
    async def charting1button9(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.learncmd}", custom_id="charting1button10",row=1,disabled=False)
    async def charting1button10(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=LearnCmdViewStart(),embed=CommandsEmbed())


    

    @disnake.ui.button(style=disnake.ButtonStyle.red,emoji=f"{emojis.confirmed}", custom_id="charting1button16",row=3,disabled=False)#chart
    async def charting1button16(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=CommandsStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button17",row=3,disabled=True)
    async def charting1button17(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.eye}", custom_id="charting1button18",disabled=False,row=3)#DOWNARROW
    async def downarrow(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=DDCmdViewStart(), embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button19",row=3,disabled=True)#data
    async def charting1button19(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.flowcmd}", custom_id="charting1button20",row=3,disabled=False)#magicwand
    async def charting1button20(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=FlowCmdViewStart())


    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button21",row=4,disabled=True)#data
    async def charting1button21(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.earnings}", custom_id="charting1button22",row=4,disabled=False)#pins
    async def charting1button22(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EarningsCmdViewStart(),embed=CommandsEmbed())


    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.economy}", custom_id="charting1button23",row=4,disabled=False)#alert
    async def charting1button23(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=EconomyCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.green,emoji=f"{emojis.othercmd}", custom_id="charting1button24",row=4,disabled=True)#sectorrotation
    async def charting1button24(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=OtherCmdViewStart(), embed=CommandsEmbed())

    @disnake.ui.button(style=disnake.ButtonStyle.grey,emoji=f"{emojis.movingchart}", custom_id="charting1button25",row=4,disabled=True)#data
    async def linkbutton25(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
        await inter.response.edit_message(view=None)


class CommandsEmbed(disnake.Embed):
    def __init__(self):
        super().__init__(
            title=f"{e.fudstop} FUDSTOP Application 2.0 Online",
            description="```py\nThis is the FUDSTOP Application 2.0.``````py\nWithin this APP, you can click the buttons on the main page to get anything you need related to markets. From cited works to datasets, core play screener and bot-command help, as well as a server menu and YouTube videos - simply click what you need! Use the legend below to identify each category:```",
            color=disnake.Colour.dark_orange(), url="https://www.fudstop.io")
        
        self.add_field(name="<a:_:1042676749357555794>", value="```py\n/webull\nCommands using Webull's API! Features data from CBOE hanweck.```")
        self.add_field(name=f"{e.optioncmd}", value="```py\n/Returns options related data and charts.```")
        self.add_field(name=f"<a:_:1044503531878621195>",value="```py\n/dp\n\nCommands for dark-pool data such as biggest prints, weekly prints, day summary, and much more.```")
        self.add_field(name="<a:_:1043013214180483112>", value="```py\n/stock\n\nGather ticker data for specific stocks - such as orderflow, leverage, liquidity, earnings crush, and much more.```")
        self.add_field(name="<a:_:1043015881631993856>", value="```py\n/learn\n\nCommands used to learn several topics from discord to markets.```")
        self.add_field(name="<a:_:1043016260415410206>", value="```py\n/c\n\n Command used to call stock charts to Discord.```")
        self.add_field(name="<a:_:1043016260415410206>", value="```py\n/dd\n\nDue diligence commands from Open BB Bot.```")
        self.add_field(name="<a:_:1043016503710208030>",value="```py\n/flow\n\nThese commands are for visualizing flow data for options.```")
        self.add_field(name="<a:_:1043016743246901339>", value="```py\n/earnings\n\nCommands used for earnings related data.```")
        self.add_field(name="<a:_:1043016869797441607>", value="```py\n/economy & /econ\n\nCommands related to economic information / data.```")
        self.add_field(name="<a:_:1043022403393040414>", value="```py\n/analysis\n\nAnalyze markets, situations, and trends.```")
        self.add_field(name="<a:_:1043024795404599438>", value="```py\n/jasmy\n\nJasmycoin related commands!```")
        self.add_field(name="<a:_:1043017902191808523>", value="```py\n/stream\n\nCommands that return real-time data.```")
        self.set_footer(text="Select a command set from the dropdown list to have the entire set printed to chat. Then, click the command to use it.")

